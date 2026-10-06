"""Build data/OULAD/OULAD_coursework.csv from the raw OULAD tables.

Each row is one learner in one module presentation. For every presentation the
weighted coursework assessments (TMA and CMA with weight > 0; exams excluded)
are ordered by due date, then by assessment id. Test_k is the contribution of
the k-th assessment to the coursework score,

    Test_k = score_k * weight_k / 100,

and W_k is that assessment's weight (its maximum contribution). In OULAD the
coursework weights of a presentation sum to 100, so sum_k Test_k is the 0-100
coursework score to which the Open University's 40% threshold applies.
Missing submissions contribute 0. sum_click is the learner's total number of
VLE clicks in the presentation.

Usage (from the repository root):
    python tools/prepare_oulad.py path/to/oulad_raw_folder
The folder must contain assessments.csv, studentAssessment.csv,
studentInfo.csv and studentVle.csv (https://analyse.kmi.open.ac.uk/open_dataset).
"""
import os
import sys
import numpy as np
import pandas as pd

MODULES = ['AAA', 'BBB', 'EEE', 'FFF']
KEY = ['code_module', 'code_presentation']
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'OULAD', 'OULAD_coursework.csv')


def main(raw):
    a = pd.read_csv(f'{raw}/assessments.csv')
    a = a[a.code_module.isin(MODULES) & (a.assessment_type != 'Exam') & (a.weight > 0)].copy()
    a['date'] = pd.to_numeric(a.date, errors='coerce')
    a = a.sort_values(KEY + ['date', 'id_assessment'])
    a['k'] = a.groupby(KEY).cumcount() + 1
    wsum = a.groupby(KEY).weight.sum()
    print('coursework weight sum per presentation:\n', wsum.to_string())

    sa = pd.read_csv(f'{raw}/studentAssessment.csv')
    sa['score'] = pd.to_numeric(sa.score, errors='coerce').fillna(0.0)
    sa = sa.merge(a[['id_assessment', 'k', 'weight'] + KEY], on='id_assessment')
    sa['contrib'] = sa.score * sa.weight / 100.0

    info = pd.read_csv(f'{raw}/studentInfo.csv')
    info = info[info.code_module.isin(MODULES)][['id_student'] + KEY + ['final_result']]

    T = sa.pivot_table(index=['id_student'] + KEY, columns='k', values='contrib', aggfunc='sum')
    K = int(a.k.max())
    T = T.reindex(columns=range(1, K + 1))
    T.columns = [f'Test_{k}' for k in T.columns]
    W = a.pivot_table(index=KEY, columns='k', values='weight').reindex(columns=range(1, K + 1))
    W.columns = [f'W_{k}' for k in W.columns]

    d = info.merge(T.reset_index(), on=['id_student'] + KEY, how='left').merge(W.reset_index(), on=KEY, how='left')
    tests, ws = [f'Test_{k}' for k in range(1, K + 1)], [f'W_{k}' for k in range(1, K + 1)]
    d[ws] = d[ws].fillna(0.0)
    d[tests] = d[tests].fillna(0.0)

    clicks = 0
    for ch in pd.read_csv(f'{raw}/studentVle.csv', usecols=['id_student', 'code_module', 'code_presentation', 'sum_click'],
                          chunksize=2_000_000):
        ch = ch[ch.code_module.isin(MODULES)]
        c = ch.groupby(['id_student'] + KEY).sum_click.sum()
        clicks = c if isinstance(clicks, int) else clicks.add(c, fill_value=0)
    d = d.merge(clicks.rename('sum_click').reset_index(), on=['id_student'] + KEY, how='left')
    d['sum_click'] = d.sum_click.fillna(0.0)

    d = d[['id_student'] + KEY + ['sum_click'] + tests + ws + ['final_result']]
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    d.to_csv(OUT, index=False)
    score = d[tests].sum(axis=1)
    print(f'{len(d):,} rows, {K} coursework assessments max; coursework score range {score.min():.1f}-{score.max():.1f} -> {OUT}')


if __name__ == '__main__':
    main(sys.argv[1])
