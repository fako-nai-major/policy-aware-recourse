"""Add the v2 'bounded+joint' variant to the v1 external-baseline results of the
education domains without re-running NICE, MCCE or CARE.

The v1 runs stored every returned vector.  For each 'bounded' vector this script
rebuilds the same outcome model f (same seed), the query and its bounds, applies
v2 joint completion and the v2 gate, and writes results_v2/ext_<ds>_<regime>_s<seed>[_care].csv
with the v1 rows (re-gated by the v2 gate) plus the new variant.

Usage:  python ext_joint_education.py path/to/v1_results_dir [more dirs ...]
"""
import sys, os, glob, json, re, warnings
import numpy as np, pandas as pd
from sklearn.model_selection import GroupShuffleSplit
import prescriptive as P
from recourse import core as C
from recourse.domains import DOMAINS

warnings.filterwarnings('ignore')


def unround(x, spec):
    """v1 stored vectors rounded to 6 decimals; restore values that the rounding moved
    just across a bound (|x - bound| <= 1e-6 * max(1, |bound|))."""
    for f in spec.actionable:
        for b in spec.bounds[f]:
            if abs(float(x[f]) - b) <= 1e-6 * max(1.0, abs(b)):
                x[f] = b
    return x


def process(path, out_dir='results_v2'):
    m = re.search(r'ext_(OULAD|AUC|HarvardX)_(aligned|floor)_s(\d+)(_care)?\.csv$', os.path.basename(path))
    if not m:
        return
    name, regime, seed, tag = m.group(1), m.group(2), int(m.group(3)), m.group(4) or ''
    dom = DOMAINS[name]().load(); df = dom.df
    tr, _ = next(GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=seed).split(df, df[dom.y], df[dom.group]))
    f = P.cat(seed).fit(df.iloc[tr][dom.features], df.iloc[tr][dom.y])
    predict = lambda x: f.predict(pd.DataFrame([x[dom.features].astype(float)]))[0]
    pol = dom.policy()
    v1 = pd.read_csv(path)
    rows = []
    for (k, q, meth), g in v1.groupby(['stage', 'query', 'method'], sort=False):
        row = df.loc[q]
        orig = row[dom.features].astype(float).copy()
        if k:
            orig[dom.cfg.tests[k:]] = 0.0
        spec = dom.spec(row, k, regime)[0]
        cands = {}
        for r in g.itertuples():
            cands[r.variant] = None if pd.isna(r.vector) else unround(pd.Series(json.loads(r.vector))[dom.features].astype(float), spec)
        b = cands.get('bounded')
        cands['bounded+joint'] = None if b is None else C.complete_joint(b, orig, spec, pol, predict)
        sec = g.seconds.iloc[0]
        v1rows = {r.variant: r for r in g.itertuples()}
        for var in ['native', 'bounded', 'bounded+edit', 'bounded+joint']:
            cand = cands.get(var)
            ok, reasons, sc = C.gate(cand, orig, spec, pol, predict)
            if var in v1rows:     # v1 variants: keep the v1 verdict on the exact (unrounded) vector
                r1 = v1rows[var]
                ok, reasons, sc = bool(r1.accepted), str(r1.reasons).split(';'), r1.policy_score
            rows.append(dict(dataset=name, seed=seed, regime=regime, stage=k, query=q, method=meth, variant=var,
                             condition=f'{meth}_{var}', accepted=int(ok), reasons=';'.join([x for x in reasons if x != 'OK']) or 'OK',
                             policy_score=sc, seconds=sec,
                             effort=C.effort(cand, orig, spec) if cand is not None else np.nan,
                             sparsity=C.sparsity(cand, orig, spec) if cand is not None else np.nan))
    out = pd.DataFrame(rows)
    # v2 gate must agree with v1 on the v1 variants
    chk = v1.merge(out, on=['stage', 'query', 'method', 'variant'], suffixes=('_v1', '_v2'))
    mism = int((chk.accepted_v1 != chk.accepted_v2).sum())
    os.makedirs(out_dir, exist_ok=True)
    out.to_csv(f'{out_dir}/ext_{name}_{regime}_s{seed}{tag}.csv', index=False)
    print(os.path.basename(path), 'rows', len(out), 'v1/v2 gate mismatches', mism, flush=True)


if __name__ == '__main__':
    for d in sys.argv[1:]:
        for p in sorted(glob.glob(os.path.join(d, 'ext_*.csv'))):
            process(p)
