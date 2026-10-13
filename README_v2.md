# Version 2: domain-agnostic policy-aware recourse

Branch `v2` adds a domain-agnostic core next to the v1 code. The v1 scripts (`prescriptive.py`, `analyze.py`, …) are unchanged and still reproduce the published results.

## What is new

| Component | v1 | v2 (`recourse/core.py`) |
|---|---|---|
| Policy | one weighted sum of assessment marks ≥ τ | any list of linear constraints `Σ w_j x_j ≥ τ` or `≤ τ` (e.g. debt-to-income ≤ 50 and loan-to-value ≤ 97) |
| Completion | fills actionable features equal to 0 with the cheapest of 10 grid values that meets the policy on its own (`complete_grid`, kept for comparison) | `complete_joint`: moves the actionable features the candidate left unchanged (and any out-of-bounds feature) jointly, at minimum normalised change, into their bounds and onto the policy (a small linear program), raising the target in steps until the outcome model agrees |
| Gate | coursework threshold, prediction, bounds, immutables | the same four checks for any policy; failed constraints are named in the reasons |
| Direct repair | greedy fill of assessment marks | exact v1 greedy for one `≥` constraint, linear program otherwise |
| Domains | education only | `recourse/domains.py`: the three education domains (wrapping v1 exactly) and a declarative `Tabular` domain for any single-stage dataset |

`experiment.py` runs every v1 condition plus two new ones:

- `rank_joint`: ranking with joint completion;
- `rank_joint_fallback`: the same tried over the ranked pool until the gate passes.

## Verified

- **Exact reproduction of v1:** every per-query result of v1 is reproduced exactly (AUC seed 0: 30,657 rows; HarvardX seed 0: 6,000 rows; identical acceptance, selected vector and rejection reasons).
- **Floor bounds (OULAD, seed 0, 180-query sample):** joint completion removes the floor-bounds weakness. Grid completion is accepted for 87.8% of queries (88.9% with fallback); joint completion for 94.4% (95.0% with fallback), the same as with aligned bounds.
- **Generic domain:** `tests/test_tabular.py` runs the generic domain with a two-constraint `≤` policy on synthetic data. This is a smoke test, not a result.

## Adding a domain

```python
from recourse.domains import register
register(dict(
    name='HMDA', path='HMDA/hmda.csv', y='approved', group=None,
    features=['income', 'loan_amount', 'dti', 'cltv', ...],
    actionable=dict(dti=dict(direction='decrease', lo=10, hi=70),
                    cltv=dict(direction='decrease', lo=50, hi=105)),
    policy=[dict(weights={'dti': 1}, op='<=', tau=50, name='dti'),
            dict(weights={'cltv': 1}, op='<=', tau=97, name='cltv')]))
```

Then run `python experiment.py HMDA --seeds 0,1,2,3,4 --regimes aligned`. Bounds per query are `[x0, hi]` for features that may only increase, `[lo, x0]` for those that may only decrease, and `[lo, hi]` otherwise.

## New domains (v2 branch)

| Domain | Data | Rule | Queries |
|---|---|---|---|
| Lending | HMDA 2025, Virginia, conventional first-lien home purchases (`tools/prepare_hmda.py`) | DTI ≤ 50% (Fannie Mae Selling Guide B3-6-02, DU); combined LTV ≤ 97%; DTI also tested at 43 and 45 | 1,301 predicted denials, 5 seeds |
| Health | Pima Indians Diabetes, original NIDDK file (`data/PIMA/diabetes.csv`); rows with missing glucose, blood pressure or BMI removed, insulin and skin thickness dropped | 2-h OGTT glucose < 140 mg/dL (ADA normal range) and BMI < 30; glucose also tested at < 126 | 461 predicted onsets, 10 seeds |

Run them with `python experiment.py HMDA --seeds 0,1,2,3,4 --regimes aligned --max_q 400` and `python experiment.py PIMA --seeds 0,1,2,3,4,5,6,7,8,9 --regimes aligned`. Results are in `results_v2/`.

## Full v2 runs (all five domains)

| Script | What it does |
|---|---|
| `run_edu.sh` | v2 prescriptive runs for OULAD (5 seeds, ≤300 queries per stage), AUC (10 seeds) and HarvardX (5 seeds, 400 queries) |
| `ext_joint_education.py v1ext/` | adds the `bounded+joint` variant to the v1 NICE/MCCE/CARE outputs of the education domains (from their stored vectors; v1 verdicts kept) |
| `run_ext.sh` | NICE, MCCE (all queries) and CARE (100 queries, seeds 0–2) for HMDA and Pima via `external_v2.py` |
| `analyze_v2.py` | cross-domain tables in `results_v2/tables/` (`summary_v2.md`) |

Accepted yield at the primary threshold (%, mean ± SD over seeds):

| Domain | DiCE first | DiCE + full-gate filter | Framework v2 + fallback | Direct repair + escalation |
|---|---|---|---|---|
| OULAD (aligned) | 34.5 ± 3.6 | 70.7 ± 6.5 | 95.8 ± 0.6 | 91.2 ± 2.0 |
| OULAD (floor) | 7.7 ± 1.1 | 20.6 ± 2.2 | 95.8 ± 0.6 | 91.2 ± 2.0 |
| AUC | 28.0 ± 3.8 | 37.3 ± 2.9 | 66.3 ± 4.4 | 65.9 ± 4.3 |
| HMDA | 86.2 ± 2.7 | 99.9 ± 0.2 | 99.9 ± 0.2 | 99.8 ± 0.2 |
| Pima | 45.3 ± 4.4 | 95.9 ± 1.9 | 100.0 ± 0.0 | 100.0 ± 0.0 |
| HarvardX (no rule) | 98.5 ± 0.4 | 99.9 ± 0.1 | 99.9 ± 0.1 | – |
