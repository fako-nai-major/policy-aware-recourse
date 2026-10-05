"""NICE, MCCE and CARE under the same models, query cohorts, bounds and hard gate.

Every method is run on the SAME frozen outcome model f, the SAME eligible
queries (read back from results/presc_<ds>_s<seed>_rows.csv.gz), and every
selected output passes through the unmodified PresAnEx hard gate with the
SAME bounds (query_spec) as the framework.

Variants
  <method>_native   : the method's own output with its own constraint handling.
  <method>_bounded  : the method given our bounds through its native mechanism
                      (MCCE: bound/immutability filtering of the samples before its
                      L0/L1 selection; CARE: ACTIONABILITY objective with
                      'fix' / [lb, ub] constraints; NICE has no constraint
                      mechanism, so its output is projected: immutables reset,
                      actionable features clipped to bounds).
  <method>_bounded+edit : the bounded output passed through the framework's
                      policy-aware selector with zero-feature editing (same code
                      as the framework), then the gate.
"""
import sys, time, argparse, warnings, io, contextlib, json
import os
# mccepy (@63e4fa3, patched for pandas >= 2) and CARE (@811ff09) are fetched by
# scripts/setup_external.sh into external/; override with MCCE_SRC / CARE_SRC.
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [os.environ.get('MCCE_SRC', os.path.join(_HERE, 'external', 'mccepy')),
                os.environ.get('CARE_SRC', os.path.join(_HERE, 'external', 'CARE'))]
import numpy as np, pandas as pd
from sklearn.model_selection import GroupShuffleSplit
from sklearn.preprocessing import MinMaxScaler
from datasets import LOADERS
import prescriptive as P

warnings.filterwarnings('ignore')


def cohort(name, seed, regime):
    rows = pd.read_csv(f'results/presc_{name}_s{seed}_rows.csv.gz',
                       usecols=['stage', 'regime', 'query', 'condition'])
    q = rows[(rows.regime == regime) & (rows.condition == 'dice_first')].drop_duplicates(['stage', 'query'])
    return list(q[['stage', 'query']].itertuples(index=False, name=None))


def snap(cfg, cand, orig):
    """Undo float round-off from scaling round-trips (e.g. 6.0 -> 6.0000000001) so the
    exact immutability check in the gate does not penalise a method for numerical noise."""
    if cand is None:
        return None
    x = cand.copy()
    for c in cfg.features:
        if abs(float(x[c]) - float(orig[c])) <= 1e-6 * max(1.0, abs(float(orig[c]))):
            x[c] = float(orig[c])
    return x


def project(cfg, cand, orig, act, gb):
    x = orig.copy()
    for a in act:
        x[a] = float(np.clip(float(cand[a]), gb[a][0], gb[a][1]))
    return x


# ------------------------------------------------------------------- NICE
class NiceRunner:
    def __init__(self, cfg, f, Xtr, ytr):
        from nice import NICE
        self.cfg = cfg
        self.exp = NICE(predict_fn=lambda X: f.predict_proba(pd.DataFrame(X, columns=cfg.features)),
                        X_train=Xtr.values, cat_feat=[], num_feat=list(range(len(cfg.features))),
                        y_train=ytr.values, optimization='sparsity', justified_cf=True)

    def run(self, orig, act, gb, k):
        cf = self.exp.explain(orig[self.cfg.features].values.reshape(1, -1).astype(float))
        native = pd.Series(np.asarray(cf).reshape(-1), index=self.cfg.features).astype(float)
        return native, project(self.cfg, native, orig, act, gb)


# ------------------------------------------------------------------- MCCE
class MinimalData:
    def __init__(self, cont, imm):
        self.continuous, self.categorical, self.immutables = cont, [], imm
        self.categorical_encoded, self.immutables_encoded = [], imm


class MCCERunner:
    """mccepy (Redelmeier et al., 2024) CART sampler; K samples per query."""

    def __init__(self, cfg, f, Xtr, K=1000, seed=0):
        self.cfg, self.f, self.Xtr, self.K, self.seed = cfg, f, Xtr.copy(), K, seed
        self.models = {}
        self.scale = (Xtr.max() - Xtr.min()).replace(0, 1.0)

    def _model(self, imm):
        from mcce.mcce import MCCE
        key = tuple(imm)
        if key not in self.models:
            df = self.Xtr.copy(); df['const__'] = 0.0
            imm_ = list(imm) + ['const__']
            cols = imm_ + [c for c in self.cfg.features if c not in imm_]
            df = df[cols]
            m = MCCE(dataset=MinimalData(list(df.columns), imm_), model=self.f, seed=self.seed)
            with contextlib.redirect_stdout(io.StringIO()):
                m.fit(df, {c: 'float' for c in df.columns})
            self.models[key] = (m, cols)
        return self.models[key]

    def run(self, orig, act, gb, k):
        # MCCE fixes the features that are immutable at this stage
        imm = [c for c in self.cfg.features if c not in act and c not in self.cfg.tests[k:]] if self.cfg.tests \
            else [c for c in self.cfg.features if c not in act]
        m, cols = self._model(imm)
        q = orig.copy(); q['const__'] = 0.0
        qf = pd.DataFrame([q[cols].values], columns=cols, index=[0])
        with contextlib.redirect_stdout(io.StringIO()):
            S = m.generate(qf, k=self.K)[cols]
        S = S[self.cfg.features].astype(float).reset_index(drop=True)
        pos = S[self.f.predict(S) == 1].drop_duplicates()

        def pick(D):
            if len(D) == 0:
                return None
            diff = (D - orig[self.cfg.features].values)
            l0 = (diff.abs() > 1e-9).sum(1)
            l1 = (diff.abs() / self.scale).sum(1)
            D = D.assign(l0=l0, l1=l1).sort_values(['l0', 'l1'], kind='stable')
            return D.iloc[0][self.cfg.features].astype(float)
        native = pick(pos)
        ok = np.ones(len(pos), bool)
        for c in self.cfg.features:
            if c in act:
                ok &= (pos[c].values >= gb[c][0] - 1e-9) & (pos[c].values <= gb[c][1] + 1e-9)
            else:
                ok &= np.isclose(pos[c].values, float(orig[c]))
        return native, pick(pos[ok])


# ------------------------------------------------------------------- CARE
class CARERunner:
    """Original CARE implementation (Rasouli & Yu), continuous features only."""

    def __init__(self, cfg, f, Xtr, ytr, soundness=True, n_population=200, n_generation=20):
        from care.care import CARE
        self.cfg, self.f = cfg, f
        n = len(cfg.features)
        scaler = MinMaxScaler().fit(Xtr.values)
        prec = [int(max(0, min(6, -np.floor(np.log10(np.min(np.diff(np.unique(Xtr[c].values)))
                                                      if Xtr[c].nunique() > 1 else 1.0)))))
                for c in cfg.features]
        self.ds = dict(name=cfg.name, feature_names=list(cfg.features), feature_width=np.ones(n),
                       continuous_indices=list(range(n)), discrete_indices=[],
                       continuous_availability=True, discrete_availability=False,
                       num_feature_scaler=scaler, ord_feature_encoder=None, ohe_feature_encoder=None,
                       len_continuous_ord=[0, n], len_discrete_ord=[n, n], len_continuous_ohe=[0, n],
                       len_discrete_ohe=[n, n], len_continuous_org=[0, n], len_discrete_org=[n, n],
                       continuous_precision=prec)
        self.scaler = scaler
        inv = lambda X: pd.DataFrame(scaler.inverse_transform(np.atleast_2d(X)), columns=cfg.features)
        self.pred = lambda X: f.predict(inv(X)).astype(int).ravel()
        self.proba = lambda X: f.predict_proba(inv(X))
        self.kw = dict(task='classification', predict_fn=self.pred, predict_proba_fn=self.proba,
                       SOUNDNESS=soundness, COHERENCY=False, n_cf=5,
                       n_population=n_population, n_generation=n_generation)
        self.Xtr_ord = scaler.transform(Xtr.values); self.ytr = ytr.values
        self.fitted = {}

    def _explainer(self, actionability):
        from care.care import CARE
        if actionability not in self.fitted:
            e = CARE(self.ds, ACTIONABILITY=actionability, **self.kw)
            with contextlib.redirect_stdout(io.StringIO()):
                e.fit(self.Xtr_ord, self.ytr)
            self.fitted[actionability] = e
        e = self.fitted[actionability]
        e.n_population = self.kw['n_population']   # CARE overwrites this when 'adaptive'
        return e

    def _explain(self, orig, prefs):
        x_ord = self.scaler.transform(orig[self.cfg.features].values.reshape(1, -1).astype(float)).ravel()
        e = self._explainer(prefs is not None)
        with contextlib.redirect_stdout(io.StringIO()):
            out = e.explain(x_ord, cf_class=1, user_preferences=prefs)
        cfs = out['cfs_ord']
        cf = self.scaler.inverse_transform(cfs.values[:1])[0]
        return pd.Series(cf, index=self.cfg.features).astype(float)

    def run(self, orig, act, gb, k):
        native = self._explain(orig, None)
        cons = [('fix' if c not in act else [gb[c][0], gb[c][1]]) for c in self.cfg.features]
        prefs = dict(constraint=cons, importance=[1] * len(cons))
        return native, self._explain(orig, prefs)


# ------------------------------------------------------------------- driver
def run(name, seed, regime, methods, max_q, care_q, out):
    cfg = LOADERS[name](); df = cfg.df
    tr, te = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(df, df[cfg.y], df[cfg.group]))
    dtr = df.iloc[tr]
    f = P.cat(seed).fit(dtr[cfg.features], dtr[cfg.y])
    w, tau = P.policy(cfg)
    Q = cohort(name, seed, regime)
    rng = np.random.RandomState(seed)
    if max_q and len(Q) > max_q:
        Q = [Q[i] for i in sorted(rng.choice(len(Q), max_q, replace=False))]
    care_set = set(Q[i] for i in sorted(np.random.RandomState(1000 + seed).choice(len(Q), min(care_q, len(Q)), replace=False)))
    runners = {}
    if 'NICE' in methods: runners['NICE'] = NiceRunner(cfg, f, dtr[cfg.features].astype(float), dtr[cfg.y])
    if 'MCCE' in methods: runners['MCCE'] = MCCERunner(cfg, f, dtr[cfg.features].astype(float), seed=seed)
    if 'CARE' in methods: runners['CARE'] = CARERunner(cfg, f, dtr[cfg.features].astype(float), dtr[cfg.y])
    rows = []
    t0 = time.time()
    for i, (k, q) in enumerate(Q):
        row = df.loc[q]
        orig = row[cfg.features].astype(float).copy()
        if cfg.tests and k:
            orig[cfg.tests[k:]] = 0.0
        act, imm, _, gb = P.query_spec(cfg, row, k, regime)
        for mname, r in runners.items():
            if mname == 'CARE' and (k, q) not in care_set:
                continue
            ts = time.time()
            try:
                native, bounded = r.run(orig, act, gb, k)
                native, bounded = snap(cfg, native, orig), snap(cfg, bounded, orig)
            except Exception as ex:
                native = bounded = None
                print('fail', mname, k, q, repr(ex)[:200], flush=True)
            el = time.time() - ts
            edited = None
            if bounded is not None:
                edited, _ = P.select(orig, pd.DataFrame([bounded[cfg.features]]), act, imm, w, tau, gb, True, P.LAMBDA)
            for var, cand in [('native', native), ('bounded', bounded), ('bounded+edit', edited)]:
                if cand is None:
                    ok, reasons, s = False, 'no_candidate', np.nan
                else:
                    ok, a = P.gate(cfg, f, cand, orig, act, gb, w, tau)
                    reasons, s = ';'.join(a['reasons']) or 'OK', a['policy_score']
                rows.append(dict(dataset=name, seed=seed, regime=regime, stage=k, query=q, method=mname,
                                 variant=var, condition=f'{mname}_{var}', accepted=int(ok), reasons=reasons,
                                 policy_score=s, seconds=el,
                                 effort=P.effort(cand, orig, act, gb) if cand is not None else np.nan,
                                 sparsity=P.sparsity(cand, orig, act) if cand is not None else np.nan,
                                 vector=None if cand is None else json.dumps({c: round(float(cand[c]), 6) for c in cfg.features})))
        if (i + 1) % 25 == 0:
            print(f'{name} s{seed} {regime} {i+1}/{len(Q)} {time.time()-t0:.0f}s', flush=True)
            pd.DataFrame(rows).to_csv(out, index=False)
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f'{name} s{seed} {regime} done {len(Q)} queries {time.time()-t0:.0f}s', flush=True)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('dataset'); ap.add_argument('--seeds', default='0'); ap.add_argument('--regime', default='aligned')
    ap.add_argument('--methods', default='NICE,MCCE,CARE'); ap.add_argument('--max_q', type=int, default=0)
    ap.add_argument('--care_q', type=int, default=100); ap.add_argument('--tag', default='')
    a = ap.parse_args()
    for s in [int(x) for x in a.seeds.split(',')]:
        run(a.dataset, s, a.regime, a.methods.split(','), a.max_q, a.care_q,
            f'results/ext_{a.dataset}_{a.regime}_s{s}{a.tag}.csv')
