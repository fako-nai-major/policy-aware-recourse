"""Smoke test of the generic Tabular domain with a two-constraint '<=' policy
(synthetic lending-style data; not a result)."""
import os, sys, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
rng = np.random.default_rng(0); n = 3000
income = rng.lognormal(4.3, 0.4, n); loan = income * rng.uniform(2, 6, n)
dti = np.clip(rng.normal(38, 10, n), 5, 70); cltv = np.clip(rng.normal(85, 10, n), 30, 105)
logit = 2.5 - 0.08 * (dti - 36) - 0.07 * (cltv - 80) + 0.3 * np.log(income / 70)
y = (rng.uniform(size=n) < 1 / (1 + np.exp(-logit))).astype(int)
d = os.environ.get('PAR_DATA', 'data'); os.makedirs(f'{d}/SYNTH', exist_ok=True)
pd.DataFrame(dict(income=income, loan=loan, dti=dti, cltv=cltv, y=y)).to_csv(f'{d}/SYNTH/synth.csv', index=False)
from recourse.domains import register
register(dict(name='SYNTH', path='SYNTH/synth.csv', y='y', group=None, features=['income', 'loan', 'dti', 'cltv'],
              actionable=dict(dti=dict(direction='decrease', lo=10, hi=70), cltv=dict(direction='decrease', lo=50, hi=105),
                              income=dict(direction='increase', lo=0, hi=400)),
              policy=[dict(weights={'dti': 1.0}, op='<=', tau=45.0, name='dti'), dict(weights={'cltv': 1.0}, op='<=', tau=97.0, name='cltv')]))
import experiment
experiment.run('SYNTH', 0, ['aligned'], 80, 'results_v2test/presc_SYNTH_s0', audits=True)
r = pd.read_csv('results_v2test/presc_SYNTH_s0_rows.csv.gz')
print(r.groupby('condition').accepted.mean().round(3).to_string())
print(r[r.accepted == 0].reasons.str.split(';').explode().value_counts().head(8).to_string())
