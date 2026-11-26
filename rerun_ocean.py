"""Re-run OCEAN on the random-forest files of experiment_v3 and add the fairer variant.

Conditions written (replacing earlier OCEAN rows):
  ocean             OCEAN CP-SAT with fixed / increase / decrease actionability (unchanged method)
  ocean_joint       + v2 joint completion (only untouched or out-of-bounds features move)
  ocean_joint_free  + joint completion that may also move the actionable features of violated
                    rule constraints, within their bounds (core.complete_joint(free_violated=True))
OCEAN vectors are stored (column `vector`, JSON) so later variants need no re-run.
Resumable; finished files are listed in logs/ocean_rerun_done.txt.

Usage: python rerun_ocean.py [results_v3] [filter-substring]
"""
import glob, json, os, sys, time, warnings
import numpy as np, pandas as pd
from sklearn.model_selection import GroupShuffleSplit
import prescriptive as P
from recourse import core as C
from recourse.domains import DOMAINS
import recourse.configs  # noqa: F401
from experiment_v3 import make_model, cost, ocean_setup, ocean_explain

warnings.filterwarnings('ignore')
RES = sys.argv[1] if len(sys.argv) > 1 else 'results_v3'
FILT = sys.argv[2] if len(sys.argv) > 2 else ''
DONE = os.environ.get('OCEAN_DONE', 'logs/ocean_rerun_done.txt')


def main():
    done = set(open(DONE).read().split()) if os.path.exists(DONE) else set()
    for path in sorted(glob.glob(f'{RES}/v3_*_rf_s*.csv.gz')):
        if path in done or FILT not in path:
            continue
        d = pd.read_csv(path)
        name, seed = d.dataset.iloc[0], int(d.seed.iloc[0])
        dom = DOMAINS[name]().load(); df = dom.df
        tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(df, df[dom.y], df[dom.group]))
        dtr, dte = df.iloc[tr], df.iloc[te]
        f = make_model('rf', seed).fit(dtr[dom.features], dtr[dom.y])
        predict = lambda x, f=f: int(f.predict(pd.DataFrame([x[dom.features].astype(float)]))[0])
        oc = ocean_setup(f, df, dom.features)
        pol = dom.policy()
        REV = os.environ.get('OCEAN_REV') == '1'
        part = path.replace('.csv.gz', '.ocean.part2.csv' if REV else '.ocean.part.csv')
        other = path.replace('.csv.gz', '.ocean.part.csv' if REV else '.ocean.part2.csv')
        new = pd.read_csv(part).to_dict('records') if os.path.exists(part) else []
        seen = {(r['stage'], r['query'], r['regime']) for r in new}
        keys = d[d.condition == 'exact'][['stage', 'query', 'regime', 'y_true']].drop_duplicates(['stage', 'query', 'regime'])
        partials, t0 = {}, time.time()
        rows = list(keys.itertuples(index=False))
        for k, q, rg, yt in (rows[::-1] if REV else rows):
            if os.path.exists(other):
                try:
                    seen |= set(zip(*[pd.read_csv(other)[c] for c in ['stage', 'query', 'regime']]))
                except Exception:
                    pass
            if (k, q, rg) in seen:
                continue
            if k not in partials:
                partials[k] = dom.stage(k, dte, f, dtr, P.cat(seed))[0]
            row = df.loc[q]; x0 = partials[k].loc[q].astype(float)
            spec = dom.spec(row, k, rg)[0]
            xo, st, so = ocean_explain(oc, x0, spec, dom.features)
            base = dict(dataset=name, model='rf', seed=seed, stage=k, regime=rg, query=q, y_true=yt)
            for cond, x, sec in [('ocean', xo, so)] + [
                    (c, None if xo is None else C.complete_joint(xo, x0, spec, pol, predict, free_violated=fv), None)
                    for c, fv in [('ocean_joint', False), ('ocean_joint_free', True)]]:
                t1 = time.time()
                ok, reasons, _ = C.gate(x, x0, spec, pol, predict)
                new.append(dict(base, condition=cond, accepted=int(ok), reasons=';'.join(reasons) or 'OK',
                                effort=C.effort(x, x0, spec) if x is not None else np.nan,
                                sparsity=C.sparsity(x, x0, spec) if x is not None else np.nan,
                                cost=cost(x, x0, spec), seconds=so if sec is not None else so + (time.time() - t1),
                                exact_status=st,
                                vector=json.dumps({c: float(x[c]) for c in dom.features}) if x is not None else ''))
            pd.DataFrame(new).to_csv(part, index=False)
        if os.path.exists(other):
            new = new + pd.read_csv(other).to_dict('records')
        N = pd.DataFrame(new).drop_duplicates(['stage', 'query', 'regime', 'condition'])
        if len(N) != 3 * len(keys):
            print(f'{path}: waiting for the other worker ({len(N)}/{3*len(keys)})', flush=True)
            continue
        out = pd.concat([d[~d.condition.isin(['ocean', 'ocean_joint', 'ocean_joint_free'])], N], ignore_index=True)
        out.to_csv(path, index=False)
        for pth in (part, other):
            if os.path.exists(pth):
                os.remove(pth)
        with open(DONE, 'a') as fh:
            fh.write(path + '\n')
        print(f'{path}: OCEAN re-run on {len(keys)} queries in {time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    main()
