## External baselines on matched queries (yield %, mean ± SD over seeds)
| dataset   | regime   | subset                          | condition                         | yield_pct   |   effort_accepted |
|:----------|:---------|:--------------------------------|:----------------------------------|:------------|------------------:|
| AUC       | aligned  | CARE queries (n=300, seeds=3)   | CARE_bounded                      | 38.0 ± 9.5  |             2.066 |
| AUC       | aligned  | CARE queries (n=300, seeds=3)   | CARE_bounded+edit                 | 39.0 ± 10.1 |             2.083 |
| AUC       | aligned  | CARE queries (n=300, seeds=3)   | CARE_native                       | 13.7 ± 4.2  |             2.48  |
| AUC       | aligned  | CARE queries (n=300, seeds=3)   | DiCE first candidate              | 32.7 ± 2.3  |             1.806 |
| AUC       | aligned  | CARE queries (n=300, seeds=3)   | Direct policy repair + escalation | 71.7 ± 4.6  |             2.152 |
| AUC       | aligned  | CARE queries (n=300, seeds=3)   | DiCE + post-hoc full gate         | 39.7 ± 1.2  |             1.833 |
| AUC       | aligned  | CARE queries (n=300, seeds=3)   | Framework (ranking + edit + gate) | 71.7 ± 4.7  |             2.064 |
| AUC       | aligned  | CARE queries (n=300, seeds=3)   | Framework + fallback              | 72.3 ± 4.0  |             2.062 |
| AUC       | aligned  | MCCE queries (n=2587, seeds=10) | MCCE_bounded                      | 31.1 ± 6.3  |             2.142 |
| AUC       | aligned  | MCCE queries (n=2587, seeds=10) | MCCE_bounded+edit                 | 31.1 ± 6.3  |             2.142 |
| AUC       | aligned  | MCCE queries (n=2587, seeds=10) | MCCE_native                       | 19.3 ± 4.9  |             2.128 |
| AUC       | aligned  | MCCE queries (n=2587, seeds=10) | DiCE first candidate              | 28.0 ± 3.8  |             1.849 |
| AUC       | aligned  | MCCE queries (n=2587, seeds=10) | Direct policy repair + escalation | 65.9 ± 4.3  |             2.181 |
| AUC       | aligned  | MCCE queries (n=2587, seeds=10) | DiCE + post-hoc full gate         | 37.3 ± 2.9  |             1.921 |
| AUC       | aligned  | MCCE queries (n=2587, seeds=10) | Framework (ranking + edit + gate) | 65.6 ± 4.2  |             2.092 |
| AUC       | aligned  | MCCE queries (n=2587, seeds=10) | Framework + fallback              | 66.3 ± 4.4  |             2.091 |
| AUC       | aligned  | NICE queries (n=2587, seeds=10) | NICE_bounded                      | 14.4 ± 3.8  |             2.263 |
| AUC       | aligned  | NICE queries (n=2587, seeds=10) | NICE_bounded+edit                 | 28.0 ± 3.4  |             2.369 |
| AUC       | aligned  | NICE queries (n=2587, seeds=10) | NICE_native                       | 14.3 ± 3.4  |             2.26  |
| AUC       | aligned  | NICE queries (n=2587, seeds=10) | DiCE first candidate              | 28.0 ± 3.8  |             1.849 |
| AUC       | aligned  | NICE queries (n=2587, seeds=10) | Direct policy repair + escalation | 65.9 ± 4.3  |             2.181 |
| AUC       | aligned  | NICE queries (n=2587, seeds=10) | DiCE + post-hoc full gate         | 37.3 ± 2.9  |             1.921 |
| AUC       | aligned  | NICE queries (n=2587, seeds=10) | Framework (ranking + edit + gate) | 65.6 ± 4.2  |             2.092 |
| AUC       | aligned  | NICE queries (n=2587, seeds=10) | Framework + fallback              | 66.3 ± 4.4  |             2.091 |
| HarvardX  | aligned  | CARE queries (n=300, seeds=3)   | CARE_bounded                      | 100.0 ± 0.0 |             0.405 |
| HarvardX  | aligned  | CARE queries (n=300, seeds=3)   | CARE_bounded+edit                 | 100.0 ± 0.0 |             0.405 |
| HarvardX  | aligned  | CARE queries (n=300, seeds=3)   | CARE_native                       | 45.3 ± 11.0 |             0.46  |
| HarvardX  | aligned  | CARE queries (n=300, seeds=3)   | DiCE first candidate              | 98.0 ± 2.0  |             1.357 |
| HarvardX  | aligned  | CARE queries (n=300, seeds=3)   | DiCE + post-hoc full gate         | 100.0 ± 0.0 |             1.373 |
| HarvardX  | aligned  | CARE queries (n=300, seeds=3)   | Framework (ranking + edit + gate) | 100.0 ± 0.0 |             0.786 |
| HarvardX  | aligned  | CARE queries (n=300, seeds=3)   | Framework + fallback              | 100.0 ± 0.0 |             0.786 |
| HarvardX  | aligned  | MCCE queries (n=1999, seeds=5)  | MCCE_bounded                      | 99.8 ± 0.1  |             0.554 |
| HarvardX  | aligned  | MCCE queries (n=1999, seeds=5)  | MCCE_bounded+edit                 | 99.8 ± 0.1  |             0.554 |
| HarvardX  | aligned  | MCCE queries (n=1999, seeds=5)  | MCCE_native                       | 59.8 ± 2.4  |             0.57  |
| HarvardX  | aligned  | MCCE queries (n=1999, seeds=5)  | DiCE first candidate              | 98.5 ± 0.4  |             1.404 |
| HarvardX  | aligned  | MCCE queries (n=1999, seeds=5)  | DiCE + post-hoc full gate         | 99.9 ± 0.1  |             1.412 |
| HarvardX  | aligned  | MCCE queries (n=1999, seeds=5)  | Framework (ranking + edit + gate) | 99.9 ± 0.1  |             0.843 |
| HarvardX  | aligned  | MCCE queries (n=1999, seeds=5)  | Framework + fallback              | 99.9 ± 0.1  |             0.843 |
| HarvardX  | aligned  | NICE queries (n=1999, seeds=5)  | NICE_bounded                      | 50.5 ± 1.7  |             0.348 |
| HarvardX  | aligned  | NICE queries (n=1999, seeds=5)  | NICE_bounded+edit                 | 50.5 ± 1.7  |             0.348 |
| HarvardX  | aligned  | NICE queries (n=1999, seeds=5)  | NICE_native                       | 50.5 ± 1.7  |             0.348 |
| HarvardX  | aligned  | NICE queries (n=1999, seeds=5)  | DiCE first candidate              | 98.5 ± 0.4  |             1.404 |
| HarvardX  | aligned  | NICE queries (n=1999, seeds=5)  | DiCE + post-hoc full gate         | 99.9 ± 0.1  |             1.412 |
| HarvardX  | aligned  | NICE queries (n=1999, seeds=5)  | Framework (ranking + edit + gate) | 99.9 ± 0.1  |             0.843 |
| HarvardX  | aligned  | NICE queries (n=1999, seeds=5)  | Framework + fallback              | 99.9 ± 0.1  |             0.843 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | CARE_bounded                      | 29.3 ± 7.1  |             1.599 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | CARE_bounded+edit                 | 67.0 ± 2.6  |             1.813 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | CARE_native                       | 9.0 ± 4.6   |             1.267 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | DiCE first candidate              | 37.7 ± 2.5  |             1.724 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | Direct policy repair + escalation | 91.0 ± 2.6  |             1.911 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | DiCE + post-hoc full gate         | 70.0 ± 7.5  |             1.789 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | Framework (ranking + edit + gate) | 93.3 ± 1.2  |             1.759 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | Framework + fallback              | 94.3 ± 1.2  |             1.765 |
| OULAD     | aligned  | MCCE queries (n=4500, seeds=5)  | MCCE_bounded                      | 45.2 ± 2.2  |             2.426 |
| OULAD     | aligned  | MCCE queries (n=4500, seeds=5)  | MCCE_bounded+edit                 | 62.5 ± 1.8  |             2.414 |
| OULAD     | aligned  | MCCE queries (n=4500, seeds=5)  | MCCE_native                       | 25.5 ± 5.0  |             1.967 |
| OULAD     | aligned  | MCCE queries (n=4500, seeds=5)  | DiCE first candidate              | 34.5 ± 3.6  |             1.706 |
| OULAD     | aligned  | MCCE queries (n=4500, seeds=5)  | Direct policy repair + escalation | 91.2 ± 2.0  |             1.955 |
| OULAD     | aligned  | MCCE queries (n=4500, seeds=5)  | DiCE + post-hoc full gate         | 70.7 ± 6.5  |             1.802 |
| OULAD     | aligned  | MCCE queries (n=4500, seeds=5)  | Framework (ranking + edit + gate) | 94.2 ± 1.2  |             1.776 |
| OULAD     | aligned  | MCCE queries (n=4500, seeds=5)  | Framework + fallback              | 95.2 ± 1.0  |             1.782 |
| OULAD     | aligned  | NICE queries (n=4500, seeds=5)  | NICE_bounded                      | 4.9 ± 1.2   |             1.244 |
| OULAD     | aligned  | NICE queries (n=4500, seeds=5)  | NICE_bounded+edit                 | 37.4 ± 5.6  |             1.693 |
| OULAD     | aligned  | NICE queries (n=4500, seeds=5)  | NICE_native                       | 4.9 ± 1.2   |             1.244 |
| OULAD     | aligned  | NICE queries (n=4500, seeds=5)  | DiCE first candidate              | 34.5 ± 3.6  |             1.706 |
| OULAD     | aligned  | NICE queries (n=4500, seeds=5)  | Direct policy repair + escalation | 91.2 ± 2.0  |             1.955 |
| OULAD     | aligned  | NICE queries (n=4500, seeds=5)  | DiCE + post-hoc full gate         | 70.7 ± 6.5  |             1.802 |
| OULAD     | aligned  | NICE queries (n=4500, seeds=5)  | Framework (ranking + edit + gate) | 94.2 ± 1.2  |             1.776 |
| OULAD     | aligned  | NICE queries (n=4500, seeds=5)  | Framework + fallback              | 95.2 ± 1.0  |             1.782 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | CARE_bounded                      | 40.0        |             3.222 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | CARE_bounded+edit                 | 65.0        |             4.913 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | CARE_native                       | 3.0         |             1.68  |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | DiCE first candidate              | 10.0        |             2.408 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | Direct policy repair + escalation | 93.0        |             4.512 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | DiCE + post-hoc full gate         | 21.0        |             2.55  |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | Framework (ranking + edit + gate) | 85.0        |             4.721 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | Framework + fallback              | 86.0        |             4.776 |
| OULAD     | floor    | MCCE queries (n=4500, seeds=5)  | MCCE_bounded                      | 64.1 ± 1.7  |             5.543 |
| OULAD     | floor    | MCCE queries (n=4500, seeds=5)  | MCCE_bounded+edit                 | 64.1 ± 1.7  |             5.543 |
| OULAD     | floor    | MCCE queries (n=4500, seeds=5)  | MCCE_native                       | 6.1 ± 1.8   |             2.414 |
| OULAD     | floor    | MCCE queries (n=4500, seeds=5)  | DiCE first candidate              | 7.7 ± 1.1   |             2.359 |
| OULAD     | floor    | MCCE queries (n=4500, seeds=5)  | Direct policy repair + escalation | 91.2 ± 2.0  |             4.507 |
| OULAD     | floor    | MCCE queries (n=4500, seeds=5)  | DiCE + post-hoc full gate         | 20.6 ± 2.2  |             2.581 |
| OULAD     | floor    | MCCE queries (n=4500, seeds=5)  | Framework (ranking + edit + gate) | 82.8 ± 5.5  |             4.464 |
| OULAD     | floor    | MCCE queries (n=4500, seeds=5)  | Framework + fallback              | 86.0 ± 3.9  |             4.516 |
| OULAD     | floor    | NICE queries (n=4500, seeds=5)  | NICE_bounded                      | 47.3 ± 5.9  |             4.312 |
| OULAD     | floor    | NICE queries (n=4500, seeds=5)  | NICE_bounded+edit                 | 47.3 ± 5.9  |             4.312 |
| OULAD     | floor    | NICE queries (n=4500, seeds=5)  | NICE_native                       | 0.7 ± 0.4   |             1.889 |
| OULAD     | floor    | NICE queries (n=4500, seeds=5)  | DiCE first candidate              | 7.7 ± 1.1   |             2.359 |
| OULAD     | floor    | NICE queries (n=4500, seeds=5)  | Direct policy repair + escalation | 91.2 ± 2.0  |             4.507 |
| OULAD     | floor    | NICE queries (n=4500, seeds=5)  | DiCE + post-hoc full gate         | 20.6 ± 2.2  |             2.581 |
| OULAD     | floor    | NICE queries (n=4500, seeds=5)  | Framework (ranking + edit + gate) | 82.8 ± 5.5  |             4.464 |
| OULAD     | floor    | NICE queries (n=4500, seeds=5)  | Framework + fallback              | 86.0 ± 3.9  |             4.516 |

## Paired tests vs framework (McNemar, learner-cluster bootstrap, Holm)
| dataset   | regime   | framework                         | baseline          |    n |   diff_pp |   ci_lo |   ci_hi |   only_framework |   only_baseline |     p |   p_holm |
|:----------|:---------|:----------------------------------|:------------------|-----:|----------:|--------:|--------:|-----------------:|----------------:|------:|---------:|
| AUC       | aligned  | Framework (ranking + edit + gate) | CARE_bounded      |  300 |    33.667 |  27.723 |  39.467 |              102 |               1 | 0     |    0     |
| AUC       | aligned  | Framework + fallback              | CARE_bounded      |  300 |    34.333 |  28.471 |  39.935 |              103 |               0 | 0     |    0     |
| AUC       | aligned  | Framework (ranking + edit + gate) | CARE_bounded+edit |  300 |    32.667 |  26.736 |  38.365 |               99 |               1 | 0     |    0     |
| AUC       | aligned  | Framework + fallback              | CARE_bounded+edit |  300 |    33.333 |  27.336 |  38.961 |              100 |               0 | 0     |    0     |
| AUC       | aligned  | Framework (ranking + edit + gate) | CARE_native       |  300 |    58     |  51.785 |  63.871 |              175 |               1 | 0     |    0     |
| AUC       | aligned  | Framework + fallback              | CARE_native       |  300 |    58.667 |  52.541 |  64.516 |              176 |               0 | 0     |    0     |
| AUC       | aligned  | Framework (ranking + edit + gate) | MCCE_bounded      | 2587 |    34.557 |  32.642 |  36.489 |              900 |               6 | 0     |    0     |
| AUC       | aligned  | Framework + fallback              | MCCE_bounded      | 2587 |    35.176 |  33.23  |  37.082 |              910 |               0 | 0     |    0     |
| AUC       | aligned  | Framework (ranking + edit + gate) | MCCE_bounded+edit | 2587 |    34.557 |  32.642 |  36.489 |              900 |               6 | 0     |    0     |
| AUC       | aligned  | Framework + fallback              | MCCE_bounded+edit | 2587 |    35.176 |  33.23  |  37.082 |              910 |               0 | 0     |    0     |
| AUC       | aligned  | Framework (ranking + edit + gate) | MCCE_native       | 2587 |    46.308 |  44.165 |  48.383 |             1203 |               5 | 0     |    0     |
| AUC       | aligned  | Framework + fallback              | MCCE_native       | 2587 |    46.927 |  44.784 |  49.073 |             1214 |               0 | 0     |    0     |
| AUC       | aligned  | Framework (ranking + edit + gate) | NICE_bounded      | 2587 |    51.14  |  49.123 |  53.234 |             1326 |               3 | 0     |    0     |
| AUC       | aligned  | Framework + fallback              | NICE_bounded      | 2587 |    51.759 |  49.725 |  53.861 |             1339 |               0 | 0     |    0     |
| AUC       | aligned  | Framework (ranking + edit + gate) | NICE_bounded+edit | 2587 |    37.572 |  35.387 |  39.753 |              975 |               3 | 0     |    0     |
| AUC       | aligned  | Framework + fallback              | NICE_bounded+edit | 2587 |    38.191 |  35.991 |  40.391 |              988 |               0 | 0     |    0     |
| AUC       | aligned  | Framework (ranking + edit + gate) | NICE_native       | 2587 |    51.295 |  49.285 |  53.375 |             1330 |               3 | 0     |    0     |
| AUC       | aligned  | Framework + fallback              | NICE_native       | 2587 |    51.913 |  49.883 |  54.016 |             1343 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework (ranking + edit + gate) | CARE_bounded      |  300 |     0     |   0     |   0     |                0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Framework + fallback              | CARE_bounded      |  300 |     0     |   0     |   0     |                0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Framework (ranking + edit + gate) | CARE_bounded+edit |  300 |     0     |   0     |   0     |                0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Framework + fallback              | CARE_bounded+edit |  300 |     0     |   0     |   0     |                0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Framework (ranking + edit + gate) | CARE_native       |  300 |    54.667 |  49     |  60.333 |              164 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework + fallback              | CARE_native       |  300 |    54.667 |  49     |  60.333 |              164 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework (ranking + edit + gate) | MCCE_bounded      | 1999 |     0.1   |   0     |   0.25  |                2 |               0 | 0.5   |    1     |
| HarvardX  | aligned  | Framework + fallback              | MCCE_bounded      | 1999 |     0.1   |   0     |   0.25  |                2 |               0 | 0.5   |    1     |
| HarvardX  | aligned  | Framework (ranking + edit + gate) | MCCE_bounded+edit | 1999 |     0.1   |   0     |   0.25  |                2 |               0 | 0.5   |    1     |
| HarvardX  | aligned  | Framework + fallback              | MCCE_bounded+edit | 1999 |     0.1   |   0     |   0.25  |                2 |               0 | 0.5   |    1     |
| HarvardX  | aligned  | Framework (ranking + edit + gate) | MCCE_native       | 1999 |    40.12  |  37.969 |  42.371 |              802 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework + fallback              | MCCE_native       | 1999 |    40.12  |  37.969 |  42.371 |              802 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework (ranking + edit + gate) | NICE_bounded      | 1999 |    49.375 |  47.224 |  51.626 |              987 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework + fallback              | NICE_bounded      | 1999 |    49.375 |  47.224 |  51.626 |              987 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework (ranking + edit + gate) | NICE_bounded+edit | 1999 |    49.375 |  47.224 |  51.626 |              987 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework + fallback              | NICE_bounded+edit | 1999 |    49.375 |  47.224 |  51.626 |              987 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework (ranking + edit + gate) | NICE_native       | 1999 |    49.375 |  47.224 |  51.626 |              987 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework + fallback              | NICE_native       | 1999 |    49.375 |  47.224 |  51.626 |              987 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | CARE_bounded      |  300 |    64     |  58.471 |  69.831 |              193 |               1 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | CARE_bounded      |  300 |    65     |  59.468 |  70.667 |              195 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | CARE_bounded+edit |  300 |    26.333 |  21.121 |  31.79  |               81 |               2 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | CARE_bounded+edit |  300 |    27.333 |  22.331 |  32.55  |               82 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | CARE_native       |  300 |    84.333 |  79.796 |  88.553 |              253 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | CARE_native       |  300 |    85.333 |  81     |  89.227 |              256 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | MCCE_bounded      | 4500 |    49     |  47.373 |  50.694 |             2224 |              19 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | MCCE_bounded      | 4500 |    49.911 |  48.353 |  51.529 |             2251 |               5 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | MCCE_bounded+edit | 4500 |    31.756 |  30.424 |  33.184 |             1455 |              26 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | MCCE_bounded+edit | 4500 |    32.667 |  31.368 |  34.032 |             1477 |               7 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | MCCE_native       | 4500 |    68.756 |  67.377 |  70.21  |             3100 |               6 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | MCCE_native       | 4500 |    69.667 |  68.295 |  71.088 |             3135 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | NICE_bounded      | 4500 |    89.311 |  88.421 |  90.255 |             4019 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | NICE_bounded      | 4500 |    90.222 |  89.379 |  91.117 |             4060 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | NICE_bounded+edit | 4500 |    56.8   |  55.128 |  58.454 |             2577 |              21 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | NICE_bounded+edit | 4500 |    57.711 |  56.045 |  59.365 |             2606 |               9 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | NICE_native       | 4500 |    89.311 |  88.421 |  90.255 |             4019 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | NICE_native       | 4500 |    90.222 |  89.379 |  91.117 |             4060 |               0 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | CARE_bounded      |  100 |    45     |  34.694 |  55.556 |               47 |               2 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | CARE_bounded      |  100 |    46     |  35.92  |  56.436 |               48 |               2 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | CARE_bounded+edit |  100 |    20     |   9.998 |  30     |               26 |               6 | 0.001 |    0.005 |
| OULAD     | floor    | Framework + fallback              | CARE_bounded+edit |  100 |    21     |  11.34  |  31     |               26 |               5 | 0     |    0.002 |
| OULAD     | floor    | Framework (ranking + edit + gate) | CARE_native       |  100 |    82     |  74.257 |  89.323 |               82 |               0 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | CARE_native       |  100 |    83     |  75.248 |  90.099 |               83 |               0 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | MCCE_bounded      | 4500 |    18.667 |  17.152 |  20.204 |             1107 |             267 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | MCCE_bounded      | 4500 |    21.844 |  20.426 |  23.285 |             1155 |             172 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | MCCE_bounded+edit | 4500 |    18.667 |  17.152 |  20.204 |             1107 |             267 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | MCCE_bounded+edit | 4500 |    21.844 |  20.426 |  23.285 |             1155 |             172 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | MCCE_native       | 4500 |    76.667 |  75.305 |  78.035 |             3466 |              16 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | MCCE_native       | 4500 |    79.844 |  78.646 |  81.086 |             3593 |               0 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | NICE_bounded      | 4500 |    35.467 |  33.736 |  37.185 |             1855 |             259 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | NICE_bounded      | 4500 |    38.644 |  36.944 |  40.267 |             1922 |             183 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | NICE_bounded+edit | 4500 |    35.467 |  33.736 |  37.185 |             1855 |             259 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | NICE_bounded+edit | 4500 |    38.644 |  36.944 |  40.267 |             1922 |             183 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | NICE_native       | 4500 |    82.067 |  80.905 |  83.196 |             3695 |               2 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | NICE_native       | 4500 |    85.244 |  84.157 |  86.261 |             3836 |               0 | 0     |    0     |

## Rejection reasons (% of rejected)
|                                              |   below_policy_threshold |   classifier_target_not_met |   immutable_changed |   no_candidate |   out_of_bounds |
|:---------------------------------------------|-------------------------:|----------------------------:|--------------------:|---------------:|----------------:|
| ('AUC', 'aligned', 'CARE_bounded')           |                     96.2 |                         0   |                 3.8 |            0   |             0   |
| ('AUC', 'aligned', 'CARE_bounded+edit')      |                     96.2 |                         0   |                 3.8 |            0   |             0   |
| ('AUC', 'aligned', 'CARE_native')            |                      0   |                         0   |                81.1 |            0   |            18.9 |
| ('AUC', 'aligned', 'MCCE_bounded')           |                     29.5 |                         0   |                 0   |           70.5 |             0   |
| ('AUC', 'aligned', 'MCCE_bounded+edit')      |                     29.5 |                         0   |                 0   |           70.5 |             0   |
| ('AUC', 'aligned', 'MCCE_native')            |                     30.5 |                         0   |                 0   |           53.1 |            16.4 |
| ('AUC', 'aligned', 'NICE_bounded')           |                     98.5 |                         1.5 |                 0   |            0   |             0   |
| ('AUC', 'aligned', 'NICE_bounded+edit')      |                     97.4 |                         2.6 |                 0   |            0   |             0   |
| ('AUC', 'aligned', 'NICE_native')            |                     59.3 |                         0   |                39.4 |            0   |             1.3 |
| ('HarvardX', 'aligned', 'CARE_native')       |                      0   |                         0   |                 0   |            0   |           100   |
| ('HarvardX', 'aligned', 'MCCE_bounded')      |                      0   |                         0   |                 0   |          100   |             0   |
| ('HarvardX', 'aligned', 'MCCE_bounded+edit') |                      0   |                         0   |                 0   |          100   |             0   |
| ('HarvardX', 'aligned', 'MCCE_native')       |                      0   |                         0   |                 0   |            0.1 |            99.9 |
| ('HarvardX', 'aligned', 'NICE_bounded')      |                      0   |                       100   |                 0   |            0   |             0   |
| ('HarvardX', 'aligned', 'NICE_bounded+edit') |                      0   |                       100   |                 0   |            0   |             0   |
| ('HarvardX', 'aligned', 'NICE_native')       |                      0   |                         0   |                 0.5 |            0   |            99.5 |
| ('OULAD', 'aligned', 'CARE_bounded')         |                     96.7 |                         0   |                 2.8 |            0   |             0.5 |
| ('OULAD', 'aligned', 'CARE_bounded+edit')    |                     83.8 |                         3   |                 6.1 |            0   |             7.1 |
| ('OULAD', 'aligned', 'CARE_native')          |                     72.2 |                         0   |                24.9 |            0   |             2.9 |
| ('OULAD', 'aligned', 'MCCE_bounded')         |                     49.7 |                         0   |                 0   |           50.3 |             0   |
| ('OULAD', 'aligned', 'MCCE_bounded+edit')    |                     21.8 |                         4.7 |                 0   |           73.5 |             0   |
| ('OULAD', 'aligned', 'MCCE_native')          |                     40.7 |                         0   |                 0.3 |           31.1 |            27.9 |
| ('OULAD', 'aligned', 'NICE_bounded')         |                     97.8 |                         2.2 |                 0   |            0   |             0   |
| ('OULAD', 'aligned', 'NICE_bounded+edit')    |                     67.6 |                        32.4 |                 0   |            0   |             0   |
| ('OULAD', 'aligned', 'NICE_native')          |                     77.5 |                         0   |                18.5 |            0   |             4   |
| ('OULAD', 'floor', 'CARE_bounded')           |                     48.3 |                         0   |                 1.7 |            0   |            50   |
| ('OULAD', 'floor', 'CARE_bounded+edit')      |                     62.9 |                         2.9 |                 2.9 |            0   |            31.4 |
| ('OULAD', 'floor', 'CARE_native')            |                     78.4 |                         0   |                 4.1 |            0   |            17.5 |
| ('OULAD', 'floor', 'MCCE_bounded')           |                      7.9 |                         0   |                 0   |           88.6 |             3.5 |
| ('OULAD', 'floor', 'MCCE_bounded+edit')      |                      7.9 |                         0   |                 0   |           88.6 |             3.5 |
| ('OULAD', 'floor', 'MCCE_native')            |                     32.3 |                         0   |                 0.1 |           24.7 |            42.9 |
| ('OULAD', 'floor', 'NICE_bounded')           |                     67.9 |                        32.1 |                 0   |            0   |             0   |
| ('OULAD', 'floor', 'NICE_bounded+edit')      |                     67.9 |                        32.1 |                 0   |            0   |             0   |
| ('OULAD', 'floor', 'NICE_native')            |                     74.2 |                         0   |                 0.8 |            0   |            25   |

## Mean seconds per query
|                      |   seconds |
|:---------------------|----------:|
| ('AUC', 'CARE')      |     9.745 |
| ('AUC', 'MCCE')      |     0.02  |
| ('AUC', 'NICE')      |     0.006 |
| ('HarvardX', 'CARE') |     9.572 |
| ('HarvardX', 'MCCE') |     0.038 |
| ('HarvardX', 'NICE') |     0.005 |
| ('OULAD', 'CARE')    |    13.83  |
| ('OULAD', 'MCCE')    |     0.047 |
| ('OULAD', 'NICE')    |     0.013 |