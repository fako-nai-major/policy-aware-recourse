#!/bin/bash
# bounds workers: $1 = filter, $2 = reverse (optional)
cd "$(dirname "$0")"
python3 verify_bounds.py "$1" "$2" >> logs/bounds_$2.log 2>&1
