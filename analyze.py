"""Aggregate per-query results into the tables reported in the paper (CSV + Markdown)."""
import glob, numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests

OUT = 'results/tables'
PRIMARY = {'OULAD': 40.0, 'AUC': 15.001, 'HarvardX': -1.0}
MAIN = ['dice_first', 'posthoc_policy_filter', 'posthoc_full_gate', 'rank_only', 'rank_edit',
        'rank_edit_fallback', 'policy_repair', 'policy_repair_escalate']
LABEL = {'dice_first': 'DiCE first candidate', 'posthoc_policy_filter': 'Post-hoc policy filter',
         'posthoc_full_gate': 'Post-hoc full-gate filter', 'rank_only': 'Policy-aware ranking (no edit)',
         'rank_edit': 'Policy-aware ranking + edit (framework)',
         'rank_edit_fallback': 'Framework + fallback over ranked pool',
         'policy_repair': 'Direct policy repair (no DiCE)',
         'policy_repair_escalate': 'Direct policy repair + classifier escalation'}


def ms(x):
    x = np.asarray(x, float)
    return f'{100*np.mean(x):.1f} ± {100*np.std(x, ddof=1):.1f}' if len(x) > 1 else f'{100*np.mean(x):.1f}'


def load_rows():
    fs = sorted(glob.glob('results/presc_*_rows.csv.gz'))
    d = pd.concat([pd.read_csv(f) for f in fs], ignore_index=True)
    d['primary'] = d.apply(lambda r: np.isclose(r.tau, PRIMARY[r.dataset]), axis=1)
    return d


def cluster_boot_diff(a, b, clusters, reps=2000, seed=0):
    rng = np.random.RandomState(seed)
    df = pd.DataFrame(dict(a=a, b=b, c=clusters)).groupby('c')[['a', 'b']].agg(['sum', 'count'])
    sa, sb, n = df[('a', 'sum')].values, df[('b', 'sum')].values, df[('a', 'count')].values
    idx = rng.randint(0, len(n), size=(reps, len(n)))
    diffs = (sa[idx].sum(1) - sb[idx].sum(1)) / n[idx].sum(1)
    return np.percentile(diffs, [2.5, 97.5]) * 100


def main():
    import os; os.makedirs(OUT, exist_ok=True)
    md = []
    # ---------------- cohort
    coh = pd.concat([pd.read_csv(f) for f in glob.glob('results/presc_*_cohort.csv')])
    c = coh.groupby(['dataset', 'stage']).agg(n_test=('n_test', 'mean'), at_risk=('n_at_risk', 'mean'),
                                             eligible=('n_eligible', 'mean'), evaluated=('n_evaluated', 'mean'),
                                             true_fail=('true_fail_rate_eligible', 'mean'), seeds=('seed', 'nunique')).round(2)
    c.to_csv(f'{OUT}/cohort.csv'); md += ['## Query cohorts (mean per seed)', c.to_markdown(), '']

    d = load_rows()
    p = d[d.primary]
    # per-query yield pooled over stages; per-seed yield then mean ± sd over seeds
    main = p[p.condition.isin(MAIN)]
    seed_y = main.groupby(['dataset', 'regime', 'condition', 'seed']).accepted.mean().reset_index()
    tab = seed_y.groupby(['dataset', 'regime', 'condition']).accepted.agg(ms).unstack('condition')
    tab = tab[[c for c in MAIN if c in tab.columns]].rename(columns=LABEL)
    # share of queries for which the policy is reachable at all within bounds
    pr_ = main[main.condition == 'policy_repair'].copy()
    if len(pr_):
        pr_['reach'] = (~pr_.reasons.str.contains('below_policy_threshold')).astype(int)
        reach = pr_.groupby(['dataset', 'regime', 'seed']).reach.mean().groupby(['dataset', 'regime']).agg(ms)
        tab['Policy reachable within bounds (upper bound)'] = reach
    tab.to_csv(f'{OUT}/ablation_yield.csv')
    md += ['## Final accepted yield (%) at the primary threshold, mean ± SD over seeds', tab.T.to_markdown(), '']

    acc = main[main.accepted == 1].groupby(['dataset', 'regime', 'condition']).agg(
        effort=('effort', 'mean'), sparsity=('sparsity', 'mean'), score=('policy_score', 'mean')).round(3)
    acc.to_csv(f'{OUT}/accepted_characteristics.csv')
    md += ['## Characteristics of accepted recommendations (normalised effort, #changed, policy score)',
           acc.unstack('regime').to_markdown(), '']

    # by stage
    st = main[main.regime == 'aligned'].groupby(['dataset', 'stage', 'condition']).accepted.mean().mul(100).round(1).unstack('condition')
    st = st[[c for c in MAIN if c in st.columns]].rename(columns=LABEL)
    st.to_csv(f'{OUT}/yield_by_stage.csv'); md += ['## Yield by stage (aligned bounds, %)', st.T.to_markdown(), '']

    # rejection reasons for the framework
    rr = main[(main.condition == 'rank_edit') & (main.accepted == 0)].copy()
    rr['reason'] = rr.reasons.str.split(';').str[0].str.replace(r':.*', '', regex=True)
    rt = (rr.groupby(['dataset', 'regime']).reason.value_counts(normalize=True) * 100).round(1).unstack('reason').fillna(0)
    rt.to_csv(f'{OUT}/framework_rejections.csv'); md += ['## Framework rejection reasons (% of rejected)', rt.to_markdown(), '']

    # paired tests: framework vs baselines
    tests = []
    for (ds, rg), g in main.groupby(['dataset', 'regime']):
        piv = g.pivot_table(index=['seed', 'stage', 'query'], columns='condition', values='accepted', aggfunc='first')
        clusters = [f'{s}-{q}' for s, _, q in piv.index]
        for base in ['dice_first', 'posthoc_full_gate', 'rank_only', 'policy_repair_escalate', 'rank_edit_fallback']:
            for fw in ['rank_edit', 'rank_edit_fallback']:
                if base == fw or base not in piv or fw not in piv:
                    continue
                a, b = piv[fw].values, piv[base].values
                tbl = [[np.sum((a == 1) & (b == 1)), np.sum((a == 1) & (b == 0))],
                       [np.sum((a == 0) & (b == 1)), np.sum((a == 0) & (b == 0))]]
                pv = mcnemar(tbl, exact=min(tbl[0][1], tbl[1][0]) < 25).pvalue
                lo, hi = cluster_boot_diff(a, b, clusters)
                tests.append(dict(dataset=ds, regime=rg, method=LABEL[fw], baseline=LABEL[base], n=len(a),
                                  diff_pp=100 * (a.mean() - b.mean()), ci_lo=lo, ci_hi=hi,
                                  only_method=tbl[0][1], only_baseline=tbl[1][0], p=pv))
    tt = pd.DataFrame(tests)
    if len(tt):
        tt['p_holm'] = multipletests(tt.p, method='holm')[1]
        tt = tt.round(3); tt.to_csv(f'{OUT}/paired_tests.csv', index=False)
        md += ['## Paired comparisons (McNemar, learner-cluster bootstrap 95% CI, Holm-adjusted)', tt.to_markdown(index=False), '']

    # objective audit (aligned regime)
    au = p[(p.condition.str.startswith('audit:')) | (p.condition == 'rank_edit')]
    rows = []
    for (ds, rg), g in au.groupby(['dataset', 'regime']):
        base = g[g.condition == 'rank_edit'].set_index(['seed', 'stage', 'query'])
        for cond, h in g.groupby('condition'):
            h = h.set_index(['seed', 'stage', 'query'])
            j = h.join(base[['sel', 'accepted']], rsuffix='_full', how='inner')
            # audits exist only for queries with a DiCE pool; queries without a pool count as rejected
            full_acc = h.accepted.reindex(base.index).fillna(0)
            sy = full_acc.groupby(level='seed').mean()
            rows.append(dict(dataset=ds, regime=rg, variant=cond.replace('audit:', ''), yield_=ms(sy),
                             changed_selection_pct=round(100 * (j.sel != j.sel_full).mean(), 1),
                             mean_effort_accepted=round(h[h.accepted == 1].effort.mean(), 3)))
    at = pd.DataFrame(rows); at.to_csv(f'{OUT}/objective_audit.csv', index=False)
    md += ['## Objective audit (leave-one-term-out and lambda sweep)', at.to_markdown(index=False), '']

    # tau sweep
    ts = d[d.condition.isin(['dice_first', 'posthoc_full_gate', 'rank_only', 'rank_edit', 'rank_edit_fallback',
                             'policy_repair_escalate']) & (d.regime == 'aligned') & (d.dataset != 'HarvardX')]
    tsy = ts.groupby(['dataset', 'tau', 'condition', 'seed']).accepted.mean().reset_index()
    tst = tsy.groupby(['dataset', 'tau', 'condition']).accepted.agg(ms).unstack('condition').rename(columns=LABEL)
    tst.to_csv(f'{OUT}/tau_sweep.csv'); md += ['## Threshold sensitivity (aligned bounds)', tst.to_markdown(), '']

    # candidate pools
    pool = p[p.condition == 'dice_first'].groupby(['dataset', 'regime']).agg(
        queries=('query', 'size'), with_pool=('pool_size', lambda x: (x > 0).mean() * 100),
        mean_pool=('pool_size', 'mean'), pool_policy_valid=('pool_policy_valid', 'mean')).round(3)
    pool.to_csv(f'{OUT}/pools.csv'); md += ['## DiCE pools', pool.to_markdown(), '']

    # predictive
    pr = [pd.read_csv(f) for f in glob.glob('results/predictive_*.csv')]
    if pr:
        pr = pd.concat(pr)
        agg = pr.groupby(['dataset', 'stage', 'sampler', 'model'])[['roc_auc', 'bal_acc', 'f1_macro', 'recall_fail']].agg(['mean', 'std'])
        agg.to_csv(f'{OUT}/predictive_all.csv')
        best = pr.groupby(['dataset', 'stage', 'sampler', 'model']).roc_auc.mean().reset_index()
        best = best.loc[best.groupby(['dataset', 'stage']).roc_auc.idxmax()]
        cb = pr[pr.model == 'CB'].groupby(['dataset', 'stage', 'sampler'])[['roc_auc', 'bal_acc', 'f1_macro', 'recall_fail']].agg(lambda x: f'{x.mean():.3f} ± {x.std():.3f}')
        cb.to_csv(f'{OUT}/predictive_catboost.csv')
        md += ['## Best model per stage (mean ROC-AUC over grouped folds)', best.round(3).to_markdown(index=False), '',
               '## CatBoost (grouped 5-fold, mean ± SD)', cb.to_markdown(), '']
        # Friedman over models per dataset-stage (sampler=none)
        fr = []
        for (ds, s), g in pr[pr.sampler == 'none'].groupby(['dataset', 'stage']):
            m = g.pivot_table(index='fold', columns='model', values='roc_auc')
            if m.shape[1] > 2:
                fr.append(dict(dataset=ds, stage=s, friedman_p=stats.friedmanchisquare(*[m[c] for c in m]).pvalue,
                               cb_rank=m.rank(axis=1, ascending=False)['CB'].mean() if 'CB' in m else np.nan,
                               top=m.mean().idxmax(), top_auc=m.mean().max(), cb_auc=m.mean().get('CB', np.nan)))
        fr = pd.DataFrame(fr).round(4); fr.to_csv(f'{OUT}/predictive_friedman.csv', index=False)
        md += ['## Friedman test across models (no resampling)', fr.to_markdown(index=False), '']
    open(f'{OUT}/summary.md', 'w').write('\n'.join(md))
    print('\n'.join(md))


if __name__ == '__main__':
    main()
