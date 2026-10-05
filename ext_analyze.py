"""Tables for the external baselines (NICE, MCCE, CARE) matched to the framework."""
import glob, numpy as np, pandas as pd
from statsmodels.stats.contingency_tables import mcnemar
from statsmodels.stats.multitest import multipletests
from analyze import cluster_boot_diff, ms, PRIMARY

OUT = 'results/tables'
FW = {'rank_edit': 'Framework (ranking + edit + gate)', 'rank_edit_fallback': 'Framework + fallback',
      'posthoc_full_gate': 'DiCE + post-hoc full gate', 'dice_first': 'DiCE first candidate',
      'policy_repair_escalate': 'Direct policy repair + escalation'}


def main():
    ext = pd.concat([pd.read_csv(f) for f in glob.glob('results/ext_*.csv')], ignore_index=True)
    fw = pd.concat([pd.read_csv(f, usecols=['dataset', 'seed', 'regime', 'stage', 'query', 'condition', 'tau',
                                            'accepted', 'effort'])
                    for f in glob.glob('results/presc_*_rows.csv.gz')], ignore_index=True)
    fw = fw[fw.condition.isin(FW) & fw.apply(lambda r: np.isclose(r.tau, PRIMARY[r.dataset]), axis=1)]
    key = ['dataset', 'seed', 'regime', 'stage', 'query']
    md, yrows, tests = [], [], []
    for (ds, rg, meth), e in ext.groupby(['dataset', 'regime', 'method']):
        qs = e[key].drop_duplicates()
        f = fw.merge(qs, on=key)
        both = pd.concat([e[key + ['condition', 'accepted', 'effort']], f[key + ['condition', 'accepted', 'effort']]])
        seeds = sorted(qs.seed.unique())
        for cond, g in both.groupby('condition'):
            sy = g.groupby('seed').accepted.mean()
            acc = g[g.accepted == 1]
            yrows.append(dict(dataset=ds, regime=rg, subset=f'{meth} queries (n={len(qs)}, seeds={len(seeds)})',
                              condition=FW.get(cond, cond), yield_pct=ms(sy), effort_accepted=round(acc.effort.mean(), 3)))
        piv = both.pivot_table(index=key, columns='condition', values='accepted', aggfunc='first')
        clusters = [f'{i[1]}-{i[4]}' for i in piv.index]
        for c in [c for c in piv.columns if c.startswith(meth)]:
            for base in ['rank_edit', 'rank_edit_fallback']:
                a, b = piv[base].values, piv[c].values
                t = [[np.sum((a == 1) & (b == 1)), np.sum((a == 1) & (b == 0))],
                     [np.sum((a == 0) & (b == 1)), np.sum((a == 0) & (b == 0))]]
                lo, hi = cluster_boot_diff(a, b, clusters)
                tests.append(dict(dataset=ds, regime=rg, framework=FW[base], baseline=c, n=len(a),
                                  diff_pp=100 * (a.mean() - b.mean()), ci_lo=lo, ci_hi=hi,
                                  only_framework=t[0][1], only_baseline=t[1][0],
                                  p=mcnemar(t, exact=min(t[0][1], t[1][0]) < 25).pvalue))
    Y = pd.DataFrame(yrows)
    Y.to_csv(f'{OUT}/external_yield.csv', index=False)
    T = pd.DataFrame(tests); T['p_holm'] = multipletests(T.p, method='holm')[1]
    T = T.round(3); T.to_csv(f'{OUT}/external_paired_tests.csv', index=False)
    rr = ext[ext.accepted == 0].copy()
    rr['reason'] = rr.reasons.str.split(';').str[0].str.replace(r':.*', '', regex=True)
    R = (rr.groupby(['dataset', 'regime', 'condition']).reason.value_counts(normalize=True) * 100).round(1).unstack('reason').fillna(0)
    R.to_csv(f'{OUT}/external_rejections.csv')
    tm = ext.drop_duplicates(key + ['method']).groupby(['dataset', 'method']).seconds.mean().round(3)
    tm.to_csv(f'{OUT}/external_runtime.csv')
    md += ['## External baselines on matched queries (yield %, mean ± SD over seeds)', Y.to_markdown(index=False), '',
           '## Paired tests vs framework (McNemar, learner-cluster bootstrap, Holm)', T.to_markdown(index=False), '',
           '## Rejection reasons (% of rejected)', R.to_markdown(), '', '## Mean seconds per query', tm.to_markdown()]
    open(f'{OUT}/external_summary.md', 'w').write('\n'.join(md))
    print('\n'.join(md))


if __name__ == '__main__':
    main()
