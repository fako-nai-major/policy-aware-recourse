"""Checks for the exact (MILP) solver: brute-force optimality on a 2-feature grid,
disjunctive rules, structural links, certified infeasibility.  Run: python tests/test_exact.py"""
import os, sys, warnings
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from catboost import CatBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from recourse import core as C, exact as E

rng = np.random.RandomState(0)
n = 3000
X = pd.DataFrame({'a': rng.uniform(0, 100, n), 'b': rng.uniform(0, 100, n), 'c': rng.uniform(0, 10, n)})
y = ((X.a * 0.6 + X.b * 0.4 + rng.normal(0, 8, n)) > 55).astype(int)
F = list(X.columns)
models = {'lr': LogisticRegression(max_iter=1000).fit(X, y),
          'rf': RandomForestClassifier(30, max_depth=5, random_state=0).fit(X, y),
          'cat': CatBoostClassifier(iterations=60, depth=4, verbose=0, random_seed=0).fit(X, y),
          'mlp': make_pipeline(StandardScaler(), MLPClassifier((20, 20), max_iter=1000, random_state=0)).fit(X, y)}

def brute(m, x0, spec, pol, lam_spar=0.5, step=0.5):
    best = None
    ga = np.arange(spec.bounds['a'][0], spec.bounds['a'][1] + 1e-9, step)
    gb = np.arange(spec.bounds['b'][0], spec.bounds['b'][1] + 1e-9, step)
    A, Bv = np.meshgrid(ga, gb); P = pd.DataFrame({'a': A.ravel(), 'b': Bv.ravel(), 'c': x0['c']})
    ok = m.predict(P[F]) == 1
    for i in np.where(ok)[0]:
        x = P.iloc[i]
        if not (pol.ok(x) and spec.links_ok(x)):
            continue
        cost = C.effort(x, x0, spec) + lam_spar * C.sparsity(x, x0, spec)
        if best is None or cost < best:
            best = cost
    return best

fails = 0
# parser check: sign of the parsed MLP logit equals sklearn's prediction
m = models['mlp']; enc = E.parse_model(m, F); Z = X.sample(500, random_state=1)
agree = np.mean([(E.score(enc, z.values) > 0) == bool(p) for (_, z), p in zip(Z.iterrows(), m.predict(Z))])
print('mlp parser agreement', agree); fails += agree < 1
x0 = pd.Series({'a': 30.0, 'b': 40.0, 'c': 5.0})
spec = C.Spec(F, ['a', 'b'], ['c'], {'a': (30.0, 100.0), 'b': (40.0, 100.0)})
rules = {
    'and': C.Policy([C.Constraint({'a': 1, 'b': 1}, '>=', 110, 'sum')]),
    'or': C.Policy([], [[C.Constraint({'a': 1}, '>=', 80, 'a_hi')], [C.Constraint({'b': 1}, '>=', 90, 'b_hi')]]),
}
for mname, m in models.items():
    enc = E.parse_model(m, F)
    predict = lambda x, m=m: m.predict(pd.DataFrame([x[F].astype(float)]))[0]
    for rname, pol in rules.items():
        r = E.solve_exact(enc, x0, spec, pol)
        ok, reasons, _ = C.gate(r.x, x0, spec, pol, predict)
        cost = C.effort(r.x, x0, spec) + 0.5 * C.sparsity(r.x, x0, spec)
        bf = brute(m, x0, spec, pol)
        good = ok and r.status == 'optimal' and cost <= bf + 1e-3
        fails += not good
        print(f'{mname:4s} {rname:4s} exact={cost:.4f} grid={bf:.4f} gate={ok} {reasons} {"OK" if good else "FAIL"}')
# extra brute-force checks for the ReLU network at random starting points
m = models['mlp']; enc = E.parse_model(m, F); predict = lambda x, m=m: m.predict(pd.DataFrame([x[F].astype(float)]))[0]
for t in range(6):
    a0, b0 = rng.uniform(5, 45), rng.uniform(5, 45)
    xq = pd.Series({'a': a0, 'b': b0, 'c': rng.uniform(0, 10)})
    sq = C.Spec(F, ['a', 'b'], ['c'], {'a': (a0, 100.0), 'b': (b0, 100.0)})
    for rname, pol in rules.items():
        r = E.solve_exact(enc, xq, sq, pol)
        ok, reasons, _ = C.gate(r.x, xq, sq, pol, predict)
        cst = C.effort(r.x, xq, sq) + 0.5 * C.sparsity(r.x, xq, sq)
        bf = brute(m, xq, sq, pol)
        good = ok and r.status == 'optimal' and cst <= bf + 1e-3
        fails += not good
        print(f'mlp#{t} {rname:4s} exact={cst:.4f} grid={bf:.4f} {"OK" if good else "FAIL"}')
# structural link: b moves with a (b - b0 = 0.5 (a - a0)); a is the only costed action
spec2 = C.Spec(F, ['a', 'b'], ['c'], {'a': (30.0, 100.0), 'b': (40.0, 100.0)},
               links=[C.Constraint({'b': 1, 'a': -0.5}, '==', 40.0 - 0.5 * 30.0, 'b_follows_a')], derived=('b',))
pol = rules['and']
m = models['rf']; enc = E.parse_model(m, F); predict = lambda x: m.predict(pd.DataFrame([x[F].astype(float)]))[0]
r = E.solve_exact(enc, x0, spec2, pol)
ok, reasons, _ = C.gate(r.x, x0, spec2, pol, predict)
print('link', r.status, ok, reasons, dict(r.x[['a', 'b']].round(3)))
fails += not ok
# completion respects links
xc = C.complete_joint(x0.copy(), x0, spec2, pol, predict)
okc, rc, _ = C.gate(xc, x0, spec2, pol, predict)
print('link completion', okc, rc, dict(xc[['a', 'b']].round(3)))
fails += not okc
# certified infeasibility: rule unattainable within bounds
pol_bad = C.Policy([C.Constraint({'a': 1, 'b': 1}, '>=', 250, 'sum')])
r = E.solve_exact(enc, x0, spec, pol_bad)
print('infeasible ->', r.status); fails += r.status != 'infeasible'
print('FAILURES:', fails)
sys.exit(1 if fails else 0)
