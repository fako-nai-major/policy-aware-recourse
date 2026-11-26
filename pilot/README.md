# Feasibility pilot: exact rule-verified recourse (MILP)

`recourse/exact.py` encodes logistic regression, scikit-learn random forests and CatBoost,
together with the linear rule, bounds and fixed features, as one mixed-integer linear
program solved with HiGHS (via SciPy). Infeasible = certified empty acceptable set.

    python pilot/pilot_exact.py PIMA 0        # all three models, seed-0 queries
    python pilot/pilot_exact.py HMDA 0
    python pilot/pilot_exact_edu.py OULAD 0 40   # CatBoost, 40 queries per stage, aligned + floor

Results: pilot/exact_<DS>_s0.csv. Every returned vector is re-checked by the v2 gate
(`recourse.core.gate`) with the real model's predict().
