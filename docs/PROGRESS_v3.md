# Rule-verified recourse — v3 progress log

Status as of 25 Nov 2026. This file explains what has been run for the merged
"one strong paper" (target: Machine Learning, Springer), why, and what came out.
The IJAIED submission (IJAIE-D-26-00093) is still under review; nothing here may be
submitted elsewhere until that is resolved. OULAD results are reported; AUC data are not.

## 1. What the paper now claims

A recommendation is acceptable only if the **whole final vector** satisfies the
institution's rule Π, receives the favourable class from a fresh prediction of the model
f, stays within actionable bounds and leaves immutable features unchanged
(acceptable set A(x0)). v3 adds an **exact solver** that finds the cheapest member of
A(x0) — or certifies that A(x0) is empty — for logistic regression, random forests and
CatBoost, and compares it with every practical alternative under one shared gate.

## 2. Pipeline

| Step | Script | What it does |
|---|---|---|
| Pilot | `pilot/pilot_exact*.py` | Go/no-go: could an open-source MILP (HiGHS) solve the exact problem fast enough? Result: go. |
| Main runs | `experiment_v3.py`, `run_v3.sh` | Per domain × model × seed: train model, draw unfavourable held-out queries, run all conditions, gate every output. Per-query checkpoints (container restarts). |
| DACE / MACE | `ext_dace_mace.py`, `run_ext_v3.sh` | External baselines on the same queries, native and with the rule built into their own optimisation problem (`dace_rule`, `mace_rule`). |
| Exact re-run | `rerun_exact.py` (+ `--fix`) | Recomputed every exact row after the solver fixes (highspy, integrality tol 1e-9; verified snapping). |
| OCEAN re-run | `rerun_ocean.py`, `run_ocean.sh` | Re-ran OCEAN on all RF files and added the fairer completion variant (`ocean_joint_free`). |
| Tables | `analyze_v3.py` | `results_v3/tables/`: yield, exact solver stats, cost gap to exact, paired McNemar tests (Holm), rejection reasons. |
| Tests | `tests/test_exact.py` | Brute-force check of the MILP against a grid for lr/rf/cat × AND/OR rules, structural links and certified infeasibility. 0 failures. |

### Domains (rules)
* **HMDA** lending: DTI ≤ 50 and CLTV ≤ 97.
* **HMDA_OR**: CLTV ≤ 97 and (DTI ≤ 45 or (DTI ≤ 50 and CLTV ≤ 80)) — disjunctive (illustrative).
* **HMDA_S**: structural lending — loan amount in $k, CLTV tied to the loan exactly, DTI tied to the mortgage payment at 6.5 %.
* **PIMA**: clinical-threshold rule.
* **OULAD**: education rule (assessment floor), two regimes — *aligned* (rule and model agree) and *floor* (rule stricter than the model); staged queries.

### Models
Standardised logistic regression (lr), random forest (100 trees, depth 8; rf), CatBoost (500 iterations; cat), and a ReLU network (two hidden layers of 20, early stopping; mlp). 5 seeds on lending/Pima; OULAD 3 seeds (RF baselines DACE/MACE: seed 0 only because of run time).

### Conditions compared (all judged by the same gate)
| Condition | Meaning |
|---|---|
| `dice_first` | First DiCE counterfactual, no rule awareness |
| `posthoc_full_gate` | First DiCE candidate that passes the gate (filter) |
| `framework` | v2 framework: rank DiCE pool, joint completion, gate |
| `repair` / `repair_esc` | Rule-only minimum-change repair; with escalation of the rule margin until f agrees |
| `repair_sparse0` / `repair_sparse` | Rule-only MILP (effort + sparsity, no model); with escalation |
| `exact` | MILP optimum of effort + 0.5·sparsity over A(x0); time limit 120 s (60 s OULAD) |
| `ocean` / `ocean_joint` / `ocean_joint_free` | OCEAN (RF only); + v2 completion of untouched features; + completion that may also move rule features OCEAN already changed |
| `dace`, `dace_rule`, `mace`, `mace_rule` | External baselines, native and with the rule added to their own problem |

## 3. Results (final, 104 result files)

### Exact solver
* 100 % yield on lending and Pima; on OULAD it reaches the rule-attainable ceiling (95–97 %).
* Proven optimal on essentially every lending/Pima query (CatBoost/HMDA_S: 0.1–0.4 % certified infeasible). OULAD (after v3.1): lr 95 %; CatBoost 96 % (aligned) / 95 % (floor); RF 92 % / 80 %; the rest of the solvable queries hit the 60 s limit and are reported as best-found.
* Median time < 1 s on lending/Pima; 9–17 s on OULAD tree models; lr is instantaneous.

### Accepted yield (%) — highlights
| Domain, model | DiCE first | Gate filter | Framework | Repair+esc | Exact |
|---|---|---|---|---|---|
| HMDA rf | 89 | 100 | 100 | 100 | 100 |
| HMDA_S rf | 31 | 89 | 99.6 | 99.6 | 99.6 |
| PIMA rf | 45 | 98 | 100 | 100 | 100 |
| OULAD rf aligned | 53 | 92 | 96.7 | 95.6 | 96.7 |
| OULAD rf floor | 14 | 28 | 96.7 | 95.6 | 96.7 |

### Cost above the exact optimum (queries both accept)
| Method | Lending | Pima | OULAD |
|---|---|---|---|
| Framework | 21–31 % | 28–32 % | 10–15 % |
| Repair + escalation | 0–2 % (optimal on 96–100 %) | 7–13 % | 3–24 % |
| Gate filter | 39–117 % | 55–65 % | 19–30 % |
| MACE + rule | 0–22 % | 8–16 % | 42–65 % |
| DACE + rule | 0–40 % | 40–54 % | 32 % (lr) |

### External baselines
* DACE / MACE in their native form almost never produce rule-compliant recourse (~0 % lending, 5–13 % Pima).
* With the rule added: MACE 97–100 % (OULAD RF 67 %); DACE 52–92 % on lending/Pima, 0 % on OULAD RF.
* Paired tests: exact beats DACE + rule by +32 pp (HMDA RF), +48 pp (Pima RF), +95 pp (OULAD RF).

### OCEAN (RF only) — the fairer variant
| Domain | OCEAN | + completion | + completion incl. rule features | Exact | Cost above exact (fair variant) |
|---|---|---|---|---|---|
| HMDA | 0.1 | 2.2 | 100 | 100 | 3 % |
| HMDA_OR | 0.2 | 2.4 | 100 | 100 | 3 % |
| HMDA_S | 0.0 | 3.5 | 99.5 | 99.6 | 0 % |
| PIMA | 16.6 | 49.9 | 98.4 | 100 | 22 % |
| OULAD aligned | 11.1 | 62.2 | 96.7 | 96.7 | 58 % |
| OULAD floor | 7.2 | 85.6 | 96.7 | 96.7 | 8 % |

Reading: OCEAN alone cannot see the rule. Given generous completion it reaches the
acceptable set, but pays a cost premium on the harder domains, and it is limited to
scikit-learn random forests; the exact solver covers lr, rf and CatBoost with the
optimum or a certificate.

### ReLU network (added 26 Nov)
Encoded exactly with big-M ReLU rows and per-query interval bounds (THEORY §2); ~36–40 binaries, so the
exact solver is fast (median 0.02–0.3 s; max 9 s) and proves optimality on every query that has a solution.

| Domain | DiCE first | Gate filter | Framework | Repair+esc | Exact | Cost above exact: framework / repair+esc |
|---|---|---|---|---|---|---|
| HMDA | 78 | 100 | 100 | 100 | 100 | 25 % / 0 % |
| HMDA_OR | 72 | 100 | 100 | 100 | 100 | 24 % / 1 % |
| HMDA_S | 29 | 87 | 100 | 100 | 100 | 28 % / 0 % |
| PIMA | 46 | 89 | 98.1 | 91.8 | 98.5 | 28 % / 11 % |
| OULAD aligned | 54 | 93 | 96.7 | 94.0 | 96.7 | 13 % / 19 % |
| OULAD floor | 14 | 27 | 96.7 | 94.0 | 96.7 | 15 % / 5 % |

Exact beats repair+escalation on Pima (+5.5 pp, p_Holm = 0.003) and the gate filter on HMDA_S (+13 pp) and
OULAD floor (+70 pp). Price of compliance: +26–39 % on lending, +70 % on Pima. Caveat: Pima has ~580 training
rows; the network is weaker than logistic regression there (accuracy 0.62–0.80 vs 0.70–0.81) and on seed 1 it
predicts every record favourable, so that seed has no queries. HMDA and OULAD accuracy matches the other models.

### Standard benchmarks: Adult and Give Me Some Credit (added 26 Nov)
Data: the CARLA versions (Pawelczyk et al., 2021; github.com/carla-recourse/cf-data; missing values removed,
categoricals binarised, outcome 1 = desired). The UCI/OpenML hosts are blocked from the workspace.
* **Adult** (employment; policy scenario): weekly hours ≤ 48 (EU Working Time Directive 2003/88/EC, Art. 6(b)).
  Actions: up to 4 more years of education, change of weekly hours (1–99). 5 seeds × 200 queries × lr/rf/cat/mlp.
* **GMSC** (consumer credit): debt-to-income ≤ 0.43 (CFPB Ability-to-Repay / Qualified Mortgage rule,
  12 CFR 1026.43(e)(2)(vi), in force 2014–2021). Actions: lower debt ratio, revolving utilisation and number of open
  credit lines. 5 seeds × 200 queries (rf: 50 queries, 120 s limit).
* DACE / MACE: lr and rf, 20 queries per seed (Adult 3 seeds; GMSC lr 3 seeds, rf seed 0).

| Accepted yield (%) | DiCE first | Gate filter | Framework | Repair+esc | OCEAN+compl.(free) | DACE+rule | MACE+rule | Exact |
|---|---|---|---|---|---|---|---|---|
| Adult lr | 4 | 18.5 | 18.7 | 0 | – | 18 | 33 | 29.1 |
| Adult rf | 7 | 26.9 | 27.1 | 0.2 | 27.8 | 20 | 32 | 29.7 |
| Adult cat / mlp | 10 / 8 | 26 / 26 | 27 / 26 | 1 / 0 | – | – | – | 30.7 / 31.0 |
| GMSC lr | 52 | 77 | 80.6 | 4 | – | 70 | 80 | 80.9 |
| GMSC rf | 75 | 98.0 | 98.4 | 61 | 97.6 | 0 | 50 | 98.8 |
| GMSC cat / mlp | 76 / 47 | 97 / 61 | 98.0 / 62.2 | 57 / 23 | – | – | – | 98.5 / 62.6 |

(DACE/MACE on 60 Adult and 20–60 GMSC queries, so their yields are noisy; MACE+rule never beats exact on a
matched query, McNemar "only baseline" = 0.)

* **Exact solver**: proven optimal or certified infeasible on every Adult and GMSC query (no time limits; median
  0.01–0.9 s, GMSC rf 26 s). Cost above exact: framework 31–57 %, gate filter 44–128 %, repair+escalation 1–23 %,
  OCEAN+completion 3 % (Adult) / 29 % (GMSC), MACE+rule 11–72 %, DACE+rule 5–54 %.
* **Adult abstentions** (≈70 % of queries) are certified: no vector within the action limits is accepted. Without the
  48-hour cap, recourse would exist for an extra 8–29 % of queries (lr 28.5 %, cat 13.5 %, mlp 8.1 %, rf 0.5 %) — the
  price of the rule in *access*; for the rest, more hours or education within the limits is not enough for the model.
  Repair is useless here (the rule rarely binds; it only touches hours).
* **GMSC**: the rule never removes recourse (lowering debt also helps the model); price of compliance in cost
  +14–33 %. Exact beats repair+escalation by 38–77 pp and DACE+rule by 100 pp on rf.

### v3.1 correction (26 Nov): split margin of the tree encoding
The tree encoding required a fixed gap of 1e-4 on the strict side of every split. On GMSC, many random-forest
thresholds lie closer together (or closer to 0) than that, which excluded real actions; the sanity check found 433
tree-model rows where a heuristic beat a "proven" optimum and one false infeasibility. The margin is now a few float32
ulps (THEORY §2). All random-forest and CatBoost exact rows (all domains) and their bounds were recomputed: optimal
costs and yields are unchanged on HMDA, HMDA_OR, HMDA_S, Pima and OULAD and on Adult (2 rows 0.001 cheaper); only
GMSC changed (exact yield on rf 79.6 % → 98.8 %, no time limits). After the correction all integrity checks pass on all
domains. OULAD time-limited rows were re-solved without CPU contention.

## 4. Integrity checks (all pass)
* Exact is never infeasible where another method found an accepted vector.
* Nothing is cheaper than a proven exact optimum (tolerance 1e-3).
* No optimal exact solution is rejected by the gate.
* After v3.1 (all 179 files, 20,812 queries, 7 domains, 4 models): 63 rows on 19 time-limited OULAD queries were beaten by another method → reported as best-found, not optimal. No method ever accepted a query that exact rejected (McNemar "only baseline" = 0 in every comparison).
* OCEAN reproducibility: identical across runs except 3 OULAD queries where OCEAN's CP-SAT hit its 60 s limit (net yield change: one query).

## 5. Problems met and how they were fixed (for the methods section / reproducibility)
* **Solver tolerance**: HiGHS' default integrality tolerance let big-M rows move features "for free"; one OULAD query looked cheaper than the optimum. Fixed: highspy with tolerance 1e-9, all exact rows re-run.
* **Snapping round-off** broke structural links / the LR score on 177 rows. Fixed: snap only if the rule, links and parsed model still hold; re-solved those rows.
* **Rule tolerance**: rule rows tightened by 1e-6·max(1,|τ|) so solver round-off cannot land just below a threshold.
* **DACE memory** on HMDA: stratified 2,000-row training subsample. **DACE hang**: hard per-call timeout.
* Library pins: PuLP 2.9.0, NumPy-2 alias shim for MACE, separate `utils` namespaces for DACE/MACE.
* Container restarts: per-query checkpoints, resumable scripts, keep-alive reminders.

## 6. Files
* Results: `results_v3/v3_<domain>_<model>_s<seed>.csv.gz` (our methods + OCEAN), `results_v3/v3x_*` (DACE/MACE).
* Tables: `results_v3/tables/summary_v3.md` and CSVs.
* Backups of earlier states: `results_v3_before_rerun_exact/`, `results_v3_before_fix/`, `results_v3_before_ocean/` (cloud workspace).

## 7. Next (weeks 4–5 onward)
1. ~~Theory~~ — done: `docs/THEORY_v3.md` (soundness, ε-completeness / certified abstention, lower bounds and price of compliance, escalation theorem), verified on all 9,911 queries (`verify_bounds.py`, `analyze_bounds.py`, tables `theory_checks_v3.md` etc.).
1b. ~~Sparsity-aware repair~~ — tested (`exact.repair_sparse`, `add_repair_sparse.py`): no real gain; OULAD rule optima are degenerate (ties) and only the model can pick the acceptable one (THEORY §8).
2. ~~A neural-network model~~ — done (ReLU MLP; see §3).
3. ~~Standard benchmarks~~ — done: Adult and Give Me Some Credit (§3).
4. Writing the Machine Learning manuscript.
