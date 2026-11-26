import sys, os, warnings; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
from sklearn.model_selection import GroupShuffleSplit
import prescriptive as P
from recourse.domains import DOMAINS
from recourse import core as C, exact as E
ds, seed, perstage = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
dom = DOMAINS[ds]().load(); df = dom.df; cfg = dom.cfg
tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(df, df[dom.y], df[dom.group]))
dtr, dte = df.iloc[tr], df.iloc[te]
f = P.cat(seed).fit(dtr[dom.features], dtr[dom.y]); enc = E.parse_model(f, dom.features)
predict = lambda x: f.predict(pd.DataFrame([x[dom.features].astype(float)]))[0]
rows = pd.read_csv(f'results_v2/presc_{ds}_s{seed}_rows.csv.gz')
tau0 = dom.policy().constraints[0].tau
rows = rows[np.isclose(rows.tau, tau0)]
out = []
for regime in ['aligned', 'floor']:
    qs = rows[(rows.regime == regime) & (rows.condition == 'dice_first')][['stage', 'query']].drop_duplicates()
    qs = qs.groupby('stage').head(perstage)
    for k, q in qs.itertuples(index=False):
        row = df.loc[q]; x0 = row[dom.features].astype(float).copy()
        if k: x0[cfg.tests[k:]] = 0.0
        spec = dom.spec(row, k, regime)[0]; pol = dom.policy()
        r = E.solve_exact(enc, x0, spec, pol, lam_spar=0.5, time_limit=120)
        ok, reasons, _ = C.gate(r.x, x0, spec, pol, predict) if r.x is not None else (False, [r.status], None)
        out.append(dict(dataset=ds, seed=seed, regime=regime, stage=k, query=q, status=r.status, accepted=int(ok), reasons=';'.join(reasons),
                        seconds=r.seconds, n_binary=r.n_binary, effort=C.effort(r.x, x0, spec) if r.x is not None else np.nan,
                        sparsity=C.sparsity(r.x, x0, spec) if r.x is not None else np.nan))
        if len(out) % 25 == 0:
            d = pd.DataFrame(out); print(len(d), d.status.value_counts().to_dict(), 'sec med', round(d.seconds.median(), 2), 'max', round(d.seconds.max(), 1), flush=True)
pd.DataFrame(out).to_csv(f'pilot/exact_{ds}_s{seed}.csv', index=False)
d = pd.DataFrame(out); print(d.groupby(['regime', 'stage']).agg(n=('accepted', 'size'), acc=('accepted', 'mean'), sec=('seconds', 'median'), secmax=('seconds', 'max'), nb=('n_binary', 'median')))
print(d.status.value_counts())
