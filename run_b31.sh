#!/bin/bash
cd /home/claude/v2
for p in ADULT_rf ADULT_cat GMSC_cat HMDA_rf HMDA_cat HMDA_OR_rf HMDA_OR_cat HMDA_S_rf HMDA_S_cat PIMA_rf PIMA_cat GMSC_rf; do python3 verify_bounds.py $p >> logs/b31.log 2>&1; done
touch logs/B31_DONE
