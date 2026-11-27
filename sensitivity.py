"""Sensitivity of the comparison to the rule threshold tau and the sparsity weight lambda.

Seed 0, logistic regression and random forest, the queries of experiment_v3 (at most 100; GMSC rf 8: about 15 min per query).
  tau sweep (primary rule constraint): HMDA DTI {43,45,50}; PIMA glucose {125,139,155};
           GMSC DTI {0.36,0.43,0.50}; ADULT hours {40,48,60}
           conditions: posthoc_full_gate, framework, repair_esc, exact (same DiCE pool for every tau)
  lambda sweep (default tau): exact with lambda in {0, 0.25, 1, 2}; heuristic costs are re-scored
           from their stored effort and sparsity (cost = effort + lambda * sparsity).
Writes results_sens/sens_<domain>_<model>.csv (resumable).
"""
import os, sys, time, warnings
import numpy as np, pandas as pd
import dice_ml
from sklearn.model_selection import GroupShuffleSplit
from recourse import core as C, exact as E
from recourse.domains import DOMAINS
import recourse.configs  # noqa: F401
import prescriptive as P
from experiment_v3 import make_model

warnings.filterwarnings('ignore')
TAUS = {'HMDA': [43.0, 45.0, 50.0], 'PIMA': [125.0, 139.0, 155.0], 'GMSC': [0.36, 0.43, 0.50], 'ADULT': [40.0, 48.0, 60.0]}
LAMS = [0.0, 0.25, 1.0, 2.0]
SEED = 0


def main(name, mname):
    out = f'results_sens/sens_{name}_{mname}.csv'
    rows = pd.read_csv(out).to_dict('records') if os.path.exists(out) else []
    seen = {r['query'] for r in rows}
    dom = DOMAINS[name]().load(); df = dom.df
    tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED).split(df, df[dom.y], df[dom.group]))
    dtr, dte = df.iloc[tr], df.iloc[te]
    f = make_model(mname, SEED).fit(dtr[dom.features], dtr[dom.y]); enc = E.parse_model(f, dom.features)
    predict = lambda x: int(f.predict(pd.DataFrame([x[dom.features].astype(float)]))[0])
    d = pd.read_csv(f'results_v3/v3_{name}_{mname}_s{SEED}.csv.gz')
    qs = sorted(d[d.condition == 'exact']['query'].unique())[: (8 if (name == 'GMSC' and mname == 'rf') else 100)]
    dd = dice_ml.Data(dataframe=dtr[dom.features + [dom.y]].copy(), continuous_features=list(dom.features), outcome_name=dom.y)
    expl = dice_ml.Dice(dd, dice_ml.Model(model=f, backend='sklearn'), method='random')
    limit = 120 if mname == 'rf' else 60
    for q in qs:
        if q in seen:
            continue
        row = df.loc[q]; x0 = row[dom.features].astype(float)
        spec, rng_d, act_d = dom.spec(row, 0, 'aligned')
        qi = list(dte.index).index(q)
        try:
            r = expl.generate_counterfactuals(pd.DataFrame([x0[dom.features]]), total_CFs=10, desired_class=1, features_to_vary=act_d,
                                              permitted_range=rng_d, random_seed=SEED * 100003 + int(qi))
            pool = r.cf_examples_list[0].final_cfs_df
            pool = None if pool is None or len(pool) == 0 else pool[dom.features].astype(float).reset_index(drop=True)
        except Exception:
            pool = None
        base = dict(domain=name, model=mname, query=q)

        def rec(sweep, val, cond, x, lam=0.5, pol=None, **extra):
            ok = C.gate(x, x0, spec, pol, predict)[0]
            e = C.effort(x, x0, spec) if x is not None else np.nan; s = C.sparsity(x, x0, spec) if x is not None else np.nan
            rows.append(dict(base, sweep=sweep, value=val, condition=cond, accepted=int(ok), effort=e, sparsity=s,
                             cost=e + lam * s if x is not None else np.nan, **extra))
        for tau in TAUS[name]:
            pol = dom.policy(tau=tau)
            fo = fb = None
            if pool is not None:
                for _, c in pool.iterrows():
                    if C.gate(c, x0, spec, pol, predict)[0]:
                        fo = c; break
                bi, ranked = C.rank(pool, x0, spec, pol, P.LAMBDA)
                for idx in ranked.sort_values('objective_score', kind='stable').index:
                    cand = C.complete_joint(pool.loc[idx], x0, spec, pol, predict)
                    if C.gate(cand, x0, spec, pol, predict)[0]:
                        fb = cand; break
            rec('tau', tau, 'posthoc_full_gate', fo, pol=pol)
            rec('tau', tau, 'framework', fb, pol=pol)
            rec('tau', tau, 'repair_esc', C.repair(x0, spec, pol, predict), pol=pol)
            rx = E.solve_exact(enc, x0, spec, pol, lam_spar=0.5, time_limit=limit)
            rec('tau', tau, 'exact', rx.x, pol=pol, status=rx.status, seconds=rx.seconds)
        pol = dom.policy()
        for lam in LAMS:
            rx = E.solve_exact(enc, x0, spec, pol, lam_spar=lam, time_limit=limit)
            rec('lambda', lam, 'exact', rx.x, lam=lam, pol=pol, status=rx.status, seconds=rx.seconds)
        pd.DataFrame(rows).to_csv(out, index=False)
    print(name, mname, 'done', flush=True)


if __name__ == '__main__':
    for job in sys.argv[1].split(','):
        main(*job.split(':'))
