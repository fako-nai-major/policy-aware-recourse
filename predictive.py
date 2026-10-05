"""RQ1: predictive evaluation of the early-warning and outcome models.

Protocol:
  * learner IDs, id_assessment and date fields are NOT features;
  * StratifiedGroupKFold on the learner ID (no learner in train and test);
  * resampling (SMOTE / NearMiss-3) is applied to the training fold only;
  * ROC-AUC is computed from scores (predict_proba / decision_function),
    not from hard labels;
  * features are scaled inside a Pipeline fitted on the training fold;
  * staged models only see assessments released by stage k.
"""
import sys, time, warnings
import numpy as np, pandas as pd
from sklearn.model_selection import StratifiedGroupKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, balanced_accuracy_score, f1_score, recall_score, precision_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (RandomForestClassifier, ExtraTreesClassifier, AdaBoostClassifier,
                              GradientBoostingClassifier)
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import RidgeClassifierCV, LogisticRegression
from sklearn.svm import SVC
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import NearMiss
from imblearn.pipeline import Pipeline
from xgboost import XGBClassifier
from catboost import CatBoostClassifier
from datasets import LOADERS

warnings.filterwarnings('ignore')


def model_zoo(seed):
    return {
        'NB': BernoulliNB(),
        'DT': DecisionTreeClassifier(random_state=seed),
        'XT': ExtraTreesClassifier(random_state=seed, n_jobs=2),
        'RF': RandomForestClassifier(random_state=seed, n_jobs=2),
        'MLP': MLPClassifier(random_state=seed, max_iter=500),
        'KNN': KNeighborsClassifier(),
        'Ridge': RidgeClassifierCV(),
        'LR': LogisticRegression(max_iter=2000),
        'SVC': SVC(random_state=seed),
        'ABC': AdaBoostClassifier(random_state=seed),
        'GBC': GradientBoostingClassifier(random_state=seed),
        'XGB': XGBClassifier(random_state=seed, eval_metric='logloss', verbosity=0, n_jobs=2),
        'CB': CatBoostClassifier(random_seed=seed, verbose=0, iterations=500, thread_count=2),
    }


def scores(est, X):
    if hasattr(est, 'predict_proba'):
        return est.predict_proba(X)[:, 1]
    return est.decision_function(X)


def stage_features(cfg, k):
    if k == 0 or k is None:
        return list(cfg.features)
    return cfg.tests[:k] + list(cfg.immutable_extra)


def run(name, n_splits=5, seed=0, samplers=('none', 'smote', 'nearmiss')):
    cfg = LOADERS[name]()
    df = cfg.df
    y = df[cfg.y].values
    g = df[cfg.group].values
    stages = [k for k in cfg.stages if k] + ['full']
    rows = []
    cv = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    folds = list(cv.split(df, y, g))
    for st in stages:
        feats = stage_features(cfg, None if st == 'full' else st)
        X = df[feats].values.astype(float)
        for smp in samplers:
            for mname in model_zoo(seed):
                t0 = time.time()
                for fi, (tr, te) in enumerate(folds):
                    steps = [('scale', StandardScaler())]
                    if smp == 'smote':
                        steps.append(('smp', SMOTE(random_state=seed)))
                    elif smp == 'nearmiss':
                        steps.append(('smp', NearMiss(version=3)))
                    steps.append(('clf', model_zoo(seed)[mname]))
                    pipe = Pipeline(steps)
                    try:
                        pipe.fit(X[tr], y[tr])
                    except Exception as ex:  # e.g. NearMiss failure on tiny folds
                        print('fit fail', name, st, smp, mname, ex, flush=True)
                        continue
                    s = scores(pipe, X[te]); p = pipe.predict(X[te])
                    rows.append(dict(dataset=name, stage=str(st), sampler=smp, model=mname, fold=fi,
                                     roc_auc=roc_auc_score(y[te], s),
                                     bal_acc=balanced_accuracy_score(y[te], p),
                                     f1_macro=f1_score(y[te], p, average='macro'),
                                     f1_fail=f1_score(y[te], p, pos_label=0),
                                     recall_fail=recall_score(y[te], p, pos_label=0),
                                     precision_fail=precision_score(y[te], p, pos_label=0, zero_division=0),
                                     n_test=len(te)))
                print(f'{name} stage={st} {smp} {mname} {time.time()-t0:.1f}s', flush=True)
        pd.DataFrame(rows).to_csv(f'results/predictive_{name}.csv', index=False)
    return pd.DataFrame(rows)


if __name__ == '__main__':
    for n in sys.argv[1:]:
        run(n)
