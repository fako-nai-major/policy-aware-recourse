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
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | CARE_bounded                      | 43.7 ± 3.1  |             0.785 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | CARE_bounded+edit                 | 83.0 ± 8.2  |             0.991 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | CARE_native                       | 14.7 ± 3.1  |             0.681 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | DiCE first candidate              | 76.0 ± 5.0  |             1.29  |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | Direct policy repair + escalation | 94.7 ± 2.1  |             0.706 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | DiCE + post-hoc full gate         | 98.7 ± 0.6  |             1.371 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | Framework (ranking + edit + gate) | 100.0 ± 0.0 |             0.879 |
| OULAD     | aligned  | CARE queries (n=300, seeds=3)   | Framework + fallback              | 100.0 ± 0.0 |             0.879 |
| OULAD     | aligned  | MCCE queries (n=3914, seeds=5)  | MCCE_bounded                      | 44.3 ± 5.3  |             1.283 |
| OULAD     | aligned  | MCCE queries (n=3914, seeds=5)  | MCCE_bounded+edit                 | 67.3 ± 2.1  |             1.363 |
| OULAD     | aligned  | MCCE queries (n=3914, seeds=5)  | MCCE_native                       | 26.5 ± 3.3  |             1.223 |
| OULAD     | aligned  | MCCE queries (n=3914, seeds=5)  | DiCE first candidate              | 76.5 ± 2.1  |             1.287 |
| OULAD     | aligned  | MCCE queries (n=3914, seeds=5)  | Direct policy repair + escalation | 91.2 ± 8.6  |             0.686 |
| OULAD     | aligned  | MCCE queries (n=3914, seeds=5)  | DiCE + post-hoc full gate         | 99.3 ± 0.4  |             1.344 |
| OULAD     | aligned  | MCCE queries (n=3914, seeds=5)  | Framework (ranking + edit + gate) | 99.9 ± 0.1  |             0.873 |
| OULAD     | aligned  | MCCE queries (n=3914, seeds=5)  | Framework + fallback              | 100.0 ± 0.0 |             0.873 |
| OULAD     | aligned  | NICE queries (n=3914, seeds=5)  | NICE_bounded                      | 15.5 ± 7.7  |             0.521 |
| OULAD     | aligned  | NICE queries (n=3914, seeds=5)  | NICE_bounded+edit                 | 57.9 ± 9.6  |             0.902 |
| OULAD     | aligned  | NICE queries (n=3914, seeds=5)  | NICE_native                       | 15.5 ± 7.7  |             0.521 |
| OULAD     | aligned  | NICE queries (n=3914, seeds=5)  | DiCE first candidate              | 76.5 ± 2.1  |             1.287 |
| OULAD     | aligned  | NICE queries (n=3914, seeds=5)  | Direct policy repair + escalation | 91.2 ± 8.6  |             0.686 |
| OULAD     | aligned  | NICE queries (n=3914, seeds=5)  | DiCE + post-hoc full gate         | 99.3 ± 0.4  |             1.344 |
| OULAD     | aligned  | NICE queries (n=3914, seeds=5)  | Framework (ranking + edit + gate) | 99.9 ± 0.1  |             0.873 |
| OULAD     | aligned  | NICE queries (n=3914, seeds=5)  | Framework + fallback              | 100.0 ± 0.0 |             0.873 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | CARE_bounded                      | 20.0        |             3.729 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | CARE_bounded+edit                 | 80.0        |             3.371 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | CARE_native                       | 0.0         |           nan     |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | DiCE first candidate              | 0.0         |           nan     |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | Direct policy repair + escalation | 99.0        |             2.753 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | DiCE + post-hoc full gate         | 1.0         |             3.043 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | Framework (ranking + edit + gate) | 96.0        |             3.273 |
| OULAD     | floor    | CARE queries (n=100, seeds=1)   | Framework + fallback              | 100.0       |             3.28  |
| OULAD     | floor    | MCCE queries (n=3914, seeds=5)  | MCCE_bounded                      | 14.8 ± 2.1  |             4.132 |
| OULAD     | floor    | MCCE queries (n=3914, seeds=5)  | MCCE_bounded+edit                 | 14.8 ± 2.1  |             4.132 |
| OULAD     | floor    | MCCE queries (n=3914, seeds=5)  | MCCE_native                       | 0.1 ± 0.1   |             1.894 |
| OULAD     | floor    | MCCE queries (n=3914, seeds=5)  | DiCE first candidate              | 0.3 ± 0.1   |             2.496 |
| OULAD     | floor    | MCCE queries (n=3914, seeds=5)  | Direct policy repair + escalation | 99.6 ± 0.3  |             2.655 |
| OULAD     | floor    | MCCE queries (n=3914, seeds=5)  | DiCE + post-hoc full gate         | 0.7 ± 0.2   |             2.58  |
| OULAD     | floor    | MCCE queries (n=3914, seeds=5)  | Framework (ranking + edit + gate) | 98.5 ± 1.4  |             3.166 |
| OULAD     | floor    | MCCE queries (n=3914, seeds=5)  | Framework + fallback              | 99.9 ± 0.1  |             3.17  |
| OULAD     | floor    | NICE queries (n=3914, seeds=5)  | NICE_bounded                      | 87.1 ± 5.2  |             2.72  |
| OULAD     | floor    | NICE queries (n=3914, seeds=5)  | NICE_bounded+edit                 | 87.1 ± 5.2  |             2.72  |
| OULAD     | floor    | NICE queries (n=3914, seeds=5)  | NICE_native                       | 0.0 ± 0.1   |             1.588 |
| OULAD     | floor    | NICE queries (n=3914, seeds=5)  | DiCE first candidate              | 0.3 ± 0.1   |             2.496 |
| OULAD     | floor    | NICE queries (n=3914, seeds=5)  | Direct policy repair + escalation | 99.6 ± 0.3  |             2.655 |
| OULAD     | floor    | NICE queries (n=3914, seeds=5)  | DiCE + post-hoc full gate         | 0.7 ± 0.2   |             2.58  |
| OULAD     | floor    | NICE queries (n=3914, seeds=5)  | Framework (ranking + edit + gate) | 98.5 ± 1.4  |             3.166 |
| OULAD     | floor    | NICE queries (n=3914, seeds=5)  | Framework + fallback              | 99.9 ± 0.1  |             3.17  |

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
| OULAD     | aligned  | Framework (ranking + edit + gate) | CARE_bounded      |  300 |    56.333 |  50.336 |  61.746 |              169 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | CARE_bounded      |  300 |    56.333 |  50.336 |  61.746 |              169 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | CARE_bounded+edit |  300 |    17     |  12.957 |  21.452 |               51 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | CARE_bounded+edit |  300 |    17     |  12.957 |  21.452 |               51 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | CARE_native       |  300 |    85.333 |  81.271 |  89.216 |              256 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | CARE_native       |  300 |    85.333 |  81.271 |  89.216 |              256 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | MCCE_bounded      | 3914 |    55.723 |  54.03  |  57.344 |             2182 |               1 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | MCCE_bounded      | 3914 |    55.774 |  54.097 |  57.38  |             2183 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | MCCE_bounded+edit | 3914 |    32.652 |  31.155 |  34.05  |             1279 |               1 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | MCCE_bounded+edit | 3914 |    32.703 |  31.206 |  34.12  |             1280 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | MCCE_native       | 3914 |    73.454 |  72.029 |  74.944 |             2875 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | MCCE_native       | 3914 |    73.505 |  72.068 |  74.981 |             2877 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | NICE_bounded      | 3914 |    84.543 |  83.24  |  85.847 |             3309 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | NICE_bounded      | 3914 |    84.594 |  83.312 |  85.893 |             3311 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | NICE_bounded+edit | 3914 |    42.003 |  40.345 |  43.795 |             1645 |               1 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | NICE_bounded+edit | 3914 |    42.054 |  40.395 |  43.839 |             1646 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework (ranking + edit + gate) | NICE_native       | 3914 |    84.543 |  83.24  |  85.847 |             3309 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback              | NICE_native       | 3914 |    84.594 |  83.312 |  85.893 |             3311 |               0 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | CARE_bounded      |  100 |    76     |  67     |  84.468 |               77 |               1 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | CARE_bounded      |  100 |    80     |  72     |  87.5   |               80 |               0 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | CARE_bounded+edit |  100 |    16     |   7.611 |  25     |               19 |               3 | 0.001 |    0.008 |
| OULAD     | floor    | Framework + fallback              | CARE_bounded+edit |  100 |    20     |  12.121 |  28.713 |               20 |               0 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | CARE_native       |  100 |    96     |  91.919 |  99.029 |               96 |               0 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | CARE_native       |  100 |   100     | 100     | 100     |              100 |               0 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | MCCE_bounded      | 3914 |    83.572 |  82.302 |  84.797 |             3281 |              10 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | MCCE_bounded      | 3914 |    85.079 |  83.928 |  86.245 |             3331 |               1 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | MCCE_bounded+edit | 3914 |    83.572 |  82.302 |  84.797 |             3281 |              10 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | MCCE_bounded+edit | 3914 |    85.079 |  83.928 |  86.245 |             3331 |               1 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | MCCE_native       | 3914 |    98.39  |  97.977 |  98.771 |             3851 |               0 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | MCCE_native       | 3914 |    99.898 |  99.773 |  99.975 |             3910 |               0 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | NICE_bounded      | 3914 |    11.446 |  10.315 |  12.574 |              462 |              14 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | NICE_bounded      | 3914 |    12.954 |  11.762 |  14.079 |              507 |               0 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | NICE_bounded+edit | 3914 |    11.446 |  10.315 |  12.574 |              462 |              14 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | NICE_bounded+edit | 3914 |    12.954 |  11.762 |  14.079 |              507 |               0 | 0     |    0     |
| OULAD     | floor    | Framework (ranking + edit + gate) | NICE_native       | 3914 |    98.416 |  98     |  98.801 |             3852 |               0 | 0     |    0     |
| OULAD     | floor    | Framework + fallback              | NICE_native       | 3914 |    99.923 |  99.821 | 100     |             3911 |               0 | 0     |    0     |

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
| ('OULAD', 'aligned', 'CARE_bounded')         |                     96.4 |                         0   |                 3.6 |            0   |             0   |
| ('OULAD', 'aligned', 'CARE_bounded+edit')    |                     21.6 |                        66.7 |                11.8 |            0   |             0   |
| ('OULAD', 'aligned', 'CARE_native')          |                     73.8 |                         0   |                23.4 |            0   |             2.7 |
| ('OULAD', 'aligned', 'MCCE_bounded')         |                     47.2 |                         0   |                 0   |           52.8 |             0   |
| ('OULAD', 'aligned', 'MCCE_bounded+edit')    |                      2.1 |                         7.9 |                 0   |           90   |             0   |
| ('OULAD', 'aligned', 'MCCE_native')          |                     41.8 |                         0   |                 0   |           36.7 |            21.5 |
| ('OULAD', 'aligned', 'NICE_bounded')         |                     85.4 |                        14.6 |                 0   |            0   |             0   |
| ('OULAD', 'aligned', 'NICE_bounded+edit')    |                      0.7 |                        99.3 |                 0   |            0   |             0   |
| ('OULAD', 'aligned', 'NICE_native')          |                     62.2 |                         0   |                33.2 |            0   |             4.6 |
| ('OULAD', 'floor', 'CARE_bounded')           |                     15   |                         0   |                 2.5 |            0   |            82.5 |
| ('OULAD', 'floor', 'CARE_bounded+edit')      |                      0   |                        20   |                10   |            0   |            70   |
| ('OULAD', 'floor', 'CARE_native')            |                     56   |                         0   |                 0   |            0   |            44   |
| ('OULAD', 'floor', 'MCCE_bounded')           |                      0.1 |                         0   |                 0   |           99.8 |             0.1 |
| ('OULAD', 'floor', 'MCCE_bounded+edit')      |                      0.1 |                         0   |                 0   |           99.8 |             0.1 |
| ('OULAD', 'floor', 'MCCE_native')            |                     30.8 |                         0   |                 0   |           27   |            42.3 |
| ('OULAD', 'floor', 'NICE_bounded')           |                     40.5 |                        59.5 |                 0   |            0   |             0   |
| ('OULAD', 'floor', 'NICE_bounded+edit')      |                     40.5 |                        59.5 |                 0   |            0   |             0   |
| ('OULAD', 'floor', 'NICE_native')            |                     52.7 |                         0   |                 0.1 |            0   |            47.2 |

## Mean seconds per query
|                      |   seconds |
|:---------------------|----------:|
| ('AUC', 'CARE')      |     9.745 |
| ('AUC', 'MCCE')      |     0.02  |
| ('AUC', 'NICE')      |     0.006 |
| ('HarvardX', 'CARE') |     9.572 |
| ('HarvardX', 'MCCE') |     0.038 |
| ('HarvardX', 'NICE') |     0.005 |
| ('OULAD', 'CARE')    |    12.402 |
| ('OULAD', 'MCCE')    |     0.028 |
| ('OULAD', 'NICE')    |     0.008 |