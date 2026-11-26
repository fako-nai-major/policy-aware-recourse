"""Domain-agnostic policy-aware recourse (v2).

A recommendation is accepted only if the complete final vector
  (i)   satisfies every constraint of the encoded policy,
  (ii)  receives the desired class from a fresh prediction of the outcome model f,
  (iii) keeps every actionable feature within its bounds, and
  (iv)  leaves every non-actionable feature exactly unchanged.

The policy is a list of linear constraints  sum_j w_j x_j  (>= or <=)  tau.
The v1 education rule is the special case of one '>=' constraint over the
assessment features.  Everything here reproduces v1 exactly for that case
(selection, 'grid' completion, gate, direct repair); 'joint' completion and
multi-constraint policies are the v2 extensions.
"""
from dataclasses import dataclass, field
import numpy as np
import pandas as pd
from scipy.optimize import linprog

EQ_TOL = 1e-6      # tolerance for equality (structural) constraints


# ---------------------------------------------------------------- policy
@dataclass
class Constraint:
    weights: dict          # feature -> weight
    op: str                # '>=' or '<='
    tau: float
    name: str = 'policy'

    def value(self, x):
        return float(sum(float(x[f]) * w for f, w in self.weights.items()))

    def ok(self, x):
        v = self.value(x)
        if self.op == '==':
            return abs(v - self.tau) <= EQ_TOL * max(1.0, abs(self.tau))
        return v >= self.tau if self.op == '>=' else v <= self.tau

    def violation(self, x):
        """Normalised shortfall (v1: max(0, tau - s) / tau)."""
        v = self.value(x)
        if self.op == '==':
            gap = abs(v - self.tau) if not self.ok(x) else 0.0
        else:
            gap = (self.tau - v) if self.op == '>=' else (v - self.tau)
        return max(0.0, gap) / abs(self.tau) if self.tau != 0 else max(0.0, gap)

    def shifted(self, delta):
        """Constraint tightened by delta (>= : tau+delta, <= : tau-delta)."""
        if self.op == '==':
            return self
        return Constraint(self.weights, self.op, self.tau + (delta if self.op == '>=' else -delta), self.name)


@dataclass
class Policy:
    """Rule = AND(constraints) and, if any_of is given, OR over branches (each an AND list)."""
    constraints: list = field(default_factory=list)   # empty list = no rule (criterion inactive)
    any_of: list = field(default_factory=list)        # list of lists of Constraint (v3 disjunctive rules)
    name_any: str = 'any_of'

    @property
    def active(self):
        return len(self.constraints) > 0 or len(self.any_of) > 0

    def branch_ok(self, x, b):
        return all(c.ok(x) for c in b)

    def ok(self, x):
        return all(c.ok(x) for c in self.constraints) and (not self.any_of or any(self.branch_ok(x, b) for b in self.any_of))

    def penalty(self, x):
        p = float(sum(c.violation(x) for c in self.constraints))
        if self.any_of:
            p += min(float(sum(c.violation(x) for c in b)) for b in self.any_of)
        return p

    def score(self, x):
        """Primary constraint value (reported as policy_score)."""
        if self.constraints:
            return self.constraints[0].value(x)
        return self.any_of[0][0].value(x) if self.any_of else np.nan

    def failed(self, x):
        out = [c for c in self.constraints if not c.ok(x)]
        if self.any_of and not any(self.branch_ok(x, b) for b in self.any_of):
            out.append(Constraint({}, '>=', 0.0, self.name_any))
        return out

    def branches(self):
        """Conjunctive branches: list of constraint lists (one per any_of branch)."""
        if not self.any_of:
            return [list(self.constraints)]
        return [list(self.constraints) + list(b) for b in self.any_of]

    def shifted(self, frac):
        """Tighten every constraint by frac * |tau|."""
        return Policy([c.shifted(frac * abs(c.tau)) for c in self.constraints],
                      [[c.shifted(frac * abs(c.tau)) for c in b] for b in self.any_of], self.name_any)

    def with_tau(self, tau):
        """Replace the threshold of a single-constraint policy (threshold sweeps)."""
        assert len(self.constraints) == 1
        c = self.constraints[0]
        return Policy([Constraint(c.weights, c.op, tau, c.name)])


# ---------------------------------------------------------------- query specification
@dataclass
class Spec:
    features: list         # model feature order
    actionable: list
    immutable: list
    bounds: dict           # actionable feature -> (lb, ub)  (gate / completion bounds)
    links: list = field(default_factory=list)     # v3: structural linear constraints (Constraint, op <=, >= or ==)
    derived: tuple = ()                            # v3: actionable features that follow from others (no effort)

    def rng(self, f):
        return max(self.bounds[f][1] - self.bounds[f][0], 1e-9)

    @property
    def costed(self):
        return [f for f in self.actionable if f not in self.derived]

    def links_ok(self, x):
        return all(c.ok(x) for c in self.links)


def effort(x, x0, spec):
    return float(sum(abs(float(x[f]) - float(x0[f])) / spec.rng(f) for f in spec.costed))


def sparsity(x, x0, spec):
    return int(sum(not np.isclose(float(x[f]), float(x0[f])) for f in spec.costed))


# ---------------------------------------------------------------- selection (v1 objective)
LAMBDA = dict(lambda_policy=1000.0, lambda_feas=1000.0, lambda_prox=1.0, lambda_spar=0.5)


def _feas(x, x0, spec):
    n = 0
    for f in spec.actionable:
        lb, ub = spec.bounds[f]
        if not lb <= x[f] <= ub:
            n += 1
    for f in spec.immutable:
        if not np.isclose(x[f], x0[f]):
            n += 1
    n += sum(1 for c in spec.links if not c.ok(x))
    return n


def objective_terms(x, x0, spec, policy):
    pol = policy.penalty(x) if policy.active else 0.0
    return pol, _feas(x, x0, spec), effort(x, x0, spec), sparsity(x, x0, spec)


def rank(pool, x0, spec, policy, lam=LAMBDA):
    """Return pool with objective columns, sorted as v1 (stable) and the best index."""
    rows = []
    for i, (_, x) in enumerate(pool.iterrows()):
        pol, feas, prox, spar = objective_terms(x, x0, spec, policy)
        obj = lam['lambda_policy'] * pol + lam['lambda_feas'] * feas + lam['lambda_prox'] * prox + lam['lambda_spar'] * spar
        rows.append((i, obj))
    objs = np.array([o for _, o in rows])
    tied = [i for i, o in rows if abs(o - objs.min()) <= 1e-3]

    def tiebreak(i):
        x = pool.iloc[i]
        return (sum(not np.isclose(x[f], x0[f]) for f in spec.actionable),
                sum(abs(x[f] - x0[f]) for f in spec.actionable),
                sum(x[f] for f in spec.actionable if not np.isclose(x[f], 0)))
    best = sorted(tied, key=tiebreak)[0]
    ranked = pool.copy()
    ranked['objective_score'] = objs
    return best, ranked


# ---------------------------------------------------------------- completion
def complete_grid(x, x0, spec, policy, lam=LAMBDA):
    """v1 bounded editing: each actionable feature equal to 0 is replaced by the
    lowest-cost value of linspace(lb, ub, 10) at which the policy is met on its own."""
    x = x.copy()
    for f in spec.actionable:
        if x[f] == 0:
            lb, ub = spec.bounds[f]
            best = None
            for v in np.linspace(lb, ub, num=10):
                t = x.copy(); t[f] = v
                if not lb <= v <= ub:
                    continue
                if not all(np.isclose(t[m], x0[m]) for m in spec.immutable):
                    continue
                if (policy.penalty(t) if policy.active else 0.0) != 0:
                    continue
                o = lam['lambda_prox'] * abs(v - x0[f]) / spec.rng(f) + lam['lambda_spar'] * (not np.isclose(v, x0[f]))
                if best is None or o < best[1]:
                    best = (v, o)
            if best is not None:
                x[f] = best[0]
    return x


def _lp_fill(x, x0, spec, policy, free, margin=0.0):
    """Minimum normalised L1 change of the free features (from their current
    values) s.t. bounds, structural links and the policy tightened by margin*|tau|.
    For a disjunctive policy each branch is solved and the cheapest is kept.
    Returns the new vector or None if infeasible.  Non-free features keep their values."""
    free = list(free)
    pol = policy.shifted(margin) if policy.active else policy
    if not free:
        return x.copy() if (pol.ok(x) and spec.links_ok(x)) else None
    n = len(free)
    cur = np.array([float(x[f]) for f in free])
    # variables: v (n), u (n) with u >= |v - cur|; minimise sum u / range (derived features cost nothing)
    c = np.concatenate([np.zeros(n), [0.0 if f in spec.derived else 1.0 / spec.rng(f) for f in free]])
    A0, b0 = [], []
    for i in range(n):           # v - cur <= u ; cur - v <= u
        r = np.zeros(2 * n); r[i] = 1; r[n + i] = -1; A0.append(r); b0.append(cur[i])
        r = np.zeros(2 * n); r[i] = -1; r[n + i] = -1; A0.append(r); b0.append(-cur[i])
    Ae, be = [], []
    for con in spec.links:
        fixed = sum(float(x[f]) * w for f, w in con.weights.items() if f not in free)
        coef = np.concatenate([[con.weights.get(f, 0.0) for f in free], np.zeros(n)])
        if con.op == '==':
            Ae.append(coef); be.append(con.tau - fixed)
        elif con.op == '>=':
            A0.append(-coef); b0.append(-(con.tau - fixed))
        else:
            A0.append(coef); b0.append(con.tau - fixed)
    bnds = [spec.bounds[f] for f in free] + [(0, None)] * n
    best = None
    for branch in (pol.branches() if pol.active else [[]]):
        A, b = list(A0), list(b0)
        for con in branch:
            fixed = sum(float(x[f]) * w for f, w in con.weights.items() if f not in free)
            coef = np.concatenate([[con.weights.get(f, 0.0) for f in free], np.zeros(n)])
            eps = 1e-6
            if con.op == '>=':      # coef.v >= tau - fixed  ->  -coef.v <= -(tau - fixed) - eps
                A.append(-coef); b.append(-(con.tau - fixed) - eps)
            elif con.op == '<=':
                A.append(coef); b.append(con.tau - fixed - eps)
            else:
                Ae.append(coef); be.append(con.tau - fixed)
        res = linprog(c, A_ub=np.array(A), b_ub=np.array(b), A_eq=np.array(Ae) if Ae else None,
                      b_eq=np.array(be) if be else None, bounds=bnds, method='highs')
        if res.success and (best is None or res.fun < best.fun - 1e-12):
            best = res
    if best is None:
        return None
    y = x.copy()
    for i, f in enumerate(free):
        y[f] = float(np.clip(best.x[i], *spec.bounds[f]))
    return y


def complete_joint(x, x0, spec, policy, predict=None, steps=24, step_frac=0.0625, free_violated=False):
    """v2 completion.  Free set = actionable features the candidate left at their
    original value plus any actionable feature outside its bounds.  The free
    features are moved jointly, at minimum normalised change, into their bounds and
    (if possible) onto the policy.  With `predict`, the policy target is raised in
    steps of step_frac*|tau| until f also accepts (verified completion)."""
    free = [f for f in spec.actionable
            if np.isclose(float(x[f]), float(x0[f])) or not spec.bounds[f][0] <= float(x[f]) <= spec.bounds[f][1]]
    for con in spec.links:            # v3: features of violated structural links are re-solved
        if not con.ok(x):
            free += [f for f in con.weights if f in spec.actionable and f not in free]
    if free_violated and policy.active and not policy.ok(x):
        # v3 option for single-candidate generators: actionable features of violated rule
        # constraints may also be moved (within their bounds), not only the untouched ones
        viol = [c for c in policy.constraints if not c.ok(x)]
        if policy.any_of and not any(policy.branch_ok(x, br) for br in policy.any_of):
            viol += [c for br in policy.any_of for c in br if not c.ok(x)]
        for con in viol:
            free += [f for f, w in con.weights.items() if w != 0 and f in spec.actionable and f not in free]
    if not policy.active:
        y = x.copy()
        for f in free:
            y[f] = float(np.clip(float(y[f]), *spec.bounds[f]))
        return y
    best = None
    for k in range(steps + 1 if predict is not None else 1):
        y = _lp_fill(x, x0, spec, policy, free, margin=k * step_frac)
        if y is None:
            break
        best = y
        if predict is None or int(predict(y)) == 1:
            return y
    if best is not None:
        return best
    # policy unreachable over the free set: still repair bounds at minimum change
    y = x.copy()
    for f in free:
        y[f] = float(np.clip(float(y[f]), *spec.bounds[f]))
    return y


# ---------------------------------------------------------------- acceptance gate
def gate(x, x0, spec, policy, predict, desired=1):
    """Return (accepted, reasons, policy_score).  Mirrors PresAnEx.apply_hard_gate."""
    if x is None:
        return False, ['no_candidate'], np.nan
    reasons = []
    for f in spec.features:
        v = x[f]
        if pd.isna(v) or not np.isfinite(float(v)):
            return False, [f'nonfinite_feature:{f}'], np.nan
    for c in policy.failed(x) if policy.active else []:
        reasons.append('below_policy_threshold' if (len(policy.constraints) == 1 and not policy.any_of) else f'policy_violated:{c.name}')
    reasons += ['inconsistent:' + c.name for c in spec.links if not c.ok(x)]
    reasons += ['out_of_bounds:' + f for f in spec.actionable if not spec.bounds[f][0] <= float(x[f]) <= spec.bounds[f][1]]
    reasons += ['immutable_changed:' + f for f in spec.features if f not in spec.actionable and x[f] != x0[f]]
    if int(predict(x)) != desired:
        reasons.append('classifier_target_not_met')
    return (not reasons), reasons, policy.score(x)


# ---------------------------------------------------------------- direct repair baseline
def repair(x0, spec, policy, predict=None, steps=24, step_frac=0.0625):
    """Rule-based recourse without a generator: clip to bounds, then change the
    actionable policy features at minimum normalised effort until the policy holds
    (v1: greedy fill to tau + 1e-6).  With `predict`, escalate the target in steps
    of step_frac*|tau| until f agrees."""
    if not policy.active:
        return None
    allc = list(policy.constraints) + [c for b in policy.any_of for c in b]
    pol_feats = [f for f in spec.actionable if any(c.weights.get(f, 0) != 0 for c in allc)]
    # v3: actions that move rule features through structural links
    for con in spec.links:
        if any(f in pol_feats for f in con.weights):
            pol_feats += [f for f in con.weights if f in spec.actionable and f not in pol_feats]
    if not pol_feats:
        return None
    base = x0.copy()
    for f in spec.actionable:
        base[f] = min(max(float(base[f]), spec.bounds[f][0]), spec.bounds[f][1])
    single = len(policy.constraints) == 1 and not policy.any_of and not spec.links and policy.constraints[0].op == '>=' and \
        all(policy.constraints[0].weights.get(f, 0) >= 0 for f in pol_feats)
    x = base
    for k in range(steps + 1 if predict is not None else 1):
        if single:     # exact v1 greedy (equivalent to the LP for one monotone constraint)
            con = policy.constraints[0]; w = con.weights
            tests = [f for f in pol_feats if w.get(f, 0) > 0]
            order = sorted(tests, key=lambda a: 1.0 / (w[a] * spec.rng(a)))
            tgt = con.tau + k * step_frac * abs(con.tau)
            x = base.copy(); deficit = (tgt + 1e-6) - con.value(x)
            for a in order:
                if deficit <= 1e-9:
                    break
                room = (spec.bounds[a][1] - float(x[a])) * w[a]
                add = min(room, deficit)
                x[a] = float(x[a]) + add / w[a]; deficit -= add
            if deficit > 1e-9:
                return x
        else:
            y = _lp_fill(base, x0, spec, policy, pol_feats, margin=k * step_frac)
            if y is None:
                return x
            x = y
        if predict is None or int(predict(x)) == 1:
            return x
    return x
