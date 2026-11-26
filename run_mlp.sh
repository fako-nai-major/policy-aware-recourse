#!/bin/bash
# ReLU-network runs (resumable: existing files skipped, per-query checkpoints)
cd "$(dirname "$0")"
[ -f logs/MLP_${1}_DONE ] && exit 0
if [ "$1" = "A" ]; then
  python3 experiment_v3.py PIMA --seeds 0,1,2,3,4,5,6,7,8,9 --models mlp >> logs/mlp_A.log 2>&1
  python3 experiment_v3.py HMDA --seeds 0,1,2,3,4 --models mlp >> logs/mlp_A.log 2>&1
else
  python3 experiment_v3.py OULAD --seeds 0,1,2,3,4 --models mlp --regimes aligned,floor --max_q 20 --exact_limit 60 >> logs/mlp_B.log 2>&1
  python3 experiment_v3.py HMDA_OR --seeds 0,1,2 --models mlp >> logs/mlp_B.log 2>&1
  python3 experiment_v3.py HMDA_S --seeds 0,1,2 --models mlp >> logs/mlp_B.log 2>&1
fi
touch logs/MLP_${1}_DONE
