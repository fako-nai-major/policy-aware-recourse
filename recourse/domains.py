"""Domain definitions for the v2 driver.

A domain supplies the data, the outcome model's features, the query cohort
(optionally staged), the per-query specification (actionable features, DiCE
search range, gate bounds) and the policy.  The education domains wrap the v1
configuration in datasets.py unchanged, so v1 results are reproduced exactly.
"""
import numpy as np
from datasets import LOADERS
import prescriptive as P
from recourse.core import Constraint, Policy, Spec


class Domain:
    name = None
    stages = [0]
    tau_sweep = []

    # --- to implement
    def load(self): ...
    def stage(self, k, dte):
        """Return (stage model features or None, partial query matrix, at_risk mask)."""
        raise NotImplementedError
    def spec(self, row, k, regime):
        """Return (Spec, dice_range dict, dice actionable list) or None if nothing is actionable."""
        raise NotImplementedError
    def policy(self, tau=None):
        raise NotImplementedError
    def extra(self, row):
        return {}


class Education(Domain):
    """OULAD / AUC / HarvardX exactly as in v1 (datasets.py + prescriptive.query_spec)."""

    def __init__(self, name):
        self.name = name

    def load(self):
        self.cfg = cfg = LOADERS[self.name]()
        self.df, self.y, self.group, self.features = cfg.df, cfg.y, cfg.group, list(cfg.features)
        self.stages = cfg.stages
        self.tau_sweep = cfg.tau_sweep
        return self

    def stage(self, k, dte, f_model, dtr, cat):
        cfg = self.cfg
        if k:
            sf = cfg.tests[:k] + list(cfg.immutable_extra)
            g_k = cat.fit(dtr[sf], dtr[cfg.y])
            partial = dte[cfg.features].copy()
            partial[cfg.tests[k:]] = 0.0
            at_risk = g_k.predict_proba(dte[sf])[:, 1] < 0.5
        else:
            partial = dte[cfg.features].copy()
            at_risk = np.ones(len(dte), bool)
        return partial, at_risk

    def spec(self, row, k, regime):
        act, imm, dice_rng, gate_b = P.query_spec(self.cfg, row, k, regime)
        if not act:
            return None
        return Spec(self.features, act, imm, gate_b), dice_rng, act

    def policy(self, tau=None):
        if self.cfg.policy_weights is None:
            return Policy([])
        return Policy([Constraint(dict(self.cfg.policy_weights), '>=', self.cfg.tau if tau is None else tau,
                                  name='coursework' if self.name == 'OULAD' else 'grade')])

    def extra(self, row):
        return dict(learner=row[self.group], module=row.get('code_module', ''))


DOMAINS = {n: (lambda n=n: Education(n)) for n in ['OULAD', 'AUC', 'HarvardX']}


# ---------------------------------------------------------------- generic tabular domains
class Tabular(Domain):
    """Single-stage domain from a declarative config.

    config keys
      name, path (CSV under DATA), y (binary outcome, 1 = desired), group (entity id or None),
      features (model inputs), prepare (callable df -> df, optional),
      actionable: {feature: dict(direction='increase'|'decrease'|'both', lo=..., hi=...)}
                  lo/hi are absolute plausibility limits; the per-query bounds are
                  [x0, hi] (increase), [lo, x0] (decrease) or [lo, hi] (both).
      policy: list of dict(weights={f: w}, op='>='|'<=', tau=..., name=...)
      tau_sweep: optional list of primary-constraint thresholds
    Queries are held-out entities that f predicts as undesired (class 0).
    """

    def __init__(self, config):
        self.c = config
        self.name = config['name']

    def load(self):
        import os, pandas as pd
        from datasets import DATA
        df = pd.read_csv(os.path.join(DATA, self.c['path']))
        if self.c.get('prepare'):
            df = self.c['prepare'](df)
        if not self.c.get('group'):
            df['_id'] = range(len(df))
        self.df = df.reset_index(drop=True)
        self.y, self.group = self.c['y'], self.c.get('group') or '_id'
        self.features = list(self.c['features'])
        self.stages = [0]
        self.tau_sweep = list(self.c.get('tau_sweep', []))
        return self

    def stage(self, k, dte, f_model, dtr, cat):
        return dte[self.features].copy(), np.ones(len(dte), bool)

    def spec(self, row, k, regime):
        act, gate_b = [], {}
        for f, a in self.c['actionable'].items():
            x = float(row[f]); lo, hi = float(a['lo']), float(a['hi'])
            d = a.get('direction', 'both')
            lb, ub = (x, max(x, hi)) if d == 'increase' else (min(x, lo), x) if d == 'decrease' else (min(x, lo), max(x, hi))
            if ub - lb > 1e-9:
                act.append(f); gate_b[f] = (lb, ub)
        if not act:
            return None
        imm = [f for f in self.features if f not in act]
        return Spec(self.features, act, imm, gate_b), {f: list(gate_b[f]) for f in act}, act

    def policy(self, tau=None):
        cons = [Constraint(dict(p['weights']), p['op'], p['tau'], p.get('name', 'policy')) for p in self.c['policy']]
        if tau is not None and cons:
            cons[0] = Constraint(cons[0].weights, cons[0].op, tau, cons[0].name)
        return Policy(cons)


def register(config):
    DOMAINS[config['name']] = lambda c=config: Tabular(c)
