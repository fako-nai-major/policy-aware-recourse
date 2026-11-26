#!/bin/bash
# v3.1: recompute exact rows of tree models (float32-ulp split margin), all domains except OULAD
cd "$(dirname "$0")"
EXACT_DONE=logs/exact_v31_done.txt TREES_ONLY=1 SKIP=OULAD python3 rerun_exact.py results_v3 v3_ $1 >> logs/v31_$1.log 2>&1
