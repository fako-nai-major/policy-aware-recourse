#!/bin/bash
cd "$(dirname "$0")"
[ -f logs/EXACT_RERUN_DONE ] && exit 0
python3 rerun_exact.py results_v3 >> logs/rerun_exact.log 2>&1 && touch logs/EXACT_RERUN_DONE
