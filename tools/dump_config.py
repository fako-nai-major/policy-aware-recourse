"""Write configs/experiment_config.json from the code that ran the experiments.

The JSON is generated, not hand-written, so it cannot drift from the code:
dataset definitions and bounds come from datasets.py, objective weights and
bound regimes from prescriptive.py, classifier settings from predictive.py,
and baseline settings from external_baselines.py.

Usage (from the repository root):  python tools/dump_config.py
Datasets whose files are not present under data/ are skipped with a note.
"""
import inspect, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import datasets
import prescriptive as P
import predictive
import external_baselines as E

ROUND = lambda v: round(float(v), 4)


def dataset_block(name):
    try:
        cfg = datasets.LOADERS[name]()
    except FileNotFoundError as e:
        return {'note': f'data file not found ({e.filename}); see data/README.md'}
    df = cfg.df
    out = dict(records=int(len(df)), learners=int(df[cfg.group].nunique()), outcome=cfg.y,
               pass_rate=ROUND(df[cfg.y].mean()), group_key=cfg.group, features=list(cfg.features),
               assessments=list(cfg.tests), immutable_extra=list(cfg.immutable_extra),
               engagement_increase_only=list(cfg.engagement), stages=list(cfg.stages),
               policy=dict(description=cfg.policy_desc, weights=cfg.policy_weights, threshold=cfg.tau,
                           threshold_sweep=list(cfg.tau_sweep)))
    if name == 'OULAD':
        mods = sorted(df.code_module.unique())
        out['modules'] = mods
        out['assessment_weights_by_presentation'] = {
            f'{m} {pr}': {t: ROUND(v) for t, v in cfg.test_ub(g.iloc[0]).items() if v > 0}
            for (m, pr), g in df.groupby(['code_module', 'code_presentation'])}
        out['sum_click_upper_bound_by_module'] = {m: ROUND(cfg.click_hi(df[df.code_module == m].iloc[0])) for m in mods}
    elif name == 'AUC':
        out['assessment_upper_bounds'] = {t: ROUND(v) for t, v in cfg.test_ub(df.iloc[0]).items()}
        out['sum_click_upper_bound'] = ROUND(cfg.click_hi(df.iloc[0]))
    else:
        out['engagement_upper_bounds'] = {k: ROUND(v) for k, v in cfg.hx_hi.items()}
    return out


def init_defaults(cls):
    sig = inspect.signature(cls.__init__)
    return {k: v.default for k, v in sig.parameters.items() if v.default is not inspect._empty}


cfg = dict(
    generated_by='tools/dump_config.py',
    splits=dict(predictive='StratifiedGroupKFold(n_splits=5, shuffle=True, random_state=0) on the learner key',
                prescriptive='GroupShuffleSplit(test_size=0.2) on the learner key, random_state = seed'),
    seeds=dict(AUC=list(range(10)), OULAD=list(range(5)), HarvardX=list(range(5))),
    max_queries_per_stage_and_seed=dict(AUC=None, OULAD=300, HarvardX=400),
    classifiers=dict(models=list(predictive.model_zoo(0).keys()), samplers=['none', 'smote', 'nearmiss'],
                     resampling='training folds only',
                     outcome_and_early_warning_model='CatBoostClassifier(iterations=500, random_seed=seed)',
                     at_risk_rule='predicted pass probability < 0.5'),
    dice=dict(method='random', total_CFs=10, desired_class=1, backend='sklearn',
              random_seed='seed * 100003 + query index'),
    objective_weights=P.LAMBDA,
    objective_weight_variants={k: v for k, v in P.lam_variants().items()},
    bounded_completion=dict(grid='10 evenly spaced values in [lb, ub]', applies_to='actionable features equal to 0'),
    bound_regimes=dict(floor_fraction=P.FLOOR,
                       aligned='DiCE range = gate bounds = [0, w]',
                       floor=f'DiCE range = gate bounds = [{P.FLOOR}w, w]',
                       mismatch=f'DiCE range = [0, w]; gate and completion bounds = [{P.FLOOR}w, w]'),
    acceptance_gate=['policy score >= threshold', 'fresh prediction of f = pass', 'actionable features within bounds',
                     'non-actionable features unchanged'],
    external_baselines=dict(
        NICE=dict(package='NICEx 0.2.3', optimization='sparsity', justified_cf=True),
        MCCE=dict(package='mccepy @63e4fa3 (patches/mccepy-pandas2.patch)', **{k: v for k, v in init_defaults(E.MCCERunner).items() if k != 'seed'}) if hasattr(E, 'MCCERunner') else {},
        CARE=dict(package='CARE @811ff09', **init_defaults(E.CARERunner)) if hasattr(E, 'CARERunner') else {},
        care_queries_per_seed=100, snap_tolerance='1e-6 * max(1, |x0|)'),
    datasets={n: dataset_block(n) for n in ['OULAD', 'AUC', 'HarvardX']},
)
os.makedirs('configs', exist_ok=True)
json.dump(cfg, open('configs/experiment_config.json', 'w'), indent=2, default=str)
print('wrote configs/experiment_config.json')
