"""DACE and MACE baselines for the v3 experiments (logistic regression and random forest).

DACE (Kanamori et al., IJCAI 2020; github.com/kelicht/dace @9f6f07e) and MACE
(Karimi et al., AISTATS 2020; github.com/amirhk/mace @01e6a40) are run on exactly the
queries, models and gate of experiment_v3.py (same split, same model, same query sample).

Variants
  dace / mace            native: fixed / increase-only / decrease-only actionability as in
                         each method's own constraint language; the gate checks the rule.
  dace_rule / mace_rule  the rule, the per-query bounds and the structural links are added
                         to the method's own optimisation problem (PuLP model for DACE,
                         SMT formula for MACE): the strongest fair use of each method.
DACE: cost 'DACE' (l1-Mahalanobis + alpha 1-LOF, alpha = 0.01), K = 4 changes, HiGHS.
MACE: one-norm distance, epsilon 1e-3, z3 via PySMT.

Usage: python ext_dace_mace.py HMDA --seeds 0,1,2 --models lr,rf --methods dace,mace [--max_q 50]
Requires DACE_SRC and MACE_SRC (clones of the two repositories).
"""
import argparse, contextlib, os, signal, sys, tempfile, time, types, warnings
import numpy as np, pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupShuffleSplit
import prescriptive as P
from recourse import core as C
from recourse.domains import DOMAINS
import recourse.configs  # noqa: F401
from experiment_v3 import make_model, cost

warnings.filterwarnings('ignore')
DACE_SRC = os.environ.get('DACE_SRC', '/home/claude/ext/dace')
MACE_SRC = os.environ.get('MACE_SRC', '/home/claude/ext/mace')


LAST = {}


class Timeout(Exception):
    pass


@contextlib.contextmanager
def time_limit(sec):
    def h(signum, frame):
        raise Timeout()
    old = signal.signal(signal.SIGALRM, h); signal.alarm(int(sec))
    try:
        yield
    finally:
        signal.alarm(0); signal.signal(signal.SIGALRM, old)


def raw_lr(pipe):
    """Logistic regression with the scaler folded in (identical predictions)."""
    sc, lr = pipe.named_steps['standardscaler'], pipe.named_steps['logisticregression']
    m = LogisticRegression()
    m.coef_ = (lr.coef_ / sc.scale_).reshape(1, -1)
    m.intercept_ = np.array([lr.intercept_[0] - float(np.sum(lr.coef_.ravel() * sc.mean_ / sc.scale_))])
    m.classes_ = lr.classes_
    return m


def direction(spec, x0, f):
    if f in spec.immutable:
        return 'fixed'
    lb, ub = spec.bounds[f]
    if np.isclose(lb, x0[f]):
        return 'increase'
    if np.isclose(ub, x0[f]):
        return 'decrease'
    return 'any'


# ---------------------------------------------------------------- DACE
def dace_import():
    if 'lingam' not in sys.modules:           # DACE's utils imports DirectLiNGAM (only for its SCM cost)
        sys.modules['lingam'] = types.SimpleNamespace(DirectLiNGAM=object)
    # DACE and MACE both ship a top-level module called `utils`: import each with its own
    if 'linear_ce' in sys.modules:
        return sys.modules['linear_ce'], sys.modules['forest_ce']
    other = sys.modules.pop('utils', None)
    sys.path.insert(0, DACE_SRC)
    try:
        import linear_ce, forest_ce  # noqa: E401
    finally:
        sys.path.remove(DACE_SRC); sys.modules.pop('utils', None)
        if other is not None:
            sys.modules['utils'] = other
    return linear_ce, forest_ce


@contextlib.contextmanager
def pulp_extra(add):
    """Temporarily wrap pulp.LpProblem.solve so `add(prob)` can append constraints."""
    import pulp
    orig = pulp.LpProblem.solve

    def solve(self, *a, **k):
        if getattr(self, '_solved_once', False):     # DACE re-solves failures only to log them: skip
            return self.status
        if not getattr(self, '_extra_added', False):
            add(self); self._extra_added = True
        r = orig(self, *a, **k); self._solved_once = True
        LAST['status'] = pulp.LpStatus.get(self.status, str(self.status)); LAST['sol'] = pulp.LpSolution.get(self.sol_status, '')
        return r
    pulp.LpProblem.solve = solve
    try:
        yield
    finally:
        pulp.LpProblem.solve = orig


class DaceRunner:
    def __init__(self, model, Xtr, ytr, features):
        linear_ce, forest_ce = dace_import()
        self.features = features; self.model = model
        # DACE's LOF prototypes and covariance are computed on the whole training set, which
        # exhausts memory for the 41k-row lending data: use a stratified sample of 2,000 rows.
        if len(Xtr) > 2000:
            from sklearn.model_selection import train_test_split
            idx, _ = train_test_split(np.arange(len(Xtr)), train_size=2000, stratify=ytr.values, random_state=0)
            Xtr, ytr = Xtr.iloc[np.sort(idx)], ytr.iloc[np.sort(idx)]
        Xa = Xtr[features].values.astype(float)
        cons = [''] * len(features)
        if hasattr(model, 'estimators_'):
            self.ext = forest_ce.ForestActionExtractor(model, Xa, Y=ytr.values, feature_names=features,
                                                       feature_types=['C'] * len(features), feature_constraints=cons, max_cancidates=100)
        else:
            self.ext = linear_ce.LinearActionExtractor(model, Xa, Y=ytr.values, feature_names=features,
                                                       feature_types=['C'] * len(features), feature_constraints=cons, max_cancidates=100)

    def explain(self, x0, spec, pol, with_rule, limit=120):
        import pulp
        F = self.features
        cons = []
        for f in F:
            d = direction(spec, x0, f)
            cons.append({'fixed': 'FIX', 'increase': 'INC', 'decrease': 'DEC', 'any': ''}[d])
        self.ext.feature_constraints_ = cons
        self.ext.AC_.feature_constraints_ = cons
        x = x0[F].values.astype(float)

        def add(prob):
            if not with_rule:
                return
            act = {v.name: v for v in prob.variables() if v.name.startswith('act_')}
            a = {f: act.get(f'act_{i}') for i, f in enumerate(F)}
            val = lambda f: (x[F.index(f)] + a[f]) if a[f] is not None else x[F.index(f)]
            for f in spec.actionable:
                if a[f] is not None:
                    prob += val(f) >= spec.bounds[f][0]
                    prob += val(f) <= spec.bounds[f][1]
            allc = list(pol.constraints) + list(spec.links)
            for c in allc:
                e = pulp.lpSum(w * val(f) for f, w in c.weights.items())
                prob += (e >= c.tau) if c.op == '>=' else (e <= c.tau) if c.op == '<=' else (e == c.tau)
            if pol.any_of:
                z = [pulp.LpVariable(f'rule_branch_{i}', cat='Binary') for i in range(len(pol.any_of))]
                prob += pulp.lpSum(z) >= 1
                for zi, br in zip(z, pol.any_of):
                    for c in br:
                        e = pulp.lpSum(w * val(f) for f, w in c.weights.items()); M = 1e4 * max(1.0, abs(c.tau))
                        if c.op in ('>=', '=='):
                            prob += e >= c.tau - M * (1 - zi)
                        if c.op in ('<=', '=='):
                            prob += e <= c.tau + M * (1 - zi)
        t0 = time.time(); status = 'ok'
        cwd = os.getcwd(); tmp = tempfile.mkdtemp(); os.chdir(tmp)     # DACE writes infeasible.lp on failure
        try:
            with pulp_extra(add), open(os.devnull, 'w') as dn, contextlib.redirect_stdout(dn):
                a = self.ext.extract(x, max_change_num=4, cost_type='DACE', alpha=0.01, solver='HiGHS', time_limit=limit)
        except Exception as e:      # noqa: BLE001
            a, status = -1, f'error:{type(e).__name__}'
        finally:
            os.chdir(cwd)
        sec = time.time() - t0
        if isinstance(a, int):
            if status == 'ok':
                status = 'infeasible' if LAST.get('status') == 'Infeasible' else 'time_limit' if 'Not Solved' in LAST.get('status', '') else LAST.get('status', 'failed')
            return None, status, sec
        xc = x0.copy(); xc[F] = x + a.a()
        return xc.astype(float), status, sec


# ---------------------------------------------------------------- MACE
def mace_import():
    # NumPy 2 compatibility for the 2021 MACE code (aliases removed from NumPy)
    for alias, val in [('infty', np.inf), ('float', float), ('int', int), ('bool', bool), ('object', object)]:
        if not hasattr(np, alias):
            setattr(np, alias, val)
    if 'generateSATExplanations' in sys.modules:
        return sys.modules['loadData'], sys.modules['generateSATExplanations']
    other = sys.modules.pop('utils', None)
    sys.path.insert(0, MACE_SRC)
    cwd = os.getcwd(); os.chdir(MACE_SRC)
    try:
        import loadData, generateSATExplanations as G  # noqa: E401
    finally:
        os.chdir(cwd); sys.path.remove(MACE_SRC); sys.modules.pop('utils', None)
        if other is not None:
            sys.modules['utils'] = other
    return loadData, G


class MaceRunner:
    def __init__(self, model, df, features, yname):
        self.loadData, self.G = mace_import()
        self.model, self.features = model, features
        lo, hi = df[features].min(), df[features].max()
        self.glob = {f: (float(lo[f]), float(hi[f])) for f in features}
        self.yname = yname

    def _dataset(self, x0, spec):
        LD = self.loadData; attrs = {}
        names = [f'x{i}' for i in range(len(self.features))]
        frame = {}
        for i, f in enumerate(self.features):
            d = direction(spec, x0, f)
            lo, hi = self.glob[f]
            lo, hi = min(lo, float(x0[f])), max(hi, float(x0[f]))
            act = {'fixed': 'none', 'increase': 'same-or-increase', 'decrease': 'same-or-decrease', 'any': 'any'}[d]
            attrs[names[i]] = LD.DatasetAttribute(attr_name_long=names[i], attr_name_kurz=names[i], attr_type='numeric-real',
                                                  node_type='input', actionability=act, mutability=act != 'none',
                                                  parent_name_long=-1, parent_name_kurz=-1, lower_bound=lo, upper_bound=hi)
            frame[names[i]] = [lo, hi]
        attrs['y'] = LD.DatasetAttribute(attr_name_long='y', attr_name_kurz='y', attr_type='binary', node_type='output',
                                         actionability='none', mutability=False, parent_name_long=-1, parent_name_kurz=-1,
                                         lower_bound=0, upper_bound=1)
        frame['y'] = [0, 1]
        return LD.Dataset(pd.DataFrame(frame), attrs, False, 'v3'), names

    def explain(self, x0, spec, pol, with_rule, limit=120):
        from pysmt.shortcuts import And, Or, GE, LE, Equals, Plus, Times, Real, ToReal
        G = self.G
        ds, names = self._dataset(x0, spec)
        sym = lambda ms, f: ms['counterfactual'][names[self.features.index(f)]]['symbol']
        orig = G.getPlausibilityFormula

        def plaus(model_symbols, dataset_obj, factual_sample, approach_string):
            base = orig(model_symbols, dataset_obj, factual_sample, approach_string)
            if not with_rule:
                return base
            lin = lambda c: Plus([Times(ToReal(sym(model_symbols, f)), Real(float(w))) for f, w in c.weights.items()])
            rel = lambda c: GE(lin(c), Real(float(c.tau))) if c.op == '>=' else LE(lin(c), Real(float(c.tau))) if c.op == '<=' \
                else Equals(lin(c), Real(float(c.tau)))
            parts = [base]
            for f in spec.actionable:
                parts += [GE(ToReal(sym(model_symbols, f)), Real(float(spec.bounds[f][0]))),
                          LE(ToReal(sym(model_symbols, f)), Real(float(spec.bounds[f][1])))]
            parts += [rel(c) for c in list(pol.constraints) + list(spec.links)]
            if pol.any_of:
                parts.append(Or([And([rel(c) for c in br]) for br in pol.any_of]))
            return And(parts)
        G.getPlausibilityFormula = plaus
        fs = {n: float(x0[f]) for n, f in zip(names, self.features)}; fs['y'] = False
        t0 = time.time(); status = 'ok'; out = None
        logf = tempfile.mktemp(suffix='.txt')
        try:
            with time_limit(limit), open(os.devnull, 'w') as dn, contextlib.redirect_stdout(dn):
                out = G.genExp(logf, self.model, ds, fs, 'one_norm', 'mace', 1e-3)
        except Timeout:
            status = 'time_limit'
        except Exception as e:      # noqa: BLE001
            status = f'error:{type(e).__name__}:{str(e)[:80]}'
        finally:
            G.getPlausibilityFormula = orig
            if os.path.exists(logf):
                os.remove(logf)
        sec = time.time() - t0
        if out is None or not out.get('cfe_found', False):
            return None, (status if status != 'ok' else 'not_found'), sec
        cf = out['cfe_sample']
        xc = x0.copy()
        for n, f in zip(names, self.features):
            xc[f] = float(cf[n])
        return xc.astype(float), status, sec


def hard_timeout(fn, args, sec):
    """Run fn(*args) in a forked child; kill it after sec seconds (solver C code ignores signals)."""
    import multiprocessing as mp
    ctx = mp.get_context('fork'); rd, wr = ctx.Pipe(duplex=False)

    def child():
        try:
            wr.send(fn(*args))
        except Exception as e:      # noqa: BLE001
            wr.send((None, f'error:{type(e).__name__}', float('nan')))
    t0 = time.time(); p = ctx.Process(target=child); p.start()
    if rd.poll(sec):
        out = rd.recv(); p.join(5)
    else:
        p.kill(); p.join(); out = (None, 'time_limit', time.time() - t0)
    return out


# ---------------------------------------------------------------- driver
def run(name, seed, models, methods, regimes, max_q, out_dir, limit, rf_methods=None, v3_dir='results_v3'):
    dom = DOMAINS[name]().load(); df = dom.df
    tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(df, df[dom.y], df[dom.group]))
    dtr, dte = df.iloc[tr], df.iloc[te]
    pol = dom.policy()
    for mname in models:
        path = f'{out_dir}/v3x_{name}_{mname}_s{seed}.csv.gz'
        if os.path.exists(path):
            print('exists', path, flush=True); continue
        f = make_model(mname, seed).fit(dtr[dom.features], dtr[dom.y])
        predict = lambda x, f=f: int(f.predict(pd.DataFrame([x[dom.features].astype(float)]))[0])
        base_model = raw_lr(f) if mname == 'lr' else f
        runners = {}
        meths = rf_methods if (mname == 'rf' and rf_methods) else methods
        v3f = f'{v3_dir}/v3_{name}_{mname}_s{seed}.csv.gz'
        v3q = set(zip(*[pd.read_csv(v3f, usecols=['stage', 'query'])[c] for c in ['stage', 'query']])) if os.path.exists(v3f) else None
        if 'dace' in meths:
            runners['dace'] = DaceRunner(base_model, dtr, dtr[dom.y], dom.features)
        if 'mace' in meths:
            runners['mace'] = MaceRunner(base_model, df, dom.features, dom.y)
        rng = np.random.RandomState(seed)          # identical query sample to experiment_v3
        part = path.replace('.csv.gz', '.part.csv'); rows, done = [], set()
        if os.path.exists(part):
            prev = pd.read_csv(part); rows = prev.to_dict('records'); done = set(zip(prev.stage, prev['query']))
        n_new, t_all = 0, time.time()
        for k in dom.stages:
            partial, at_risk = dom.stage(k, dte, f, dtr, P.cat(seed))
            elig = np.where(at_risk & (f.predict(partial) == 0))[0]
            if v3q is not None:                  # restrict to the queries evaluated in experiment_v3 (matched comparison)
                elig = np.array([i for i in elig if (k, int(dte.index[i])) in v3q], dtype=int)
            if max_q and len(elig) > max_q:
                elig = np.sort(rng.choice(elig, max_q, replace=False))
            for qi in elig:
                if (k, int(dte.index[qi])) in done:
                    continue
                row = dte.iloc[qi]; x0 = partial.iloc[qi].astype(float)
                for regime in regimes:
                    s = dom.spec(row, k, regime)
                    if s is None:
                        continue
                    spec = s[0]
                    for meth, rnr in runners.items():
                        for with_rule in (False, True):
                            x, st, sec = hard_timeout(rnr.explain, (x0, spec, pol, with_rule, limit), limit + 60)
                            ok, reasons, _ = C.gate(x, x0, spec, pol, predict)
                            rows.append(dict(dataset=name, model=mname, seed=seed, stage=k, regime=regime, query=int(dte.index[qi]),
                                             y_true=int(row[dom.y]), condition=meth + ('_rule' if with_rule else ''),
                                             accepted=int(ok), reasons=';'.join(reasons) or 'OK',
                                             effort=C.effort(x, x0, spec) if x is not None else np.nan,
                                             sparsity=C.sparsity(x, x0, spec) if x is not None else np.nan,
                                             cost=cost(x, x0, spec), seconds=sec, exact_status=st))
                n_new += 1
                if n_new % 1 == 0:
                    pd.DataFrame(rows).to_csv(part, index=False)
            print(f'{name} {mname} seed={seed} stage={k} queries={len(elig)} elapsed={time.time()-t_all:.0f}s', flush=True)
        pd.DataFrame(rows).to_csv(path, index=False)
        if os.path.exists(part):
            os.remove(part)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('dataset'); ap.add_argument('--seeds', default='0')
    ap.add_argument('--models', default='lr,rf'); ap.add_argument('--methods', default='dace,mace')
    ap.add_argument('--regimes', default='aligned'); ap.add_argument('--max_q', type=int, default=0)
    ap.add_argument('--out', default='results_v3'); ap.add_argument('--limit', type=int, default=120)
    ap.add_argument('--rf_methods', default='')
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    for s in [int(x) for x in a.seeds.split(',')]:
        run(a.dataset, s, a.models.split(','), a.methods.split(','), a.regimes.split(','), a.max_q, a.out, a.limit,
            rf_methods=a.rf_methods.split(',') if a.rf_methods else None)
