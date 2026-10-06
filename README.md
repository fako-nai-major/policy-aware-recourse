# Policy-aware counterfactual recourse with verified acceptance

Code, configuration and per-query results for the paper

> Ako-Nai, F., de la Cal Marin, E., Tan, Q., & Soler Costa, R. *Policy-aware counterfactual recourse with verified acceptance for educational early warning.* Submitted to *Knowledge-Based Systems*.

The framework generates counterfactual candidates with DiCE. It selects one with an objective that includes an explicit institutional-policy penalty and completes pending assessments within configured bounds. It returns the recommendation only if a final gate confirms four things:

- the encoded pass rule is met;
- a fresh prediction is a pass;
- every actionable feature is within its bounds;
- fixed features are unchanged.

Otherwise it abstains. Algorithm 1 in the paper summarises the procedure.

## Repository layout

```
PresAnEx/                    framework module (selector, bounded completion, acceptance gate)
  fairness_aware_cf.py         policy-aware objective and select_best_counterfactual
  counterfactual_gate.py       apply_hard_gate (acceptance gate)
datasets.py                  dataset loaders, policies, thresholds and bounds (all configuration)
predictive.py                RQ1: 13 classifiers x 3 resampling conditions, learner-grouped 5-fold CV
prescriptive.py              RQ2: staged query cohorts, DiCE pools, ablation, objective audit, tau sweep, repair baselines
external_baselines.py        RQ3: NICE, MCCE and CARE under the same models, queries, bounds and gate
analyze.py                   tables for RQ1-RQ2 (results/tables)
ext_analyze.py               tables for the external baselines
fairness.py                  group-level audit on OULAD (needs OULAD studentInfo.csv)
configs/experiment_config.json  every setting used, generated from the code (tools/dump_config.py)
scripts/setup_external.sh    fetches mccepy and CARE at the pinned commits
scripts/run_all.sh           runs the complete pipeline in order
tools/                       dump_config.py (regenerates configs/), supplementary_tables.py (Tables S1-S6),
                             prepare_oulad.py and prepare_harvardx.py (build the OULAD and HarvardX inputs)
patches/                     one-line pandas-2 patch for mccepy
data/                        input data (see data/README.md)
results/                     per-query results and all tables (see results/README.md)
```

## Installation

Tested with Python 3.11 on Linux.

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
bash scripts/setup_external.sh      # only needed for external_baselines.py
```

## Data

The OULAD extract is included (CC BY 4.0). The HarvardX extract must be downloaded, and the AUC course data are institutional and not distributed. See [data/README.md](data/README.md). Set `PAR_DATA` to use a different data folder.

## Reproducing the results

Every table in the paper and the supplementary material can be rebuilt from the per-query results in `results/` without re-running the experiments:

```bash
python analyze.py                  # main-text Tables 4-8
python ext_analyze.py              # Table 9
python fairness.py path/to/OULAD/studentInfo.csv   # Table 10 (refits the OULAD early-warning models)
python tools/supplementary_tables.py               # supplementary Tables S1-S6
```

The first three scripts reproduce the files in `results/tables/` byte for byte. `tools/supplementary_tables.py` writes one CSV per supplementary table to `results/tables/supplementary/`.

To re-run the experiments from scratch, use `bash scripts/run_all.sh`. Approximate run times on two CPU cores:

| Step | Time |
|---|---|
| `predictive.py` (all datasets) | about 50 min |
| `prescriptive.py AUC` (10 seeds) | about 40 min |
| `prescriptive.py OULAD` (5 seeds, at most 300 queries per stage) | about 90 min |
| NICE and MCCE (all datasets) | under 1 h |
| CARE (100 queries per dataset and seed) | about 20 min per seed and dataset |

Seeds fix the data split, the models and the DiCE search jointly, so a re-run with the same package versions should give the same per-query results. Different versions of DiCE, CatBoost or scikit-learn may change individual candidates.

## Results

- Per-query results for every condition, seed and stage are in `results/`.
- The aggregated tables are in `results/tables/`; `summary.md`, `external_summary.md` and `fairness_summary.md` give readable versions.
- Column definitions are in [results/README.md](results/README.md).

## External methods

- **NICE:** installed from PyPI (`NICEx==0.2.3`).
- **MCCE:** [mccepy](https://github.com/NorskRegnesentral/mccepy) at commit `63e4fa3`, with `iteritems()` replaced by `items()` for pandas ≥ 2 (`patches/mccepy-pandas2.patch`).
- **CARE:** the authors' implementation, [peymanrasouli/CARE](https://github.com/peymanrasouli/CARE), at commit `811ff09`. CARE is distributed under GPL-3.0 and is not included in this repository.

Every method is evaluated in three variants:

- **native:** the method's own constraint handling;
- **bounded:** our bounds passed through the method's own mechanism. NICE has no such mechanism, so its output is projected onto the bounds instead;
- **bounded + editing:** the bounded output passed through the framework's bounded completion.

All variants then go through the same acceptance gate.

## Citation

See `CITATION.cff`. Please cite the paper if you use this code.

## Licence

The code in this repository is released under the MIT licence (see `LICENSE`). The OULAD data are © The Open University, released under CC BY 4.0 (Kuzilek, Hlosta & Zdrahal, 2017, *Scientific Data* 4, 170171).
