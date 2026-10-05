## Query cohorts (mean per seed)
|                 |   n_test |   at_risk |   eligible |   evaluated |   true_fail |   seeds |
|:----------------|---------:|----------:|-----------:|------------:|------------:|--------:|
| ('AUC', 1)      |    134   |      88.3 |       88.3 |        88.3 |        0.81 |      10 |
| ('AUC', 2)      |    134   |      85.4 |       85.4 |        85.4 |        0.88 |      10 |
| ('AUC', 3)      |    134   |      85   |       85   |        85   |        0.9  |      10 |
| ('HarvardX', 0) |   2205   |    2205   |     1970.8 |       400   |        0.95 |       5 |
| ('OULAD', 1)    |   2759.6 |     182.8 |      182.8 |       182.8 |        0.61 |       5 |
| ('OULAD', 2)    |   2759.6 |     404.6 |      404.6 |       300   |        0.73 |       5 |
| ('OULAD', 3)    |   2759.6 |     517.8 |      517.8 |       300   |        0.82 |       5 |

## Final accepted yield (%) at the primary threshold, mean ± SD over seeds
| condition                                    | ('AUC', 'aligned')   | ('AUC', 'floor')   | ('AUC', 'mismatch')   | ('HarvardX', 'aligned')   | ('OULAD', 'aligned')   | ('OULAD', 'floor')   | ('OULAD', 'mismatch')   |
|:---------------------------------------------|:---------------------|:-------------------|:----------------------|:--------------------------|:-----------------------|:---------------------|:------------------------|
| DiCE first candidate                         | 28.0 ± 3.8           | 26.6 ± 3.2         | 28.0 ± 3.8            | 98.5 ± 0.4                | 76.5 ± 2.1             | 0.3 ± 0.1            | 0.3 ± 0.1               |
| Post-hoc policy filter                       | 36.2 ± 3.2           | 34.2 ± 3.3         | 36.2 ± 3.2            | 98.5 ± 0.4                | 97.1 ± 0.8             | 0.5 ± 0.1            | 0.5 ± 0.2               |
| Post-hoc full-gate filter                    | 37.3 ± 2.9           | 35.6 ± 3.2         | 37.3 ± 2.9            | 99.9 ± 0.1                | 99.3 ± 0.4             | 0.7 ± 0.2            | 0.7 ± 0.2               |
| Policy-aware ranking (no edit)               | 36.7 ± 2.9           | 34.0 ± 3.1         | 36.0 ± 3.0            | 99.9 ± 0.1                | 99.2 ± 0.5             | 0.7 ± 0.2            | 0.7 ± 0.2               |
| Policy-aware ranking + edit (framework)      | 65.6 ± 4.2           | 64.6 ± 4.3         | 65.0 ± 4.5            | 99.9 ± 0.1                | 99.9 ± 0.1             | 98.5 ± 1.4           | 98.6 ± 1.2              |
| Framework + fallback over ranked pool        | 66.3 ± 4.4           | 66.3 ± 4.4         | 66.3 ± 4.4            | 99.9 ± 0.1                | 100.0 ± 0.0            | 99.9 ± 0.1           | 99.9 ± 0.1              |
| Direct policy repair (no DiCE)               | 11.7 ± 1.8           | 11.7 ± 1.8         | 11.7 ± 1.8            | nan                       | 36.1 ± 9.4             | 84.8 ± 8.4           | 84.8 ± 8.4              |
| Direct policy repair + classifier escalation | 65.9 ± 4.3           | 65.9 ± 4.3         | 65.9 ± 4.3            | nan                       | 91.2 ± 8.6             | 99.6 ± 0.3           | 99.6 ± 0.3              |
| Policy reachable within bounds (upper bound) | 67.7 ± 4.3           | 67.7 ± 4.3         | 67.7 ± 4.3            | nan                       | 100.0 ± 0.0            | 100.0 ± 0.0          | 100.0 ± 0.0             |

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
| ('OULAD', 'dice_first')               |                   1.287 |                 2.496 |                    2.402 |                     1.76  |                   2     |                      2     |                 78.63  |               53.125 |                  55.01  |
| ('OULAD', 'policy_repair')            |                   0.803 |                 2.586 |                    2.586 |                     1.391 |                   3.874 |                      3.874 |                 40     |               72.492 |                  72.492 |
| ('OULAD', 'policy_repair_escalate')   |                   0.686 |                 2.655 |                    2.655 |                     1.275 |                   3.828 |                      3.828 |                 49.424 |               70.951 |                  70.951 |
| ('OULAD', 'posthoc_full_gate')        |                   1.344 |                 2.58  |                    2.466 |                     1.793 |                   2     |                      2     |                 73.297 |               55.71  |                  54.146 |
| ('OULAD', 'posthoc_policy_filter')    |                   1.346 |                 2.687 |                    2.524 |                     1.795 |                   2     |                      2     |                 73.291 |               55.36  |                  53.514 |
| ('OULAD', 'rank_edit')                |                   0.873 |                 3.166 |                    3.192 |                     1.381 |                   3.836 |                      3.836 |                 59.629 |               84.174 |                  84.799 |
| ('OULAD', 'rank_edit_fallback')       |                   0.873 |                 3.17  |                    3.195 |                     1.381 |                   3.828 |                      3.828 |                 59.626 |               83.94  |                  84.616 |
| ('OULAD', 'rank_only')                |                   0.868 |                 2.067 |                    2.064 |                     1.371 |                   2     |                      2     |                 59.758 |               47.697 |                  47.843 |

## Yield by stage (aligned bounds, %)
| condition                                    |   ('AUC', 1) |   ('AUC', 2) |   ('AUC', 3) |   ('HarvardX', 0) |   ('OULAD', 1) |   ('OULAD', 2) |   ('OULAD', 3) |
|:---------------------------------------------|-------------:|-------------:|-------------:|------------------:|---------------:|---------------:|---------------:|
| DiCE first candidate                         |          3.9 |         50   |         30.7 |              98.5 |           71.2 |           77.7 |           78.7 |
| Post-hoc policy filter                       |         11.6 |         62.4 |         35.4 |              98.5 |           97.9 |           97.3 |           96.4 |
| Post-hoc full-gate filter                    |         11.9 |         63.9 |         36.8 |              99.9 |           99.2 |           99.3 |           99.3 |
| Policy-aware ranking (no edit)               |         11.7 |         62.9 |         36.2 |              99.9 |           99.2 |           99.3 |           99.2 |
| Policy-aware ranking + edit (framework)      |         96.3 |         63   |         36.2 |              99.9 |          100   |          100   |           99.9 |
| Framework + fallback over ranked pool        |         96.5 |         64.1 |         36.8 |              99.9 |          100   |          100   |          100   |
| Direct policy repair (no DiCE)               |          0.6 |         15.3 |         19.8 |             nan   |           34.1 |           33   |           40.1 |
| Direct policy repair + classifier escalation |         96.5 |         64.1 |         35.9 |             nan   |           92.8 |           88.3 |           93.1 |

## Framework rejection reasons (% of rejected)
|                         |   below_policy_threshold |   classifier_target_not_met |   no_candidate |   out_of_bounds |
|:------------------------|-------------------------:|----------------------------:|---------------:|----------------:|
| ('AUC', 'aligned')      |                     42.8 |                         0   |           57.2 |             0   |
| ('AUC', 'floor')        |                     44.4 |                         0   |           55.6 |             0   |
| ('AUC', 'mismatch')     |                     43.8 |                         0   |           56.2 |             0   |
| ('HarvardX', 'aligned') |                      0   |                         0   |          100   |             0   |
| ('OULAD', 'aligned')    |                     50   |                        50   |            0   |             0   |
| ('OULAD', 'floor')      |                      0   |                       100   |            0   |             0   |
| ('OULAD', 'mismatch')   |                      1.8 |                        96.4 |            0   |             1.8 |

## Paired comparisons (McNemar, learner-cluster bootstrap 95% CI, Holm-adjusted)
| dataset   | regime   | method                                  | baseline                                     |    n |   diff_pp |   ci_lo |   ci_hi |   only_method |   only_baseline |     p |   p_holm |
|:----------|:---------|:----------------------------------------|:---------------------------------------------|-----:|----------:|--------:|--------:|--------------:|----------------:|------:|---------:|
| AUC       | aligned  | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 2587 |    37.65  |  36.307 |  39.07  |           980 |               6 | 0     |    0     |
| AUC       | aligned  | Framework + fallback over ranked pool   | DiCE first candidate                         | 2587 |    38.268 |  36.911 |  39.697 |           990 |               0 | 0     |    0     |
| AUC       | aligned  | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 2587 |    28.295 |  27.184 |  29.432 |           748 |              16 | 0     |    0     |
| AUC       | aligned  | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 2587 |    28.914 |  27.818 |  30.028 |           748 |               0 | 0     |    0     |
| AUC       | aligned  | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 2587 |    28.914 |  27.818 |  30.028 |           748 |               0 | 0     |    0     |
| AUC       | aligned  | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 2587 |    29.532 |  28.367 |  30.669 |           764 |               0 | 0     |    0     |
| AUC       | aligned  | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 2587 |    -0.309 |  -0.661 |   0.039 |             8 |              16 | 0.152 |    1     |
| AUC       | aligned  | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 2587 |     0.309 |   0.116 |   0.543 |             8 |               0 | 0.008 |    0.086 |
| AUC       | aligned  | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 2587 |    -0.618 |  -0.932 |  -0.345 |             0 |              16 | 0     |    0     |
| AUC       | floor    | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 2587 |    37.998 |  36.568 |  39.469 |          1014 |              31 | 0     |    0     |
| AUC       | floor    | Framework + fallback over ranked pool   | DiCE first candidate                         | 2587 |    39.66  |  38.316 |  41.109 |          1026 |               0 | 0     |    0     |
| AUC       | floor    | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 2587 |    28.952 |  27.757 |  30.112 |           791 |              42 | 0     |    0     |
| AUC       | floor    | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 2587 |    30.615 |  29.564 |  31.677 |           792 |               0 | 0     |    0     |
| AUC       | floor    | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 2587 |    30.576 |  29.525 |  31.626 |           791 |               0 | 0     |    0     |
| AUC       | floor    | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 2587 |    32.238 |  31.108 |  33.425 |           834 |               0 | 0     |    0     |
| AUC       | floor    | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 2587 |    -1.353 |  -1.902 |  -0.845 |             9 |              44 | 0     |    0     |
| AUC       | floor    | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 2587 |     0.309 |   0.079 |   0.576 |             9 |               1 | 0.021 |    0.191 |
| AUC       | floor    | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 2587 |    -1.662 |  -2.195 |  -1.168 |             0 |              43 | 0     |    0     |
| AUC       | mismatch | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 2587 |    36.993 |  35.637 |  38.42  |           975 |              18 | 0     |    0     |
| AUC       | mismatch | Framework + fallback over ranked pool   | DiCE first candidate                         | 2587 |    38.268 |  36.911 |  39.697 |           990 |               0 | 0     |    0     |
| AUC       | mismatch | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 2587 |    27.638 |  26.5   |  28.808 |           748 |              33 | 0     |    0     |
| AUC       | mismatch | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 2587 |    28.914 |  27.818 |  30.028 |           748 |               0 | 0     |    0     |
| AUC       | mismatch | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 2587 |    28.914 |  27.818 |  30.028 |           748 |               0 | 0     |    0     |
| AUC       | mismatch | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 2587 |    30.189 |  28.982 |  31.365 |           781 |               0 | 0     |    0     |
| AUC       | mismatch | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 2587 |    -0.966 |  -1.436 |  -0.534 |             7 |              32 | 0     |    0.001 |
| AUC       | mismatch | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 2587 |     0.309 |   0.116 |   0.543 |             8 |               0 | 0.008 |    0.086 |
| AUC       | mismatch | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 2587 |    -1.276 |  -1.724 |  -0.895 |             0 |              33 | 0     |    0     |
| HarvardX  | aligned  | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 1999 |     1.351 |   0.899 |   1.901 |            27 |               0 | 0     |    0     |
| HarvardX  | aligned  | Framework + fallback over ranked pool   | DiCE first candidate                         | 1999 |     1.351 |   0.899 |   1.901 |            27 |               0 | 0     |    0     |
| HarvardX  | aligned  | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 1999 |     0     |   0     |   0     |             0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 1999 |     0     |   0     |   0     |             0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 1999 |     0     |   0     |   0     |             0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 1999 |     0     |   0     |   0     |             0 |               0 | 1     |    1     |
| HarvardX  | aligned  | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 1999 |     0     |   0     |   0     |             0 |               0 | 1     |    1     |
| OULAD     | aligned  | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 3914 |    23.403 |  21.964 |  24.866 |           916 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback over ranked pool   | DiCE first candidate                         | 3914 |    23.454 |  21.99  |  24.924 |           918 |               0 | 0     |    0     |
| OULAD     | aligned  | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 3914 |     0.664 |   0.433 |   0.928 |            26 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 3914 |     0.715 |   0.462 |   0.988 |            28 |               0 | 0     |    0     |
| OULAD     | aligned  | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 3914 |     0.715 |   0.467 |   0.987 |            28 |               0 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 3914 |     0.766 |   0.506 |   1.046 |            30 |               0 | 0     |    0     |
| OULAD     | aligned  | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 3914 |     8.738 |   7.617 |   9.873 |           344 |               2 | 0     |    0     |
| OULAD     | aligned  | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 3914 |     8.789 |   7.686 |   9.924 |           344 |               0 | 0     |    0     |
| OULAD     | aligned  | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 3914 |    -0.051 |  -0.128 |   0     |             0 |               2 | 0.5   |    1     |
| OULAD     | floor    | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 3914 |    98.135 |  97.704 |  98.547 |          3841 |               0 | 0     |    0     |
| OULAD     | floor    | Framework + fallback over ranked pool   | DiCE first candidate                         | 3914 |    99.642 |  99.436 |  99.821 |          3900 |               0 | 0     |    0     |
| OULAD     | floor    | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 3914 |    97.701 |  97.207 |  98.173 |          3824 |               0 | 0     |    0     |
| OULAD     | floor    | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 3914 |    99.208 |  98.914 |  99.47  |          3883 |               0 | 0     |    0     |
| OULAD     | floor    | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 3914 |    97.701 |  97.207 |  98.173 |          3824 |               0 | 0     |    0     |
| OULAD     | floor    | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 3914 |    99.208 |  98.914 |  99.47  |          3883 |               0 | 0     |    0     |
| OULAD     | floor    | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 3914 |    -1.201 |  -1.633 |  -0.818 |             9 |              56 | 0     |    0     |
| OULAD     | floor    | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 3914 |     0.307 |   0.102 |   0.52  |            14 |               2 | 0.004 |    0.05  |
| OULAD     | floor    | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 3914 |    -1.507 |  -1.905 |  -1.128 |             0 |              59 | 0     |    0     |
| OULAD     | mismatch | Policy-aware ranking + edit (framework) | DiCE first candidate                         | 3914 |    98.339 |  97.916 |  98.731 |          3849 |               0 | 0     |    0     |
| OULAD     | mismatch | Framework + fallback over ranked pool   | DiCE first candidate                         | 3914 |    99.642 |  99.413 |  99.822 |          3900 |               0 | 0     |    0     |
| OULAD     | mismatch | Policy-aware ranking + edit (framework) | Post-hoc full-gate filter                    | 3914 |    97.879 |  97.423 |  98.347 |          3831 |               0 | 0     |    0     |
| OULAD     | mismatch | Framework + fallback over ranked pool   | Post-hoc full-gate filter                    | 3914 |    99.182 |  98.872 |  99.458 |          3882 |               0 | 0     |    0     |
| OULAD     | mismatch | Policy-aware ranking + edit (framework) | Policy-aware ranking (no edit)               | 3914 |    97.879 |  97.423 |  98.347 |          3831 |               0 | 0     |    0     |
| OULAD     | mismatch | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)               | 3914 |    99.182 |  98.872 |  99.458 |          3882 |               0 | 0     |    0     |
| OULAD     | mismatch | Policy-aware ranking + edit (framework) | Direct policy repair + classifier escalation | 3914 |    -1.048 |  -1.435 |  -0.662 |             9 |              50 | 0     |    0     |
| OULAD     | mismatch | Framework + fallback over ranked pool   | Direct policy repair + classifier escalation | 3914 |     0.255 |   0.051 |   0.464 |            13 |               3 | 0.021 |    0.191 |
| OULAD     | mismatch | Policy-aware ranking + edit (framework) | Framework + fallback over ranked pool        | 3914 |    -1.303 |  -1.675 |  -0.948 |             0 |              51 | 0     |    0     |

## Objective audit (leave-one-term-out and lambda sweep)
| dataset   | regime   | variant     | yield_     |   changed_selection_pct |   mean_effort_accepted |
|:----------|:---------|:------------|:-----------|------------------------:|-----------------------:|
| AUC       | aligned  | drop_feas   | 56.1 ± 3.9 |                    18.8 |                  1.998 |
| AUC       | aligned  | drop_policy | 52.0 ± 5.2 |                    78   |                  2.191 |
| AUC       | aligned  | drop_prox   | 66.1 ± 4.3 |                     0.5 |                  2.091 |
| AUC       | aligned  | drop_spar   | 65.6 ± 4.2 |                     0   |                  2.092 |
| AUC       | aligned  | lp_1        | 52.0 ± 5.2 |                    78   |                  2.191 |
| AUC       | aligned  | lp_10       | 57.1 ± 5.5 |                    14.3 |                  2.151 |
| AUC       | aligned  | lp_100      | 61.4 ± 4.8 |                     7.9 |                  2.117 |
| AUC       | aligned  | lx_0.1      | 66.1 ± 4.3 |                     0.5 |                  2.091 |
| AUC       | aligned  | lx_10       | 61.6 ± 4.9 |                     7.2 |                  2.116 |
| AUC       | aligned  | rank_edit   | 65.6 ± 4.2 |                     0   |                  2.092 |
| AUC       | floor    | drop_feas   | 53.8 ± 4.5 |                    21.2 |                  3.294 |
| AUC       | floor    | drop_policy | 51.0 ± 5.4 |                    73.3 |                  3.645 |
| AUC       | floor    | drop_prox   | 66.1 ± 4.4 |                     1.8 |                  3.459 |
| AUC       | floor    | drop_spar   | 64.6 ± 4.3 |                     0   |                  3.476 |
| AUC       | floor    | lp_1        | 51.0 ± 5.4 |                    73.3 |                  3.645 |
| AUC       | floor    | lp_10       | 53.6 ± 4.6 |                    16.5 |                  3.607 |
| AUC       | floor    | lp_100      | 60.5 ± 4.2 |                     6.6 |                  3.515 |
| AUC       | floor    | lx_0.1      | 66.1 ± 4.4 |                     1.8 |                  3.459 |
| AUC       | floor    | lx_10       | 60.5 ± 4.2 |                     6.5 |                  3.515 |
| AUC       | floor    | rank_edit   | 64.6 ± 4.3 |                     0   |                  3.476 |
| AUC       | mismatch | drop_feas   | 55.5 ± 4.0 |                    18.8 |                  3.315 |
| AUC       | mismatch | drop_policy | 50.6 ± 5.4 |                    72.1 |                  3.634 |
| AUC       | mismatch | drop_prox   | 66.1 ± 4.3 |                     1.3 |                  3.457 |
| AUC       | mismatch | drop_spar   | 65.0 ± 4.5 |                     0   |                  3.469 |
| AUC       | mismatch | lp_1        | 50.6 ± 5.4 |                    72.1 |                  3.634 |
| AUC       | mismatch | lp_10       | 53.1 ± 5.0 |                    18.5 |                  3.604 |
| AUC       | mismatch | lp_100      | 60.9 ± 4.7 |                     7.7 |                  3.513 |
| AUC       | mismatch | lx_0.1      | 66.1 ± 4.3 |                     1.3 |                  3.457 |
| AUC       | mismatch | lx_10       | 61.1 ± 4.8 |                     7   |                  3.51  |
| AUC       | mismatch | rank_edit   | 65.0 ± 4.5 |                     0   |                  3.469 |
| HarvardX  | aligned  | drop_feas   | 99.8 ± 0.2 |                     0.1 |                  0.843 |
| HarvardX  | aligned  | drop_policy | 99.9 ± 0.1 |                     0   |                  0.843 |
| HarvardX  | aligned  | drop_prox   | 99.9 ± 0.1 |                     0.7 |                  0.845 |
| HarvardX  | aligned  | drop_spar   | 99.9 ± 0.1 |                     3.9 |                  0.836 |
| HarvardX  | aligned  | lp_1        | 99.9 ± 0.1 |                     0   |                  0.843 |
| HarvardX  | aligned  | lp_10       | 99.9 ± 0.1 |                     0   |                  0.843 |
| HarvardX  | aligned  | lp_100      | 99.9 ± 0.1 |                     0   |                  0.843 |
| HarvardX  | aligned  | lx_0.1      | 99.9 ± 0.1 |                     0.2 |                  0.843 |
| HarvardX  | aligned  | lx_10       | 99.9 ± 0.1 |                     3.1 |                  0.837 |
| HarvardX  | aligned  | rank_edit   | 99.9 ± 0.1 |                     0   |                  0.843 |
| OULAD     | aligned  | drop_feas   | 99.8 ± 0.1 |                     0.2 |                  0.872 |
| OULAD     | aligned  | drop_policy | 92.1 ± 4.0 |                    39   |                  0.798 |
| OULAD     | aligned  | drop_prox   | 99.9 ± 0.1 |                    18.4 |                  0.934 |
| OULAD     | aligned  | drop_spar   | 99.9 ± 0.1 |                     6.1 |                  0.866 |
| OULAD     | aligned  | lp_1        | 92.8 ± 4.1 |                    37.6 |                  0.792 |
| OULAD     | aligned  | lp_10       | 98.5 ± 1.4 |                    10.3 |                  0.835 |
| OULAD     | aligned  | lp_100      | 99.9 ± 0.1 |                     0.6 |                  0.871 |
| OULAD     | aligned  | lx_0.1      | 99.9 ± 0.1 |                     0.6 |                  0.874 |
| OULAD     | aligned  | lx_10       | 99.9 ± 0.1 |                     4.7 |                  0.865 |
| OULAD     | aligned  | rank_edit   | 99.9 ± 0.1 |                     0   |                  0.873 |
| OULAD     | floor    | drop_feas   | 98.5 ± 1.0 |                    65.9 |                  3.118 |
| OULAD     | floor    | drop_policy | 96.3 ± 3.1 |                    24.4 |                  3.036 |
| OULAD     | floor    | drop_prox   | 98.9 ± 1.0 |                    39.4 |                  3.465 |
| OULAD     | floor    | drop_spar   | 98.5 ± 1.4 |                     0.1 |                  3.166 |
| OULAD     | floor    | lp_1        | 96.3 ± 3.1 |                    23.5 |                  3.035 |
| OULAD     | floor    | lp_10       | 98.3 ± 1.4 |                     6.3 |                  3.13  |
| OULAD     | floor    | lp_100      | 98.5 ± 1.4 |                     0.4 |                  3.164 |
| OULAD     | floor    | lx_0.1      | 98.5 ± 1.4 |                     0.7 |                  3.166 |
| OULAD     | floor    | lx_10       | 98.5 ± 1.4 |                     0.5 |                  3.163 |
| OULAD     | floor    | rank_edit   | 98.5 ± 1.4 |                     0   |                  3.166 |
| OULAD     | mismatch | drop_feas   | 91.9 ± 2.2 |                    66.4 |                  3.166 |
| OULAD     | mismatch | drop_policy | 96.5 ± 3.0 |                    22.9 |                  3.067 |
| OULAD     | mismatch | drop_prox   | 98.8 ± 0.9 |                    35.7 |                  3.464 |
| OULAD     | mismatch | drop_spar   | 98.6 ± 1.2 |                     0   |                  3.192 |
| OULAD     | mismatch | lp_1        | 96.5 ± 3.0 |                    22   |                  3.067 |
| OULAD     | mismatch | lp_10       | 98.4 ± 1.4 |                     5.6 |                  3.158 |
| OULAD     | mismatch | lp_100      | 98.6 ± 1.2 |                     0.5 |                  3.188 |
| OULAD     | mismatch | lx_0.1      | 98.6 ± 1.2 |                     0.5 |                  3.192 |
| OULAD     | mismatch | lx_10       | 98.6 ± 1.2 |                     0.6 |                  3.188 |
| OULAD     | mismatch | rank_edit   | 98.6 ± 1.2 |                     0   |                  3.192 |

## Threshold sensitivity (aligned bounds)
|                 | DiCE first candidate   | Direct policy repair + classifier escalation   | Post-hoc full-gate filter   | Policy-aware ranking + edit (framework)   | Framework + fallback over ranked pool   | Policy-aware ranking (no edit)   |
|:----------------|:-----------------------|:-----------------------------------------------|:----------------------------|:------------------------------------------|:----------------------------------------|:---------------------------------|
| ('AUC', 12.5)   | 37.3 ± 2.6             | 72.0 ± 3.0                                     | 43.1 ± 3.2                  | 72.5 ± 3.0                                | 72.5 ± 3.0                              | 43.1 ± 3.2                       |
| ('AUC', 15.001) | 28.0 ± 3.8             | 65.9 ± 4.3                                     | 37.3 ± 2.9                  | 65.6 ± 4.2                                | 66.3 ± 4.4                              | 36.7 ± 2.9                       |
| ('AUC', 16.0)   | 4.3 ± 1.0              | 50.4 ± 3.6                                     | 16.9 ± 1.9                  | 45.5 ± 3.3                                | 47.6 ± 3.4                              | 16.6 ± 1.9                       |
| ('AUC', 17.0)   | 0.0 ± 0.0              | 20.3 ± 3.2                                     | 0.0 ± 0.0                   | 17.4 ± 2.8                                | 17.5 ± 2.7                              | 0.0 ± 0.0                        |
| ('OULAD', 30.0) | 88.9 ± 1.7             | 88.5 ± 11.2                                    | 100.0 ± 0.1                 | 100.0 ± 0.0                               | 100.0 ± 0.0                             | 100.0 ± 0.1                      |
| ('OULAD', 40.0) | 76.5 ± 2.1             | 91.2 ± 8.6                                     | 99.3 ± 0.4                  | 99.9 ± 0.1                                | 100.0 ± 0.0                             | 99.2 ± 0.5                       |
| ('OULAD', 50.0) | 63.7 ± 2.4             | 99.0 ± 0.6                                     | 95.1 ± 1.6                  | 99.7 ± 0.2                                | 99.9 ± 0.1                              | 95.0 ± 1.6                       |
| ('OULAD', 60.0) | 51.7 ± 2.9             | 99.8 ± 0.2                                     | 80.9 ± 2.0                  | 99.1 ± 0.2                                | 99.7 ± 0.2                              | 80.9 ± 2.0                       |

## DiCE pools
|                         |   queries |   with_pool |   mean_pool |   pool_policy_valid |
|:------------------------|----------:|------------:|------------:|--------------------:|
| ('AUC', 'aligned')      |      2587 |      80.286 |       8.027 |               0.355 |
| ('AUC', 'floor')        |      2587 |      80.286 |       8.029 |               0.347 |
| ('AUC', 'mismatch')     |      2587 |      80.286 |       8.027 |               0.355 |
| ('HarvardX', 'aligned') |      1999 |      99.9   |       9.99  |             nan     |
| ('OULAD', 'aligned')    |      3914 |     100     |      10     |               0.782 |
| ('OULAD', 'floor')      |      3914 |     100     |      10     |               0.801 |
| ('OULAD', 'mismatch')   |      3914 |     100     |      10     |               0.782 |

## Best model per stage (mean ROC-AUC over grouped folds)
| dataset   | stage   | sampler   | model   |   roc_auc |
|:----------|:--------|:----------|:--------|----------:|
| AUC       | 1       | nearmiss  | MLP     |     0.822 |
| AUC       | 2       | nearmiss  | Ridge   |     0.93  |
| AUC       | 3       | none      | MLP     |     0.948 |
| AUC       | full    | none      | MLP     |     1     |
| HarvardX  | full    | smote     | MLP     |     0.96  |
| OULAD     | 1       | smote     | MLP     |     0.664 |
| OULAD     | 2       | none      | GBC     |     0.784 |
| OULAD     | 3       | none      | MLP     |     0.857 |
| OULAD     | full    | none      | CB      |     0.926 |

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
| ('OULAD', '1', 'nearmiss')       | 0.510 ± 0.007 | 0.516 ± 0.006 | 0.274 ± 0.009 | 0.975 ± 0.007 |
| ('OULAD', '1', 'none')           | 0.660 ± 0.018 | 0.558 ± 0.007 | 0.544 ± 0.010 | 0.155 ± 0.010 |
| ('OULAD', '1', 'smote')          | 0.659 ± 0.018 | 0.611 ± 0.014 | 0.596 ± 0.013 | 0.536 ± 0.034 |
| ('OULAD', '2', 'nearmiss')       | 0.725 ± 0.011 | 0.656 ± 0.008 | 0.646 ± 0.007 | 0.560 ± 0.020 |
| ('OULAD', '2', 'none')           | 0.782 ± 0.016 | 0.661 ± 0.010 | 0.681 ± 0.012 | 0.376 ± 0.016 |
| ('OULAD', '2', 'smote')          | 0.779 ± 0.018 | 0.702 ± 0.015 | 0.702 ± 0.016 | 0.571 ± 0.023 |
| ('OULAD', '3', 'nearmiss')       | 0.832 ± 0.019 | 0.757 ± 0.013 | 0.780 ± 0.015 | 0.568 ± 0.020 |
| ('OULAD', '3', 'none')           | 0.854 ± 0.016 | 0.754 ± 0.011 | 0.780 ± 0.012 | 0.553 ± 0.020 |
| ('OULAD', '3', 'smote')          | 0.852 ± 0.017 | 0.772 ± 0.014 | 0.780 ± 0.014 | 0.645 ± 0.024 |
| ('OULAD', 'full', 'nearmiss')    | 0.902 ± 0.004 | 0.829 ± 0.008 | 0.842 ± 0.008 | 0.715 ± 0.016 |
| ('OULAD', 'full', 'none')        | 0.926 ± 0.006 | 0.827 ± 0.007 | 0.848 ± 0.008 | 0.695 ± 0.012 |
| ('OULAD', 'full', 'smote')       | 0.923 ± 0.006 | 0.843 ± 0.009 | 0.844 ± 0.008 | 0.770 ± 0.017 |

## Friedman test across models (no resampling)
| dataset   | stage   |   friedman_p |   cb_rank | top   |   top_auc |   cb_auc |
|:----------|:--------|-------------:|----------:|:------|----------:|---------:|
| AUC       | 1       |       0      |       4.2 | LR    |    0.822  |   0.811  |
| AUC       | 2       |       0      |       5   | MLP   |    0.9291 |   0.9186 |
| AUC       | 3       |       0      |       5.1 | MLP   |    0.9483 |   0.9367 |
| AUC       | full    |       0.0001 |       5.2 | MLP   |    0.9999 |   0.9987 |
| HarvardX  | full    |       0      |       2.2 | MLP   |    0.9599 |   0.9578 |
| OULAD     | 1       |       0      |       2.6 | MLP   |    0.6625 |   0.6604 |
| OULAD     | 2       |       0      |       2.6 | GBC   |    0.7843 |   0.7817 |
| OULAD     | 3       |       0      |       3   | MLP   |    0.857  |   0.8537 |
| OULAD     | full    |       0      |       1.4 | CB    |    0.9258 |   0.9258 |
