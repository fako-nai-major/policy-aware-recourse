"""Dataset loaders and policy configurations for all experiments.

Every configuration choice reported in the paper lives here:
features, outcome, grouping key, stages, policy score, threshold, and
per-feature bounds.  Nothing is read from notebook state.
"""
import os
import numpy as np
import pandas as pd

# Folder containing OULAD/, AUC/ and HarvardX/ (see data/README.md).
DATA = os.environ.get('PAR_DATA', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))


class Config:
    """Container for one dataset's experimental configuration."""

    def __init__(self, **kw):
        self.__dict__.update(kw)


# ----------------------------------------------------------------- OULAD
# Built by tools/prepare_oulad.py from the raw OULAD tables: Test_k is the
# contribution of the k-th weighted coursework assessment (score x weight / 100,
# exams excluded) and W_k its weight, so sum_k Test_k is the 0-100 coursework
# score to which the Open University's 40% threshold applies.
OULAD_MODULES = ['AAA', 'BBB', 'EEE', 'FFF']


def load_oulad():
    o = pd.read_csv(f'{DATA}/OULAD/OULAD_coursework.csv')
    o = o[o.code_module.isin(OULAD_MODULES)].copy()
    # Withdrawn learners have no final assessment outcome; they are excluded.
    o = o[o.final_result != 'Withdrawn'].copy()
    o['y'] = o.final_result.isin(['Pass', 'Distinction']).astype(int)
    tests = sorted([c for c in o.columns if c.startswith('Test_')], key=lambda c: int(c.split('_')[1]))
    o[tests] = o[tests].fillna(0.0).astype(float)          # non-submission = 0
    o['sum_click'] = o['sum_click'].astype(float)
    mods = pd.get_dummies(o.code_module, prefix='mod').astype(float)
    o = pd.concat([o, mods], axis=1)
    mod_cols = list(mods.columns)
    features = tests + ['sum_click'] + mod_cols
    click_hi = o.groupby('code_module')['sum_click'].quantile(0.95)
    return Config(
        name='OULAD', df=o.reset_index(drop=True), y='y', group='id_student',
        features=features, tests=tests, immutable_extra=mod_cols,
        engagement=['sum_click'], stages=[1, 2, 3],
        policy_weights={t: 1.0 for t in tests}, tau=40.0,
        tau_sweep=[30.0, 40.0, 50.0, 60.0],
        # upper bound of each assessment = its weight in this presentation
        test_ub=lambda row: {t: float(row['W_' + t.split('_')[1]]) for t in tests},
        click_hi=lambda row: float(click_hi.loc[row['code_module']]),
        policy_desc='coursework score (sum of weighted assessment contributions, 0-100) >= 40 (OU threshold)')


# ------------------------------------------------------------------- AUC
AUC_TESTS = ['Test_1', 'Test_2', 'Test_3', 'Test_4']   # Test_5/final_exam are all zero


def load_auc():
    a = pd.read_csv(f'{DATA}/AUC/assignment_grades_cleaned.csv')
    a['y'] = a['final_result'].astype(int)
    a[AUC_TESTS] = a[AUC_TESTS].astype(float)
    a['sum_click'] = a['sum_click'].astype(float)
    features = AUC_TESTS + ['sum_click']
    ub = {'Test_1': 10.0, 'Test_2': 20.0, 'Test_3': 20.0, 'Test_4': 20.0}
    hi = float(a.sum_click.quantile(0.95))
    return Config(
        name='AUC', df=a.reset_index(drop=True), y='y', group='id_student',
        features=features, tests=AUC_TESTS, immutable_extra=[],
        engagement=['sum_click'], stages=[1, 2, 3],
        # final_grade = 0.25 * sum(tests); pass iff final_grade > 15.0
        policy_weights={t: 0.25 for t in AUC_TESTS}, tau=15.001,
        tau_sweep=[12.5, 15.001, 16.0, 17.0],
        test_ub=lambda row: dict(ub), click_hi=lambda row: hi,
        policy_desc='0.25 * sum(assignment marks) > 15 (the rule that generated the label)')


# -------------------------------------------------------------- HarvardX
HX_ACTION = ['nevents', 'ndays_act', 'nchapters']   # nplay_video / nforum_posts are constant 0


def load_harvardx():
    h = pd.read_csv(f'{DATA}/HarvardX/harvardx-cs250.csv')
    h['y'] = h['certified'].astype(int)
    h[HX_ACTION] = h[HX_ACTION].astype(float)
    hi = h[HX_ACTION].quantile(0.99)
    return Config(
        name='HarvardX', df=h.reset_index(drop=True), y='y', group='userid',
        features=HX_ACTION, tests=[], immutable_extra=[], engagement=HX_ACTION,
        stages=[0], policy_weights=None, tau=None, tau_sweep=[],
        test_ub=lambda row: {}, click_hi=None, hx_hi={k: float(v) for k, v in hi.items()},
        policy_desc='no institutional grading rule exists; policy criterion not applicable')


LOADERS = {'OULAD': load_oulad, 'AUC': load_auc, 'HarvardX': load_harvardx}
