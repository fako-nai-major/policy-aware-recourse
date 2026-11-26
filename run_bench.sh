#!/bin/bash
# Standard benchmarks (Adult, Give Me Some Credit); resumable.
cd "$(dirname "$0")"
[ -f logs/BENCH_${1}_DONE ] && exit 0
export DACE_SRC=${DACE_SRC:-/home/claude/ext/dace} MACE_SRC=${MACE_SRC:-/home/claude/ext/mace}
X="python3 ext_dace_mace.py"
if [ "$1" = "A" ]; then
  python3 experiment_v3.py ADULT --seeds 0,1,2,3,4 --models lr,rf,cat,mlp --max_q 200 >> logs/bench_A.log 2>&1
  python3 experiment_v3.py GMSC --seeds 0,1,2,3,4 --models lr,cat,mlp --max_q 200 >> logs/bench_A.log 2>&1
  $X ADULT --seeds 0,1,2 --models lr,rf --methods dace,mace --max_q 20 --limit 120 >> logs/bench_A.log 2>&1
  $X GMSC --seeds 0,1,2 --models lr --methods dace,mace --max_q 20 --limit 120 >> logs/bench_A.log 2>&1
else
  # random forests on GMSC: ~50 s per exact query (many thresholds on 3 continuous actions)
  python3 experiment_v3.py GMSC --seeds 0,1,2,3,4 --models rf --max_q 50 --exact_limit 60 >> logs/bench_B.log 2>&1
  $X GMSC --seeds 0 --models rf --methods dace,mace --max_q 20 --limit 120 >> logs/bench_B.log 2>&1
fi
touch logs/BENCH_${1}_DONE
