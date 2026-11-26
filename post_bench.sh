#!/bin/bash
cd "$(dirname "$0")"
python3 rerun_ocean.py results_v3 ADULT_rf >> logs/post_bench.log 2>&1
python3 rerun_ocean.py results_v3 GMSC_rf >> logs/post_bench.log 2>&1
python3 add_repair_sparse.py ADULT >> logs/post_bench.log 2>&1
python3 add_repair_sparse.py GMSC >> logs/post_bench.log 2>&1
python3 verify_bounds.py ADULT >> logs/post_bench.log 2>&1
python3 verify_bounds.py GMSC >> logs/post_bench.log 2>&1
touch logs/POST_BENCH_DONE
true
