"""Prescriptive experiments (matched ablation, audits, baselines).

Design (per dataset, per seed):
  1. Learner-grouped 80/20 split.  f = CatBoost outcome model on complete
     records (non-submission encoded as 0).  g_k = CatBoost early-warning model
     that only sees assessments released by stage k.
  2. Query cohort at stage k = held-out learners flagged at risk by g_k whose
     partial record (pending assessments = 0) is also predicted to fail by f.
  3. One DiCE pool (<=10 candidates, method='random') per query and bound
     regime; every condition re-uses the same pool.
  4. Every returned vector goes through PresAnEx.counterfactual_gate.apply_hard_gate
     (unmodified) with a fresh prediction from f.

Bound regimes (pending assessments):
  aligned  : DiCE range = gate bounds = [0, weight]
  floor    : DiCE range = gate bounds = [0.4*weight, weight]
  mismatch : DiCE range = [0, weight], gate/editing bounds = [0.4*weight, weight]
             (DiCE searches a wider range than the gate enforces)
"""
import sys, json, time, warnings, hashlib, argparse
import numpy as np, pandas as pd
import dice_ml
from catboost import CatBoostClassifier
from sklearn.model_selection import GroupShuffleSplit
from datasets import LOADERS
from PresAnEx import fairness_aware_cf as fcf
from PresAnEx.counterfactual_gate import apply_hard_gate

warnings.filterwarnings('ignore')
import logging; logging.disable(logging.WARNING)
import tqdm, functools  # silence dice progress bars
tqdm.tqdm.__init__ = functools.partialmethod(tqdm.tqdm.__init__, disable=True)

LAMBDA = dict(lambda_policy=1000.0, lambda_feas=1000.0, lambda_prox=1.0, lambda_spar=0.5)
FLOOR = 0.4


def cat(seed):
    return CatBoostClassifier(random_seed=seed, verbose=0, iterations=500, thread_count=2)


# ------------------------------------------------------------------ query set-up
def query_spec(cfg, row, k, regime):
    """Actionable features, immutable features, DiCE ranges and gate bounds for one query."""
    ub = cfg.test_ub(row)
    pending = [t for t in cfg.tests[k:] if ub.get(t, 0) > 0] if cfg.tests else []
    act, dice_rng, gate_b = [], {}, {}
    for t in pending:
        lo_dice = FLOOR * ub[t] if regime == 'floor' else 0.0
        lo_gate = FLOOR * ub[t] if regime in ('floor', 'mismatch') else 0.0
        act.append(t); dice_rng[t] = [lo_dice, ub[t]]; gate_b[t] = (lo_gate, ub[t])
    for e in cfg.engagement:
        cur = float(row[e])
        hi = cfg.hx_hi[e] if cfg.name == 'HarvardX' else cfg.click_hi(row)
        if hi > cur + 1e-9:           # increase-only engagement
            act.append(e); dice_rng[e] = [cur, hi]; gate_b[e] = (cur, hi)
    imm = [c for c in cfg.features if c not in act]
    return act, imm, dice_rng, gate_b


def policy(cfg):
    if cfg.policy_weights is None:        # HarvardX: policy criterion vacuous
        return {cfg.features[0]: 0.0}, -1.0
    return cfg.policy_weights, cfg.tau


def score(x, w):
    return float(sum(float(x[f]) * v for f, v in w.items()))


def effort(x, orig, act, bounds):
    return float(sum(abs(float(x[f]) - float(orig[f])) / max(bounds[f][1] - bounds[f][0], 1e-9) for f in act))


def sparsity(x, orig, act):
    return int(sum(not np.isclose(float(x[f]), float(orig[f])) for f in act))


# ------------------------------------------------------------------ conditions
def gate(cfg, f_model, cand, orig, act, gate_b, w, tau):
    pred = lambda D: f_model.predict(D[cfg.features])
    acc, audit = apply_hard_gate(cand, orig, feature_columns=cfg.features, actionable_features=act,
                                 feature_bounds=gate_b, assessment_weights=w,
                                 institutional_threshold=tau, predict=pred)
    return acc is not None, audit


def select(orig, pool, act, imm, w, tau, bounds, edit, lam):
    ranges = {f: max(bounds[f][1] - bounds[f][0], 1e-9) for f in act}
    best, ranked, _ = fcf.select_best_counterfactual(
        original_instance=orig, cf_examples=pool.reset_index(drop=True), institutional_threshold=tau,
        actionable_features=act, immutable_features=imm, assessment_weights=w,
        feature_bounds=bounds, effort_weights={f: 1.0 for f in act}, feature_ranges=ranges,
        plot_scores=False, edit_zero_features=edit, **lam)
    return best, ranked


def policy_repair(cfg, f_model, orig, act, gate_b, w, tau, escalate):
    """Direct linear-policy recourse without DiCE: raise pending assessments at the
    lowest effort per score point until S(x) >= target; escalate target if f disagrees."""
    tests = [a for a in act if a in w and w[a] > 0]
    if not tests:
        return None
    base = orig.copy()
    for a in act:
        base[a] = min(max(float(base[a]), gate_b[a][0]), gate_b[a][1])
    # cost per score point: 1/(w * range) -> fill largest-range assessments first
    order = sorted(tests, key=lambda a: 1.0 / (w[a] * max(gate_b[a][1] - gate_b[a][0], 1e-9)))
    targets = [tau] + ([tau + s for s in np.arange(2.5, 60.1, 2.5) * (tau / 40.0)] if escalate else [])
    for tgt in targets:
        x = base.copy(); deficit = (tgt + 1e-6) - score(x, w)  # epsilon guards float round-off at the gate
        for a in order:
            if deficit <= 1e-9:
                break
            room = (gate_b[a][1] - float(x[a])) * w[a]
            add = min(room, deficit)
            x[a] = float(x[a]) + add / w[a]; deficit -= add
        if deficit > 1e-9:
            return x  # infeasible target; gate will reject
        if not escalate or int(f_model.predict(pd.DataFrame([x[cfg.features]]))[0]) == 1:
            return x
    return x


def vec_hash(x, act):
    if x is None:
        return 'none'
    return hashlib.md5(json.dumps([round(float(x[a]), 4) for a in act]).encode()).hexdigest()[:10]


def evaluate_query(cfg, f_model, orig, pool, act, imm, gate_b, taus, lam_variants, regime):
    """Return list of result rows for all conditions on one query."""
    w, tau0 = policy(cfg)
    out = []

    def rec(cond, cand, tau, **extra):
        if cand is None:
            ok, reasons, s = False, 'no_candidate', np.nan
        else:
            ok, audit = gate(cfg, f_model, cand, orig, act, gate_b, w, tau)
            reasons, s = ';'.join(audit['reasons']) or 'OK', audit['policy_score']
        out.append(dict(condition=cond, tau=tau, accepted=int(ok), reasons=reasons, policy_score=s,
                        effort=effort(cand, orig, act, gate_b) if cand is not None else np.nan,
                        sparsity=sparsity(cand, orig, act) if cand is not None else np.nan,
                        sel=vec_hash(cand, act), **extra))

    has_pool = pool is not None and len(pool) > 0
    for tau in taus:
        if has_pool:
            rec('dice_first', pool.iloc[0], tau)
            pol = [r for _, r in pool.iterrows() if score(r, w) >= tau]
            rec('posthoc_policy_filter', pol[0] if pol else None, tau)
            first_ok = None
            for _, r in pool.iterrows():
                if gate(cfg, f_model, r, orig, act, gate_b, w, tau)[0]:
                    first_ok = r; break
            rec('posthoc_full_gate', first_ok, tau)
            b0, _ = select(orig, pool, act, imm, w, tau, gate_b, False, LAMBDA)
            rec('rank_only', b0, tau)
            b1, ranked = select(orig, pool, act, imm, w, tau, gate_b, True, LAMBDA)
            rec('rank_edit', b1, tau)
            # ranked selection with fallback: try candidates in objective order
            fb = None
            for idx in ranked.sort_values('objective_score', kind='stable').index:
                one, _ = select(orig, pool.loc[[idx]], act, imm, w, tau, gate_b, True, LAMBDA)
                if gate(cfg, f_model, one, orig, act, gate_b, w, tau)[0]:
                    fb = one; break
            rec('rank_edit_fallback', fb, tau)
        else:
            for c in ['dice_first', 'posthoc_policy_filter', 'posthoc_full_gate', 'rank_only',
                      'rank_edit', 'rank_edit_fallback']:
                rec(c, None, tau)
        if cfg.policy_weights is not None:
            rec('policy_repair', policy_repair(cfg, f_model, orig, act, gate_b, w, tau, False), tau)
            rec('policy_repair_escalate', policy_repair(cfg, f_model, orig, act, gate_b, w, tau, True), tau)
    # objective audits at the primary threshold
    if has_pool:
        for name, lam in lam_variants.items():
            b, _ = select(orig, pool, act, imm, w, tau0, gate_b, True, lam)
            rec('audit:' + name, b, tau0)
    return out


def lam_variants():
    v = {}
    for t in ['policy', 'feas', 'prox', 'spar']:
        l = dict(LAMBDA); l['lambda_' + t] = 0.0; v['drop_' + t] = l
    for lp in [1.0, 10.0, 100.0]:
        l = dict(LAMBDA); l['lambda_policy'] = lp; v[f'lp_{lp:g}'] = l
    for lx in [0.1, 10.0]:
        l = dict(LAMBDA); l['lambda_prox'] = lx; v[f'lx_{lx:g}'] = l
    return v


# ------------------------------------------------------------------ driver
def run(name, seed, regimes, max_q, out_prefix):
    cfg = LOADERS[name]()
    df = cfg.df
    gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed)
    tr, te = next(gss.split(df, df[cfg.y], df[cfg.group]))
    dtr, dte = df.iloc[tr], df.iloc[te]
    f_model = cat(seed).fit(dtr[cfg.features], dtr[cfg.y])
    ddf = dtr[cfg.features + [cfg.y]].copy()
    dice_data = dice_ml.Data(dataframe=ddf, continuous_features=list(cfg.features), outcome_name=cfg.y)
    explainer = dice_ml.Dice(dice_data, dice_ml.Model(model=f_model, backend='sklearn'), method='random')
    w, tau0 = policy(cfg)
    taus = sorted(set(cfg.tau_sweep + [tau0])) if cfg.tau_sweep else [tau0]
    lv = lam_variants()
    rows, cohort = [], []
    rng = np.random.RandomState(seed)
    for k in cfg.stages:
        if k:
            sf = cfg.tests[:k] + list(cfg.immutable_extra)
            g_k = cat(seed).fit(dtr[sf], dtr[cfg.y])
            partial = dte[cfg.features].copy()
            partial[cfg.tests[k:]] = 0.0
            at_risk = g_k.predict_proba(dte[sf])[:, 1] < 0.5
        else:
            partial = dte[cfg.features].copy()
            at_risk = np.ones(len(dte), bool)
        f_fail = f_model.predict(partial) == 0
        elig = np.where(at_risk & f_fail)[0]
        n_elig = len(elig)
        if max_q and len(elig) > max_q:
            elig = np.sort(rng.choice(elig, max_q, replace=False))
        cohort.append(dict(dataset=name, seed=seed, stage=k, n_test=len(dte), n_at_risk=int(at_risk.sum()),
                           n_eligible=n_elig, n_evaluated=len(elig),
                           true_fail_rate_eligible=float(1 - dte[cfg.y].values[np.where(at_risk & f_fail)[0]].mean()) if n_elig else np.nan))
        t0 = time.time()
        for qi in elig:
            row = dte.iloc[qi]
            orig = partial.iloc[qi].astype(float)
            pools = {}
            for regime in regimes:
                act, imm, dice_rng, gate_b = query_spec(cfg, row, k, regime)
                if not act:
                    continue
                dice_regime = 'aligned' if regime == 'mismatch' else regime
                if dice_regime not in pools:
                    act_d, _, rng_d, _ = query_spec(cfg, row, k, dice_regime)
                    try:
                        r = explainer.generate_counterfactuals(
                            pd.DataFrame([orig[cfg.features]]), total_CFs=10, desired_class=1,
                            features_to_vary=act_d, permitted_range=rng_d, random_seed=seed * 100003 + int(qi))
                        pool = r.cf_examples_list[0].final_cfs_df
                        pool = None if pool is None else pool[cfg.features].astype(float).reset_index(drop=True)
                    except Exception:
                        pool = None
                    pools[dice_regime] = pool
                pool = pools[dice_regime]
                res = evaluate_query(cfg, f_model, orig, pool, act, imm, gate_b, taus, lv, regime)
                for r_ in res:
                    r_.update(dataset=name, seed=seed, stage=k, regime=regime, query=int(dte.index[qi]),
                              learner=row[cfg.group], y_true=int(row[cfg.y]),
                              pool_size=0 if pool is None else len(pool),
                              pool_policy_valid=np.nan if pool is None or cfg.policy_weights is None else
                              float(np.mean([score(p, w) >= tau0 for _, p in pool.iterrows()])),
                              module=row.get('code_module', ''))
                rows.extend(res)
        print(f'{name} seed={seed} stage={k} eligible={n_elig} evaluated={len(elig)} {time.time()-t0:.0f}s', flush=True)
    pd.DataFrame(rows).to_csv(f'{out_prefix}_rows.csv.gz', index=False)
    pd.DataFrame(cohort).to_csv(f'{out_prefix}_cohort.csv', index=False)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('dataset'); ap.add_argument('--seeds', default='0')
    ap.add_argument('--regimes', default='aligned,floor,mismatch')
    ap.add_argument('--max_q', type=int, default=0)
    a = ap.parse_args()
    for s in [int(x) for x in a.seeds.split(',')]:
        run(a.dataset, s, a.regimes.split(','), a.max_q, f'results/presc_{a.dataset}_s{s}')
