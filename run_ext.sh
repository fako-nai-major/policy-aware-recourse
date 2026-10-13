#!/bin/bash
# runs after the education re-run; resumable via done markers
cd "$(dirname "$0")"

while [ ! -f logs/EDU_DONE ]; do sleep 60; done
job() { tag=$1; shift; [ -f logs/ext_$tag.done ] || { python3 external_v2.py "$@" >> logs/ext_v2.log 2>&1 && touch logs/ext_$tag.done; }; }
for s in 0 1 2 3 4 5 6 7 8 9; do job pima_nm_$s PIMA --seeds $s --methods NICE,MCCE; done
for s in 0 1 2; do job pima_care_$s PIMA --seeds $s --methods CARE --care_q 100 --tag _care; done
for s in 0 1 2 3 4; do job hmda_nm_$s HMDA --seeds $s --methods NICE,MCCE --max_q 400; done
for s in 0 1 2; do job hmda_care_$s HMDA --seeds $s --methods CARE --care_q 100 --tag _care; done
echo done > logs/EXT_DONE
