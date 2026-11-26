"""Recompute the 'exact' rows of finished experiment_v3 files with the current solver
(highspy with integrality tolerance 1e-9; tightened inequality links).  Other conditions
are untouched.  Resumable: finished files are listed in logs/exact_rerun_done.txt.

Usage: python rerun_exact.py [results_v3]
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
RES = sys.argv[1] if len(sys.argv) > 1 else 'results_v3'
DONE = os.environ.get('EXACT_DONE', 'logs/exact_rerun_done.txt')
LIMIT = {'OULAD': 60}
FIX_ONLY = '--fix' in sys.argv
if FIX_ONLY:
    sys.argv.remove('--fix'); DONE = 'logs/exact_fix_done.txt'
TL_ONLY = '--tl' in sys.argv           # re-solve only time-limited rows (e.g. after a run under CPU contention)
if TL_ONLY:
    sys.argv.remove('--tl'); DONE = os.environ.get('EXACT_DONE', 'logs/exact_tl_done.txt'); FIX_ONLY = True


def main():
    done = set(open(DONE).read().split()) if os.path.exists(DONE) else set()
    files = sorted(glob.glob(f'{RES}/v3_*.csv.gz'), key=lambda p: ('OULAD' in p, 'rf' in p, p))
    if len(sys.argv) > 3 and sys.argv[3] == 'reverse':
        files = files[::-1]
    for path in files:
        done = set(open(DONE).read().split()) if os.path.exists(DONE) else set()   # re-read: other workers
        if path in done or (len(sys.argv) > 2 and sys.argv[2] not in path) or \
                (os.environ.get('TREES_ONLY') and not any(f'_{m}_s' in path for m in ('rf', 'cat'))) or \
                (os.environ.get('SKIP') and os.environ['SKIP'] in path):
            continue
        part0 = path.replace('.csv.gz', '.exact.part.csv'); lock = path + '.lock'
        if os.path.exists(lock) and time.time() - os.path.getmtime(part0 if os.path.exists(part0) else lock) < 600:
            continue                       # another worker is on this file
        open(lock, 'w').close()
        d = pd.read_csv(path)
        name, mname, seed = d.dataset.iloc[0], d.model.iloc[0], int(d.seed.iloc[0])
        dom = DOMAINS[name]().load(); df = dom.df
        tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(df, df[dom.y], df[dom.group]))
        dtr, dte = df.iloc[tr], df.iloc[te]
        f = make_model(mname, seed).fit(dtr[dom.features], dtr[dom.y]); enc = E.parse_model(f, dom.features)
        predict = lambda x, f=f: int(f.predict(pd.DataFrame([x[dom.features].astype(float)]))[0])
        pol = dom.policy()
        part = path.replace('.csv.gz', '.exact.part.csv')
        new = pd.read_csv(part).to_dict('records') if os.path.exists(part) else []
        seen = {(r['stage'], r['query'], r['regime']) for r in new}
        partials = {}
        t0 = time.time()
        ex = d[d.condition == 'exact']
        if FIX_ONLY:                       # re-solve only optimal solutions the gate rejected
            ex = ex[ex.exact_status == 'time_limit'] if TL_ONLY else ex[(ex.exact_status == 'optimal') & (ex.accepted == 0)]
            if not len(ex):
                os.remove(lock); continue
        for i, (k, q, rg) in enumerate(zip(ex.stage, ex['query'], ex.regime)):
            if (k, q, rg) in seen:
                continue
            if k not in partials:
                partials[k] = dom.stage(k, dte, f, dtr, P.cat(seed))[0]
            row = df.loc[q]; x0 = partials[k].loc[q].astype(float)
            spec = dom.spec(row, k, rg)[0]
            r = E.solve_exact(enc, x0, spec, pol, lam_spar=LAM_SPAR, time_limit=LIMIT.get(name, 120))
            ok, reasons, _ = C.gate(r.x, x0, spec, pol, predict)
            new.append(dict(stage=k, query=q, regime=rg, accepted=int(ok), reasons=';'.join(reasons) or 'OK',
                            effort=C.effort(r.x, x0, spec) if r.x is not None else np.nan,
                            sparsity=C.sparsity(r.x, x0, spec) if r.x is not None else np.nan,
                            cost=cost(r.x, x0, spec), seconds=r.seconds, exact_status=r.status,
                            n_binary=r.n_binary, objective=r.objective))
            pd.DataFrame(new).to_csv(part, index=False)
        N = pd.DataFrame(new).set_index(['stage', 'query', 'regime'])
        m = d.condition == 'exact'
        if FIX_ONLY:
            m = m & d.set_index(['stage', 'query', 'regime']).index.isin(N.index)
        key = list(zip(d.loc[m, 'stage'], d.loc[m, 'query'], d.loc[m, 'regime']))
        for col in ['accepted', 'reasons', 'effort', 'sparsity', 'cost', 'seconds', 'exact_status', 'n_binary', 'objective']:
            d.loc[m, col] = [N.loc[kk, col] for kk in key]
        d.to_csv(path, index=False)
        os.remove(part)
        if os.path.exists(lock):
            os.remove(lock)
        with open(DONE, 'a') as fh:
            fh.write(path + '\n')
        print(f'{path}: {m.sum()} exact rows recomputed in {time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
