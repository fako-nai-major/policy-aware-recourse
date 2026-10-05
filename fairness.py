"""Group-level fairness audit for OULAD (needs OULAD studentInfo.csv).

Usage:  python3 fairness.py /path/to/studentInfo.csv

Part A (early warning): for the stage-k early-warning models g_k and the
complete-record model f, per group: flag rate (predicted fail), recall of true
failers (TPR for the fail class) and false-flag rate among true passers.
Reports demographic-parity difference (DPD) and equal-opportunity difference (EOD).

Part B (recourse): for the framework and the baselines, per group: accepted
yield, normalised effort and policy score among accepted recommendations.
Chi-square test of yield vs group; Kruskal-Wallis on effort. Holm-adjusted.
"""
import sys, glob, numpy as np, pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests
from sklearn.model_selection import GroupShuffleSplit
from datasets import load_oulad
import prescriptive as P

OUT = 'results/tables'
ATTRS = ['gender', 'age', 'imd', 'disability']
LABEL = {'rank_edit_fallback': 'Framework + fallback', 'rank_edit': 'Framework',
         'posthoc_full_gate': 'DiCE + full gate', 'dice_first': 'DiCE first candidate',
         'policy_repair_escalate': 'Policy repair + escalation',
         'MCCE_bounded': 'MCCE (bounded)', 'NICE_bounded': 'NICE (bounded)', 'CARE_bounded': 'CARE (bounded)'}


def groups(info):
    g = info.copy()
    g['age'] = np.where(g.age_band == '0-35', '0-35', '35+')
    imd = g.imd_band.astype(str).str.extract(r'^(\d+)')[0].astype(float)
    g['imd'] = pd.cut(imd, [-1, 29, 69, 100], labels=['IMD 0-30% (most deprived)', 'IMD 30-70%', 'IMD 70-100%']).astype(str)
    g.loc[imd.isna(), 'imd'] = 'IMD missing'
    g['disability'] = g.disability.map({'Y': 'Disability: yes', 'N': 'Disability: no'})
    g['gender'] = g.gender.map({'F': 'Female', 'M': 'Male'})
    return g[['id_student', 'code_module', 'code_presentation'] + ATTRS]


def part_a(cfg, g, seeds):
    df = cfg.df.merge(g, on=['id_student', 'code_module', 'code_presentation'], how='left')
    rows = []
    for seed in seeds:
        tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(df, df[cfg.y], df[cfg.group]))
        dtr, dte = df.iloc[tr], df.iloc[te]
        models = {f'stage {k}': (cfg.tests[:k] + list(cfg.immutable_extra)) for k in cfg.stages}
        models['complete record'] = list(cfg.features)
        for name, feats in models.items():
            m = P.cat(seed).fit(dtr[feats], dtr[cfg.y])
            flag = (m.predict_proba(dte[feats])[:, 1] < 0.5).astype(int)
            y = dte[cfg.y].values
            for a in ATTRS:
                for grp, idx in dte.groupby(a).indices.items():
                    fl, yy = flag[idx], y[idx]
                    rows.append(dict(seed=seed, model=name, attribute=a, group=grp, n=len(idx),
                                     flag_rate=fl.mean(), fail_recall=fl[yy == 0].mean() if (yy == 0).any() else np.nan,
                                     false_flag=fl[yy == 1].mean() if (yy == 1).any() else np.nan,
                                     base_fail=(yy == 0).mean()))
        print('part A seed', seed, flush=True)
    A = pd.DataFrame(rows)
    per = A.groupby(['model', 'attribute', 'group'])[['n', 'base_fail', 'flag_rate', 'fail_recall', 'false_flag']].mean()
    gap = A.groupby(['seed', 'model', 'attribute']).agg(
        DPD=('flag_rate', lambda x: x.max() - x.min()), EOD=('fail_recall', lambda x: x.max() - x.min()),
        FPR_gap=('false_flag', lambda x: x.max() - x.min())).groupby(['model', 'attribute']).agg(['mean', 'std'])
    return per, gap


def part_b(cfg, g):
    key = cfg.df[['id_student', 'code_module', 'code_presentation']].copy(); key['query'] = key.index
    key = key.merge(g, on=['id_student', 'code_module', 'code_presentation'], how='left')
    fw = pd.concat([pd.read_csv(f) for f in glob.glob('results/presc_OULAD_s*_rows.csv.gz')])
    fw = fw[(fw.tau == 40.0) & (fw.regime == 'aligned') & fw.condition.isin(LABEL)]
    ex = pd.concat([pd.read_csv(f) for f in glob.glob('results/ext_OULAD_aligned_s*.csv')])
    ex = ex[ex.condition.isin(LABEL)]
    cols = ['seed', 'stage', 'query', 'condition', 'accepted', 'effort', 'policy_score']
    rows = pd.concat([fw[cols], ex[cols]]).merge(key[['query'] + ATTRS], on='query', how='left')
    out, tests = [], []
    for cond, d in rows.groupby('condition'):
        for a in ATTRS:
            for grp, h in d.groupby(a):
                acc = h[h.accepted == 1]
                out.append(dict(method=LABEL[cond], attribute=a, group=grp, n=len(h),
                                yield_pct=100 * h.accepted.mean(), effort=acc.effort.mean(),
                                policy_score=acc.policy_score.mean()))
            ct = pd.crosstab(d[a], d.accepted)
            p_y = stats.chi2_contingency(ct)[1] if ct.shape == (ct.shape[0], 2) and ct.shape[0] > 1 else np.nan
            eff = [h[h.accepted == 1].effort.dropna().values for _, h in d.groupby(a)]
            eff = [e for e in eff if len(e) > 1]
            p_e = stats.kruskal(*eff).pvalue if len(eff) > 1 else np.nan
            ys = d.groupby(a).accepted.mean() * 100
            es = d[d.accepted == 1].groupby(a).effort.mean()
            tests.append(dict(method=LABEL[cond], attribute=a, n=len(d), yield_gap_pp=ys.max() - ys.min(),
                              p_yield=p_y, effort_gap=es.max() - es.min(), effort_gap_rel_pct=100 * (es.max() - es.min()) / es.mean(),
                              p_effort=p_e))
    B = pd.DataFrame(out); T = pd.DataFrame(tests)
    for c in ['p_yield', 'p_effort']:
        ok = T[c].notna()
        T.loc[ok, c + '_holm'] = multipletests(T.loc[ok, c], method='holm')[1]
    return B, T


CONTRASTS = {'gender': ('Female', 'Male'), 'age': ('35+', '0-35'),
             'imd': ('IMD 0-30% (most deprived)', 'IMD 70-100%'), 'disability': ('Disability: yes', 'Disability: no')}


def part_c(cfg, g):
    """Module x stage adjusted contrasts (linear probability for yield, OLS for effort),
    cluster-robust SEs by learner. Separates group effects from course composition."""
    import statsmodels.formula.api as smf
    key = cfg.df[['id_student', 'code_module', 'code_presentation']].copy(); key['query'] = key.index
    key = key.merge(g, on=['id_student', 'code_module', 'code_presentation'], how='left')
    fw = pd.concat([pd.read_csv(f) for f in glob.glob('results/presc_OULAD_s*_rows.csv.gz')])
    fw = fw[(fw.tau == 40.0) & (fw.regime == 'aligned') & fw.condition.isin(LABEL)]
    ex = pd.concat([pd.read_csv(f) for f in glob.glob('results/ext_OULAD_aligned_s*.csv')])
    ex = ex[ex.condition.isin(LABEL)]
    cols = ['seed', 'stage', 'query', 'condition', 'accepted', 'effort']
    rows = pd.concat([fw[cols], ex[cols]]).merge(key[['query', 'id_student', 'code_module'] + ATTRS], on='query')
    out = []
    for cond, d in rows.groupby('condition'):
        for a, (grp, ref) in CONTRASTS.items():
            h = d[d[a].isin([grp, ref])].copy(); h['G'] = (h[a] == grp).astype(int)
            for outcome, data in [('yield_pp', h), ('effort', h[h.accepted == 1])]:
                y = 'accepted' if outcome == 'yield_pp' else 'effort'
                raw = data.groupby('G')[y].mean(); raw_d = raw.get(1, np.nan) - raw.get(0, np.nan)
                est = lo = hi = p = np.nan
                if data[y].nunique() > 1 and data.G.nunique() == 2:
                    try:
                        m = smf.ols(f'{y} ~ G + C(code_module)*C(stage)', data=data).fit(
                            cov_type='cluster', cov_kwds={'groups': data['id_student']})
                        est, (lo, hi), p = m.params['G'], m.conf_int().loc['G'].values, m.pvalues['G']
                    except Exception:
                        pass
                sc = 100 if outcome == 'yield_pp' else 1
                out.append(dict(method=LABEL[cond], attribute=a, contrast=f'{grp} - {ref}', outcome=outcome,
                                n=len(data), raw_diff=sc * raw_d, adj_diff=sc * est, ci_lo=sc * lo, ci_hi=sc * hi, p=p))
    C = pd.DataFrame(out)
    ok = C.p.notna(); C.loc[ok, 'p_holm'] = multipletests(C.loc[ok, 'p'], method='holm')[1]
    return C


def main(path):
    info = pd.read_csv(path)
    cfg = load_oulad()
    g = groups(info)
    per, gap = part_a(cfg, g, seeds=[0, 1, 2, 3, 4])
    B, T = part_b(cfg, g)
    C = part_c(cfg, g); C.round(4).to_csv(f'{OUT}/fairness_recourse_adjusted.csv', index=False)
    per.round(3).to_csv(f'{OUT}/fairness_prediction_groups.csv'); gap.round(3).to_csv(f'{OUT}/fairness_prediction_gaps.csv')
    B.round(3).to_csv(f'{OUT}/fairness_recourse_groups.csv', index=False); T.round(4).to_csv(f'{OUT}/fairness_recourse_tests.csv', index=False)
    md = ['## A. Early-warning fairness (mean over 5 seeds)', per.round(3).to_markdown(), '',
          '## A. Gaps (max-min across groups; mean, SD over seeds)', gap.round(3).to_markdown(), '',
          '## B. Recourse by group', B.round(3).to_markdown(index=False), '',
          '## B. Recourse gaps and tests (Holm-adjusted)', T.round(4).to_markdown(index=False), '',
          '## C. Module x stage adjusted contrasts (cluster-robust by learner, Holm)', C.round(4).to_markdown(index=False)]
    open(f'{OUT}/fairness_summary.md', 'w').write('\n'.join(md)); print('\n'.join(md))


if __name__ == '__main__':
    main(sys.argv[1])
