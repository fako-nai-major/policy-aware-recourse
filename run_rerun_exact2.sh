#!/bin/bash
cd "$(dirname "$0")"
[ -f logs/EXACT_RERUN_DONE ] && exit 0
python3 rerun_exact.py results_v3 OULAD_rf reverse >> logs/rerun_exact2.log 2>&1
