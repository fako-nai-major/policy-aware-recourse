#!/bin/bash
# Resumable v3 runs (each dataset/model/seed file is skipped if it exists).
cd "$(dirname "$0")"
[ -f logs/V3_${1}_DONE ] && { echo "worker $1 already done"; exit 0; }
mkdir -p logs results_v3
if [ "$1" = "A" ]; then
  python3 experiment_v3.py PIMA --seeds 0,1,2,3,4,5,6,7,8,9 >> logs/v3_A.log 2>&1
  python3 experiment_v3.py HMDA --seeds 0,1,2,3,4 >> logs/v3_A.log 2>&1
  python3 experiment_v3.py HMDA_OR --seeds 0,1,2 >> logs/v3_A.log 2>&1
  touch logs/V3_A_DONE
else
  python3 experiment_v3.py OULAD --seeds 0,1,2,3,4 --models lr,cat --regimes aligned,floor --max_q 20 --exact_limit 60 >> logs/v3_B.log 2>&1
  python3 experiment_v3.py HMDA_S --seeds 0,1,2 >> logs/v3_B.log 2>&1
  # random forests on OULAD are the slowest case (~3.5 min per query): three seeds, run last
  python3 experiment_v3.py OULAD --seeds 0,1,2 --models rf --regimes aligned,floor --max_q 20 --exact_limit 60 >> logs/v3_B.log 2>&1
  touch logs/V3_B_DONE
fi
