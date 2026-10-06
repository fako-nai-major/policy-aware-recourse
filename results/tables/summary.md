## Query cohorts (mean per seed)
|                 |   n_test |   at_risk |   eligible |   evaluated |   true_fail |   seeds |
|:----------------|---------:|----------:|-----------:|------------:|------------:|--------:|
| ('AUC', 1)      |    134   |      88.3 |       88.3 |        88.3 |        0.81 |      10 |
| ('AUC', 2)      |    134   |      85.4 |       85.4 |        85.4 |        0.88 |      10 |
| ('AUC', 3)      |    134   |      85   |       85   |        85   |        0.9  |      10 |
| ('HarvardX', 0) |   2205   |    2205   |     1970.8 |       400   |        0.95 |       5 |
| ('OULAD', 1)    |   2746.2 |     340.2 |      340.2 |       300   |        0.79 |       5 |
| ('OULAD', 2)    |   2746.2 |     509.2 |      509.2 |       300   |        0.82 |       5 |
| ('OULAD', 3)    |   2746.2 |     580.2 |      580.2 |       300   |        0.86 |       5 |

## Final accepted yield (%) at the primary threshold, mean ± SD over seeds
| condition                                    | ('AUC', 'aligned')   | ('AUC', 'floor')   | ('AUC', 'mismatch')   | ('HarvardX', 'aligned')   | ('OULAD', 'aligned')   | ('OULAD', 'floor')   | ('OULAD', 'mismatch')   |
|:---------------------------------------------|:---------------------|:-------------------|:----------------------|:--------------------------|:-----------------------|:---------------------|:------------------------|
| DiCE first candidate                         | 28.0 ± 3.8           | 26.6 ± 3.2         | 28.0 ± 3.8            | 98.5 ± 0.4                | 34.5 ± 3.6             | 7.7 ± 1.1            | 7.2 ± 0.6               |
| Post-hoc policy filter                       | 36.2 ± 3.2           | 34.2 ± 3.3         | 36.2 ± 3.2            | 98.5 ± 0.4                | 69.9 ± 6.4             | 15.3 ± 2.1           | 15.3 ± 1.9              |
| Post-hoc full-gate filter                    | 37.3 ± 2.9           | 35.6 ± 3.2         | 37.3 ± 2.9            | 99.9 ± 0.1                | 70.7 ± 6.5             | 20.6 ± 2.2           | 21.0 ± 2.0              |
| Policy-aware ranking (no edit)               | 36.7 ± 2.9           | 34.0 ± 3.1         | 36.0 ± 3.0            | 99.9 ± 0.1                | 70.7 ± 6.5             | 20.6 ± 2.2           | 21.0 ± 2.0              |
| Policy-aware ranking + edit (framework)      | 65.6 ± 4.2           | 64.6 ± 4.3         | 65.0 ± 4.5            | 99.9 ± 0.1                | 94.2 ± 1.2             | 82.8 ± 5.5           | 84.1 ± 5.3              |
| Framework + fallback over ranked pool        | 66.3 ± 4.4           | 66.3 ± 4.4         | 66.3 ± 4.4            | 99.9 ± 0.1                | 95.2 ± 1.0             | 86.0 ± 3.9           | 87.7 ± 4.0              |
| Direct policy repair (no DiCE)               | 11.7 ± 1.8           | 11.7 ± 1.8         | 11.7 ± 1.8            | nan                       | 17.7 ± 7.3             | 16.6 ± 4.6           | 16.6 ± 4.6              |
| Direct policy repair + classifier escalation | 65.9 ± 4.3           | 65.9 ± 4.3         | 65.9 ± 4.3            | nan                       | 91.2 ± 2.0             | 91.2 ± 2.0           | 91.2 ± 2.0              |
| Policy reachable within bounds (upper bound) | 67.7 ± 4.3           | 67.7 ± 4.3         | 67.7 ± 4.3            | nan                       | 96.2 ± 0.7             | 96.2 ± 0.7           | 96.2 ± 0.7              |

## Characteristics of accepted recommendations (normalised effort, #changed, policy score)
|                                       |   ('effort', 'aligned') |   ('effort', 'floor') |   ('effort', 'mismatch') |   ('sparsity', 'aligned') |   ('sparsity', 'floor') |   ('sparsity', 'mismatch') |   ('score', 'aligned') |   ('score', 'floor') |   ('score', 'mismatch') |
|:--------------------------------------|------------------------:|----------------------:|-------------------------:|--------------------------:|------------------------:|---------------------------:|-----------------------:|---------------------:|------------------------:|
| ('AUC', 'dice_first')                 |                   1.849 |                 2.822 |                    2.908 |                     1.967 |                   1.934 |                      1.967 |                 15.573 |               15.539 |                  15.573 |
| ('AUC', 'policy_repair')              |                   1.349 |                 2.249 |                    2.249 |                     1.464 |                   1.464 |                      1.464 |                 15.001 |               15.001 |                  15.001 |
| ('AUC', 'policy_repair_escalate')     |                   2.181 |                 3.635 |                    3.635 |                     2.321 |                   2.321 |                      2.321 |                 15.787 |               15.787 |                  15.787 |
| ('AUC', 'posthoc_full_gate')          |                   1.921 |                 2.945 |                    3.045 |                     2.035 |                   1.992 |                      2.035 |                 15.561 |               15.534 |                  15.561 |
| ('AUC', 'posthoc_policy_filter')      |                   1.922 |                 2.942 |                    3.048 |                     2.038 |                   1.994 |                      2.038 |                 15.564 |               15.537 |                  15.564 |
| ('AUC', 'rank_edit')                  |                   2.092 |                 3.476 |                    3.469 |                     2.339 |                   2.359 |                      2.346 |                 15.259 |               15.2   |                  15.21  |
| ('AUC', 'rank_edit_fallback')         |                   2.091 |                 3.459 |                    3.456 |                     2.337 |                   2.347 |                      2.337 |                 15.26  |               15.202 |                  15.211 |
| ('AUC', 'rank_only')                  |                   1.651 |                 2.655 |                    2.735 |                     1.818 |                   1.781 |                      1.821 |                 15.228 |               15.22  |                  15.228 |
| ('HarvardX', 'dice_first')            |                   1.404 |               nan     |                  nan     |                     1.928 |                 nan     |                    nan     |                  0     |              nan     |                 nan     |
| ('HarvardX', 'posthoc_full_gate')     |                   1.412 |               nan     |                  nan     |                     1.935 |                 nan     |                    nan     |                  0     |              nan     |                 nan     |
| ('HarvardX', 'posthoc_policy_filter') |                   1.404 |               nan     |                  nan     |                     1.928 |                 nan     |                    nan     |                  0     |              nan     |                 nan     |
| ('HarvardX', 'rank_edit')             |                   0.843 |               nan     |                  nan     |                     1.629 |                 nan     |                    nan     |                  0     |              nan     |                 nan     |
| ('HarvardX', 'rank_edit_fallback')    |                   0.843 |               nan     |                  nan     |                     1.629 |                 nan     |                    nan     |                  0     |              nan     |                 nan     |
| ('HarvardX', 'rank_only')             |                   0.843 |               nan     |                  nan     |                     1.629 |                 nan     |                    nan     |                  0     |              nan     |                 nan     |
| ('OULAD', 'dice_first')               |                   1.706 |                 2.359 |                    2.47  |                     1.999 |                   1.914 |                      1.926 |                 50.401 |               55.314 |                  56.342 |
| ('OULAD', 'policy_repair')            |                   1.443 |                 3.124 |                    3.124 |                     1.995 |                   4.035 |                      4.035 |                 40     |               41.924 |                  41.924 |
| ('OULAD', 'policy_repair_escalate')   |                   1.955 |                 4.507 |                    4.507 |                     2.458 |                   5.077 |                      5.077 |                 51.686 |               52.732 |                  52.732 |
| ('OULAD', 'posthoc_full_gate')        |                   1.802 |                 2.581 |                    2.613 |                     2.088 |                   1.963 |                      1.968 |                 49.898 |               56.411 |                  56.716 |
| ('OULAD', 'posthoc_policy_filter')    |                   1.8   |                 2.559 |                    2.618 |                     2.086 |                   1.948 |                      1.954 |                 49.941 |               53.887 |                  54.364 |
| ('OULAD', 'rank_edit')                |                   1.776 |                 4.464 |                    4.529 |                     2.263 |                   4.649 |                      4.693 |                 44.949 |               55.908 |                  56.049 |
| ('OULAD', 'rank_edit_fallback')       |                   1.782 |                 4.516 |                    4.596 |                     2.27  |                   4.705 |                      4.768 |                 44.911 |               55.903 |                  56.097 |
| ('OULAD', 'rank_only')                |                   1.584 |                 2.286 |                    2.298 |                     1.992 |                   1.882 |                      1.876 |                 46.259 |               52.419 |                  52.721 |

## Yield by stage (aligned bounds, %)
| condition                                    |   ('AUC', 1) |   ('AUC', 2) |   ('AUC', 3) |   ('HarvardX', 0) |   ('OULAD', 1) |   ('OULAD', 2) |   ('OULAD', 3) |
|:---------------------------------------------|-------------:|-------------:|-------------:|------------------:|---------------:|---------------:|---------------:|
| DiCE first candidate                         |          3.9 |         50   |         30.7 |              98.5 |           28.3 |           37.3 |           38   |
| Post-hoc policy filter                       |         11.6 |         62.4 |         35.4 |              98.5 |           69.1 |           80.1 |           60.3 |
| Post-hoc full-gate filter                    |         11.9 |         63.9 |         36.8 |              99.9 |           69.9 |           80.9 |           61.4 |
| Policy-aware ranking (no edit)               |         11.7 |         62.9 |         36.2 |              99.9 |           69.9 |           80.9 |           61.3 |
| Policy-aware ranking + edit (framework)      |         96.3 |         63   |         36.2 |              99.9 |           98.3 |           98.9 |           85.5 |
| Framework + fallback over ranked pool        |         96.5 |         64.1 |         36.8 |              99.9 |           99.4 |           99.4 |           86.7 |
| Direct policy repair (no DiCE)               |          0.6 |         15.3 |         19.8 |             nan   |           13   |           22.3 |           17.7 |
| Direct policy repair + classifier escalation |         96.5 |         64.1 |         35.9 |             nan   |          100   |           99.4 |           74.1 |

## Framework rejection reasons (% of rejected)
|                         |   below_policy_threshold |   classifier_target_not_met |   no_candidate |   out_of_bounds |
|:------------------------|-------------------------:|----------------------------:|---------------:|----------------:|
| ('AUC', 'aligned')      |                     42.8 |                         0   |           57.2 |             0   |
| ('AUC', 'floor')        |                     44.4 |                         0   |           55.6 |             0   |
| ('AUC', 'mismatch')     |                     43.8 |                         0   |           56.2 |             0   |
| ('HarvardX', 'aligned') |                      0   |                         0   |          100   |             0   |
| ('OULAD', 'aligned')    |                     87.3 |                        12.7 |            0   |             0   |
| ('OULAD', 'floor')      |                     29.8 |                        13.5 |            0   |            56.6 |
| ('OULAD', 'mismatch')   |                     32.5 |                        17.9 |            0   |            49.6 |

## Paired comparisons (McNemar, learner-cluster bootstrap 95% CI, Holm-adjusted)
| dataset   | regime   | method                                  | baseline                                     |    n |   diff_pp |   ci_lo |   ci_hi |   only_method |   only_baseline |     p |   p_holm |
|:----------|:---------|:----------------------------------------|:---------------------------------------------|-----:|----------:|--------:|--------:|--------------:|----------------:|------:|---------:|
| AUC       | aligned  | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 2587 |    37.65  |  36.307 |  39.07  |           980 |               6 | 0     |    0     |
| AUC       | aligned  | Framework + fallback over ranked pool   | DiCE first candidate                         | 2587 |    38.268 |  36.911 |  39.697 |           990 |               0 | 0     |    0     |
| AUC       | aligned  | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 2587 |    28.295 |  27.184 |  29.432 |           748 |              16 | 0     |    0     |
| AUC       | aligned  | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 2587 |    28.914 |  27.818 |  30.028 |           748 |               0 | 0     |    0     |
| AUC       | aligned  | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 2587 |    28.914 |  27.818 |  30.028 |           748 |               0 | 0     |    0     |
| AUC       | aligned  | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 2587 |    29.532 |  28.367 |  30.669 |           764 |               0 | 0     |    0     |
| AUC       | aligned  | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 2587 |    -0.309 |  -0.661 |   0.039 |             8 |              16 | 0.152 |    0.91  |
| AUC       | aligned  | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 2587 |     0.309 |   0.116 |   0.543 |             8 |               0 | 0.008 |    0.07  |
| AUC       | aligned  | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 2587 |    -0.618 |  -0.932 |  -0.345 |             0 |              16 | 0     |    0     |
| AUC       | floor    | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 2587 |    37.998 |  36.568 |  39.469 |          1014 |              31 | 0     |    0     |
| AUC       | floor    | Framework + fallback over ranked pool   | DiCE first candidate                         | 2587 |    39.66  |  38.316 |  41.109 |          1026 |               0 | 0     |    0     |
| AUC       | floor    | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 2587 |    28.952 |  27.757 |  30.112 |           791 |              42 | 0     |    0     |
| AUC       | floor    | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 2587 |    30.615 |  29.564 |  31.677 |           792 |               0 | 0     |    0     |
| AUC       | floor    | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 2587 |    30.576 |  29.525 |  31.626 |           791 |               0 | 0     |    0     |
| AUC       | floor    | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 2587 |    32.238 |  31.108 |  33.425 |           834 |               0 | 0     |    0     |
| AUC       | floor    | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 2587 |    -1.353 |  -1.902 |  -0.845 |             9 |              44 | 0     |    0     |
| AUC       | floor    | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 2587 |     0.309 |   0.079 |   0.576 |             9 |               1 | 0.021 |    0.15  |
| AUC       | floor    | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 2587 |    -1.662 |  -2.195 |  -1.168 |             0 |              43 | 0     |    0     |
| AUC       | mismatch | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 2587 |    36.993 |  35.637 |  38.42  |           975 |              18 | 0     |    0     |
| AUC       | mismatch | Framework + fallback over ranked pool   | DiCE first candidate                         | 2587 |    38.268 |  36.911 |  39.697 |           990 |               0 | 0     |    0     |
| AUC       | mismatch | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 2587 |    27.638 |  26.5   |  28.808 |           748 |              33 | 0     |    0     |
| AUC       | mismatch | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 2587 |    28.914 |  27.818 |  30.028 |           748 |               0 | 0     |    0     |
| AUC       | mismatch | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 2587 |    28.914 |  27.818 |  30.028 |           748 |               0 | 0     |    0     |
| AUC       | mismatch | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 2587 |    30.189 |  28.982 |  31.365 |           781 |               0 | 0     |    0     |
| AUC       | mismatch | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 2587 |    -0.966 |  -1.436 |  -0.534 |             7 |              32 | 0     |    0.001 |
| AUC       | mismatch | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 2587 |     0.309 |   0.116 |   0.543 |             8 |               0 | 0.008 |    0.07  |
| AUC       | mismatch | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 2587 |    -1.276 |  -1.724 |  -0.895 |             0 |              33 | 0     |    0     |
| HarvardX  | aligned  | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 1999 |     1.351 |   0.899 |   1.901 |            27 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework + fallback over ranked pool   | DiCE first candidate                         | 1999 |     1.351 |   0.899 |   1.901 |            27 |               0 | 0     |    0     |
| HarvardX  | aligned  | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 1999 |     0     |   0     |   0     |             0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 1999 |     0     |   0     |   0     |             0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 1999 |     0     |   0     |   0     |             0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 1999 |     0     |   0     |   0     |             0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 1999 |     0     |   0     |   0     |             0 |               0 | 1     |    1     |
| OULAD     | aligned  | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 4500 |    59.733 |  58.27  |  61.227 |          2688 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback over ranked pool   | DiCE first candidate                         | 4500 |    60.644 |  59.164 |  62.128 |          2729 |               0 | 0     |    0     |
| OULAD     | aligned  | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 4500 |    23.533 |  22.071 |  24.961 |          1059 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 4500 |    24.444 |  22.995 |  25.851 |          1100 |               0 | 0     |    0     |
| OULAD     | aligned  | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 4500 |    23.556 |  22.127 |  24.967 |          1060 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 4500 |    24.467 |  23.039 |  25.87  |          1101 |               0 | 0     |    0     |
| OULAD     | aligned  | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 4500 |     3.089 |   2.337 |   3.871 |           210 |              71 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 4500 |     4     |   3.328 |   4.739 |           220 |              40 | 0     |    0     |
| OULAD     | aligned  | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 4500 |    -0.911 |  -1.208 |  -0.646 |             0 |              41 | 0     |    0     |
| OULAD     | floor    | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 4500 |    75.044 |  73.743 |  76.304 |          3377 |               0 | 0     |    0     |
| OULAD     | floor    | Framework + fallback over ranked pool   | DiCE first candidate                         | 4500 |    78.222 |  77.028 |  79.393 |          3520 |               0 | 0     |    0     |
| OULAD     | floor    | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 4500 |    62.178 |  60.799 |  63.611 |          2798 |               0 | 0     |    0     |
| OULAD     | floor    | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 4500 |    65.356 |  63.976 |  66.696 |          2941 |               0 | 0     |    0     |
| OULAD     | floor    | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 4500 |    62.178 |  60.799 |  63.611 |          2798 |               0 | 0     |    0     |
| OULAD     | floor    | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 4500 |    65.356 |  63.976 |  66.696 |          2941 |               0 | 0     |    0     |
| OULAD     | floor    | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 4500 |    -8.378 |  -9.769 |  -7.113 |           208 |             585 | 0     |    0     |
| OULAD     | floor    | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 4500 |    -5.2   |  -6.482 |  -3.996 |           220 |             454 | 0     |    0     |
| OULAD     | floor    | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 4500 |    -3.178 |  -3.7   |  -2.659 |             0 |             143 | 0     |    0     |
| OULAD     | mismatch | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 4500 |    76.844 |  75.626 |  78.099 |          3458 |               0 | 0     |    0     |
| OULAD     | mismatch | Framework + fallback over ranked pool   | DiCE first candidate                         | 4500 |    80.422 |  79.286 |  81.577 |          3619 |               0 | 0     |    0     |
| OULAD     | mismatch | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 4500 |    63.111 |  61.791 |  64.476 |          2840 |               0 | 0     |    0     |
| OULAD     | mismatch | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 4500 |    66.689 |  65.41  |  68.069 |          3001 |               0 | 0     |    0     |
| OULAD     | mismatch | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 4500 |    63.111 |  61.791 |  64.476 |          2840 |               0 | 0     |    0     |
| OULAD     | mismatch | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 4500 |    66.689 |  65.41  |  68.069 |          3001 |               0 | 0     |    0     |
| OULAD     | mismatch | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 4500 |    -7.067 |  -8.393 |  -5.837 |           209 |             527 | 0     |    0     |
| OULAD     | mismatch | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 4500 |    -3.489 |  -4.62  |  -2.352 |           220 |             377 | 0     |    0     |
| OULAD     | mismatch | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 4500 |    -3.578 |  -4.161 |  -3.028 |             0 |             161 | 0     |    0     |

## Objective audit (leave-one-term-out and lambda sweep)
| dataset   | regime   | variant     | yield_      |   changed_selection_pct |   mean_effort_accepted |
|:----------|:---------|:------------|:------------|------------------------:|-----------------------:|
| AUC       | aligned  | drop_feas   | 56.1 ± 3.9  |                    18.8 |                  1.998 |
| AUC       | aligned  | drop_policy | 52.0 ± 5.2  |                    78   |                  2.191 |
| AUC       | aligned  | drop_prox   | 66.1 ± 4.3  |                     0.5 |                  2.091 |
| AUC       | aligned  | drop_spar   | 65.6 ± 4.2  |                     0   |                  2.092 |
| AUC       | aligned  | lp_1        | 52.0 ± 5.2  |                    78   |                  2.191 |
| AUC       | aligned  | lp_10       | 57.1 ± 5.5  |                    14.3 |                  2.151 |
| AUC       | aligned  | lp_100      | 61.4 ± 4.8  |                     7.9 |                  2.117 |
| AUC       | aligned  | lx_0.1      | 66.1 ± 4.3  |                     0.5 |                  2.091 |
| AUC       | aligned  | lx_10       | 61.6 ± 4.9  |                     7.2 |                  2.116 |
| AUC       | aligned  | rank_edit   | 65.6 ± 4.2  |                     0   |                  2.092 |
| AUC       | floor    | drop_feas   | 53.8 ± 4.5  |                    21.2 |                  3.294 |
| AUC       | floor    | drop_policy | 51.0 ± 5.4  |                    73.3 |                  3.645 |
| AUC       | floor    | drop_prox   | 66.1 ± 4.4  |                     1.8 |                  3.459 |
| AUC       | floor    | drop_spar   | 64.6 ± 4.3  |                     0   |                  3.476 |
| AUC       | floor    | lp_1        | 51.0 ± 5.4  |                    73.3 |                  3.645 |
| AUC       | floor    | lp_10       | 53.6 ± 4.6  |                    16.5 |                  3.607 |
| AUC       | floor    | lp_100      | 60.5 ± 4.2  |                     6.6 |                  3.515 |
| AUC       | floor    | lx_0.1      | 66.1 ± 4.4  |                     1.8 |                  3.459 |
| AUC       | floor    | lx_10       | 60.5 ± 4.2  |                     6.5 |                  3.515 |
| AUC       | floor    | rank_edit   | 64.6 ± 4.3  |                     0   |                  3.476 |
| AUC       | mismatch | drop_feas   | 55.5 ± 4.0  |                    18.8 |                  3.315 |
| AUC       | mismatch | drop_policy | 50.6 ± 5.4  |                    72.1 |                  3.634 |
| AUC       | mismatch | drop_prox   | 66.1 ± 4.3  |                     1.3 |                  3.457 |
| AUC       | mismatch | drop_spar   | 65.0 ± 4.5  |                     0   |                  3.469 |
| AUC       | mismatch | lp_1        | 50.6 ± 5.4  |                    72.1 |                  3.634 |
| AUC       | mismatch | lp_10       | 53.1 ± 5.0  |                    18.5 |                  3.604 |
| AUC       | mismatch | lp_100      | 60.9 ± 4.7  |                     7.7 |                  3.513 |
| AUC       | mismatch | lx_0.1      | 66.1 ± 4.3  |                     1.3 |                  3.457 |
| AUC       | mismatch | lx_10       | 61.1 ± 4.8  |                     7   |                  3.51  |
| AUC       | mismatch | rank_edit   | 65.0 ± 4.5  |                     0   |                  3.469 |
| HarvardX  | aligned  | drop_feas   | 99.8 ± 0.2  |                     0.1 |                  0.843 |
| HarvardX  | aligned  | drop_policy | 99.9 ± 0.1  |                     0   |                  0.843 |
| HarvardX  | aligned  | drop_prox   | 99.9 ± 0.1  |                     0.7 |                  0.845 |
| HarvardX  | aligned  | drop_spar   | 99.9 ± 0.1  |                     3.9 |                  0.836 |
| HarvardX  | aligned  | lp_1        | 99.9 ± 0.1  |                     0   |                  0.843 |
| HarvardX  | aligned  | lp_10       | 99.9 ± 0.1  |                     0   |                  0.843 |
| HarvardX  | aligned  | lp_100      | 99.9 ± 0.1  |                     0   |                  0.843 |
| HarvardX  | aligned  | lx_0.1      | 99.9 ± 0.1  |                     0.2 |                  0.843 |
| HarvardX  | aligned  | lx_10       | 99.9 ± 0.1  |                     3.1 |                  0.837 |
| HarvardX  | aligned  | rank_edit   | 99.9 ± 0.1  |                     0   |                  0.843 |
| OULAD     | aligned  | drop_feas   | 91.0 ± 1.4  |                     3.7 |                  1.749 |
| OULAD     | aligned  | drop_policy | 78.8 ± 10.6 |                    77.6 |                  1.735 |
| OULAD     | aligned  | drop_prox   | 94.2 ± 1.2  |                     3.8 |                  1.788 |
| OULAD     | aligned  | drop_spar   | 94.2 ± 1.2  |                     0.6 |                  1.776 |
| OULAD     | aligned  | lp_1        | 83.7 ± 5.5  |                    64.9 |                  1.689 |
| OULAD     | aligned  | lp_10       | 92.9 ± 1.4  |                    11.5 |                  1.749 |
| OULAD     | aligned  | lp_100      | 94.1 ± 1.3  |                     0.9 |                  1.775 |
| OULAD     | aligned  | lx_0.1      | 94.2 ± 1.2  |                     0   |                  1.777 |
| OULAD     | aligned  | lx_10       | 94.1 ± 1.3  |                     1.1 |                  1.775 |
| OULAD     | aligned  | rank_edit   | 94.2 ± 1.2  |                     0   |                  1.776 |
| OULAD     | floor    | drop_feas   | 80.4 ± 4.7  |                    12.8 |                  4.402 |
| OULAD     | floor    | drop_policy | 71.9 ± 6.0  |                    50.4 |                  4.042 |
| OULAD     | floor    | drop_prox   | 82.8 ± 5.5  |                     2.6 |                  4.481 |
| OULAD     | floor    | drop_spar   | 82.8 ± 5.5  |                     1   |                  4.462 |
| OULAD     | floor    | lp_1        | 73.6 ± 4.2  |                    48.9 |                  4.134 |
| OULAD     | floor    | lp_10       | 81.0 ± 5.6  |                     7.5 |                  4.446 |
| OULAD     | floor    | lp_100      | 82.7 ± 5.4  |                     0.7 |                  4.464 |
| OULAD     | floor    | lx_0.1      | 82.8 ± 5.5  |                     0.1 |                  4.465 |
| OULAD     | floor    | lx_10       | 82.7 ± 5.4  |                     1.3 |                  4.462 |
| OULAD     | floor    | rank_edit   | 82.8 ± 5.5  |                     0   |                  4.464 |
| OULAD     | mismatch | drop_feas   | 81.7 ± 5.1  |                    13.8 |                  4.465 |
| OULAD     | mismatch | drop_policy | 71.6 ± 6.2  |                    49.6 |                  4.052 |
| OULAD     | mismatch | drop_prox   | 84.1 ± 5.3  |                     2.6 |                  4.548 |
| OULAD     | mismatch | drop_spar   | 84.1 ± 5.3  |                     0.3 |                  4.529 |
| OULAD     | mismatch | lp_1        | 73.5 ± 5.0  |                    47.4 |                  4.161 |
| OULAD     | mismatch | lp_10       | 82.3 ± 5.0  |                     7.7 |                  4.499 |
| OULAD     | mismatch | lp_100      | 83.8 ± 5.4  |                     0.8 |                  4.53  |
| OULAD     | mismatch | lx_0.1      | 84.1 ± 5.3  |                     0   |                  4.529 |
| OULAD     | mismatch | lx_10       | 83.9 ± 5.4  |                     0.9 |                  4.529 |
| OULAD     | mismatch | rank_edit   | 84.1 ± 5.3  |                     0   |                  4.529 |

## Threshold sensitivity (aligned bounds)
|                 | DiCE first candidate   | Direct policy repair + classifier escalation   | Post-hoc full-gate filter   | Policy-aware ranking + edit (framework)   | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)   |
|:----------------|:-----------------------|:-----------------------------------------------|:----------------------------|:------------------------------------------|:----------------------------------------|:---------------------------------|
| ('AUC', 12.5)   | 37.3 ± 2.6             | 72.0 ± 3.0                                     | 43.1 ± 3.2                  | 72.5 ± 3.0                                | 72.5 ± 3.0                              | 43.1 ± 3.2                       |
| ('AUC', 15.001) | 28.0 ± 3.8             | 65.9 ± 4.3                                     | 37.3 ± 2.9                  | 65.6 ± 4.2                                | 66.3 ± 4.4                              | 36.7 ± 2.9                       |
| ('AUC', 16.0)   | 4.3 ± 1.0              | 50.4 ± 3.6                                     | 16.9 ± 1.9                  | 45.5 ± 3.3                                | 47.6 ± 3.4                              | 16.6 ± 1.9                       |
| ('AUC', 17.0)   | 0.0 ± 0.0              | 20.3 ± 3.2                                     | 0.0 ± 0.0                   | 17.4 ± 2.8                                | 17.5 ± 2.7                              | 0.0 ± 0.0                        |
| ('OULAD', 30.0) | 64.1 ± 6.7             | 90.5 ± 1.6                                     | 93.6 ± 3.0                  | 98.3 ± 0.3                                | 98.3 ± 0.3                              | 93.6 ± 3.0                       |
| ('OULAD', 40.0) | 34.5 ± 3.6             | 91.2 ± 2.0                                     | 70.7 ± 6.5                  | 94.2 ± 1.2                                | 95.2 ± 1.0                              | 70.7 ± 6.5                       |
| ('OULAD', 50.0) | 15.1 ± 1.2             | 89.8 ± 2.2                                     | 47.3 ± 5.0                  | 87.0 ± 2.7                                | 89.5 ± 3.2                              | 47.3 ± 5.0                       |
| ('OULAD', 60.0) | 4.4 ± 1.1              | 85.0 ± 1.4                                     | 21.4 ± 3.3                  | 60.7 ± 5.4                                | 64.7 ± 6.0                              | 21.4 ± 3.3                       |

## DiCE pools
|                         |   queries |   with_pool |   mean_pool |   pool_policy_valid |
|:------------------------|----------:|------------:|------------:|--------------------:|
| ('AUC', 'aligned')      |      2587 |      80.286 |       8.027 |               0.355 |
| ('AUC', 'floor')        |      2587 |      80.286 |       8.029 |               0.347 |
| ('AUC', 'mismatch')     |      2587 |      80.286 |       8.027 |               0.355 |
| ('HarvardX', 'aligned') |      1999 |      99.9   |       9.99  |             nan     |
| ('OULAD', 'aligned')    |      4500 |     100     |      10     |               0.347 |
| ('OULAD', 'floor')      |      4500 |     100     |      10     |               0.339 |
| ('OULAD', 'mismatch')   |      4500 |     100     |      10     |               0.347 |

## Best model per stage (mean ROC-AUC over grouped folds)
| dataset   | stage   | sampler   | model   |   roc_auc |
|:----------|:--------|:----------|:--------|----------:|
| AUC       | 1       | nearmiss  | MLP     |     0.822 |
| AUC       | 2       | nearmiss  | Ridge   |     0.93  |
| AUC       | 3       | none      | MLP     |     0.948 |
| AUC       | full    | none      | MLP     |     1     |
| HarvardX  | full    | smote     | MLP     |     0.96  |
| OULAD     | 1       | none      | MLP     |     0.747 |
| OULAD     | 2       | none      | MLP     |     0.843 |
| OULAD     | 3       | none      | MLP     |     0.89  |
| OULAD     | full    | none      | MLP     |     0.953 |

## CatBoost (grouped 5-fold, mean ± SD)
|                                  | roc_auc       | bal_acc       | f1_macro      | recall_fail   |
|:---------------------------------|:--------------|:--------------|:--------------|:--------------|
| ('AUC', '1', 'nearmiss')         | 0.739 ± 0.058 | 0.722 ± 0.031 | 0.663 ± 0.033 | 0.519 ± 0.057 |
| ('AUC', '1', 'none')             | 0.811 ± 0.035 | 0.720 ± 0.033 | 0.723 ± 0.031 | 0.833 ± 0.061 |
| ('AUC', '1', 'smote')            | 0.804 ± 0.035 | 0.734 ± 0.061 | 0.696 ± 0.054 | 0.614 ± 0.066 |
| ('AUC', '2', 'nearmiss')         | 0.881 ± 0.030 | 0.822 ± 0.025 | 0.812 ± 0.026 | 0.823 ± 0.064 |
| ('AUC', '2', 'none')             | 0.919 ± 0.021 | 0.833 ± 0.027 | 0.827 ± 0.020 | 0.853 ± 0.044 |
| ('AUC', '2', 'smote')            | 0.916 ± 0.019 | 0.830 ± 0.022 | 0.819 ± 0.021 | 0.830 ± 0.058 |
| ('AUC', '3', 'nearmiss')         | 0.912 ± 0.038 | 0.842 ± 0.037 | 0.830 ± 0.031 | 0.830 ± 0.033 |
| ('AUC', '3', 'none')             | 0.937 ± 0.024 | 0.856 ± 0.047 | 0.849 ± 0.042 | 0.870 ± 0.044 |
| ('AUC', '3', 'smote')            | 0.931 ± 0.024 | 0.864 ± 0.017 | 0.854 ± 0.017 | 0.858 ± 0.042 |
| ('AUC', 'full', 'nearmiss')      | 0.998 ± 0.002 | 0.974 ± 0.014 | 0.968 ± 0.015 | 0.960 ± 0.016 |
| ('AUC', 'full', 'none')          | 0.999 ± 0.001 | 0.986 ± 0.017 | 0.984 ± 0.015 | 0.984 ± 0.010 |
| ('AUC', 'full', 'smote')         | 0.999 ± 0.001 | 0.986 ± 0.018 | 0.984 ± 0.017 | 0.984 ± 0.016 |
| ('HarvardX', 'full', 'nearmiss') | 0.943 ± 0.006 | 0.832 ± 0.008 | 0.826 ± 0.007 | 0.957 ± 0.005 |
| ('HarvardX', 'full', 'none')     | 0.958 ± 0.003 | 0.810 ± 0.008 | 0.818 ± 0.005 | 0.962 ± 0.003 |
| ('HarvardX', 'full', 'smote')    | 0.956 ± 0.003 | 0.891 ± 0.007 | 0.825 ± 0.006 | 0.921 ± 0.004 |
| ('OULAD', '1', 'nearmiss')       | 0.644 ± 0.010 | 0.528 ± 0.005 | 0.314 ± 0.015 | 0.972 ± 0.007 |
| ('OULAD', '1', 'none')           | 0.744 ± 0.008 | 0.647 ± 0.008 | 0.661 ± 0.010 | 0.330 ± 0.020 |
| ('OULAD', '1', 'smote')          | 0.742 ± 0.009 | 0.676 ± 0.008 | 0.677 ± 0.008 | 0.542 ± 0.018 |
| ('OULAD', '2', 'nearmiss')       | 0.809 ± 0.010 | 0.736 ± 0.008 | 0.752 ± 0.007 | 0.556 ± 0.027 |
| ('OULAD', '2', 'none')           | 0.838 ± 0.006 | 0.732 ± 0.010 | 0.755 ± 0.010 | 0.511 ± 0.026 |
| ('OULAD', '2', 'smote')          | 0.836 ± 0.007 | 0.754 ± 0.004 | 0.760 ± 0.003 | 0.631 ± 0.017 |
| ('OULAD', '3', 'nearmiss')       | 0.868 ± 0.004 | 0.791 ± 0.009 | 0.810 ± 0.007 | 0.636 ± 0.020 |
| ('OULAD', '3', 'none')           | 0.887 ± 0.003 | 0.791 ± 0.006 | 0.814 ± 0.005 | 0.622 ± 0.014 |
| ('OULAD', '3', 'smote')          | 0.886 ± 0.004 | 0.801 ± 0.003 | 0.812 ± 0.003 | 0.685 ± 0.011 |
| ('OULAD', 'full', 'nearmiss')    | 0.929 ± 0.007 | 0.869 ± 0.005 | 0.874 ± 0.006 | 0.802 ± 0.007 |
| ('OULAD', 'full', 'none')        | 0.952 ± 0.004 | 0.873 ± 0.002 | 0.888 ± 0.002 | 0.781 ± 0.004 |
| ('OULAD', 'full', 'smote')       | 0.950 ± 0.005 | 0.881 ± 0.005 | 0.886 ± 0.006 | 0.819 ± 0.007 |

## Friedman test across models (no resampling)
| dataset   | stage   |   friedman_p |   cb_rank | top   |   top_auc |   cb_auc |
|:----------|:--------|-------------:|----------:|:------|----------:|---------:|
| AUC       | 1       |       0      |       4.2 | LR    |    0.822  |   0.811  |
| AUC       | 2       |       0      |       5   | MLP   |    0.9291 |   0.9186 |
| AUC       | 3       |       0      |       5.1 | MLP   |    0.9483 |   0.9367 |
| AUC       | full    |       0.0001 |       5.2 | MLP   |    0.9999 |   0.9987 |
| HarvardX  | full    |       0      |       2.2 | MLP   |    0.9599 |   0.9578 |
| OULAD     | 1       |       0      |       3   | MLP   |    0.7468 |   0.7442 |
| OULAD     | 2       |       0      |       4.8 | MLP   |    0.8435 |   0.838  |
| OULAD     | 3       |       0      |       2.6 | MLP   |    0.8899 |   0.8874 |
| OULAD     | full    |       0      |       3.8 | MLP   |    0.9529 |   0.952  |
