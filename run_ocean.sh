#!/bin/bash
# OCEAN re-run workers: $1 = filter (e.g. OULAD or HMDA or PIMA)
cd "$(dirname "$0")"
python3 rerun_ocean.py results_v3 "$1" >> logs/rerun_ocean_$1.log 2>&1
