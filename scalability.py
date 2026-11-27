"""Scalability of the exact solver: run time and size of the MILP as the model grows.

Domains PIMA (coarse clinical units) and GMSC (fine-grained ratios); seed 0; 20 held-out queries
that each model predicts unfavourable; time limit 60 s.  Configurations:
  rf   trees T in {25,50,100,200,400} at depth 8, and depth D in {4,6,10,12} at T = 100
  cat  iterations in {100,250,1000} at depth 6, depth in {4,8} at 500 iterations (+ default 500/6)
  mlp  two hidden layers of width {10,20,50,100}; depth {1,3} at width 20
Writes results_scale/scale_<domain>.csv (resumable).
"""
import os, sys, time, warnings
import numpy as np, pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from catboost import CatBoostClassifier
from recourse import core as C, exact as E
from recourse.domains import DOMAINS
import recourse.configs  # noqa: F401
from experiment_v3 import cost, LAM_SPAR

warnings.filterwarnings('ignore')
Q, LIMIT = 20, 60
SEED = int(os.environ.get('SEED', '0'))
CONFIGS = ([('rf', dict(T=t, D=8)) for t in [25, 50, 100, 200, 400]] + [('rf', dict(T=100, D=d)) for d in [4, 6, 10, 12]] +
           [('cat', dict(I=i, D=6)) for i in [100, 250, 500, 1000]] + [('cat', dict(I=500, D=d)) for d in [4, 8]] +
           [('mlp', dict(H=(w, w))) for w in [10, 20, 50, 100]] + [('mlp', dict(H=h)) for h in [(20,), (20, 20, 20)]])


def build(kind, p):
    if kind == 'rf':
        return RandomForestClassifier(n_estimators=p['T'], max_depth=p['D'], random_state=SEED, n_jobs=1)
    if kind == 'cat':
        return CatBoostClassifier(iterations=p['I'], depth=p['D'], verbose=0, random_seed=SEED, thread_count=1)
    return make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=p['H'], max_iter=1000, early_stopping=True, random_state=SEED))


WS = os.environ.get('WS') == '1'      # warm start: cheapest gate-accepted of repair+esc, sparse repair, framework (DiCE)


def main(name):
    out = f'results_scale/scale_{name}{"_ws" if WS else ""}{os.environ.get("OUT_SUFFIX", "")}{f"_s{SEED}" if SEED else ""}.csv'
    rows = pd.read_csv(out).to_dict('records') if os.path.exists(out) else []
    seen = {(r['model'], r['config'], r['query']) for r in rows}
    dom = DOMAINS[name]().load(); df = dom.df; pol = dom.policy()
    tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED).split(df, df[dom.y], df[dom.group]))
    dtr, dte = df.iloc[tr], df.iloc[te]
    for kind, p in CONFIGS:
        if WS and os.environ.get('WS_KIND') and kind != os.environ['WS_KIND']:
            continue
        cfg = ','.join(f'{k}={v}' for k, v in p.items())
        only, excl = os.environ.get('CFG_ONLY'), os.environ.get('CFG_EXCLUDE')
        if (only and cfg not in only.split(';')) or (excl and cfg in excl.split(';')):
            continue
        f = build(kind, p).fit(dtr[dom.features], dtr[dom.y]); enc = E.parse_model(f, dom.features)
        predict = lambda x, f=f: int(f.predict(pd.DataFrame([x[dom.features].astype(float)]))[0])
        acc = float((f.predict(dte[dom.features]) == dte[dom.y]).mean())
        if WS:
            import dice_ml, prescriptive as P
            dd = dice_ml.Data(dataframe=dtr[dom.features + [dom.y]].copy(), continuous_features=list(dom.features), outcome_name=dom.y)
            expl = dice_ml.Dice(dd, dice_ml.Model(model=f, backend='sklearn'), method='random')
        neg = np.where(f.predict(dte[dom.features]) == 0)[0]
        qs = np.sort(np.random.RandomState(SEED).choice(neg, min(Q, len(neg)), replace=False))
        for qi in qs:
            q = int(dte.index[qi])
            if (kind, cfg, q) in seen:
                continue
            row = dte.iloc[qi]; x0 = row[dom.features].astype(float)
            s = dom.spec(row, 0, 'aligned')
            if s is None:
                continue
            spec = s[0]
            xs, ok_s = None, False
            if WS:
                cands = [C.repair(x0, spec, pol, predict), E.repair_sparse(x0, spec, pol, predict, lam_spar=LAM_SPAR)]
                try:
                    _, rng_d, act_d = s
                    rr = expl.generate_counterfactuals(pd.DataFrame([x0[dom.features]]), total_CFs=10, desired_class=1,
                                                       features_to_vary=act_d, permitted_range=rng_d, random_seed=SEED * 100003 + int(qi))
                    pool = rr.cf_examples_list[0].final_cfs_df
                    if pool is not None and len(pool):
                        pool = pool[dom.features].astype(float).reset_index(drop=True)
                        _, ranked = C.rank(pool, x0, spec, pol, P.LAMBDA)
                        for idx in ranked.sort_values('objective_score', kind='stable').index:
                            cand = C.complete_joint(pool.loc[idx], x0, spec, pol, predict)
                            if C.gate(cand, x0, spec, pol, predict)[0]:
                                cands.append(cand); break
                except Exception:
                    pass
                cands = [c for c in cands if c is not None and C.gate(c, x0, spec, pol, predict)[0]]
                ok_s = bool(cands)
                xs = min(cands, key=lambda c: cost(c, x0, spec)) if cands else None
            r = E.solve_exact(enc, x0, spec, pol, lam_spar=LAM_SPAR, time_limit=LIMIT, start=xs if ok_s else None)
            ok = C.gate(r.x, x0, spec, pol, predict)[0]
            rows.append(dict(domain=name, model=kind, config=cfg, seed=SEED, query=q, accuracy=acc, status=r.status, accepted=int(ok),
                             seconds=r.seconds, n_binary=r.n_binary, n_vars=r.n_vars, n_rows=r.n_rows,
                             n_actionable=len(spec.actionable), cost=cost(r.x, x0, spec), gap=r.gap, bound=r.bound,
                             start_cost=cost(xs, x0, spec) if ok_s else np.nan))
            pd.DataFrame(rows).to_csv(out, index=False)
        print(name, kind, cfg, 'done', flush=True)


if __name__ == '__main__':
    for n in sys.argv[1].split(','):
        main(n)
