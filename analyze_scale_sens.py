"""Tables for the scalability (results_scale/) and sensitivity (results_sens/) runs -> results_v3/tables/."""
import glob, os
import numpy as np, pandas as pd

OUT = 'results_v3/tables'
LAM_DEFAULT = 0.5


def scale():
    d = pd.concat([pd.read_csv(f) for f in sorted(glob.glob('results_scale/scale_*.csv')) if '_ws' not in f], ignore_index=True)
    d['seed'] = d['seed'].fillna(0).astype(int) if 'seed' in d else 0
    g = d.groupby(['domain', 'model', 'config'], sort=False).agg(
        accuracy=('accuracy', 'mean'), seeds=('seed', 'nunique'), n=('query', 'size'),
        optimal_pct=('status', lambda s: round(100 * (s == 'optimal').mean(), 1)),
        infeasible_pct=('status', lambda s: round(100 * (s == 'infeasible').mean(), 1)),
        time_limit_pct=('status', lambda s: round(100 * (s == 'time_limit').mean(), 1)),
        sec_median=('seconds', lambda s: round(s.median(), 2)), sec_p90=('seconds', lambda s: round(s.quantile(.9), 1)),
        binaries=('n_binary', 'median'), rows=('n_rows', 'median')).reset_index()
    g['accuracy'] = g.accuracy.round(3)
    if 'acc' in g: g = g.drop(columns='acc')
    g.to_csv(f'{OUT}/scalability_v3.csv', index=False)
    md = ['## Scalability of the exact solver (seeds 0-2, 20 queries per seed, 60 s limit)', g.to_markdown(index=False), '']
    ws = sorted(glob.glob('results_scale/scale_*_ws*.csv'))
    if ws:
        w = pd.concat([pd.read_csv(f) for f in ws], ignore_index=True)
        w['seed'] = w['seed'].fillna(0).astype(int) if 'seed' in w else 0
        k = ['domain', 'model', 'config', 'seed', 'query']
        j = w.merge(d[k + ['status', 'accepted', 'cost', 'seconds']], on=k, suffixes=('_ws', '_cold'))
        t = j.groupby(['domain', 'model', 'config'], sort=False).agg(
            n=('query', 'size'), start_found=('start_cost', lambda s: round(100 * s.notna().mean(), 1)),
            accepted_cold=('accepted_cold', lambda s: round(100 * s.mean(), 1)), accepted_ws=('accepted_ws', lambda s: round(100 * s.mean(), 1)),
            proven_cold=('status_cold', lambda s: round(100 * s.isin(['optimal', 'infeasible']).mean(), 1)),
            proven_ws=('status_ws', lambda s: round(100 * s.isin(['optimal', 'infeasible']).mean(), 1)),
            sec_cold=('seconds_cold', lambda s: round(s.median(), 1)), sec_ws=('seconds_ws', lambda s: round(s.median(), 1)),
            ws_below_start_pct=('cost_ws', lambda s: np.nan)).reset_index()
        jj = j[j.start_cost.notna() & j.cost_ws.notna()]
        imp = jj.groupby(['domain', 'model', 'config'], sort=False).apply(lambda g: round(100 * (g.cost_ws < g.start_cost - 1e-3).mean(), 1))
        t['ws_improves_start_pct'] = t.set_index(['domain', 'model', 'config']).index.map(lambda i: imp.get(i, np.nan))
        t = t.drop(columns='ws_below_start_pct')
        t.to_csv(f'{OUT}/warmstart_v3.csv', index=False)
        md += ['## Warm start (MIP start from the cheapest accepted heuristic)', t.to_markdown(index=False), '']
    return md


def sens():
    d = pd.concat([pd.read_csv(f) for f in sorted(glob.glob('results_sens/sens_*.csv'))], ignore_index=True)
    md = []
    t = d[d.sweep == 'tau']
    y = t.groupby(['domain', 'model', 'value', 'condition']).accepted.mean().mul(100).round(1).unstack('condition')
    rows = []
    for (dm, m, v), g in t.groupby(['domain', 'model', 'value']):
        w = g.pivot_table(index='query', columns='condition', values=['accepted', 'cost'])
        for c in ['posthoc_full_gate', 'framework', 'repair_esc']:
            both = w[(w[('accepted', c)] == 1) & (w[('accepted', 'exact')] == 1)]
            if len(both):
                rows.append(dict(domain=dm, model=m, value=v, method=c + '_excess%', n=len(both),
                                 excess_pct=round(100 * (both[('cost', c)].mean() / both[('cost', 'exact')].mean() - 1), 1)))
    ex = pd.DataFrame(rows).pivot_table(index=['domain', 'model', 'value'], columns='method', values='excess_pct')
    y = y.join(ex)
    y.to_csv(f'{OUT}/sensitivity_tau_v3.csv')
    md += ['## Sensitivity to the rule threshold tau: yield (%) and cost excess over exact (%)', y.to_markdown(), '']
    # lambda: exact trade-off, and heuristics (main v3 seed-0 rows) re-scored with each lambda
    l = d[(d.sweep == 'lambda') & (d.accepted == 1)]
    lt = l.groupby(['domain', 'model', 'value']).agg(effort=('effort', 'mean'), sparsity=('sparsity', 'mean')).round(3)
    rows = []
    for (dm, m), g in l.groupby(['domain', 'model']):
        v3 = pd.read_csv(f'results_v3/v3_{dm}_{m}_s0.csv.gz')
        v3 = v3[v3['query'].isin(g['query'].unique())]
        for lam, gl in g.groupby('value'):
            ex_cost = gl.set_index('query').cost
            for c in ['framework', 'repair_esc', 'posthoc_full_gate']:
                h = v3[(v3.condition == c) & (v3.accepted == 1)].set_index('query')
                q = h.index.intersection(ex_cost.index)
                if len(q):
                    hc = h.loc[q, 'effort'] + lam * h.loc[q, 'sparsity']
                    rows.append(dict(domain=dm, model=m, lam=lam, method=c, excess_pct=round(100 * (hc.mean() / ex_cost.loc[q].mean() - 1), 1)))
    lx = pd.DataFrame(rows).pivot_table(index=['domain', 'model', 'lam'], columns='method', values='excess_pct')
    lt = lt.reset_index().merge(lx.reset_index(), left_on=['domain', 'model', 'value'],
                                                                  right_on=['domain', 'model', 'lam'], how='left').drop(columns='lam')
    lt.to_csv(f'{OUT}/sensitivity_lambda_v3.csv', index=False)
    md += ['## Sensitivity to the sparsity weight lambda: exact effort / sparsity, and heuristic cost excess re-scored with lambda (%)',
           lt.to_markdown(index=False), '']
    return md


def main():
    md = []
    if glob.glob('results_scale/*.csv'):
        md += scale()
    if glob.glob('results_sens/*.csv'):
        md += sens()
    open(f'{OUT}/scale_sens_v3.md', 'w').write('\n'.join(md)); print('\n'.join(md))


if __name__ == '__main__':
    main()
