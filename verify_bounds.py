"""Per-query bounds for the theory section (docs/THEORY_v3.md).

For every query of a finished experiment_v3 file this computes
  lb_rule    min cost over the rule-feasible set R(x0)  (model ignored)      -> lower bound on OPT (Prop. 4)
  opt_model  min cost over {f(x)=1} without the rule  (unconstrained recourse) -> price of compliance
             (with its MILP dual bound when the time limit is hit)
  esc_end    for single-constraint / separable rules: is the end point of the escalation path
             accepted by the gate?  (Prop. 5 predicts repair_esc success from it when the model is
             linear and sign-aligned with the rule)
and stores them in results_v3/bounds/<file>.csv.  Resumable, per-file locks (two workers).

Usage: python verify_bounds.py [filter] [reverse]
"""
import glob, os, sys, time, warnings
import numpy as np, pandas as pd
from sklearn.model_selection import GroupShuffleSplit
import prescriptive as P
from recourse import core as C, exact as E
from recourse.domains import DOMAINS
import recourse.configs  # noqa: F401
from experiment_v3 import make_model, LAM_SPAR

warnings.filterwarnings('ignore')
OUT = 'results_v3/bounds'
LIMIT = {'OULAD': 20}      # model-only MILPs on OULAD trees are weakly bounded; dual bound recorded
FILT = sys.argv[1] if len(sys.argv) > 1 else ''
REV = len(sys.argv) > 2 and sys.argv[2] == 'reverse'
ALWAYS = E.Linear(np.zeros(1), 1.0)          # placeholder; replaced per domain (always favourable)


def main():
    os.makedirs(OUT, exist_ok=True)
    files = sorted(glob.glob('results_v3/v3_*.csv.gz'), key=lambda p: ('OULAD' in p, 'rf' in p, p))
    files = [p for p in files if FILT in p]
    for path in (files[::-1] if REV else files):
        out = f"{OUT}/{os.path.basename(path).replace('.csv.gz', '.csv')}"
        if os.path.exists(out):
            continue
        part, lock = out + '.part', out + '.lock'
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
        f = make_model(mname, seed).fit(dtr[dom.features], dtr[dom.y]); enc = E.parse_model(f, dom.features)
        always = E.Linear(np.zeros(len(dom.features)), 1.0)
        predict = lambda x, f=f: int(f.predict(pd.DataFrame([x[dom.features].astype(float)]))[0])
        never = lambda x: 0
        pol = dom.policy(); nopol = C.Policy([])
        new = pd.read_csv(part).to_dict('records') if os.path.exists(part) else []
        seen = {(r['stage'], r['query'], r['regime']) for r in new}
        partials = {}
        ex = d[d.condition == 'exact']
        for k, q, rg in zip(ex.stage, ex['query'], ex.regime):
            if (k, q, rg) in seen:
                continue
            if k not in partials:
                partials[k] = dom.stage(k, dte, f, dtr, P.cat(seed))[0]
            row = df.loc[q]; x0 = partials[k].loc[q].astype(float)
            spec = dom.spec(row, k, rg)[0]
            rr = E.solve_exact(always, x0, spec, pol, lam_spar=LAM_SPAR, time_limit=60)
            if ((name == 'OULAD' and mname != 'lr') or (name == 'GMSC' and mname == 'rf')) and seed != 0:     # run time: OULAD tree models, seed 0 only
                rm = E.ExactResult(None, 'skipped')
            else:
                rm = E.solve_exact(enc, x0, spec, nopol, lam_spar=LAM_SPAR, time_limit=LIMIT.get(name, 120))
            xe = C.repair(x0, spec, pol, never)          # end of the escalation path (all steps)
            ok_e = C.gate(xe, x0, spec, pol, predict)[0] if xe is not None else False
            x1 = C.repair(x0, spec, pol, None)           # margin 0
            new.append(dict(stage=k, query=q, regime=rg,
                            lb_rule=rr.objective if rr.status == 'optimal' else np.nan, rule_status=rr.status,
                            opt_model=rm.objective if rm.x is not None else np.nan, model_bound=rm.bound,
                            model_status=rm.status, model_seconds=rm.seconds,
                            esc_end_ok=int(ok_e),
                            repair0_cost=(C.effort(x1, x0, spec) + LAM_SPAR * C.sparsity(x1, x0, spec)) if x1 is not None else np.nan,
                            repair0_model=predict(x1) if x1 is not None else np.nan))
            pd.DataFrame(new).to_csv(part, index=False)
        N = pd.DataFrame(new)
        N.insert(0, 'model', mname); N.insert(0, 'seed', seed); N.insert(0, 'dataset', name)
        N.to_csv(out, index=False)
        for p in (part, lock):
            if os.path.exists(p):
                os.remove(p)
        print(f'{path}: {len(N)} queries', flush=True)


if __name__ == '__main__':
    main()
