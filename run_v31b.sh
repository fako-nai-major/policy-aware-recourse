#!/bin/bash
# v3.1 stage 2: OULAD tree models (after stage 1 workers finish)
cd "$(dirname "$0")"
while pgrep -f "run_v31.sh $1" >/dev/null; do sleep 60; done
EXACT_DONE=logs/exact_v31_done.txt TREES_ONLY=1 python3 rerun_exact.py results_v3 OULAD $1 >> logs/v31_$1.log 2>&1
touch logs/V31_$1_DONE
