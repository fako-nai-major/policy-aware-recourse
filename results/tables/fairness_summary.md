## A. Early-warning fairness (mean over 5 seeds)
|                                                         |      n |   base_fail |   flag_rate |   fail_recall |   false_flag |
|:--------------------------------------------------------|-------:|------------:|------------:|--------------:|-------------:|
| ('complete record', 'age', '0-35')                      | 1902.6 |       0.297 |       0.238 |         0.706 |        0.041 |
| ('complete record', 'age', '35+')                       |  857   |       0.238 |       0.182 |         0.673 |        0.028 |
| ('complete record', 'disability', 'Disability: no')     | 2538.4 |       0.272 |       0.214 |         0.696 |        0.034 |
| ('complete record', 'disability', 'Disability: yes')    |  221.2 |       0.367 |       0.305 |         0.715 |        0.068 |
| ('complete record', 'gender', 'Female')                 | 1241.4 |       0.264 |       0.214 |         0.703 |        0.038 |
| ('complete record', 'gender', 'Male')                   | 1518.2 |       0.291 |       0.227 |         0.694 |        0.035 |
| ('complete record', 'imd', 'IMD 0-30% (most deprived)') |  827.4 |       0.369 |       0.299 |         0.736 |        0.043 |
| ('complete record', 'imd', 'IMD 30-70%')                | 1093.4 |       0.251 |       0.196 |         0.678 |        0.034 |
| ('complete record', 'imd', 'IMD 70-100%')               |  743.4 |       0.233 |       0.177 |         0.658 |        0.031 |
| ('complete record', 'imd', 'IMD missing')               |   95.4 |       0.174 |       0.176 |         0.683 |        0.065 |
| ('stage 1', 'age', '0-35')                              | 1902.6 |       0.297 |       0.067 |         0.138 |        0.036 |
| ('stage 1', 'age', '35+')                               |  857   |       0.238 |       0.065 |         0.163 |        0.035 |
| ('stage 1', 'disability', 'Disability: no')             | 2538.4 |       0.272 |       0.065 |         0.141 |        0.036 |
| ('stage 1', 'disability', 'Disability: yes')            |  221.2 |       0.367 |       0.085 |         0.177 |        0.032 |
| ('stage 1', 'gender', 'Female')                         | 1241.4 |       0.264 |       0.065 |         0.148 |        0.035 |
| ('stage 1', 'gender', 'Male')                           | 1518.2 |       0.291 |       0.068 |         0.143 |        0.037 |
| ('stage 1', 'imd', 'IMD 0-30% (most deprived)')         |  827.4 |       0.369 |       0.093 |         0.177 |        0.044 |
| ('stage 1', 'imd', 'IMD 30-70%')                        | 1093.4 |       0.251 |       0.06  |         0.127 |        0.037 |
| ('stage 1', 'imd', 'IMD 70-100%')                       |  743.4 |       0.233 |       0.044 |         0.11  |        0.025 |
| ('stage 1', 'imd', 'IMD missing')                       |   95.4 |       0.174 |       0.08  |         0.206 |        0.056 |
| ('stage 2', 'age', '0-35')                              | 1902.6 |       0.297 |       0.153 |         0.385 |        0.055 |
| ('stage 2', 'age', '35+')                               |  857   |       0.238 |       0.132 |         0.375 |        0.056 |
| ('stage 2', 'disability', 'Disability: no')             | 2538.4 |       0.272 |       0.143 |         0.382 |        0.054 |
| ('stage 2', 'disability', 'Disability: yes')            |  221.2 |       0.367 |       0.186 |         0.389 |        0.07  |
| ('stage 2', 'gender', 'Female')                         | 1241.4 |       0.264 |       0.125 |         0.342 |        0.047 |
| ('stage 2', 'gender', 'Male')                           | 1518.2 |       0.291 |       0.164 |         0.412 |        0.062 |
| ('stage 2', 'imd', 'IMD 0-30% (most deprived)')         |  827.4 |       0.369 |       0.194 |         0.428 |        0.057 |
| ('stage 2', 'imd', 'IMD 30-70%')                        | 1093.4 |       0.251 |       0.13  |         0.354 |        0.054 |
| ('stage 2', 'imd', 'IMD 70-100%')                       |  743.4 |       0.233 |       0.122 |         0.349 |        0.053 |
| ('stage 2', 'imd', 'IMD missing')                       |   95.4 |       0.174 |       0.126 |         0.37  |        0.078 |
| ('stage 3', 'age', '0-35')                              | 1902.6 |       0.297 |       0.198 |         0.55  |        0.048 |
| ('stage 3', 'age', '35+')                               |  857   |       0.238 |       0.166 |         0.563 |        0.041 |
| ('stage 3', 'disability', 'Disability: no')             | 2538.4 |       0.272 |       0.183 |         0.555 |        0.044 |
| ('stage 3', 'disability', 'Disability: yes')            |  221.2 |       0.367 |       0.242 |         0.54  |        0.072 |
| ('stage 3', 'gender', 'Female')                         | 1241.4 |       0.264 |       0.184 |         0.544 |        0.054 |
| ('stage 3', 'gender', 'Male')                           | 1518.2 |       0.291 |       0.191 |         0.56  |        0.039 |
| ('stage 3', 'imd', 'IMD 0-30% (most deprived)')         |  827.4 |       0.369 |       0.249 |         0.594 |        0.047 |
| ('stage 3', 'imd', 'IMD 30-70%')                        | 1093.4 |       0.251 |       0.167 |         0.524 |        0.047 |
| ('stage 3', 'imd', 'IMD 70-100%')                       |  743.4 |       0.233 |       0.155 |         0.523 |        0.043 |
| ('stage 3', 'imd', 'IMD missing')                       |   95.4 |       0.174 |       0.147 |         0.581 |        0.054 |

## A. Gaps (max-min across groups; mean, SD over seeds)
|                                   |   ('DPD', 'mean') |   ('DPD', 'std') |   ('EOD', 'mean') |   ('EOD', 'std') |   ('FPR_gap', 'mean') |   ('FPR_gap', 'std') |
|:----------------------------------|------------------:|-----------------:|------------------:|-----------------:|----------------------:|---------------------:|
| ('complete record', 'age')        |             0.057 |            0.023 |             0.043 |            0.035 |                 0.013 |                0.007 |
| ('complete record', 'disability') |             0.092 |            0.026 |             0.019 |            0.024 |                 0.034 |                0.031 |
| ('complete record', 'gender')     |             0.013 |            0.011 |             0.018 |            0.013 |                 0.005 |                0.004 |
| ('complete record', 'imd')        |             0.151 |            0.038 |             0.137 |            0.076 |                 0.051 |                0.008 |
| ('stage 1', 'age')                |             0.009 |            0.009 |             0.033 |            0.023 |                 0.01  |                0.008 |
| ('stage 1', 'disability')         |             0.02  |            0.012 |             0.036 |            0.01  |                 0.007 |                0.004 |
| ('stage 1', 'gender')             |             0.013 |            0.01  |             0.031 |            0.017 |                 0.008 |                0.006 |
| ('stage 1', 'imd')                |             0.055 |            0.01  |             0.115 |            0.085 |                 0.036 |                0.016 |
| ('stage 2', 'age')                |             0.021 |            0.013 |             0.037 |            0.03  |                 0.005 |                0.004 |
| ('stage 2', 'disability')         |             0.043 |            0.02  |             0.026 |            0.028 |                 0.016 |                0.004 |
| ('stage 2', 'gender')             |             0.039 |            0.008 |             0.07  |            0.014 |                 0.015 |                0.009 |
| ('stage 2', 'imd')                |             0.083 |            0.013 |             0.134 |            0.039 |                 0.03  |                0.023 |
| ('stage 3', 'age')                |             0.032 |            0.013 |             0.019 |            0.014 |                 0.008 |                0.006 |
| ('stage 3', 'disability')         |             0.059 |            0.018 |             0.032 |            0.033 |                 0.028 |                0.017 |
| ('stage 3', 'gender')             |             0.01  |            0.011 |             0.021 |            0.015 |                 0.016 |                0.012 |
| ('stage 3', 'imd')                |             0.122 |            0.024 |             0.149 |            0.055 |                 0.025 |                0.008 |

## B. Recourse by group
| method                     | attribute   | group                     |    n |   yield_pct |   effort |   policy_score |
|:---------------------------|:------------|:--------------------------|-----:|------------:|---------:|---------------:|
| CARE (bounded)             | gender      | Female                    |  134 |      19.403 |    0.858 |         45.33  |
| CARE (bounded)             | gender      | Male                      |  166 |      63.253 |    0.767 |         47.664 |
| CARE (bounded)             | age         | 0-35                      |  223 |      44.843 |    0.765 |         47.16  |
| CARE (bounded)             | age         | 35+                       |   77 |      40.26  |    0.849 |         47.334 |
| CARE (bounded)             | imd         | IMD 0-30% (most deprived) |  133 |      43.609 |    0.841 |         47.269 |
| CARE (bounded)             | imd         | IMD 30-70%                |  104 |      43.269 |    0.731 |         46.542 |
| CARE (bounded)             | imd         | IMD 70-100%               |   57 |      42.105 |    0.724 |         47.255 |
| CARE (bounded)             | imd         | IMD missing               |    6 |      66.667 |    0.941 |         53.291 |
| CARE (bounded)             | disability  | Disability: no            |  270 |      43.333 |    0.805 |         47.419 |
| CARE (bounded)             | disability  | Disability: yes           |   30 |      46.667 |    0.613 |         45.376 |
| MCCE (bounded)             | gender      | Female                    | 1647 |      28.112 |    1.252 |         46.202 |
| MCCE (bounded)             | gender      | Male                      | 2267 |      55.933 |    1.294 |         48.728 |
| MCCE (bounded)             | age         | 0-35                      | 2825 |      45.345 |    1.287 |         48.149 |
| MCCE (bounded)             | age         | 35+                       | 1089 |      41.322 |    1.27  |         47.778 |
| MCCE (bounded)             | imd         | IMD 0-30% (most deprived) | 1609 |      41.144 |    1.299 |         47.909 |
| MCCE (bounded)             | imd         | IMD 30-70%                | 1370 |      43.796 |    1.298 |         48.342 |
| MCCE (bounded)             | imd         | IMD 70-100%               |  806 |      47.519 |    1.247 |         48.036 |
| MCCE (bounded)             | imd         | IMD missing               |  129 |      66.667 |    1.215 |         47.206 |
| MCCE (bounded)             | disability  | Disability: no            | 3532 |      44.337 |    1.287 |         48.076 |
| MCCE (bounded)             | disability  | Disability: yes           |  382 |      43.194 |    1.238 |         47.829 |
| NICE (bounded)             | gender      | Female                    | 1647 |       5.161 |    0.56  |         46.115 |
| NICE (bounded)             | gender      | Male                      | 2267 |      22.85  |    0.514 |         47.517 |
| NICE (bounded)             | age         | 0-35                      | 2825 |      16.637 |    0.516 |         47.387 |
| NICE (bounded)             | age         | 35+                       | 1089 |      12.213 |    0.537 |         47.081 |
| NICE (bounded)             | imd         | IMD 0-30% (most deprived) | 1609 |      12.989 |    0.516 |         46.723 |
| NICE (bounded)             | imd         | IMD 30-70%                | 1370 |      17.883 |    0.525 |         48.284 |
| NICE (bounded)             | imd         | IMD 70-100%               |  806 |      15.136 |    0.523 |         46.644 |
| NICE (bounded)             | imd         | IMD missing               |  129 |      20.93  |    0.512 |         46.231 |
| NICE (bounded)             | disability  | Disability: no            | 3532 |      15.657 |    0.527 |         47.379 |
| NICE (bounded)             | disability  | Disability: yes           |  382 |      13.089 |    0.455 |         46.666 |
| DiCE first candidate       | gender      | Female                    | 1647 |      59.016 |    1.418 |         64.698 |
| DiCE first candidate       | gender      | Male                      | 2267 |      89.281 |    1.224 |         85.321 |
| DiCE first candidate       | age         | 0-35                      | 2825 |      78.549 |    1.273 |         79.579 |
| DiCE first candidate       | age         | 35+                       | 1089 |      71.35  |    1.327 |         75.92  |
| DiCE first candidate       | imd         | IMD 0-30% (most deprived) | 1609 |      76.196 |    1.303 |         78.619 |
| DiCE first candidate       | imd         | IMD 30-70%                | 1370 |      74.38  |    1.288 |         77.433 |
| DiCE first candidate       | imd         | IMD 70-100%               |  806 |      77.916 |    1.276 |         79.215 |
| DiCE first candidate       | imd         | IMD missing               |  129 |      95.349 |    1.177 |         85.677 |
| DiCE first candidate       | disability  | Disability: no            | 3532 |      77.123 |    1.291 |         78.788 |
| DiCE first candidate       | disability  | Disability: yes           |  382 |      71.204 |    1.253 |         77.053 |
| Policy repair + escalation | gender      | Female                    | 1647 |      96.539 |    0.944 |         46.096 |
| Policy repair + escalation | gender      | Male                      | 2267 |      87.34  |    0.479 |         52.096 |
| Policy repair + escalation | age         | 0-35                      | 2825 |      90.442 |    0.67  |         49.976 |
| Policy repair + escalation | age         | 35+                       | 1089 |      93.205 |    0.726 |         48.034 |
| Policy repair + escalation | imd         | IMD 0-30% (most deprived) | 1609 |      91.175 |    0.721 |         49.542 |
| Policy repair + escalation | imd         | IMD 30-70%                | 1370 |      92.628 |    0.695 |         49.342 |
| Policy repair + escalation | imd         | IMD 70-100%               |  806 |      89.082 |    0.64  |         48.931 |
| Policy repair + escalation | imd         | IMD missing               |  129 |      89.922 |    0.434 |         51.875 |
| Policy repair + escalation | disability  | Disability: no            | 3532 |      91.082 |    0.682 |         49.517 |
| Policy repair + escalation | disability  | Disability: yes           |  382 |      92.408 |    0.718 |         48.576 |
| DiCE + full gate           | gender      | Female                    | 1647 |      98.543 |    1.485 |         59.597 |
| DiCE + full gate           | gender      | Male                      | 2267 |      99.824 |    1.242 |         83.123 |
| DiCE + full gate           | age         | 0-35                      | 2825 |      99.398 |    1.328 |         74.432 |
| DiCE + full gate           | age         | 35+                       | 1089 |      98.99  |    1.385 |         70.341 |
| DiCE + full gate           | imd         | IMD 0-30% (most deprived) | 1609 |      99.254 |    1.361 |         73.082 |
| DiCE + full gate           | imd         | IMD 30-70%                | 1370 |      99.197 |    1.349 |         72.052 |
| DiCE + full gate           | imd         | IMD 70-100%               |  806 |      99.38  |    1.325 |         73.969 |
| DiCE + full gate           | imd         | IMD missing               |  129 |     100     |    1.185 |         84.908 |
| DiCE + full gate           | disability  | Disability: no            | 3532 |      99.264 |    1.345 |         73.556 |
| DiCE + full gate           | disability  | Disability: yes           |  382 |      99.476 |    1.335 |         70.914 |
| Framework                  | gender      | Female                    | 1647 |      99.939 |    1.125 |         50.844 |
| Framework                  | gender      | Male                      | 2267 |      99.956 |    0.69  |         66.01  |
| Framework                  | age         | 0-35                      | 2825 |      99.965 |    0.854 |         60.367 |
| Framework                  | age         | 35+                       | 1089 |      99.908 |    0.922 |         57.712 |
| Framework                  | imd         | IMD 0-30% (most deprived) | 1609 |     100     |    0.904 |         58.95  |
| Framework                  | imd         | IMD 30-70%                | 1370 |      99.854 |    0.878 |         59.229 |
| Framework                  | imd         | IMD 70-100%               |  806 |     100     |    0.84  |         60.578 |
| Framework                  | imd         | IMD missing               |  129 |     100     |    0.642 |         66.406 |
| Framework                  | disability  | Disability: no            | 3532 |      99.943 |    0.87  |         59.87  |
| Framework                  | disability  | Disability: yes           |  382 |     100     |    0.902 |         57.402 |
| Framework + fallback       | gender      | Female                    | 1647 |     100     |    1.125 |         50.847 |
| Framework + fallback       | gender      | Male                      | 2267 |     100     |    0.691 |         66.004 |
| Framework + fallback       | age         | 0-35                      | 2825 |     100     |    0.854 |         60.369 |
| Framework + fallback       | age         | 35+                       | 1089 |     100     |    0.923 |         57.698 |
| Framework + fallback       | imd         | IMD 0-30% (most deprived) | 1609 |     100     |    0.904 |         58.95  |
| Framework + fallback       | imd         | IMD 30-70%                | 1370 |     100     |    0.879 |         59.214 |
| Framework + fallback       | imd         | IMD 70-100%               |  806 |     100     |    0.84  |         60.591 |
| Framework + fallback       | imd         | IMD missing               |  129 |     100     |    0.642 |         66.406 |
| Framework + fallback       | disability  | Disability: no            | 3532 |     100     |    0.87  |         59.864 |
| Framework + fallback       | disability  | Disability: yes           |  382 |     100     |    0.902 |         57.429 |

## B. Recourse gaps and tests (Holm-adjusted)
| method                     | attribute   |    n |   yield_gap_pp |   p_yield |   effort_gap |   effort_gap_rel_pct |   p_effort |   p_yield_holm |   p_effort_holm |
|:---------------------------|:------------|-----:|---------------:|----------:|-------------:|---------------------:|-----------:|---------------:|----------------:|
| CARE (bounded)             | gender      |  300 |        43.85   |    0      |       0.0917 |              11.2888 |     0.3619 |         0      |          1      |
| CARE (bounded)             | age         |  300 |         4.5833 |    0.5715 |       0.0834 |              10.3333 |     0.1749 |         1      |          1      |
| CARE (bounded)             | imd         |  300 |        24.5614 |    0.7164 |       0.2172 |              26.8365 |     0.3446 |         1      |          1      |
| CARE (bounded)             | disability  |  300 |         3.3333 |    0.8767 |       0.1924 |              27.124  |     0.0658 |         1      |          0.9863 |
| MCCE (bounded)             | gender      | 3914 |        27.8212 |    0      |       0.0415 |               3.2591 |     0.0206 |         0      |          0.37   |
| MCCE (bounded)             | age         | 3914 |         4.0228 |    0.0254 |       0.0167 |               1.3095 |     0.5042 |         0.3813 |          1      |
| MCCE (bounded)             | imd         | 3914 |        25.5231 |    0      |       0.0834 |               6.5912 |     0.1414 |         0      |          1      |
| MCCE (bounded)             | disability  | 3914 |         1.1438 |    0.7089 |       0.0495 |               3.9223 |     0.1823 |         1      |          1      |
| NICE (bounded)             | gender      | 3914 |        17.6887 |    0      |       0.0451 |               8.4061 |     0.6154 |         0      |          1      |
| NICE (bounded)             | age         | 3914 |         4.4241 |    0.0007 |       0.0201 |               3.821  |     0.6832 |         0.0135 |          1      |
| NICE (bounded)             | imd         | 3914 |         7.9408 |    0.0008 |       0.0139 |               2.6776 |     0.5095 |         0.0145 |          1      |
| NICE (bounded)             | disability  | 3914 |         2.5678 |    0.2127 |       0.0722 |              14.7171 |     0.0542 |         1      |          0.868  |
| DiCE first candidate       | gender      | 3914 |        30.2646 |    0      |       0.1945 |              14.7214 |     0      |         0      |          0      |
| DiCE first candidate       | age         | 3914 |         7.1988 |    0      |       0.0538 |               4.1391 |     0.006  |         0      |          0.1141 |
| DiCE first candidate       | imd         | 3914 |        20.9693 |    0      |       0.1259 |               9.9808 |     0.0407 |         0      |          0.6915 |
| DiCE first candidate       | disability  | 3914 |         5.9193 |    0.0114 |       0.038  |               2.9877 |     0.1641 |         0.1824 |          1      |
| Policy repair + escalation | gender      | 3914 |         9.1991 |    0      |       0.4656 |              65.4558 |     0      |         0      |          0      |
| Policy repair + escalation | age         | 3914 |         2.7623 |    0.0075 |       0.0559 |               8.0149 |     0      |         0.1281 |          0.0001 |
| Policy repair + escalation | imd         | 3914 |         3.5459 |    0.041  |       0.287  |              46.1211 |     0      |         0.5737 |          0      |
| Policy repair + escalation | disability  | 3914 |         1.3268 |    0.4384 |       0.0357 |               5.0915 |     0.1397 |         1      |          1      |
| DiCE + full gate           | gender      | 3914 |         1.2808 |    0      |       0.2424 |              17.7733 |     0      |         0.0001 |          0      |
| DiCE + full gate           | age         | 3914 |         0.4083 |    0.2515 |       0.0572 |               4.2172 |     0.0012 |         1      |          0.0249 |
| DiCE + full gate           | imd         | 3914 |         0.8029 |    0.7528 |       0.1759 |              13.4794 |     0.0005 |         1      |          0.0111 |
| DiCE + full gate           | disability  | 3914 |         0.2126 |    0.8818 |       0.0094 |               0.6989 |     0.6122 |         1      |          1      |
| Framework                  | gender      | 3914 |         0.0166 |    1      |       0.435  |              47.9303 |     0      |         1      |          0      |
| Framework                  | age         | 3914 |         0.0564 |    1      |       0.0679 |               7.6408 |     0      |         1      |          0.0007 |
| Framework                  | imd         | 3914 |         0.146  |    0.2938 |       0.2619 |              32.101  |     0      |         1      |          0      |
| Framework                  | disability  | 3914 |         0.0566 |    1      |       0.0316 |               3.5628 |     0.1851 |         1      |          1      |
| Framework + fallback       | gender      | 3914 |         0      |  nan      |       0.4344 |              47.8441 |     0      |       nan      |          0      |
| Framework + fallback       | age         | 3914 |         0      |  nan      |       0.0689 |               7.7508 |     0      |       nan      |          0.0007 |
| Framework + fallback       | imd         | 3914 |         0      |  nan      |       0.2619 |              32.0896 |     0      |       nan      |          0      |
| Framework + fallback       | disability  | 3914 |         0      |  nan      |       0.0311 |               3.5108 |     0.1897 |       nan      |          1      |

## C. Module x stage adjusted contrasts (cluster-robust by learner, Holm)
| method                     | attribute   | contrast                                | outcome   |    n |   raw_diff |   adj_diff |    ci_lo |    ci_hi |        p |   p_holm |
|:---------------------------|:------------|:----------------------------------------|:----------|-----:|-----------:|-----------:|---------:|---------:|---------:|---------:|
| CARE (bounded)             | gender      | Female - Male                           | yield_pp  |  300 |   -43.85   |     6.8335 |  -5.0157 |  18.6827 |   0.2583 |     1    |
| CARE (bounded)             | gender      | Female - Male                           | effort    |  131 |     0.0917 |    -0.0098 |  -0.1594 |   0.1399 |   0.8982 |     1    |
| CARE (bounded)             | age         | 35+ - 0-35                              | yield_pp  |  300 |    -4.5833 |     2.0924 |  -7.9814 |  12.1661 |   0.6839 |     1    |
| CARE (bounded)             | age         | 35+ - 0-35                              | effort    |  131 |     0.0834 |     0.0166 |  -0.1173 |   0.1505 |   0.8085 |     1    |
| CARE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  |  190 |     1.5038 |     1.4438 | -10.649  |  13.5366 |   0.815  |     1    |
| CARE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    |   82 |     0.1169 |     0.1126 |  -0.068  |   0.2933 |   0.2216 |     1    |
| CARE (bounded)             | disability  | Disability: yes - Disability: no        | yield_pp  |  300 |     3.3333 |     3.7281 | -10.2629 |  17.7191 |   0.6015 |     1    |
| CARE (bounded)             | disability  | Disability: yes - Disability: no        | effort    |  131 |    -0.1924 |    -0.1385 |  -0.2902 |   0.0132 |   0.0735 |     1    |
| MCCE (bounded)             | gender      | Female - Male                           | yield_pp  | 3914 |   -27.8212 |     5.9051 |   0.9963 |  10.814  |   0.0184 |     1    |
| MCCE (bounded)             | gender      | Female - Male                           | effort    | 1731 |    -0.0415 |    -0.0742 |  -0.1318 |  -0.0166 |   0.0115 |     0.68 |
| MCCE (bounded)             | age         | 35+ - 0-35                              | yield_pp  | 3914 |    -4.0228 |     0.4427 |  -3.4301 |   4.3155 |   0.8227 |     1    |
| MCCE (bounded)             | age         | 35+ - 0-35                              | effort    | 1731 |    -0.0167 |    -0.0346 |  -0.0772 |   0.008  |   0.1111 |     1    |
| MCCE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2415 |    -6.375  |    -2.57   |  -7.4443 |   2.3042 |   0.3014 |     1    |
| MCCE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    | 1045 |     0.0518 |     0.0259 |  -0.0301 |   0.0819 |   0.3643 |     1    |
| MCCE (bounded)             | disability  | Disability: yes - Disability: no        | yield_pp  | 3914 |    -1.1438 |     2.4795 |  -2.9237 |   7.8826 |   0.3684 |     1    |
| MCCE (bounded)             | disability  | Disability: yes - Disability: no        | effort    | 1731 |    -0.0495 |    -0.0181 |  -0.0855 |   0.0494 |   0.5995 |     1    |
| NICE (bounded)             | gender      | Female - Male                           | yield_pp  | 3914 |   -17.6887 |     1.6247 |  -1.5761 |   4.8254 |   0.3198 |     1    |
| NICE (bounded)             | gender      | Female - Male                           | effort    |  603 |     0.0451 |    -0.0411 |  -0.0863 |   0.0041 |   0.0746 |     1    |
| NICE (bounded)             | age         | 35+ - 0-35                              | yield_pp  | 3914 |    -4.4241 |    -1.5384 |  -3.8429 |   0.7662 |   0.1908 |     1    |
| NICE (bounded)             | age         | 35+ - 0-35                              | effort    |  603 |     0.0201 |    -0.003  |  -0.0325 |   0.0266 |   0.8427 |     1    |
| NICE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2415 |    -2.147  |    -0.0874 |  -3.0532 |   2.8784 |   0.9539 |     1    |
| NICE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    |  331 |    -0.007  |     0.0059 |  -0.03   |   0.0419 |   0.7464 |     1    |
| NICE (bounded)             | disability  | Disability: yes - Disability: no        | yield_pp  | 3914 |    -2.5678 |     0.7036 |  -2.6655 |   4.0728 |   0.6823 |     1    |
| NICE (bounded)             | disability  | Disability: yes - Disability: no        | effort    |  603 |    -0.0722 |    -0.0349 |  -0.0837 |   0.014  |   0.1617 |     1    |
| DiCE first candidate       | gender      | Female - Male                           | yield_pp  | 3914 |   -30.2646 |     1.8106 |  -1.7871 |   5.4083 |   0.3239 |     1    |
| DiCE first candidate       | gender      | Female - Male                           | effort    | 2996 |     0.1945 |     0.0088 |  -0.0378 |   0.0554 |   0.7115 |     1    |
| DiCE first candidate       | age         | 35+ - 0-35                              | yield_pp  | 3914 |    -7.1988 |    -1.7021 |  -4.4968 |   1.0926 |   0.2326 |     1    |
| DiCE first candidate       | age         | 35+ - 0-35                              | effort    | 2996 |     0.0538 |     0.0186 |  -0.0148 |   0.052  |   0.275  |     1    |
| DiCE first candidate       | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2415 |    -1.7192 |     2.4257 |  -0.7844 |   5.6358 |   0.1386 |     1    |
| DiCE first candidate       | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    | 1854 |     0.026  |     0.0049 |  -0.0376 |   0.0474 |   0.8212 |     1    |
| DiCE first candidate       | disability  | Disability: yes - Disability: no        | yield_pp  | 3914 |    -5.9193 |    -2.2934 |  -6.1858 |   1.599  |   0.2482 |     1    |
| DiCE first candidate       | disability  | Disability: yes - Disability: no        | effort    | 2996 |    -0.038  |    -0.0508 |  -0.1086 |   0.007  |   0.0848 |     1    |
| Policy repair + escalation | gender      | Female - Male                           | yield_pp  | 3914 |     9.1991 |     0.1142 |  -3.351  |   3.5794 |   0.9485 |     1    |
| Policy repair + escalation | gender      | Female - Male                           | effort    | 3570 |     0.4656 |    -0.0179 |  -0.0522 |   0.0163 |   0.3041 |     1    |
| Policy repair + escalation | age         | 35+ - 0-35                              | yield_pp  | 3914 |     2.7623 |     1.0558 |  -1.3321 |   3.4437 |   0.3862 |     1    |
| Policy repair + escalation | age         | 35+ - 0-35                              | effort    | 3570 |     0.0559 |    -0.0305 |  -0.0577 |  -0.0033 |   0.0282 |     1    |
| Policy repair + escalation | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2415 |     2.0928 |     1.0662 |  -2.263  |   4.3954 |   0.5302 |     1    |
| Policy repair + escalation | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    | 2185 |     0.0802 |     0.0326 |   0.0009 |   0.0643 |   0.0438 |     1    |
| Policy repair + escalation | disability  | Disability: yes - Disability: no        | yield_pp  | 3914 |     1.3268 |     0.8539 |  -2.7394 |   4.4472 |   0.6414 |     1    |
| Policy repair + escalation | disability  | Disability: yes - Disability: no        | effort    | 3570 |     0.0357 |    -0.0179 |  -0.0596 |   0.0239 |   0.4015 |     1    |
| DiCE + full gate           | gender      | Female - Male                           | yield_pp  | 3914 |    -1.2808 |    -0.1064 |  -0.9783 |   0.7654 |   0.8109 |     1    |
| DiCE + full gate           | gender      | Female - Male                           | effort    | 3886 |     0.2424 |    -0.0033 |  -0.0423 |   0.0356 |   0.8678 |     1    |
| DiCE + full gate           | age         | 35+ - 0-35                              | yield_pp  | 3914 |    -0.4083 |    -0.1843 |  -0.8975 |   0.5289 |   0.6125 |     1    |
| DiCE + full gate           | age         | 35+ - 0-35                              | effort    | 3886 |     0.0572 |     0.0129 |  -0.0148 |   0.0405 |   0.3616 |     1    |
| DiCE + full gate           | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2415 |    -0.1255 |     0.0147 |  -0.6484 |   0.6777 |   0.9654 |     1    |
| DiCE + full gate           | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    | 2398 |     0.0357 |     0.0057 |  -0.0316 |   0.043  |   0.7637 |     1    |
| DiCE + full gate           | disability  | Disability: yes - Disability: no        | yield_pp  | 3914 |     0.2126 |     0.3466 |  -0.6303 |   1.3235 |   0.4868 |     1    |
| DiCE + full gate           | disability  | Disability: yes - Disability: no        | effort    | 3886 |    -0.0094 |    -0.041  |  -0.0882 |   0.0061 |   0.088  |     1    |
| Framework                  | gender      | Female - Male                           | yield_pp  | 3914 |    -0.0166 |     0.0596 |  -0.1173 |   0.2365 |   0.5088 |     1    |
| Framework                  | gender      | Female - Male                           | effort    | 3912 |     0.435  |    -0.0242 |  -0.0553 |   0.0069 |   0.1274 |     1    |
| Framework                  | age         | 35+ - 0-35                              | yield_pp  | 3914 |    -0.0564 |    -0.0154 |  -0.1446 |   0.1139 |   0.8158 |     1    |
| Framework                  | age         | 35+ - 0-35                              | effort    | 3912 |     0.0679 |    -0.0139 |  -0.0385 |   0.0107 |   0.2697 |     1    |
| Framework                  | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2415 |     0      |   nan      | nan      | nan      | nan      |   nan    |
| Framework                  | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    | 2415 |     0.0635 |     0.0083 |  -0.0224 |   0.0389 |   0.5973 |     1    |
| Framework                  | disability  | Disability: yes - Disability: no        | yield_pp  | 3914 |     0.0566 |     0.0519 |  -0.0262 |   0.1301 |   0.1929 |     1    |
| Framework                  | disability  | Disability: yes - Disability: no        | effort    | 3912 |     0.0316 |    -0.0261 |  -0.0609 |   0.0087 |   0.1414 |     1    |
| Framework + fallback       | gender      | Female - Male                           | yield_pp  | 3914 |     0      |   nan      | nan      | nan      | nan      |   nan    |
| Framework + fallback       | gender      | Female - Male                           | effort    | 3914 |     0.4344 |    -0.0252 |  -0.0564 |   0.006  |   0.1134 |     1    |
| Framework + fallback       | age         | 35+ - 0-35                              | yield_pp  | 3914 |     0      |   nan      | nan      | nan      | nan      |   nan    |
| Framework + fallback       | age         | 35+ - 0-35                              | effort    | 3914 |     0.0689 |    -0.0133 |  -0.0379 |   0.0114 |   0.2914 |     1    |
| Framework + fallback       | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2415 |     0      |   nan      | nan      | nan      | nan      |   nan    |
| Framework + fallback       | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    | 2415 |     0.0635 |     0.0083 |  -0.0224 |   0.0389 |   0.5973 |     1    |
| Framework + fallback       | disability  | Disability: yes - Disability: no        | yield_pp  | 3914 |     0      |   nan      | nan      | nan      | nan      |   nan    |
| Framework + fallback       | disability  | Disability: yes - Disability: no        | effort    | 3914 |     0.0311 |    -0.0264 |  -0.0612 |   0.0085 |   0.1378 |     1    |