#!/bin/bash
# DACE and MACE baselines; each worker starts when the matching main v3 worker has finished.
cd "$(dirname "$0")"
[ -f logs/V3X_${1}_DONE ] && { echo "worker $1 already done"; exit 0; }
export DACE_SRC=${DACE_SRC:-/home/claude/ext/dace} MACE_SRC=${MACE_SRC:-/home/claude/ext/mace}
X="python3 ext_dace_mace.py"
if [ "$1" = "C" ]; then
  while [ ! -f logs/V3_A_DONE ]; do sleep 120; done
  $X PIMA    --seeds 0,1,2 --models lr,rf --methods dace,mace --max_q 20 --limit 120 >> logs/v3x_C.log 2>&1
  $X HMDA    --seeds 0,1,2 --models lr,rf --methods dace,mace --max_q 20 --limit 120 >> logs/v3x_C.log 2>&1
  $X HMDA_OR --seeds 0,1,2 --models lr,rf --methods dace,mace --rf_methods mace --max_q 20 --limit 120 >> logs/v3x_C.log 2>&1
  touch logs/V3X_C_DONE
else
  $X HMDA_S  --seeds 0,1,2 --models lr,rf --methods dace,mace --rf_methods mace --max_q 20 --limit 120 >> logs/v3x_D.log 2>&1
  while [ ! -f logs/V3_B_DONE ]; do sleep 120; done
  $X OULAD   --seeds 0,1,2 --models lr --methods dace,mace --regimes aligned --max_q 7 --limit 120 >> logs/v3x_D.log 2>&1
  # random forests on OULAD: DACE and MACE hit the 3-minute limit on nearly every query, so one seed only
  $X OULAD   --seeds 0 --models rf --methods dace,mace --regimes aligned --max_q 7 --limit 120 >> logs/v3x_D.log 2>&1
  touch logs/V3X_D_DONE
fi
