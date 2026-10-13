"""Cross-domain tables for the v2 experiments (results_v2/ -> results_v2/tables/)."""
import glob, os
import numpy as np, pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests
from analyze import ms, cluster_boot_diff

RES, OUT = 'results_v2', 'results_v2/tables'
PRIMARY = {'OULAD': 40.0, 'AUC': 15.001, 'HMDA': 50.0, 'PIMA': 139.0}
ORDER = ['OULAD', 'AUC', 'HMDA', 'PIMA', 'HarvardX']
COND = ['dice_first', 'posthoc_policy_filter', 'posthoc_full_gate', 'rank_only', 'rank_edit', 'rank_edit_fallback',
        'rank_joint', 'rank_joint_fallback', 'policy_repair', 'policy_repair_escalate']
LABEL = {'dice_first': 'DiCE first candidate', 'posthoc_policy_filter': 'DiCE + policy filter',
         'posthoc_full_gate': 'DiCE + full-gate filter', 'rank_only': 'Ranking, no completion',
         'rank_edit': 'Framework v1 (grid completion)', 'rank_edit_fallback': 'Framework v1 + fallback',
         'rank_joint': 'Framework v2 (joint completion)', 'rank_joint_fallback': 'Framework v2 + fallback',
         'policy_repair': 'Direct repair', 'policy_repair_escalate': 'Direct repair + escalation'}


def load():
    fs = sorted(glob.glob(f'{RES}/presc_*_rows.csv.gz'))
    d = pd.concat([pd.read_csv(f, usecols=lambda c: c not in ('learner', 'module')) for f in fs], ignore_index=True)
    d['primary'] = d.apply(lambda r: pd.isna(r.tau) if r.dataset == 'HarvardX' else np.isclose(r.tau, PRIMARY[r.dataset]), axis=1)
    d['cluster'] = d.dataset + '_' + d['query'].astype(str)
    return d


def main():
    os.makedirs(OUT, exist_ok=True)
    d = load(); p = d[d.primary & d.condition.isin(COND)]
    md = []
    sy = p.groupby(['dataset', 'regime', 'condition', 'seed']).accepted.mean().reset_index()
    tab = sy.groupby(['dataset', 'regime', 'condition']).accepted.agg(ms).unstack('condition')
    tab = tab[[c for c in COND if c in tab.columns]].rename(columns=LABEL)
    tab = tab.reindex([i for ds in ORDER for i in tab.index if i[0] == ds])
    q = p[p.condition == 'dice_first'].groupby(['dataset', 'regime']).size().rename('queries')
    tab = tab.join(q)
    tab.to_csv(f'{OUT}/yield_v2.csv'); md += ['## Accepted yield (%) at the primary threshold', tab.to_markdown(), '']

    # paired tests: v2 framework vs gate filter, v1 framework, direct repair + escalation
    tests = []
    for (ds, rg), g in p.groupby(['dataset', 'regime']):
        w = g.pivot_table(index=['seed', 'stage', 'query', 'cluster'], columns='condition', values='accepted').reset_index()
        for a, b in [('rank_joint_fallback', 'posthoc_full_gate'), ('rank_joint_fallback', 'rank_edit_fallback'),
                     ('rank_joint_fallback', 'policy_repair_escalate'), ('rank_joint', 'rank_edit')]:
            if a not in w or b not in w:
                continue
            x, y = w[a].values, w[b].values
            n01, n10 = int(((x == 1) & (y == 0)).sum()), int(((x == 0) & (y == 1)).sum())
            pv = mcnemar([[0, n01], [n10, 0]], exact=(n01 + n10) < 25).pvalue if n01 + n10 else 1.0
            lo, hi = cluster_boot_diff(x, y, w.cluster.values)
            tests.append(dict(dataset=ds, regime=rg, method=LABEL[a], baseline=LABEL[b], n=len(w),
                              diff_pp=round(100 * (x.mean() - y.mean()), 2), ci_lo=round(lo, 2), ci_hi=round(hi, 2),
                              only_method=n01, only_baseline=n10, p=pv))
    T = pd.DataFrame(tests); T['p_holm'] = multipletests(T.p, method='holm')[1]
    T.round(4).to_csv(f'{OUT}/paired_v2.csv', index=False); md += ['## Paired comparisons (McNemar, cluster bootstrap, Holm)', T.round(4).to_markdown(index=False), '']

    # rule violations of raw DiCE candidates and failure modes
    pv = d[(d.condition == 'dice_first') & d.primary].drop_duplicates(['dataset', 'seed', 'regime', 'stage', 'query'])
    v = pv.groupby(['dataset', 'regime']).pool_policy_valid.mean().mul(100).round(1).rename('policy-valid DiCE candidates (%)')
    md += ['## Share of DiCE candidates satisfying the rule', v.to_frame().to_markdown(), '']

    # tau sweep
    sw = d[d.condition.isin(['dice_first', 'posthoc_full_gate', 'rank_joint_fallback', 'policy_repair_escalate']) & (d.regime == 'aligned')]
    sw = sw[sw.dataset != 'HarvardX']
    s2 = sw.groupby(['dataset', 'tau', 'condition', 'seed']).accepted.mean().groupby(['dataset', 'tau', 'condition']).agg(ms).unstack('condition').rename(columns=LABEL)
    s2.to_csv(f'{OUT}/tau_sweep_v2.csv'); md += ['## Threshold sweep (aligned)', s2.to_markdown(), '']

    # objective audit (grid completion, as in v1)
    au = d[d.condition.str.startswith('audit:') | (d.condition == 'rank_edit')]
    au = au[au.primary & (au.regime == 'aligned')]
    a2 = au.groupby(['dataset', 'condition', 'seed']).accepted.mean().groupby(['dataset', 'condition']).agg(ms).unstack('condition')
    a2.to_csv(f'{OUT}/objective_audit_v2.csv'); md += ['## Objective audit (grid completion)', a2.to_markdown(), '']

    # external methods
    ef = sorted(glob.glob(f'{RES}/ext_*.csv'))
    if ef:
        e = pd.concat([pd.read_csv(f) for f in ef], ignore_index=True)
        fw = p[p.condition.isin(['rank_joint_fallback', 'posthoc_full_gate', 'dice_first', 'policy_repair_escalate'])]
        outs = []
        for (ds, rg, meth), g in e.groupby(['dataset', 'regime', 'method']):
            keys = g[['seed', 'stage', 'query']].drop_duplicates()
            sub = fw[(fw.dataset == ds) & (fw.regime == rg)].merge(keys, on=['seed', 'stage', 'query'])
            both = pd.concat([g[['seed', 'condition', 'accepted']], sub[['seed', 'condition', 'accepted']]])
            r = both.groupby(['condition', 'seed']).accepted.mean().groupby('condition').agg(ms)
            r.index = [LABEL.get(i, i) for i in r.index]
            outs.append(r.rename(f'{ds} {rg} ({meth} queries, n={len(keys)})'))
        E = pd.concat(outs, axis=1)
        E.to_csv(f'{OUT}/external_v2.csv'); md += ['## External methods on matched queries', E.to_markdown(), '']
    open(f'{OUT}/summary_v2.md', 'w').write('\n'.join(md)); print('\n'.join(md))


if __name__ == '__main__':
    main()
