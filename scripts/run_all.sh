#!/usr/bin/env bash
# Full pipeline as run for the paper. Run from the repository root.
# Requires the data described in data/README.md; the external baselines need
# scripts/setup_external.sh, and fairness.py needs OULAD studentInfo.csv.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p results/tables logs
STUDENTINFO=${STUDENTINFO:-data/OULAD/studentInfo.csv}

# RQ1: predictive models (13 classifiers x 3 resampling conditions, grouped 5-fold CV)
python predictive.py AUC HarvardX OULAD                                   > logs/predictive.log 2>&1

# RQ2: prescriptive experiments (matched pools, ablation, objective audit, tau sweep, repair baselines)
python prescriptive.py AUC --seeds 0,1,2,3,4,5,6,7,8,9                    > logs/presc_AUC.log 2>&1
python prescriptive.py HarvardX --seeds 0,1,2,3,4 --regimes aligned --max_q 400 > logs/presc_HX.log 2>&1
python prescriptive.py OULAD --seeds 0,1,2,3,4 --max_q 300                > logs/presc_OULAD.log 2>&1
python analyze.py                                                         > logs/analyze.log 2>&1

# RQ3: external baselines under the same models, queries, bounds and gate
python external_baselines.py AUC --seeds 0,1,2,3,4,5,6,7,8,9 --methods NICE,MCCE > logs/ext_AUC.log 2>&1
python external_baselines.py HarvardX --seeds 0,1,2,3,4 --methods NICE,MCCE        > logs/ext_HX.log 2>&1
python external_baselines.py OULAD --seeds 0,1,2,3,4 --methods NICE,MCCE           > logs/ext_OULAD.log 2>&1
python external_baselines.py OULAD --seeds 0,1,2,3,4 --regime floor --methods NICE,MCCE > logs/ext_OULAD_floor.log 2>&1
for s in 0 1 2; do
  for ds in AUC OULAD HarvardX; do
    python external_baselines.py $ds --seeds $s --methods CARE --care_q 100 --tag _care >> logs/ext_CARE.log 2>&1
  done
done
python external_baselines.py OULAD --seeds 0 --regime floor --methods CARE --care_q 100 --tag _care >> logs/ext_CARE.log 2>&1
python ext_analyze.py                                                     > logs/ext_analyze.log 2>&1

# Group-level audit (OULAD) and supplementary tables
python fairness.py "$STUDENTINFO"                                         > logs/fairness.log 2>&1
python tools/supplementary_tables.py
echo "All results written to results/ and results/tables/."
