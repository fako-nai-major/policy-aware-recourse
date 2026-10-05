"""Build the supplementary tables (S1-S6) from the result files.

Usage (from the repository root):  python tools/supplementary_tables.py
Writes one CSV per table to results/tables/supplementary/ plus supplementary.json
(captions, headers, rows and notes, used to typeset the supplementary document).
Run analyze.py, ext_analyze.py and fairness.py first if results/tables is empty.
"""
import json, glob
import pandas as pd

import os
R = 'results'
T = f'{R}/tables'
S = []
ms = lambda m, s, d=3: f'{m:.{d}f} ± {s:.{d}f}'
DS_ORDER = {'OULAD': 0, 'AUC': 1, 'HarvardX': 2}
STAGE = {'1': 'Stage 1', '2': 'Stage 2', '3': 'Stage 3', 'full': 'Complete', '0': '–'}
SAMP = {'none': 'None', 'smote': 'SMOTE', 'nearmiss': 'NearMiss'}
MODEL = {'ABC': 'AdaBoost', 'CB': 'CatBoost', 'DT': 'Decision tree', 'GBC': 'Gradient boosting', 'KNN': 'k-NN',
         'LR': 'Logistic regression', 'MLP': 'MLP', 'NB': 'Naive Bayes', 'RF': 'Random forest', 'Ridge': 'Ridge',
         'SVC': 'SVM', 'XGB': 'XGBoost', 'XT': 'Extra trees'}

# ------------------------------------------------------------------ S1
d = pd.concat([pd.read_csv(f, dtype={'stage': str}) for f in glob.glob(f'{R}/predictive_*.csv')])
g = d.groupby(['dataset', 'stage', 'sampler', 'model'])[['roc_auc', 'bal_acc', 'f1_fail', 'recall_fail']].agg(['mean', 'std']).reset_index()
g['o'] = g.dataset.map(DS_ORDER); g['so'] = g.sampler.map({'none': 0, 'smote': 1, 'nearmiss': 2})
g = g.sort_values(['o', 'stage', 'so', 'model'])
rows, bold = [], []
best = d[d.sampler == 'none'].groupby(['dataset', 'stage', 'model']).roc_auc.mean()
for _, r in g.iterrows():
    k = (r.dataset.iloc[0] if hasattr(r.dataset, 'iloc') else r['dataset'])
    rr = [r[('dataset', '')], STAGE[r[('stage', '')]], SAMP[r[('sampler', '')]], MODEL[r[('model', '')]]] + \
         [ms(r[(c, 'mean')], r[(c, 'std')]) for c in ['roc_auc', 'bal_acc', 'f1_fail', 'recall_fail']]
    if r[('model', '')] == 'CB':
        bold.append(len(rows))
    rows.append(rr)
S.append(dict(id='S1', caption='**Table S1.** Predictive performance of all thirteen classifiers under three resampling conditions (learner-grouped 5-fold cross-validation; mean ± SD over folds). CatBoost, the model used by the prescriptive layer, is shaded.',
              header=['Dataset', 'Model input', 'Resampling', 'Classifier', 'ROC-AUC', 'Balanced acc.', 'F1 (fail)', 'Recall (fail)'],
              widths=[850, 950, 1050, 1450, 1175, 1175, 1175, 1175], rows=rows, bold=bold,
              foot='ROC-AUC is computed from predicted scores (predict_proba or decision_function). SMOTE and NearMiss are applied to the training folds only; validation folds are never resampled. Stage k models use the assessments released by stage k (and, for OULAD, the module indicator); "Complete" is the complete-record outcome model f. "Fail" is the at-risk class; F1 and recall use a 0.5 threshold. Learner and assessment identifiers are excluded from all models. Decision trees, and Naive Bayes on the small AUC folds, produce near-binary scores, so their ROC-AUC can equal their balanced accuracy.',
              repeat=True))

fr = pd.read_csv(f'{T}/predictive_friedman.csv', dtype={'stage': str})
fr['o'] = fr.dataset.map(DS_ORDER); fr = fr.sort_values(['o', 'stage'])
S.append(dict(id='S1b', caption='**Table S1 (continued).** Friedman tests across the thirteen classifiers (no resampling; folds as blocks) and CatBoost\'s mean rank.',
              header=['Dataset', 'Model input', 'Friedman p', 'CatBoost mean rank', 'Best model', 'Best ROC-AUC', 'CatBoost ROC-AUC'],
              widths=[1100, 1200, 1100, 1500, 1500, 1300, 1300],
              rows=[[r.dataset, STAGE[r.stage], '< .001' if r.friedman_p < 0.001 else f'{r.friedman_p:.3f}', f'{r.cb_rank:.1f}',
                     MODEL[r.top], f'{r.top_auc:.3f}', f'{r.cb_auc:.3f}'] for r in fr.itertuples()],
              foot='Ranks are computed per fold over ROC-AUC (1 = best). With five folds per test the Friedman test has limited power to separate individual models; the differences between CatBoost and the best model are at most 0.012 in ROC-AUC.'))

# ------------------------------------------------------------------ S2
c = pd.read_csv(f'{T}/cohort.csv', dtype={'stage': str}); y = pd.read_csv(f'{T}/yield_by_stage.csv', dtype={'stage': str})
m = c.merge(y, on=['dataset', 'stage']); m['o'] = m.dataset.map(DS_ORDER); m = m.sort_values(['o', 'stage'])
cols = ['DiCE first candidate', 'Post-hoc full-gate filter', 'Policy-aware ranking (no edit)', 'Policy-aware ranking + edit (framework)',
        'Framework + fallback over ranked pool', 'Direct policy repair + classifier escalation']
f = lambda v: 'n/a' if pd.isna(v) else f'{v:.1f}'
S.append(dict(id='S2', caption='**Table S2.** Query cohorts and accepted yield (%) by early-warning stage (aligned bounds; mean over seeds).',
              header=['Dataset', 'Stage', 'Eligible / evaluated', 'True failures', 'DiCE first', 'DiCE + full gate', 'Ranking, no edit', 'Framework', 'Framework + fallback', 'Repair + escalation'],
              widths=[880, 620, 1100, 820, 830, 930, 930, 930, 980, 980],
              rows=[[r.dataset, STAGE[r.stage], f'{r.eligible:,.0f} / {r.evaluated:,.0f}', f'{r.true_fail*100:.0f}%'] + [f(getattr(r, '_x') if False else r._asdict()[k]) for k in []] +
                    [f(m.loc[i, k]) for k in cols] for i, r in zip(m.index, m.itertuples())],
              foot='Stage k queries are held-out learners flagged at risk by the stage-k model and predicted to fail by f with pending assessments coded 0. OULAD evaluates at most 300 queries per stage and seed; HarvardX at most 400. AUC stage 1 leaves three assessments pending, so the policy is nearly always reachable; at stage 3 a single assessment remains and the attainable ceiling falls accordingly.'))

# ------------------------------------------------------------------ S3
a = pd.read_csv(f'{T}/ablation_yield.csv'); a = a[a.dataset != 'HarvardX']
a['o'] = a.dataset.map(DS_ORDER); a['ro'] = a.regime.map({'aligned': 0, 'floor': 1, 'mismatch': 2}); a = a.sort_values(['o', 'ro'])
strat = [c for c in a.columns if c not in ('dataset', 'regime', 'o', 'ro')]
names = {'DiCE first candidate': 'DiCE, first candidate', 'Post-hoc policy filter': 'DiCE, post-hoc policy filter',
         'Post-hoc full-gate filter': 'DiCE, post-hoc full-gate filter', 'Policy-aware ranking (no edit)': 'Policy-aware ranking, no editing',
         'Policy-aware ranking + edit (framework)': 'Framework (ranking + editing + gate)', 'Framework + fallback over ranked pool': 'Framework with fallback',
         'Direct policy repair (no DiCE)': 'Direct policy repair (no DiCE)', 'Direct policy repair + classifier escalation': 'Direct policy repair + escalation',
         'Policy reachable within bounds (upper bound)': 'Policy reachable within bounds (ceiling)'}
keys = [(r.dataset, r.regime) for r in a.itertuples()]
rows = []
for s in strat:
    rows.append([names[s]] + [str(a.loc[(a.dataset == d_) & (a.regime == g_), s].iloc[0]) for d_, g_ in keys])
ex = pd.read_csv(f'{T}/external_yield.csv')
ext_rows = []
for meth in ['NICE', 'MCCE', 'CARE']:
    for var, lab in [('native', 'native'), ('bounded', 'bounded'), ('bounded+edit', 'bounded + editing')]:
        r = [f'{meth} {lab}']
        for d_, g_ in keys:
            v = ex[(ex.dataset == d_) & (ex.regime == g_) & (ex.condition == f'{meth}_{var}')]
            r.append(str(v.yield_pct.iloc[0]) if len(v) else '–')
        ext_rows.append(r)
S.append(dict(id='S3', caption='**Table S3.** Accepted yield (% of eligible queries, mean ± SD over seeds) under the three bound configurations.',
              header=['Strategy'] + [f'{d_} {g_}' for d_, g_ in keys], widths=[2700] + [1050] * 6,
              rows=rows + [['*External methods (same queries, models, bounds and gate)*'] + [''] * 6] + ext_rows, sectionrow=[len(rows)],
              foot='Aligned: DiCE search range and gate bounds both [0, w] for a pending assessment of weight w. Floor: both [0.4w, w]. Mismatch: DiCE searches [0, w] while the gate enforces [0.4w, w]. Queries per configuration: AUC 2,587 (10 seeds); OULAD 3,914 (5 seeds). On AUC the bounds bind rarely, so the three configurations give similar results. NICE and MCCE were run on all queries under aligned bounds and, for OULAD, floor bounds; CARE on 100 queries per seed for seeds 0–2 (aligned, n = 300) and seed 0 (OULAD floor, n = 100, single run, no SD). External methods were not run under the mismatch configuration (–). For the CARE subset, framework yields on the same queries are reported in the main text (Table 9).'))

# ------------------------------------------------------------------ S4
o = pd.read_csv(f'{T}/objective_audit.csv')
VAR = [('rank_edit', 'Reference (λ = 1000, 1000, 1, 0.5)'), ('drop_policy', 'Without policy penalty'), ('drop_feas', 'Without feasibility penalty'),
       ('drop_prox', 'Without proximity'), ('drop_spar', 'Without sparsity'), ('lp_1', 'λ_{policy} = 1'), ('lp_10', 'λ_{policy} = 10'),
       ('lp_100', 'λ_{policy} = 100'), ('lx_0.1', 'λ_{prox} = 0.1'), ('lx_10', 'λ_{prox} = 10')]
rows, sec = [], []
for d_ in ['OULAD', 'AUC', 'HarvardX']:
    for g_ in ['aligned', 'floor', 'mismatch']:
        sub = o[(o.dataset == d_) & (o.regime == g_)]
        if not len(sub):
            continue
        sec.append(len(rows)); rows.append([f'*{d_}, {g_} bounds*', '', '', ''])
        for v, lab in VAR:
            r = sub[sub.variant == v].iloc[0]
            rows.append([lab, r.yield_, f'{r.changed_selection_pct:.1f}', f'{r.mean_effort_accepted:.2f}'])
S.append(dict(id='S4', caption='**Table S4.** Objective audit and weight sensitivity (framework without fallback; editing and gate held fixed).',
              header=['Variant', 'Accepted yield (%)', 'Selection changed (%)', 'Mean effort (accepted)'], widths=[3600, 1800, 1800, 1800],
              rows=rows, sectionrow=sec,
              foot='Reference weights (λ_{policy}, λ_{feas}, λ_{prox}, λ_{spar}) = (1000, 1000, 1, 0.5). Each row changes one weight. "Selection changed" is the share of queries whose selected candidate differs from the reference. Effort is the normalised L1 change of the accepted recommendation. With λ_{policy} = 1 the policy term is on the scale of proximity, which is equivalent to removing it in most queries. On OULAD the yield is stable for λ_{policy} ≥ 100 and for λ_{prox} between 0.1 and 10; on AUC, λ_{policy} = 100 or λ_{prox} = 10 lowers the yield by about four points.'))

# ------------------------------------------------------------------ S5
t = pd.read_csv(f'{T}/tau_sweep.csv'); t['o'] = t.dataset.map(DS_ORDER); t = t.sort_values(['o', 'tau'])
tc = ['DiCE first candidate', 'Post-hoc full-gate filter', 'Policy-aware ranking (no edit)', 'Policy-aware ranking + edit (framework)',
      'Framework + fallback over ranked pool', 'Direct policy repair + classifier escalation']
def tlab(r):
    if r.dataset == 'AUC':
        return f'grade > {15 if abs(r.tau - 15.001) < 1e-6 else r.tau:g}' + (' (primary)' if abs(r.tau - 15.001) < 1e-6 else '')
    return f'score ≥ {r.tau:g}' + (' (primary)' if r.tau == 40 else '')
S.append(dict(id='S5', caption='**Table S5.** Accepted yield (%, mean ± SD over seeds) under alternative policy thresholds (aligned bounds, fixed candidate pools).',
              header=['Dataset', 'Threshold', 'DiCE first', 'DiCE + full gate', 'Ranking, no edit', 'Framework', 'Framework + fallback', 'Repair + escalation'],
              widths=[900, 1500, 1100, 1100, 1100, 1100, 1100, 1100],
              rows=[[r.dataset, tlab(r)] + [r._asdict()[f'_{t.columns.get_loc(k) + 1}'] for k in tc] for r in t.itertuples()],
              foot='Only the threshold τ changes; models, query cohorts and DiCE pools are those of the primary analysis. AUC thresholds are on the final grade (one quarter of the sum of assignment marks); OULAD thresholds are on the 0–100 course score. The large SDs of repair + escalation on OULAD at 30–40 come mainly from one seed (seed 4), in which escalation satisfied f for 69% and 77% of queries against 90–98% for the other seeds.'))

# ------------------------------------------------------------------ S6
METH = ['DiCE first candidate', 'DiCE + full gate', 'Framework', 'Framework + fallback', 'Policy repair + escalation', 'NICE (bounded)', 'MCCE (bounded)', 'CARE (bounded)']
ATTR = {'gender': 'Gender', 'age': 'Age band', 'imd': 'IMD band', 'disability': 'Disability'}
gr = pd.read_csv(f'{T}/fairness_recourse_groups.csv')
rows, sec = [], []
for me in METH:
    sec.append(len(rows)); rows.append([f'*{me}*', '', '', '', '', ''])
    for r in gr[gr.method == me].itertuples():
        rows.append([ATTR[r.attribute], r.group, f'{r.n:,}', f'{r.yield_pct:.1f}', '–' if pd.isna(r.effort) else f'{r.effort:.3f}', '–' if pd.isna(r.policy_score) else f'{r.policy_score:.1f}'])
S.append(dict(id='S6a', caption='**Table S6a.** Recourse outcomes by learner group (OULAD, aligned bounds, τ = 40; unadjusted).',
              header=['Attribute', 'Group', 'Queries', 'Accepted yield (%)', 'Mean effort', 'Mean policy score'], widths=[1400, 2700, 1100, 1300, 1200, 1300],
              rows=rows, sectionrow=sec, repeat=True,
              foot='Group attributes come from studentInfo.csv (100% match on learner and module presentation) and are not used by any model. CARE was run on 300 queries; all other methods on all 3,914 queries (5 seeds). Effort and policy score are averaged over accepted recommendations only. The adjusted IMD contrast (Table S6c) compares the most and least deprived bands; "IMD missing" is shown for completeness.'))

ut = pd.read_csv(f'{T}/fairness_recourse_tests.csv')
pf = lambda p: '–' if pd.isna(p) else ('< .001' if p < 0.001 else f'{p:.3f}')
rows = []
for me in METH:
    for r in ut[ut.method == me].itertuples():
        rows.append([me, ATTR[r.attribute], f'{r.yield_gap_pp:.1f}', pf(r.p_yield_holm), f'{r.effort_gap:.3f} ({r.effort_gap_rel_pct:.0f}%)', pf(r.p_effort_holm)])
S.append(dict(id='S6b', caption='**Table S6b.** Unadjusted group gaps in recourse (largest minus smallest group; Holm-adjusted p).',
              header=['Method', 'Attribute', 'Yield gap (pp)', 'p (Holm)', 'Effort gap (relative)', 'p (Holm)'], widths=[2400, 1200, 1300, 1000, 2000, 1000],
              rows=rows, repeat=True,
              foot='Gaps are absolute differences between the groups with the highest and lowest value (direction in Table S6a). Yield gaps are tested with χ² tests and effort gaps with Kruskal–Wallis tests; Holm correction within each outcome across all methods and attributes. The framework with fallback accepts every query, so it has no yield gap (–). Most of these gaps disappear once module and stage are controlled for (Table S6c), so they reflect differences in course composition between groups rather than group membership itself.'))

ad = pd.read_csv(f'{T}/fairness_recourse_adjusted.csv')
rows = []
for me in METH:
    for r in ad[(ad.method == me) & ad.p.notna()].itertuples():
        lab = r.contrast.replace(' (most deprived)', '').replace('Disability: ', '').replace(' - ', ' − ')
        out = 'Yield (pp)' if r.outcome == 'yield_pp' else 'Effort'
        dd = 1 if r.outcome == 'yield_pp' else 3
        rows.append([me, lab, out, f'{r.n:,}', f'{r.raw_diff:.{dd}f}', f'{r.adj_diff:.{dd}f} [{r.ci_lo:.{dd}f}, {r.ci_hi:.{dd}f}]', pf(r.p), pf(r.p_holm)])
S.append(dict(id='S6c', caption='**Table S6c.** Module- and stage-adjusted group contrasts for all methods (OULAD, aligned bounds).',
              header=['Method', 'Contrast', 'Outcome', 'n', 'Raw diff.', 'Adjusted diff. [95% CI]', 'p', 'p (Holm)'], widths=[1900, 1500, 900, 700, 800, 1800, 700, 700],
              rows=rows, repeat=True,
              foot='Linear models with module × stage fixed effects; standard errors clustered by learner. Yield contrasts use all queries; effort contrasts use accepted recommendations only. Contrasts that cannot be estimated (no variation in the outcome, e.g. the framework with fallback, which accepts every query) are omitted, leaving 59 estimable contrasts. Holm correction across all contrasts; the smallest adjusted p is 0.68.'))

pg = pd.read_csv(f'{T}/fairness_prediction_gaps.csv', header=[0, 1], index_col=[0, 1])
rows = []
for (mdl, at), r in pg.iterrows():
    rows.append([mdl.replace('complete record', 'Complete record (f)').replace('stage', 'Stage'), ATTR[at]] +
                [ms(r[(k, 'mean')], r[(k, 'std')]) for k in ['DPD', 'EOD', 'FPR_gap']])
rows.sort(key=lambda x: (x[0].startswith('Complete'), x[0]))
S.append(dict(id='S6d', caption='**Table S6d.** Group disparities of the OULAD early-warning and outcome models (CatBoost, no resampling; mean ± SD over five seeds).',
              header=['Model', 'Attribute', 'Demographic parity diff.', 'Equal opportunity diff.', 'FPR gap'], widths=[2000, 1400, 1900, 1900, 1800],
              rows=rows,
              foot='Each seed trains on 80% of learners and evaluates on the held-out 20% (GroupShuffleSplit by learner). Differences are between the groups with the highest and lowest rate, with "fail" (at risk) as the positive class. Demographic parity: flag rate; equal opportunity: recall of true failures; FPR gap: false alarm rate among learners who passed. The larger IMD differences follow the higher failure rates of learners from the most deprived areas: the models flag them more often and detect their failures more reliably.'))

OUTD = f'{T}/supplementary'
os.makedirs(OUTD, exist_ok=True)
for s in S:
    pd.DataFrame(s['rows'], columns=s['header']).to_csv(f"{OUTD}/Table_{s['id']}.csv", index=False)
    print(s['id'], len(s['rows']))
json.dump(S, open(f'{OUTD}/supplementary.json', 'w'), ensure_ascii=False, indent=1)
