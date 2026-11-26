"""Feasibility pilot: exact MILP recourse on seed-0 queries; compare with stored v2 results (CatBoost)."""
import sys, os, warnings, time; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import prescriptive as P
from recourse.domains import DOMAINS; import recourse.configs
from recourse import core as C, exact as E
ds, seed = sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 0
maxq = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
dom = DOMAINS[ds]().load(); df = dom.df
tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(df, df[dom.y], df[dom.group]))
Xtr, ytr = df.iloc[tr][dom.features], df.iloc[tr][dom.y]; dte = df.iloc[te]
models = {'catboost': P.cat(seed).fit(Xtr, ytr),
          'rf': RandomForestClassifier(100, max_depth=8, random_state=seed, n_jobs=2).fit(Xtr, ytr),
          'lr': make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(Xtr, ytr)}
pol = dom.policy(); out = []
for name, m in models.items():
    enc = E.parse_model(m, dom.features)
    predict = lambda x, m=m: m.predict(pd.DataFrame([x[dom.features].astype(float)]))[0]
    q = np.where(m.predict(dte[dom.features]) == 0)[0][:maxq]
    for qi in q:
        row = dte.iloc[qi]; x0 = row[dom.features].astype(float)
        s = dom.spec(row, 0, 'aligned')
        if s is None:
            continue
        spec = s[0]
        r = E.solve_exact(enc, x0, spec, pol, lam_spar=0.5, time_limit=60)
        ok, reasons, _ = C.gate(r.x, x0, spec, pol, predict) if r.x is not None else (False, [r.status], None)
        out.append(dict(dataset=ds, seed=seed, model=name, query=int(dte.index[qi]), status=r.status, accepted=int(ok),
                        reasons=';'.join(reasons), seconds=r.seconds, n_binary=r.n_binary, n_vars=r.n_vars, n_rows=r.n_rows,
                        objective=r.objective,
                        effort=C.effort(r.x, x0, spec) if r.x is not None else np.nan,
                        sparsity=C.sparsity(r.x, x0, spec) if r.x is not None else np.nan))
    d = pd.DataFrame([o for o in out if o['model'] == name])
    print(f"{ds} {name}: q={len(d)} status={d.status.value_counts().to_dict()} gate_ok={d.accepted.mean():.3f} "
          f"sec median={d.seconds.median():.2f} max={d.seconds.max():.1f} binaries~{int(d.n_binary.median())}", flush=True)
pd.DataFrame(out).to_csv(f'pilot/exact_{ds}_s{seed}.csv', index=False)
