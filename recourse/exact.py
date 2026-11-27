"""Exact rule-verified recourse by mixed-integer linear programming (v3).

Finds   argmin  sum_{j in A} |x_j - x0_j| / r_j  +  lam_spar * #{j in A : x_j != x0_j}
        s.t.    f(x) = 1 (favourable class, encoded exactly),
                every linear constraint of the rule Pi,
                lb_j <= x_j <= ub_j for actionable j,   x_I = x0_I,
for f a logistic regression, a scikit-learn random forest or a CatBoost model.
If the program is infeasible, the acceptable set A(x0) is empty (certified abstention).

Tree splits are encoded with one binary per (actionable feature, distinct threshold
inside the bounds): a_{jk} = 1  <=>  x_j <= t_{jk}, ordered a_{j1} <= a_{j2} <= ...
Leaves are continuous variables forced to the active leaf (Misic, 2020 formulation;
per-level aggregation for CatBoost's oblivious trees).  Splits on fixed features,
or on thresholds outside the bounds, are resolved to constants before encoding.
"""
import json, os, tempfile, time
from dataclasses import dataclass, field
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix

EPS_SPLIT = 1e-4      # (v3.0 split margin; v3.1 uses a float32-ulp margin, see solve_exact)
EPS_SCORE = 1e-6      # favourable class: score >= threshold + EPS_SCORE
EPS_RULE = 1e-6       # rule constraints tightened by EPS_RULE*max(1,|tau|)


# ------------------------------------------------------------------ model parsing
@dataclass
class TreeEnsemble:
    """Generic tree list.  Each tree: list of nodes; node = (feature, thr, left, right) for
    splits (go left iff x[feature] <= thr) or ('leaf', value).  score = scale*sum(values)+bias,
    favourable iff score >= cut (+ EPS_SCORE)."""
    trees: list
    scale: float
    bias: float
    cut: float
    oblivious: list = None          # for CatBoost: list of (splits[(f, border)], leaf_values)


@dataclass
class Linear:
    w: np.ndarray
    b: float                        # favourable iff w.x + b >= EPS_SCORE


@dataclass
class MLP:
    """ReLU network on raw inputs (scaler folded into the first layer).  layers: list of
    (W, b) with W of shape (n_in, n_out); hidden layers ReLU, last layer one logit;
    favourable iff logit >= EPS_SCORE (sklearn: class 1 iff sigmoid(logit) > 0.5)."""
    layers: list


def parse_model(model, features):
    name = type(model).__name__
    if name == 'Pipeline' and type(list(model.named_steps.values())[-1]).__name__ == 'MLPClassifier':
        steps = list(model.named_steps.values()); net = steps[-1]
        assert net.activation == 'relu' and net.n_outputs_ == 1
        sc = next((s for s in steps if type(s).__name__ == 'StandardScaler'), None)
        layers = [(np.array(W, float), np.array(b, float)) for W, b in zip(net.coefs_, net.intercepts_)]
        if sc is not None:
            W, b = layers[0]
            layers[0] = (W / sc.scale_[:, None], b - (sc.mean_ / sc.scale_) @ W)
        return MLP(layers)
    if name == 'Pipeline':
        steps = dict(model.named_steps)
        sc = next((s for s in steps.values() if type(s).__name__ == 'StandardScaler'), None)
        lr = list(steps.values())[-1]
        w = lr.coef_.ravel().astype(float); b = float(lr.intercept_[0])
        if sc is not None:
            b = b - float(np.sum(w * sc.mean_ / sc.scale_)); w = w / sc.scale_
        return Linear(w, b)
    if name == 'LogisticRegression':
        return Linear(model.coef_.ravel().astype(float), float(model.intercept_[0]))
    if name == 'RandomForestClassifier':
        trees = []
        for est in model.estimators_:
            t = est.tree_; nodes = []
            for n in range(t.node_count):
                if t.children_left[n] == -1:
                    v = t.value[n][0]; nodes.append(('leaf', float(v[1] / v.sum())))
                else:
                    nodes.append((int(t.feature[n]), float(t.threshold[n]), int(t.children_left[n]), int(t.children_right[n])))
            trees.append(nodes)
        # sklearn predicts class 1 iff mean p1 > 0.5 (argmax picks class 0 on ties)
        return TreeEnsemble(trees, 1.0 / len(trees), 0.0, 0.5)
    if name == 'CatBoostClassifier':
        fd, path = tempfile.mkstemp(suffix='.json'); os.close(fd)
        model.save_model(path, format='json'); j = json.load(open(path)); os.remove(path)
        scale, bias = j['scale_and_bias'][0], j['scale_and_bias'][1][0]
        obl = []
        for t in j['oblivious_trees']:
            splits = [(s['float_feature_index'], float(np.float32(s['border']))) for s in t['splits']]
            obl.append((splits, np.array(t['leaf_values'], float)))
        return TreeEnsemble(None, float(scale), float(bias), 0.0, oblivious=obl)
    raise ValueError(f'unsupported model {name}')


def score(enc, x):
    """Reference score of the parsed model (used to verify the parser)."""
    if isinstance(enc, Linear):
        return float(enc.w @ x + enc.b)
    if isinstance(enc, MLP):
        h = np.asarray(x, float)
        for i, (W, b) in enumerate(enc.layers):
            h = h @ W + b
            if i < len(enc.layers) - 1:
                h = np.maximum(h, 0.0)
        return float(h[0])
    if enc.oblivious is not None:
        s = 0.0
        xf = x.astype(np.float32)
        for splits, lv in enc.oblivious:
            idx = sum((1 << i) for i, (f, b) in enumerate(splits) if xf[f] > np.float32(b))
            s += lv[idx]
        return enc.scale * s + enc.bias
    s = 0.0
    for nodes in enc.trees:
        n = 0
        while nodes[n][0] != 'leaf':
            f, thr, l, r = nodes[n]; n = l if x[f] <= thr else r
        s += nodes[n][1]
    return enc.scale * s + enc.bias


# ------------------------------------------------------------------ MILP builder
class _Builder:
    def __init__(self):
        self.lb, self.ub, self.c, self.integ = [], [], [], []
        self.rows, self.cols, self.vals, self.rlo, self.rhi = [], [], [], [], []
        self.nr = 0

    def var(self, lb, ub, c=0.0, integer=False):
        self.lb.append(lb); self.ub.append(ub); self.c.append(c); self.integ.append(1 if integer else 0)
        return len(self.lb) - 1

    def row(self, coefs, lo, hi):
        for j, v in coefs:
            if v != 0:
                self.rows.append(self.nr); self.cols.append(j); self.vals.append(v)
        self.rlo.append(lo); self.rhi.append(hi); self.nr += 1

    def solve(self, time_limit=60, gap=1e-6, int_tol=1e-9, presolve=True, start=None):
        """Solve with HiGHS directly (highspy), so that the integrality tolerance can be tightened:
        with the default 1e-6, big-M rows such as u <= M s admit moves of M*1e-6 at no sparsity cost."""
        import highspy
        n = len(self.lb)
        A = coo_matrix((self.vals, (self.rows, self.cols)), shape=(self.nr, n)).tocsr()
        inf = highspy.kHighsInf
        fix = lambda v: [inf if x == np.inf else -inf if x == -np.inf else float(x) for x in v]
        lp = highspy.HighsLp()
        lp.num_col_, lp.num_row_ = n, self.nr
        lp.col_cost_ = np.array(self.c, float)
        lp.col_lower_, lp.col_upper_ = np.array(fix(self.lb)), np.array(fix(self.ub))
        lp.row_lower_, lp.row_upper_ = np.array(fix(self.rlo)), np.array(fix(self.rhi))
        lp.a_matrix_.format_ = highspy.MatrixFormat.kRowwise
        lp.a_matrix_.start_, lp.a_matrix_.index_, lp.a_matrix_.value_ = A.indptr, A.indices, A.data
        lp.a_matrix_.num_col_, lp.a_matrix_.num_row_ = n, self.nr
        lp.integrality_ = [highspy.HighsVarType.kInteger if i else highspy.HighsVarType.kContinuous for i in self.integ]
        h = highspy.Highs()
        for k, v in dict(output_flag=False, time_limit=float(time_limit), mip_rel_gap=gap,
                         mip_feasibility_tolerance=int_tol, threads=1, presolve='on' if presolve else 'off').items():
            h.setOptionValue(k, v)
        h.passModel(lp)
        if start:                       # partial MIP start: integer values; HiGHS completes the rest
            idx = np.array(sorted(start), dtype=np.int32)
            h.setSolution(len(idx), idx, np.array([float(start[i]) for i in idx]))
        h.run()
        ms = h.getModelStatus(); M = highspy.HighsModelStatus
        info = h.getInfo()
        has_sol = info.primal_solution_status == 2       # feasible primal solution available
        status = 0 if ms == M.kOptimal else 2 if ms == M.kInfeasible else 1 if ms == M.kTimeLimit else 4
        x = np.array(h.getSolution().col_value) if has_sol else None
        dual = getattr(info, 'mip_dual_bound', np.nan)
        if ms == M.kOptimal and not (isinstance(dual, float) and np.isfinite(dual)):
            dual = info.objective_function_value
        return type('R', (), dict(status=status, x=x, fun=info.objective_function_value if has_sol else np.nan,
                                  mip_gap=info.mip_gap, dual=dual))()


@dataclass
class ExactResult:
    x: object                    # pd.Series or None
    status: str                  # 'optimal', 'infeasible' (certified empty), 'time_limit', 'error'
    objective: float = np.nan
    seconds: float = 0.0
    n_binary: int = 0
    n_vars: int = 0
    n_rows: int = 0
    gap: float = np.nan
    bound: float = np.nan        # valid lower bound on the optimum (MILP dual bound)


def solve_exact(enc, x0, spec, policy, lam_spar=0.5, time_limit=60, extra_rules=None, int_tol=None, start=None):
    """start: optional vector (pd.Series over spec.features), e.g. an accepted heuristic output; its
    integer pattern (sparsity, split sides, OR branch, ReLU phases) is passed to HiGHS as a MIP start.
    x0: pd.Series over spec.features.  spec: recourse.core.Spec.  policy: recourse.core.Policy.
    extra_rules: optional list of (coef dict, lo, hi) linear rows over features (e.g. ratio rules)."""
    t0 = time.time()
    feats = list(spec.features); fidx = {f: i for i, f in enumerate(feats)}
    act = [f for f in spec.actionable]
    B = _Builder(); svar = {}; branch_vars = []; avar = {}; relu = []
    # feature variables (fixed features get lb = ub = x0)
    xv = {}
    for f in feats:
        v0 = float(x0[f])
        if f in act:
            lb, ub = spec.bounds[f]
            xv[f] = B.var(float(lb), float(ub))
        else:
            xv[f] = B.var(v0, v0)
    # effort + sparsity (derived features carry no cost)
    for f in [f for f in act if f not in getattr(spec, 'derived', ())]:
        r = spec.rng(f); v0 = float(x0[f]); lb, ub = spec.bounds[f]
        u = B.var(0.0, max(ub - v0, v0 - lb, 0.0), 1.0 / r)
        B.row([(xv[f], 1.0), (u, -1.0)], -np.inf, v0)        # x - u <= x0
        B.row([(xv[f], 1.0), (u, 1.0)], v0, np.inf)          # x + u >= x0
        if lam_spar:
            s = B.var(0.0, 1.0, lam_spar, integer=True); svar[f] = s
            tol = 0.99 * (1e-8 + 1e-5 * abs(v0))      # same tolerance as core.sparsity (np.isclose)
            B.row([(u, 1.0), (s, -max(ub - v0, v0 - lb, 1e-9))], -np.inf, tol)   # u <= M s (+ isclose tol)
    # rule (conjunctive part)
    def _rule_row(c, ind=None, bigm=None):
        """Add constraint c; if ind is given, enforce only when binary ind = 1 (big-M)."""
        coefs = [(xv[f], float(w)) for f, w in c.weights.items()]
        er = EPS_RULE * max(1.0, abs(c.tau))       # solver tolerance safety: gate checks the rule exactly
        if ind is None:
            if c.op == '>=':
                B.row(coefs, c.tau + er, np.inf)
            elif c.op == '<=':
                B.row(coefs, -np.inf, c.tau - er)
            else:
                B.row(coefs, c.tau, c.tau)
            return
        lo_v, hi_v = bigm(c)
        if c.op in ('>=', '=='):        # sum >= tau + er - M(1-ind)  ->  sum - M ind >= tau + er - M
            M = max(c.tau + er - lo_v, 0.0)
            B.row(coefs + [(ind, -M)], c.tau + er - M, np.inf)
        if c.op in ('<=', '=='):        # sum <= tau - er + M(1-ind)
            M = max(hi_v - (c.tau - er), 0.0)
            B.row(coefs + [(ind, M)], -np.inf, c.tau - er + M)

    def _range(c):
        lo_v = hi_v = 0.0
        for f, w in c.weights.items():
            if f in act:
                a_, b_ = spec.bounds[f]
            else:
                a_ = b_ = float(x0[f])
            lo_v += min(w * a_, w * b_); hi_v += max(w * a_, w * b_)
        return lo_v, hi_v

    if policy.active:
        for c in policy.constraints:
            _rule_row(c)
        if policy.any_of:
            inds = [B.var(0.0, 1.0, 0.0, integer=True) for _ in policy.any_of]; branch_vars = list(zip(inds, policy.any_of))
            B.row([(i, 1.0) for i in inds], 1.0, np.inf)
            for ind, branch in zip(inds, policy.any_of):
                for c in branch:
                    _rule_row(c, ind, _range)
    # structural links (exact, no tightening)
    for c in getattr(spec, 'links', []):
        coefs = [(xv[f], float(w)) for f, w in c.weights.items()]
        el = EPS_RULE * max(1.0, abs(c.tau))      # inequality links tightened like the rule (gate is exact)
        if c.op == '==':
            B.row(coefs, c.tau, c.tau)
        elif c.op == '>=':
            B.row(coefs, c.tau + el, np.inf)
        else:
            B.row(coefs, -np.inf, c.tau - el)
    for coefs, lo, hi in extra_rules or []:
        B.row([(xv[f], w) for f, w in coefs.items()], lo, hi)

    # ---- model
    if isinstance(enc, Linear):
        B.row([(xv[f], float(enc.w[fidx[f]])) for f in feats], EPS_SCORE - enc.b, np.inf)
    elif isinstance(enc, MLP):
        # ReLU network: big-M with interval-arithmetic bounds over the action box (exact encoding)
        prev = [xv[f] for f in feats]
        lo = np.array([float(spec.bounds[f][0]) if f in act else float(x0[f]) for f in feats])
        hi = np.array([float(spec.bounds[f][1]) if f in act else float(x0[f]) for f in feats])
        relu = []
        for li, (W, b) in enumerate(enc.layers):
            Wp, Wn = np.maximum(W, 0), np.minimum(W, 0)
            L = lo @ Wp + hi @ Wn + b; U = hi @ Wp + lo @ Wn + b
            if li == len(enc.layers) - 1:          # output logit >= EPS_SCORE
                B.row([(prev[i], float(W[i, 0])) for i in range(len(prev))], EPS_SCORE - float(b[0]), np.inf)
                break
            cur = []
            for j in range(W.shape[1]):
                lin = [(prev[i], -float(W[i, j])) for i in range(len(prev)) if W[i, j] != 0]
                if U[j] <= 0:
                    y = B.var(0.0, 0.0)
                elif L[j] >= 0:
                    y = B.var(float(L[j]), float(U[j]))
                    B.row([(y, 1.0)] + lin, float(b[j]), float(b[j]))                 # y = pre
                else:
                    y = B.var(0.0, float(U[j])); dl = B.var(0.0, 1.0, 0.0, integer=True); relu.append((li, j, dl))
                    B.row([(y, 1.0)] + lin, float(b[j]), np.inf)                      # y >= pre
                    B.row([(y, 1.0)] + lin + [(dl, -float(L[j]))], -np.inf, float(b[j] - L[j]))  # y <= pre - L(1-d)
                    B.row([(y, 1.0), (dl, -float(U[j]))], -np.inf, 0.0)               # y <= U d
                cur.append(y)
            prev = cur
            lo, hi = np.maximum(L, 0.0), np.maximum(U, 0.0)
    else:
        # split literal: returns ('const', bool) or ('var', a_index, sign) where True <=> x<=thr is
        # a (sign=+1) ... we always express "x_f <= thr" truth.
        thr_vars = {f: {} for f in act}

        def literal(fi, thr):
            f = feats[fi]
            if f not in act:
                return ('const', float(x0[f]) <= thr)
            lb, ub = spec.bounds[f]
            if thr >= ub:
                return ('const', True)
            if thr < lb:
                return ('const', False)
            if thr not in thr_vars[f]:
                thr_vars[f][thr] = None
            return ('var', f, thr)

        # collect literals first to create ordered threshold binaries
        tree_lits = []
        if enc.oblivious is not None:
            for splits, lv in enc.oblivious:
                # CatBoost bit = x > border  <=>  not (x <= border)   (float32 semantics)
                tree_lits.append([literal(fi, b) for fi, b in splits])
        else:
            for nodes in enc.trees:
                tree_lits.append({n: literal(nd[0], nd[1]) for n, nd in enumerate(nodes) if nd[0] != 'leaf'})
        # threshold binaries and linking
        avar = {}
        for f in act:
            ts = sorted(thr_vars[f]); lb, ub = spec.bounds[f]
            M = (ub - lb) + 1.0
            prev = None
            for t in ts:
                a = B.var(0.0, 1.0, 0.0, integer=True); avar[(f, t)] = a
                # strict side of the split.  v3.1: the margin is a few float32 ulps (the models compare
                # float32 inputs), not a fixed 1e-4, which excluded real actions whenever thresholds lie
                # closer than 1e-4 to each other or to a bound (e.g. GMSC ratios near 0).
                e = max(8.0 * float(np.spacing(np.float32(abs(t)))), 1e-9 * M + 1e-9)
                lo_side = t if enc.oblivious is not None else t - e   # CatBoost borders are float32-exact
                B.row([(xv[f], 1.0), (a, M)], -np.inf, lo_side + M)       # a=1 -> x <= t
                B.row([(xv[f], 1.0), (a, M)], t + e, np.inf)              # a=0 -> x >= t + eps
                if prev is not None:
                    B.row([(prev, 1.0), (a, -1.0)], -np.inf, 0.0)          # a_prev <= a
                prev = a
        score_terms, const = [], enc.bias / enc.scale if enc.scale else 0.0
        if enc.oblivious is not None:
            for (splits, lv), lits in zip(enc.oblivious, tree_lits):
                d = len(splits)
                # leaves consistent with constant bits
                live = []
                for l in range(1 << d):
                    ok = True
                    for i, L in enumerate(lits):
                        bit = (l >> i) & 1            # 1 <=> x > border <=> literal False
                        if L[0] == 'const' and (bit == 1) == L[1]:
                            ok = False; break
                    if ok:
                        live.append(l)
                if len(live) == 1:
                    const += lv[live[0]]; continue
                z = {l: B.var(0.0, 1.0) for l in live}
                B.row([(z[l], 1.0) for l in live], 1.0, 1.0)
                for i, L in enumerate(lits):
                    if L[0] == 'const':
                        continue
                    a = avar[(L[1], L[2])]               # a = 1 <=> x <= border <=> bit 0
                    B.row([(z[l], 1.0) for l in live if (l >> i) & 1 == 0] + [(a, -1.0)], -np.inf, 0.0)
                    B.row([(z[l], 1.0) for l in live if (l >> i) & 1 == 1] + [(a, 1.0)], -np.inf, 1.0)
                score_terms += [(z[l], float(lv[l])) for l in live]
        else:
            for nodes, lits in zip(enc.trees, tree_lits):
                # reachable leaves after constant pruning
                reach, stack = {}, [0]
                children = {}
                while stack:
                    n = stack.pop(); nd = nodes[n]
                    if nd[0] == 'leaf':
                        reach[n] = True; continue
                    L = lits[n]
                    if L[0] == 'const':
                        stack.append(nd[2] if L[1] else nd[3])
                    else:
                        stack += [nd[2], nd[3]]
                leaves = list(reach)
                if len(leaves) == 1:
                    const += nodes[leaves[0]][1]; continue
                z = {l: B.var(0.0, 1.0) for l in leaves}
                B.row([(z[l], 1.0) for l in leaves], 1.0, 1.0)

                def subtree_leaves(n):
                    out, st = [], [n]
                    while st:
                        m = st.pop(); nd = nodes[m]
                        if nd[0] == 'leaf':
                            if m in z: out.append(m)
                        else:
                            L = lits[m]
                            if L[0] == 'const':
                                st.append(nd[2] if L[1] else nd[3])
                            else:
                                st += [nd[2], nd[3]]
                    return out
                for n, L in lits.items():
                    if L[0] != 'var':
                        continue
                    a = avar[(L[1], L[2])]
                    left, right = subtree_leaves(nodes[n][2]), subtree_leaves(nodes[n][3])
                    if left:
                        B.row([(z[l], 1.0) for l in left] + [(a, -1.0)], -np.inf, 0.0)
                    if right:
                        B.row([(z[l], 1.0) for l in right] + [(a, 1.0)], -np.inf, 1.0)
                score_terms += [(z[l], float(nodes[l][1])) for l in leaves]
        # scale*(sum + const) >= cut + eps   (scale > 0)
        B.row(score_terms, (enc.cut + EPS_SCORE) / enc.scale - const, np.inf)

    n_bin = int(sum(B.integ))
    # ReLU big-M rows are numerically delicate: with the 1e-9 MIP feasibility tolerance, HiGHS presolve can
    # cut off the optimal branch (found in tests/test_exact.py), and a looser tolerance lets sparsity binaries
    # take fractional values (u <= M*1e-7 moves for free).  Networks are therefore solved with tolerance 1e-9
    # and presolve off.
    is_net = isinstance(enc, MLP)
    st = None
    if start is not None:
        xs0 = start[feats].astype(float)
        st = {}
        for f, sv in svar.items():
            st[sv] = 0.0 if abs(float(xs0[f]) - float(x0[f])) <= 1e-8 + 1e-5 * abs(float(x0[f])) else 1.0
        for (f, t), a in avar.items():
            st[a] = 1.0 if float(xs0[f]) <= t else 0.0
        for ind, br in branch_vars:
            st[ind] = 1.0 if policy.branch_ok(xs0, br) else 0.0
        if isinstance(enc, MLP) and relu:
            h = xs0.values.astype(float); pres = []
            for i, (W, b) in enumerate(enc.layers[:-1]):
                pre = h @ W + b; pres.append(pre); h = np.maximum(pre, 0.0)
            for li, j, dl in relu:
                st[dl] = 1.0 if pres[li][j] > 0 else 0.0
    res = B.solve(time_limit=time_limit, int_tol=int_tol if int_tol is not None else 1e-9, presolve=not is_net, start=st)
    sec = time.time() - t0
    st = {0: 'optimal', 1: 'time_limit', 2: 'infeasible'}.get(res.status, 'error')
    if res.x is None:
        return ExactResult(None, st, seconds=sec, n_binary=n_bin, n_vars=len(B.lb), n_rows=B.nr,
                           bound=float(getattr(res, 'dual', np.nan)))
    x = x0.copy().astype(float)
    for f in act:
        x[f] = float(np.clip(res.x[xv[f]], *spec.bounds[f]))
    # snap solver round-off on features the solver treats as unchanged, but only if the snapped
    # vector still satisfies the rule, the structural links and the model (checked on the parsed model)
    xs = x.copy()
    for f in act:
        if abs(xs[f] - float(x0[f])) < 1e-7 or (f in svar and res.x[svar[f]] < 0.5
                                                 and abs(xs[f] - float(x0[f])) <= 1e-8 + 1e-5 * abs(float(x0[f]))):
            xs[f] = float(x0[f])
    if not xs.equals(x):
        sc = score(enc, xs[feats].values.astype(float))
        fav = sc > 0 if isinstance(enc, (Linear, MLP)) else sc > enc.cut
        if (not policy.active or policy.ok(xs)) and all(c.ok(xs) for c in getattr(spec, 'links', [])) and fav:
            x = xs
    gap = getattr(res, 'mip_gap', np.nan)
    return ExactResult(x, 'optimal' if res.status == 0 else st, float(res.fun), sec, n_bin, len(B.lb), B.nr, gap,
                       float(getattr(res, 'dual', np.nan)))


# ------------------------------------------------------------------ sparsity-aware repair (v3)
def repair_sparse(x0, spec, policy, predict=None, lam_spar=0.5, steps=24, step_frac=0.0625, time_limit=30):
    """Model-free repair that minimises the full cost (effort + lam_spar * sparsity) over the
    rule-feasible set R(x0) (a small MILP: no model encoded), then escalates the rule margin in
    steps of step_frac*|tau| until `predict` agrees (same grid as core.repair).
    Returns the last vector found (None if R(x0) is empty)."""
    if not policy.active:
        return None
    always = Linear(np.zeros(len(spec.features)), 1.0)
    last = None
    for k in range(steps + 1 if predict is not None else 1):
        r = solve_exact(always, x0, spec, policy.shifted(k * step_frac) if k else policy,
                        lam_spar=lam_spar, time_limit=time_limit)
        if r.x is None:
            return last
        last = r.x
        if predict is None or int(predict(last)) == 1:
            return last
    return last
