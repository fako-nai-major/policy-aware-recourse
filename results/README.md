# Results

All files are produced by the scripts in the repository root, with the seeds listed in `configs/experiment_config.json`.

## Predictive models: `predictive_<dataset>.csv`

One row per dataset × model input × resampling condition × classifier × fold. The columns are:

- `stage`: `1`–`3` for the early-warning models, `full` for the outcome model f;
- `sampler`: `none`, `smote` or `nearmiss`;
- `model`, `fold`;
- metrics: `roc_auc` (from scores), `bal_acc`, `f1_macro`, `f1_fail`, `recall_fail`, `precision_fail`, all with fail as the positive class at a 0.5 threshold;
- `n_test`.

## Query cohorts: `presc_<dataset>_s<seed>_cohort.csv`

One row per stage, with these columns:

- `n_test`: held-out records;
- `n_at_risk`: records flagged by the stage-k model g_k;
- `n_eligible`: records also predicted to fail by f with pending assessments coded 0;
- `n_evaluated`: eligible records after the per-stage cap;
- `true_fail_rate_eligible`.

## Framework and DiCE conditions: `presc_<dataset>_s<seed>_rows.csv.gz`

One row per query × bound regime × condition × policy threshold.

**Query columns**

| Column | Meaning |
|---|---|
| `dataset`, `seed`, `stage`, `regime` | Bound regime: `aligned`, `floor` or `mismatch` (HarvardX: aligned only) |
| `query` | Row index of the learner record in the loaded dataset |
| `learner` | Learner key (OULAD `id_student`; HarvardX `userid`; AUC pseudonymous code) |
| `module` | OULAD module (empty elsewhere) |
| `y_true` | True outcome (1 = pass) |
| `pool_size` | Number of DiCE candidates for this query and regime (0 = none) |
| `pool_policy_valid` | Share of pool candidates whose policy score reaches the primary threshold |

**Outcome columns**

| Column | Meaning |
|---|---|
| `condition` | Strategy (see below) |
| `tau` | Policy threshold used by the gate (`15.001` encodes "> 15" for AUC; empty for HarvardX) |
| `accepted` | 1 if the returned recommendation passes the complete acceptance gate |
| `reasons` | `OK`, or the gate's rejection reasons separated by `;`: `below_policy_threshold`, `classifier_target_not_met`, `out_of_bounds:<feature>`, `immutable_changed:<feature>`, `no_candidate` |
| `policy_score` | Policy score S(x) of the returned vector |
| `effort` | Normalised L1 change over actionable features, each divided by its bound range |
| `sparsity` | Number of actionable features changed |
| `sel` | Hash of the returned vector, used to detect when two conditions select the same recommendation |

**Conditions** (all DiCE conditions share one candidate pool per query and regime)

| Code | Paper label |
|---|---|
| `dice_first` | DiCE, first candidate |
| `posthoc_policy_filter` | DiCE, first candidate meeting the policy threshold |
| `posthoc_full_gate` | DiCE, first candidate passing the full gate |
| `rank_only` | Policy-aware ranking, no editing |
| `rank_edit` | Framework (ranking + bounded completion + gate) |
| `rank_edit_fallback` | Framework with fallback over the ranked pool |
| `audit:drop_<term>` | Framework with one objective term removed (`policy`, `feas`, `prox`, `spar`) |
| `audit:lp_<v>`, `audit:lx_<v>` | Framework with λ_policy or λ_prox set to `<v>` |
| `policy_repair` | Direct policy repair (no DiCE) |
| `policy_repair_escalate` | Direct policy repair with classifier escalation |

The direct-repair rows were recomputed after a floating-point fix. The repair now fills to τ + 1e-6, so a repaired score cannot fall just below τ through round-off. `prescriptive.py` contains the fix, so a fresh run reproduces these rows.

## External methods: `ext_<dataset>_<regime>_s<seed>[_care].csv`

These files share the query keys `dataset`, `seed`, `regime`, `stage` and `query` with the framework files, so rows can be matched. They have the outcome columns `accepted`, `reasons`, `policy_score`, `effort` and `sparsity` as above, plus:

- `method`;
- `variant`: `native`, `bounded` or `bounded+edit`;
- `condition`: `<method>_<variant>`;
- `seconds`: runtime per query;
- `vector`: the returned vector as JSON. It is removed from the AUC files.

Files ending in `_care` hold the CARE runs (100 queries per seed).

Before gating, differences of at most 1e-6·max(1, |x₀|) between a returned vector and the original are snapped back. This removes floating-point noise from scaling round-trips, which the gate would otherwise read as a changed fixed feature.

## Tables: `tables/`

| File | Content | Produced by |
|---|---|---|
| `predictive_all.csv`, `predictive_catboost.csv`, `predictive_friedman.csv` | Predictive performance (Table 4, Table S1) | `analyze.py` |
| `cohort.csv`, `pools.csv` | Query cohorts and DiCE pools (Table 5) | `analyze.py` |
| `ablation_yield.csv`, `yield_by_stage.csv`, `paired_tests.csv`, `paired_effort.csv`, `framework_rejections.csv`, `accepted_characteristics.csv` | Matched ablation (Table 6, Tables S2–S3) | `analyze.py` |
| `objective_audit.csv` | Objective audit and weight sensitivity (Table 7, Table S4) | `analyze.py` |
| `tau_sweep.csv` | Alternative thresholds (Table 8, Table S5) | `analyze.py` |
| `external_*.csv` | External methods: yields, paired tests, rejection reasons, runtime (Table 9) | `ext_analyze.py` |
| `fairness_*.csv` | Group-level audit (Table 10, Table S6) | `fairness.py` |
| `summary.md`, `external_summary.md`, `fairness_summary.md` | Readable versions of the above | as above |
| `supplementary/Table_S*.csv` | Supplementary Tables S1–S6 as typeset | `tools/supplementary_tables.py` |

Yields are mean ± SD over seeds, computed with every eligible query in the denominator. Paired comparisons use McNemar tests and learner-cluster bootstrap CIs, with Holm adjustment.
