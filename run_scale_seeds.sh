#!/bin/bash
# extra seeds for the scalability study (cold and warm start), worker $1 = seed
cd "$(dirname "$0")"
SEED=$1 python3 scalability.py PIMA,GMSC >> logs/scale_s$1.log 2>&1
SEED=$1 WS=1 WS_KIND=rf python3 scalability.py GMSC >> logs/scale_s$1.log 2>&1
touch logs/SCALE_S$1_DONE
