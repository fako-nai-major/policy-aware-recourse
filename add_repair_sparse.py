"""Add the sparsity-aware repair to every finished experiment_v3 file.

Conditions written (replacing earlier rows of the same name):
  repair_sparse0  rule-only MILP: min effort + 0.5 sparsity over R(x0), no model (cf. 'repair')
  repair_sparse   the same with escalation of the rule margin until f agrees (cf. 'repair_esc')
Resumable (per-file part files and locks; finished files in logs/repair_sparse_done.txt).

Usage: python add_repair_sparse.py [filter] [reverse]
"""
import glob, os, sys, time, warnings
import numpy as np, pandas as pd
from sklearn.model_selection import GroupShuffleSplit
import prescriptive as P
from recourse import core as C, exact as E
from recourse.domains import DOMAINS
import recourse.configs  # noqa: F401
from experiment_v3 import make_model, cost, LAM_SPAR

warnings.filterwarnings('ignore')
DONE = 'logs/repair_sparse_done.txt'
FILT = sys.argv[1] if len(sys.argv) > 1 else ''
REV = len(sys.argv) > 2 and sys.argv[2] == 'reverse'
CONDS = ['repair_sparse0', 'repair_sparse']


def main():
    done = set(open(DONE).read().split()) if os.path.exists(DONE) else set()
    files = sorted(glob.glob('results_v3/v3_*.csv.gz'), key=lambda p: ('OULAD' in p, 'rf' in p, p))
    files = [p for p in files if FILT in p]
    for path in (files[::-1] if REV else files):
        if path in done:
            continue
        part, lock = path.replace('.csv.gz', '.rs.part.csv'), path + '.rs.lock'
        if os.path.exists(lock) and time.time() - os.path.getmtime(part if os.path.exists(part) else lock) < 900:
            continue
        if os.path.getsize(path) < 100:            # model predicted no unfavourable query (empty file)
            continue
        open(lock, 'w').close()
        d = pd.read_csv(path)
        name, mname, seed = d.dataset.iloc[0], d.model.iloc[0], int(d.seed.iloc[0])
        dom = DOMAINS[name]().load(); df = dom.df
        tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(df, df[dom.y], df[dom.group]))
        dtr, dte = df.iloc[tr], df.iloc[te]
        f = make_model(mname, seed).fit(dtr[dom.features], dtr[dom.y])
        predict = lambda x, f=f: int(f.predict(pd.DataFrame([x[dom.features].astype(float)]))[0])
        pol = dom.policy()
        new = pd.read_csv(part).to_dict('records') if os.path.exists(part) else []
        seen = {(r['stage'], r['query'], r['regime']) for r in new}
        keys = d[d.condition == 'exact'][['stage', 'query', 'regime', 'y_true']].drop_duplicates(['stage', 'query', 'regime'])
        partials, t0 = {}, time.time()
        for k, q, rg, yt in keys.itertuples(index=False):
            if (k, q, rg) in seen:
                continue
            if k not in partials:
                partials[k] = dom.stage(k, dte, f, dtr, P.cat(seed))[0]
            row = df.loc[q]; x0 = partials[k].loc[q].astype(float)
            spec = dom.spec(row, k, rg)[0]
            base = dict(dataset=name, model=mname, seed=seed, stage=k, regime=rg, query=q, y_true=yt)
            for cond, pr in [('repair_sparse0', None), ('repair_sparse', predict)]:
                t1 = time.time(); x = E.repair_sparse(x0, spec, pol, pr, lam_spar=LAM_SPAR); sec = time.time() - t1
                ok, reasons, _ = C.gate(x, x0, spec, pol, predict)
                new.append(dict(base, condition=cond, accepted=int(ok), reasons=';'.join(reasons) or 'OK',
                                effort=C.effort(x, x0, spec) if x is not None else np.nan,
                                sparsity=C.sparsity(x, x0, spec) if x is not None else np.nan,
                                cost=cost(x, x0, spec), seconds=sec))
            pd.DataFrame(new).to_csv(part, index=False)
        out = pd.concat([d[~d.condition.isin(CONDS)], pd.DataFrame(new)], ignore_index=True)
        out.to_csv(path, index=False)
        for p in (part, lock):
            if os.path.exists(p):
                os.remove(p)
        with open(DONE, 'a') as fh:
            fh.write(path + '\n')
        print(f'{path}: {len(keys)} queries in {time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
