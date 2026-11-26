"""v3 experiments: exact rule-verified recourse (MILP) against the v2 framework,
direct repair, DiCE baselines and OCEAN, for three model families.

Per seed: entity-grouped 80/20 split; models  lr (standardised logistic regression),
rf (random forest, 100 trees, depth 8) and cat (CatBoost, 500 iterations) trained on
the same training part.  Queries are held-out records that the model predicts
unfavourable (education: also flagged by the stage model), sampled up to --max_q per
stage.  All methods are judged by the same gate (recourse.core.gate).

Conditions
  dice_first, posthoc_full_gate, framework (= v2 rank_joint_fallback),
  repair (rule-only minimum-change repair), repair_esc (with escalation),
  exact (MILP, effort + 0.5 sparsity), ocean, ocean_joint (rf only; OCEAN CP-SAT with
  direction/fixed actionability, then v2 joint completion), plus
  rule_attainable: whether the rule-feasible set R(x0) is non-empty (LP, no model).

Usage: python experiment_v3.py HMDA --seeds 0,1,2,3,4 --models lr,rf,cat [--max_q 0] [--regimes aligned]
"""
import argparse, os, time, warnings
import numpy as np, pandas as pd
import dice_ml
from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
import prescriptive as P
from recourse import core as C, exact as E
from recourse.domains import DOMAINS
import recourse.configs  # noqa: F401

warnings.filterwarnings('ignore')
LAM_SPAR = 0.5


def make_model(name, seed):
    if name == 'cat':
        return P.cat(seed)
    if name == 'rf':
        return RandomForestClassifier(n_estimators=100, max_depth=8, random_state=seed, n_jobs=1)
    if name == 'lr':
        return make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    if name == 'mlp':     # ReLU network, two hidden layers of 20 units (MILP-encodable)
        return make_pipeline(StandardScaler(), MLPClassifier(hidden_layer_sizes=(20, 20), activation='relu',
                                                             max_iter=1000, early_stopping=True, random_state=seed))
    raise ValueError(name)


def cost(x, x0, spec):
    return C.effort(x, x0, spec) + LAM_SPAR * C.sparsity(x, x0, spec) if x is not None else np.nan


def ocean_setup(model, df, features):
    try:
        from ocean import ConstraintProgrammingExplainer
        from ocean.feature import parse_features
    except Exception:
        return None
    Xp, mapper = parse_features(df[features], scale=False)
    if list(Xp.columns) != list(features):
        print('OCEAN: processed columns differ from model features; skipped', flush=True)
        return None
    return ConstraintProgrammingExplainer(model, mapper=mapper)


def ocean_explain(expl, x0, spec, features, time_limit=60):
    act = {}
    for f in features:
        if f in spec.immutable:
            act[f] = 'fixed'
        else:
            lb, ub = spec.bounds[f]
            if np.isclose(lb, x0[f]):
                act[f] = 'increase'
            elif np.isclose(ub, x0[f]):
                act[f] = 'decrease'
    t0 = time.time()
    try:
        e = expl.explain(x0[features].values.astype(float), y=1, norm=1, max_time=time_limit, num_workers=1, actionability=act)
        status = expl.get_solving_status()
    except Exception as ex:          # noqa: BLE001
        e, status = None, f'error:{type(ex).__name__}'
    sec = time.time() - t0
    x = None if e is None else pd.Series(e.x, index=features).astype(float)
    return x, status, sec


def run(name, seed, models, regimes, max_q, out_dir, ocean=True, exact_limit=120):
    dom = DOMAINS[name]().load(); df = dom.df
    tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(df, df[dom.y], df[dom.group]))
    dtr, dte = df.iloc[tr], df.iloc[te]
    pol = dom.policy()
    for mname in models:
        path = f'{out_dir}/v3_{name}_{mname}_s{seed}.csv.gz'
        if os.path.exists(path):
            print('exists', path, flush=True); continue
        t_all = time.time()
        f = make_model(mname, seed).fit(dtr[dom.features], dtr[dom.y])
        enc = E.parse_model(f, dom.features)
        predict = lambda x, f=f: int(f.predict(pd.DataFrame([x[dom.features].astype(float)]))[0])
        dice_data = dice_ml.Data(dataframe=dtr[dom.features + [dom.y]].copy(), continuous_features=list(dom.features), outcome_name=dom.y)
        explainer = dice_ml.Dice(dice_data, dice_ml.Model(model=f, backend='sklearn'), method='random')
        oc = ocean_setup(f, df, dom.features) if (ocean and mname == 'rf') else None
        rng = np.random.RandomState(seed)
        part = path.replace('.csv.gz', '.part.csv')
        rows, done = [], set()
        if os.path.exists(part):            # resume after a restart: skip queries already evaluated
            prev = pd.read_csv(part); rows = prev.to_dict('records')
            done = set(zip(prev.stage, prev['query']))
        n_new = 0
        for k in dom.stages:
            partial, at_risk = dom.stage(k, dte, f, dtr, P.cat(seed))
            elig = np.where(at_risk & (f.predict(partial) == 0))[0]
            if max_q and len(elig) > max_q:
                elig = np.sort(rng.choice(elig, max_q, replace=False))
            for qi in elig:
                if (k, int(dte.index[qi])) in done:
                    continue
                row = dte.iloc[qi]; x0 = partial.iloc[qi].astype(float)
                pools = {}
                for regime in regimes:
                    s = dom.spec(row, k, regime)
                    if s is None:
                        continue
                    spec = s[0]
                    dreg = 'aligned' if regime == 'mismatch' else regime
                    base = dict(dataset=name, model=mname, seed=seed, stage=k, regime=regime, query=int(dte.index[qi]),
                                y_true=int(row[dom.y]))
                    res = {}

                    def rec(cond, x, sec, **extra):
                        ok, reasons, _ = C.gate(x, x0, spec, pol, predict)
                        rows.append(dict(base, condition=cond, accepted=int(ok), reasons=';'.join(reasons) or 'OK',
                                         effort=C.effort(x, x0, spec) if x is not None else np.nan,
                                         sparsity=C.sparsity(x, x0, spec) if x is not None else np.nan,
                                         cost=cost(x, x0, spec), seconds=sec, **extra))
                    # rule attainability (no model)
                    ra = C._lp_fill(x0.copy(), x0, spec, pol, list(spec.actionable)) is not None if pol.active else True
                    # DiCE pool
                    t0 = time.time()
                    if dreg not in pools:
                        _, rng_d, act_d = dom.spec(row, k, dreg)
                        try:
                            r = explainer.generate_counterfactuals(pd.DataFrame([x0[dom.features]]), total_CFs=10, desired_class=1,
                                                                   features_to_vary=act_d, permitted_range=rng_d,
                                                                   random_seed=seed * 100003 + int(qi))
                            pool = r.cf_examples_list[0].final_cfs_df
                            pool = None if pool is None or len(pool) == 0 else pool[dom.features].astype(float).reset_index(drop=True)
                        except Exception:
                            pool = None
                        pools[dreg] = (pool, time.time() - t0)
                    pool, t_dice = pools[dreg]
                    if pool is not None:
                        rec('dice_first', pool.iloc[0], t_dice, rule_attainable=int(ra))
                        t0 = time.time(); fo = None
                        for _, r_ in pool.iterrows():
                            if C.gate(r_, x0, spec, pol, predict)[0]:
                                fo = r_; break
                        rec('posthoc_full_gate', fo, t_dice + time.time() - t0)
                        t0 = time.time(); fb = None
                        bi, ranked = C.rank(pool, x0, spec, pol, P.LAMBDA)
                        for idx in ranked.sort_values('objective_score', kind='stable').index:
                            cand = C.complete_joint(pool.loc[idx], x0, spec, pol, predict)
                            if C.gate(cand, x0, spec, pol, predict)[0]:
                                fb = cand; break
                        rec('framework', fb, t_dice + time.time() - t0)
                    else:
                        for cnd in ['dice_first', 'posthoc_full_gate', 'framework']:
                            rec(cnd, None, t_dice, **({'rule_attainable': int(ra)} if cnd == 'dice_first' else {}))
                    if pol.active:
                        t0 = time.time(); rec('repair', C.repair(x0, spec, pol, None), time.time() - t0)
                        t0 = time.time(); rec('repair_esc', C.repair(x0, spec, pol, predict), time.time() - t0)
                    r_ex = E.solve_exact(enc, x0, spec, pol, lam_spar=LAM_SPAR, time_limit=exact_limit)
                    rec('exact', r_ex.x, r_ex.seconds, exact_status=r_ex.status, n_binary=r_ex.n_binary, objective=r_ex.objective)
                    if oc is not None:
                        xo, st, so = ocean_explain(oc, x0, spec, dom.features)
                        rec('ocean', xo, so, exact_status=st)
                        t0 = time.time()
                        xj = None if xo is None else C.complete_joint(xo, x0, spec, pol, predict)
                        rec('ocean_joint', xj, so + time.time() - t0)
                n_new += 1
                if n_new % 1 == 0:
                    pd.DataFrame(rows).to_csv(part, index=False)
            print(f'{name} {mname} seed={seed} stage={k} queries={len(elig)} elapsed={time.time()-t_all:.0f}s', flush=True)
        pd.DataFrame(rows).to_csv(path, index=False)
        if os.path.exists(part):
            os.remove(part)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('dataset'); ap.add_argument('--seeds', default='0')
    ap.add_argument('--models', default='lr,rf,cat'); ap.add_argument('--regimes', default='aligned')
    ap.add_argument('--max_q', type=int, default=0); ap.add_argument('--out', default='results_v3')
    ap.add_argument('--no_ocean', action='store_true'); ap.add_argument('--exact_limit', type=int, default=120)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for s in [int(x) for x in a.seeds.split(',')]:
        run(a.dataset, s, a.models.split(','), a.regimes.split(','), a.max_q, a.out, ocean=not a.no_ocean, exact_limit=a.exact_limit)
