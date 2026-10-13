#!/bin/bash
# resumable v2 education runs
cd "$(dirname "$0")"
one() { ds=$1; s=$2; extra=$3; [ -f results_v2/presc_${ds}_s${s}_rows.csv.gz ] || python3 experiment.py $ds --seeds $s $extra --out results_v2 >> logs/v2_${ds}_s$s.log 2>&1; }
export -f one
{ for s in 0 1 2 3 4; do echo "OULAD $s --max_q=300"; done; for s in 0 1 2 3 4 5 6 7 8 9; do echo "AUC $s"; done; for s in 0 1 2 3 4; do echo "HarvardX $s --regimes=aligned --max_q=400"; done; } | \
  xargs -P2 -L1 bash -c 'one $0 $1 "${2//=/ }"'
echo done > logs/EDU_DONE
