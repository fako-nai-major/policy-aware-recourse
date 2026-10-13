"""v2 prescriptive experiments for any domain in recourse/domains.py.

Same protocol as prescriptive.py (v1): learner/entity-grouped 80/20 split per
seed, CatBoost outcome model f, optional staged early-warning cohorts, one DiCE
pool per query and bound regime shared by all conditions, and the acceptance
gate on every returned vector.  Conditions:

  v1 (reproduced exactly):  dice_first, posthoc_policy_filter, posthoc_full_gate,
      rank_only, rank_edit (grid completion), rank_edit_fallback, policy_repair,
      policy_repair_escalate, audit:<objective variant>
  v2:  rank_joint            ranking + joint completion verified against f
       rank_joint_fallback   the same over the ranked pool until the gate passes
"""
import argparse, hashlib, json, time, warnings
import numpy as np, pandas as pd
import dice_ml
from sklearn.model_selection import GroupShuffleSplit
import prescriptive as P                      # cat(), LAMBDA, lam_variants(), silenced DiCE
from recourse import core as C
from recourse.domains import DOMAINS
import recourse.configs  # noqa: F401  registers non-education domains

warnings.filterwarnings('ignore')


def vec_hash(x, act):
    if x is None:
        return 'none'
    return hashlib.md5(json.dumps([round(float(x[a]), 4) for a in act]).encode()).hexdigest()[:10]


def evaluate_query(dom, predict, x0, pool, spec, taus, lam_variants, tau0):
    out = []
    pol0 = dom.policy()

    def rec(cond, cand, tau):
        pol = dom.policy(tau) if tau is not None and pol0.active else pol0
        ok, reasons, s = C.gate(cand, x0, spec, pol, predict)
        out.append(dict(condition=cond, tau=tau, accepted=int(ok), reasons=';'.join(reasons) or 'OK', policy_score=s,
                        effort=C.effort(cand, x0, spec) if cand is not None else np.nan,
                        sparsity=C.sparsity(cand, x0, spec) if cand is not None else np.nan,
                        sel=vec_hash(cand, spec.actionable)))

    has_pool = pool is not None and len(pool) > 0
    for tau in taus:
        pol = dom.policy(tau) if pol0.active else pol0
        if has_pool:
            rec('dice_first', pool.iloc[0], tau)
            pf = [r for _, r in pool.iterrows() if (pol.ok(r) if pol.active else True)]
            rec('posthoc_policy_filter', pf[0] if pf else None, tau)
            first_ok = None
            for _, r in pool.iterrows():
                if C.gate(r, x0, spec, pol, predict)[0]:
                    first_ok = r; break
            rec('posthoc_full_gate', first_ok, tau)
            bi, ranked = C.rank(pool, x0, spec, pol, P.LAMBDA)
            rec('rank_only', pool.iloc[bi], tau)
            rec('rank_edit', C.complete_grid(pool.iloc[bi], x0, spec, pol, P.LAMBDA), tau)
            fb = None
            for idx in ranked.sort_values('objective_score', kind='stable').index:
                cand = C.complete_grid(pool.loc[idx], x0, spec, pol, P.LAMBDA)
                if C.gate(cand, x0, spec, pol, predict)[0]:
                    fb = cand; break
            rec('rank_edit_fallback', fb, tau)
            rec('rank_joint', C.complete_joint(pool.iloc[bi], x0, spec, pol, predict), tau)
            fbj = None
            for idx in ranked.sort_values('objective_score', kind='stable').index:
                cand = C.complete_joint(pool.loc[idx], x0, spec, pol, predict)
                if C.gate(cand, x0, spec, pol, predict)[0]:
                    fbj = cand; break
            rec('rank_joint_fallback', fbj, tau)
        else:
            for c in ['dice_first', 'posthoc_policy_filter', 'posthoc_full_gate', 'rank_only', 'rank_edit',
                      'rank_edit_fallback', 'rank_joint', 'rank_joint_fallback']:
                rec(c, None, tau)
        if pol0.active:
            rec('policy_repair', C.repair(x0, spec, pol, None), tau)
            rec('policy_repair_escalate', C.repair(x0, spec, pol, predict), tau)
    if has_pool:
        pol = dom.policy(tau0) if pol0.active else pol0
        for name, lam in lam_variants.items():
            bi, _ = C.rank(pool, x0, spec, pol, lam)
            rec('audit:' + name, C.complete_grid(pool.iloc[bi], x0, spec, pol, lam), tau0)
    return out


def run(name, seed, regimes, max_q, out_prefix, audits=True):
    dom = DOMAINS[name]().load()
    df = dom.df
    tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(df, df[dom.y], df[dom.group]))
    dtr, dte = df.iloc[tr], df.iloc[te]
    f_model = P.cat(seed).fit(dtr[dom.features], dtr[dom.y])
    predict = lambda x: f_model.predict(pd.DataFrame([x[dom.features].astype(float)]))[0]
    dice_data = dice_ml.Data(dataframe=dtr[dom.features + [dom.y]].copy(), continuous_features=list(dom.features), outcome_name=dom.y)
    explainer = dice_ml.Dice(dice_data, dice_ml.Model(model=f_model, backend='sklearn'), method='random')
    pol0 = dom.policy()
    tau0 = pol0.constraints[0].tau if pol0.active else None
    taus = sorted(set(dom.tau_sweep + [tau0])) if (dom.tau_sweep and pol0.active) else [tau0]
    lv = P.lam_variants() if audits else {}
    rows, cohort = [], []
    rng = np.random.RandomState(seed)
    for k in dom.stages:
        partial, at_risk = dom.stage(k, dte, f_model, dtr, P.cat(seed))
        f_fail = f_model.predict(partial) == 0
        elig = np.where(at_risk & f_fail)[0]
        n_elig = len(elig)
        if max_q and len(elig) > max_q:
            elig = np.sort(rng.choice(elig, max_q, replace=False))
        cohort.append(dict(dataset=name, seed=seed, stage=k, n_test=len(dte), n_at_risk=int(at_risk.sum()),
                           n_eligible=n_elig, n_evaluated=len(elig),
                           true_fail_rate_eligible=float(1 - dte[dom.y].values[np.where(at_risk & f_fail)[0]].mean()) if n_elig else np.nan))
        t0 = time.time()
        for qi in elig:
            row = dte.iloc[qi]
            x0 = partial.iloc[qi].astype(float)
            pools = {}
            for regime in regimes:
                s = dom.spec(row, k, regime)
                if s is None:
                    continue
                spec, _, _ = s
                dice_regime = 'aligned' if regime == 'mismatch' else regime
                if dice_regime not in pools:
                    _, rng_d, act_d = dom.spec(row, k, dice_regime)
                    try:
                        r = explainer.generate_counterfactuals(
                            pd.DataFrame([x0[dom.features]]), total_CFs=10, desired_class=1,
                            features_to_vary=act_d, permitted_range=rng_d, random_seed=seed * 100003 + int(qi))
                        pool = r.cf_examples_list[0].final_cfs_df
                        pool = None if pool is None else pool[dom.features].astype(float).reset_index(drop=True)
                    except Exception:
                        pool = None
                    pools[dice_regime] = pool
                pool = pools[dice_regime]
                res = evaluate_query(dom, predict, x0, pool, spec, taus, lv, tau0)
                pv = np.nan
                if pool is not None and pol0.active:
                    pv = float(np.mean([pol0.ok(p) for _, p in pool.iterrows()]))
                for r_ in res:
                    r_.update(dataset=name, seed=seed, stage=k, regime=regime, query=int(dte.index[qi]),
                              y_true=int(row[dom.y]), pool_size=0 if pool is None else len(pool),
                              pool_policy_valid=pv, **dom.extra(row))
                rows.extend(res)
        print(f'{name} seed={seed} stage={k} eligible={n_elig} evaluated={len(elig)} {time.time()-t0:.0f}s', flush=True)
    pd.DataFrame(rows).to_csv(f'{out_prefix}_rows.csv.gz', index=False)
    pd.DataFrame(cohort).to_csv(f'{out_prefix}_cohort.csv', index=False)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('dataset'); ap.add_argument('--seeds', default='0')
    ap.add_argument('--regimes', default='aligned,floor,mismatch')
    ap.add_argument('--max_q', type=int, default=0)
    ap.add_argument('--no_audits', action='store_true')
    ap.add_argument('--out', default='results_v2')
    a = ap.parse_args()
    import os; os.makedirs(a.out, exist_ok=True)
    for s in [int(x) for x in a.seeds.split(',')]:
        run(a.dataset, s, a.regimes.split(','), a.max_q, f'{a.out}/presc_{a.dataset}_s{s}', audits=not a.no_audits)
