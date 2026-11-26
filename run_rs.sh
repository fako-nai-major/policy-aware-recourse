#!/bin/bash
cd "$(dirname "$0")"
python3 add_repair_sparse.py "$1" "$2" >> logs/repair_sparse_$2.log 2>&1
