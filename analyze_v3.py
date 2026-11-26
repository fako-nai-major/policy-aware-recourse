"""Tables for the v3 experiments (results_v3/ -> results_v3/tables/)."""
import glob, os, sys
import numpy as np, pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests

RES = sys.argv[1] if len(sys.argv) > 1 else 'results_v3'
OUT = f'{RES}/tables'
COND = ['dice_first', 'posthoc_full_gate', 'ocean', 'ocean_joint', 'ocean_joint_free', 'dace', 'dace_rule', 'mace', 'mace_rule', 'framework', 'repair', 'repair_esc', 'repair_sparse0', 'repair_sparse', 'exact']
ms = lambda s: f'{100 * s.mean():.1f} ± {100 * s.std(ddof=1):.1f}' if len(s) > 1 else f'{100 * s.mean():.1f}'


def load():
    d = pd.concat([pd.read_csv(f) for f in sorted(glob.glob(f'{RES}/v3_*.csv.gz') + glob.glob(f'{RES}/v3x_*.csv.gz')) if os.path.getsize(f) > 100], ignore_index=True)
    d['key'] = d.dataset + '|' + d.model + '|' + d.regime
    return d


def main():
    os.makedirs(OUT, exist_ok=True)
    d = load(); md = []
    # yield
    y = d.groupby(['dataset', 'regime', 'model', 'condition', 'seed']).accepted.mean().groupby(['dataset', 'regime', 'model', 'condition']).agg(ms).unstack('condition')
    y = y[[c for c in COND if c in y.columns]]
    q = d[d.condition == 'exact'].groupby(['dataset', 'regime', 'model']).size().rename('queries')
    ra = d[d.condition == 'dice_first'].groupby(['dataset', 'regime', 'model']).rule_attainable.mean().mul(100).round(1).rename('rule attainable %')
    y = y.join(q).join(ra); y.to_csv(f'{OUT}/yield_v3.csv'); md += ['## Accepted yield (%)', y.to_markdown(), '']
    # exact solver statistics
    ex = d[d.condition == 'exact']
    st = ex.groupby(['dataset', 'regime', 'model']).agg(
        optimal=('exact_status', lambda s: round(100 * (s == 'optimal').mean(), 1)),
        infeasible=('exact_status', lambda s: round(100 * (s == 'infeasible').mean(), 1)),
        time_limit=('exact_status', lambda s: round(100 * (s == 'time_limit').mean(), 1)),
        sec_median=('seconds', lambda s: round(s.median(), 2)), sec_p95=('seconds', lambda s: round(s.quantile(.95), 1)),
        sec_max=('seconds', lambda s: round(s.max(), 1)), binaries=('n_binary', 'median'))
    st.to_csv(f'{OUT}/exact_stats_v3.csv'); md += ['## Exact solver: status (%) and time (s)', st.to_markdown(), '']
    # cost relative to exact on queries both accept
    rows = []
    w = d.pivot_table(index=['dataset', 'regime', 'model', 'seed', 'stage', 'query'], columns='condition', values=['accepted', 'cost', 'effort'])
    for (ds, rg, m), g in w.groupby(level=[0, 1, 2]):
        for c in COND:
            if c == 'exact' or ('accepted', c) not in g:
                continue
            both = g[(g[('accepted', c)] == 1) & (g[('accepted', 'exact')] == 1)]
            if not len(both):
                continue
            cx, cc = both[('cost', 'exact')], both[('cost', c)]
            rows.append(dict(dataset=ds, regime=rg, model=m, method=c, n=len(both),
                             cost_method=round(cc.mean(), 3), cost_exact=round(cx.mean(), 3),
                             excess_pct=round(100 * (cc.mean() / cx.mean() - 1), 1),
                             optimal_pct=round(100 * (cc <= cx + 1e-3).mean(), 1),
                             effort_method=round(both[('effort', c)].mean(), 3), effort_exact=round(both[('effort', 'exact')].mean(), 3)))
    G = pd.DataFrame(rows); G.to_csv(f'{OUT}/cost_gap_v3.csv', index=False); md += ['## Cost relative to the exact optimum (queries accepted by both)', G.to_markdown(index=False), '']
    # paired yield: exact vs others
    tests = []
    for (ds, rg, m), g in w.groupby(level=[0, 1, 2]):
        for c in ['framework', 'repair_esc', 'repair_sparse', 'posthoc_full_gate', 'ocean_joint', 'ocean_joint_free', 'dace_rule', 'mace_rule']:
            if ('accepted', c) not in g or g[('accepted', c)].notna().sum() == 0:
                continue
            x, z = g[('accepted', 'exact')].values, g[('accepted', c)].values
            ok = ~(np.isnan(x) | np.isnan(z)); x, z = x[ok], z[ok]
            n01, n10 = int(((x == 1) & (z == 0)).sum()), int(((x == 0) & (z == 1)).sum())
            p = mcnemar([[0, n01], [n10, 0]], exact=(n01 + n10) < 25).pvalue if n01 + n10 else 1.0
            tests.append(dict(dataset=ds, regime=rg, model=m, baseline=c, n=len(x), diff_pp=round(100 * (x.mean() - z.mean()), 2),
                              only_exact=n01, only_baseline=n10, p=p))
    T = pd.DataFrame(tests)
    if len(T):
        T['p_holm'] = multipletests(T.p, method='holm')[1]
    T.round(4).to_csv(f'{OUT}/paired_v3.csv', index=False); md += ['## Paired yield: exact vs baselines (McNemar, Holm)', T.round(4).to_markdown(index=False), '']
    # failure reasons of baselines
    fr = d[(d.accepted == 0)].assign(reason=lambda t: t.reasons.str.split(';').str[0].str.split(':').str[0])
    fr = fr.groupby(['dataset', 'condition']).reason.agg(lambda s: '; '.join(f'{k} {v:.0%}' for k, v in s.value_counts(normalize=True).head(3).items()))
    md += ['## Main rejection reasons', fr.to_frame().to_markdown(), '']
    open(f'{OUT}/summary_v3.md', 'w').write('\n'.join(md)); print('\n'.join(md))


if __name__ == '__main__':
    main()
