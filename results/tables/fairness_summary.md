## A. Early-warning fairness (mean over 5 seeds)
|                                                         |      n |   base_fail |   flag_rate |   fail_recall |   false_flag |
|:--------------------------------------------------------|-------:|------------:|------------:|--------------:|-------------:|
| ('complete record', 'age', '0-35')                      | 1901.6 |       0.323 |       0.278 |         0.776 |        0.041 |
| ('complete record', 'age', '35+')                       |  844.6 |       0.245 |       0.209 |         0.768 |        0.028 |
| ('complete record', 'disability', 'Disability: no')     | 2533   |       0.293 |       0.252 |         0.772 |        0.037 |
| ('complete record', 'disability', 'Disability: yes')    |  213.2 |       0.366 |       0.312 |         0.79  |        0.034 |
| ('complete record', 'gender', 'Female')                 | 1255.2 |       0.289 |       0.243 |         0.756 |        0.034 |
| ('complete record', 'gender', 'Male')                   | 1491   |       0.308 |       0.269 |         0.788 |        0.039 |
| ('complete record', 'imd', 'IMD 0-30% (most deprived)') |  852.8 |       0.395 |       0.345 |         0.805 |        0.045 |
| ('complete record', 'imd', 'IMD 30-70%')                | 1072.2 |       0.28  |       0.244 |         0.773 |        0.037 |
| ('complete record', 'imd', 'IMD 70-100%')               |  721.4 |       0.228 |       0.184 |         0.717 |        0.027 |
| ('complete record', 'imd', 'IMD missing')               |   99.8 |       0.187 |       0.172 |         0.729 |        0.044 |
| ('stage 1', 'age', '0-35')                              | 1901.6 |       0.323 |       0.128 |         0.315 |        0.038 |
| ('stage 1', 'age', '35+')                               |  844.6 |       0.245 |       0.116 |         0.365 |        0.035 |
| ('stage 1', 'disability', 'Disability: no')             | 2533   |       0.293 |       0.122 |         0.328 |        0.037 |
| ('stage 1', 'disability', 'Disability: yes')            |  213.2 |       0.366 |       0.141 |         0.324 |        0.034 |
| ('stage 1', 'gender', 'Female')                         | 1255.2 |       0.289 |       0.127 |         0.342 |        0.039 |
| ('stage 1', 'gender', 'Male')                           | 1491   |       0.308 |       0.122 |         0.317 |        0.035 |
| ('stage 1', 'imd', 'IMD 0-30% (most deprived)')         |  852.8 |       0.395 |       0.17  |         0.36  |        0.045 |
| ('stage 1', 'imd', 'IMD 30-70%')                        | 1072.2 |       0.28  |       0.12  |         0.326 |        0.04  |
| ('stage 1', 'imd', 'IMD 70-100%')                       |  721.4 |       0.228 |       0.082 |         0.28  |        0.023 |
| ('stage 1', 'imd', 'IMD missing')                       |   99.8 |       0.187 |       0.074 |         0.226 |        0.044 |
| ('stage 2', 'age', '0-35')                              | 1901.6 |       0.323 |       0.196 |         0.5   |        0.051 |
| ('stage 2', 'age', '35+')                               |  844.6 |       0.245 |       0.162 |         0.535 |        0.041 |
| ('stage 2', 'disability', 'Disability: no')             | 2533   |       0.293 |       0.183 |         0.508 |        0.048 |
| ('stage 2', 'disability', 'Disability: yes')            |  213.2 |       0.366 |       0.216 |         0.504 |        0.047 |
| ('stage 2', 'gender', 'Female')                         | 1255.2 |       0.289 |       0.166 |         0.47  |        0.043 |
| ('stage 2', 'gender', 'Male')                           | 1491   |       0.308 |       0.201 |         0.539 |        0.052 |
| ('stage 2', 'imd', 'IMD 0-30% (most deprived)')         |  852.8 |       0.395 |       0.247 |         0.544 |        0.054 |
| ('stage 2', 'imd', 'IMD 30-70%')                        | 1072.2 |       0.28  |       0.179 |         0.505 |        0.053 |
| ('stage 2', 'imd', 'IMD 70-100%')                       |  721.4 |       0.228 |       0.131 |         0.455 |        0.035 |
| ('stage 2', 'imd', 'IMD missing')                       |   99.8 |       0.187 |       0.115 |         0.425 |        0.048 |
| ('stage 3', 'age', '0-35')                              | 1901.6 |       0.323 |       0.223 |         0.599 |        0.044 |
| ('stage 3', 'age', '35+')                               |  844.6 |       0.245 |       0.184 |         0.642 |        0.036 |
| ('stage 3', 'disability', 'Disability: no')             | 2533   |       0.293 |       0.207 |         0.609 |        0.041 |
| ('stage 3', 'disability', 'Disability: yes')            |  213.2 |       0.366 |       0.257 |         0.618 |        0.047 |
| ('stage 3', 'gender', 'Female')                         | 1255.2 |       0.289 |       0.192 |         0.548 |        0.047 |
| ('stage 3', 'gender', 'Male')                           | 1491   |       0.308 |       0.228 |         0.658 |        0.036 |
| ('stage 3', 'imd', 'IMD 0-30% (most deprived)')         |  852.8 |       0.395 |       0.289 |         0.649 |        0.055 |
| ('stage 3', 'imd', 'IMD 30-70%')                        | 1072.2 |       0.28  |       0.195 |         0.594 |        0.04  |
| ('stage 3', 'imd', 'IMD 70-100%')                       |  721.4 |       0.228 |       0.152 |         0.562 |        0.031 |
| ('stage 3', 'imd', 'IMD missing')                       |   99.8 |       0.187 |       0.144 |         0.595 |        0.042 |

## A. Gaps (max-min across groups; mean, SD over seeds)
|                                   |   ('DPD', 'mean') |   ('DPD', 'std') |   ('EOD', 'mean') |   ('EOD', 'std') |   ('FPR_gap', 'mean') |   ('FPR_gap', 'std') |
|:----------------------------------|------------------:|-----------------:|------------------:|-----------------:|----------------------:|---------------------:|
| ('complete record', 'age')        |             0.069 |            0.013 |             0.032 |            0.016 |                 0.012 |                0.008 |
| ('complete record', 'disability') |             0.063 |            0.036 |             0.054 |            0.028 |                 0.009 |                0.012 |
| ('complete record', 'gender')     |             0.028 |            0.021 |             0.041 |            0.016 |                 0.009 |                0.001 |
| ('complete record', 'imd')        |             0.178 |            0.037 |             0.135 |            0.031 |                 0.034 |                0.009 |
| ('stage 1', 'age')                |             0.015 |            0.008 |             0.051 |            0.037 |                 0.004 |                0.003 |
| ('stage 1', 'disability')         |             0.023 |            0.02  |             0.035 |            0.023 |                 0.01  |                0.007 |
| ('stage 1', 'gender')             |             0.018 |            0.006 |             0.041 |            0.022 |                 0.013 |                0.006 |
| ('stage 1', 'imd')                |             0.1   |            0.011 |             0.185 |            0.08  |                 0.027 |                0.005 |
| ('stage 2', 'age')                |             0.034 |            0.021 |             0.063 |            0.028 |                 0.01  |                0.009 |
| ('stage 2', 'disability')         |             0.033 |            0.022 |             0.034 |            0.013 |                 0.012 |                0.009 |
| ('stage 2', 'gender')             |             0.035 |            0.013 |             0.068 |            0.033 |                 0.009 |                0.003 |
| ('stage 2', 'imd')                |             0.132 |            0.027 |             0.166 |            0.078 |                 0.031 |                0.006 |
| ('stage 3', 'age')                |             0.039 |            0.016 |             0.049 |            0.035 |                 0.008 |                0.006 |
| ('stage 3', 'disability')         |             0.049 |            0.028 |             0.036 |            0.031 |                 0.008 |                0.003 |
| ('stage 3', 'gender')             |             0.036 |            0.01  |             0.111 |            0.014 |                 0.011 |                0.009 |
| ('stage 3', 'imd')                |             0.154 |            0.023 |             0.13  |            0.028 |                 0.03  |                0.009 |

## B. Recourse by group
| method                     | attribute   | group                     |    n |   yield_pct |   effort |   policy_score |
|:---------------------------|:------------|:--------------------------|-----:|------------:|---------:|---------------:|
| CARE (bounded)             | gender      | Female                    |  130 |      20     |    2.006 |         45.643 |
| CARE (bounded)             | gender      | Male                      |  170 |      36.471 |    1.429 |         45.209 |
| CARE (bounded)             | age         | 0-35                      |  221 |      28.959 |    1.498 |         45.049 |
| CARE (bounded)             | age         | 35+                       |   79 |      30.38  |    1.87  |         46.107 |
| CARE (bounded)             | imd         | IMD 0-30% (most deprived) |  124 |      29.032 |    1.659 |         45.526 |
| CARE (bounded)             | imd         | IMD 30-70%                |  115 |      28.696 |    1.624 |         44.416 |
| CARE (bounded)             | imd         | IMD 70-100%               |   51 |      33.333 |    1.417 |         46.892 |
| CARE (bounded)             | imd         | IMD missing               |   10 |      20     |    1.671 |         43.938 |
| CARE (bounded)             | disability  | Disability: no            |  273 |      29.304 |    1.567 |         45.356 |
| CARE (bounded)             | disability  | Disability: yes           |   27 |      29.63  |    1.92  |         45.154 |
| MCCE (bounded)             | gender      | Female                    | 1963 |      50.993 |    3.103 |         48.319 |
| MCCE (bounded)             | gender      | Male                      | 2537 |      40.796 |    1.771 |         46.395 |
| MCCE (bounded)             | age         | 0-35                      | 3291 |      44.272 |    2.316 |         47.211 |
| MCCE (bounded)             | age         | 35+                       | 1209 |      47.891 |    2.702 |         47.666 |
| MCCE (bounded)             | imd         | IMD 0-30% (most deprived) | 1861 |      45.997 |    2.573 |         47.583 |
| MCCE (bounded)             | imd         | IMD 30-70%                | 1676 |      44.451 |    2.39  |         47.202 |
| MCCE (bounded)             | imd         | IMD 70-100%               |  861 |      44.251 |    2.241 |         46.978 |
| MCCE (bounded)             | imd         | IMD missing               |  102 |      52.941 |    1.903 |         47.971 |
| MCCE (bounded)             | disability  | Disability: no            | 4097 |      45.033 |    2.425 |         47.351 |
| MCCE (bounded)             | disability  | Disability: yes           |  403 |      47.395 |    2.438 |         47.244 |
| NICE (bounded)             | gender      | Female                    | 1963 |       1.63  |    1.238 |         43.008 |
| NICE (bounded)             | gender      | Male                      | 2537 |       7.489 |    1.245 |         42.07  |
| NICE (bounded)             | age         | 0-35                      | 3291 |       5.074 |    1.28  |         42.233 |
| NICE (bounded)             | age         | 35+                       | 1209 |       4.549 |    1.134 |         42.122 |
| NICE (bounded)             | imd         | IMD 0-30% (most deprived) | 1861 |       3.923 |    1.205 |         42.28  |
| NICE (bounded)             | imd         | IMD 30-70%                | 1676 |       4.833 |    1.305 |         42.278 |
| NICE (bounded)             | imd         | IMD 70-100%               |  861 |       6.969 |    1.199 |         41.947 |
| NICE (bounded)             | imd         | IMD missing               |  102 |       7.843 |    1.325 |         42.72  |
| NICE (bounded)             | disability  | Disability: no            | 4097 |       5.028 |    1.246 |         42.214 |
| NICE (bounded)             | disability  | Disability: yes           |  403 |       3.97  |    1.216 |         42.09  |
| DiCE first candidate       | gender      | Female                    | 1963 |      25.675 |    1.828 |         49.071 |
| DiCE first candidate       | gender      | Male                      | 2537 |      41.348 |    1.647 |         51.04  |
| DiCE first candidate       | age         | 0-35                      | 3291 |      35.339 |    1.697 |         50.549 |
| DiCE first candidate       | age         | 35+                       | 1209 |      32.258 |    1.733 |         49.96  |
| DiCE first candidate       | imd         | IMD 0-30% (most deprived) | 1861 |      31.703 |    1.724 |         49.977 |
| DiCE first candidate       | imd         | IMD 30-70%                | 1676 |      35.74  |    1.711 |         50.259 |
| DiCE first candidate       | imd         | IMD 70-100%               |  861 |      36.353 |    1.671 |         51.401 |
| DiCE first candidate       | imd         | IMD missing               |  102 |      50     |    1.654 |         50.815 |
| DiCE first candidate       | disability  | Disability: no            | 4097 |      34.513 |    1.708 |         50.608 |
| DiCE first candidate       | disability  | Disability: yes           |  403 |      34.491 |    1.687 |         48.295 |
| Policy repair + escalation | gender      | Female                    | 1963 |      94.294 |    2.16  |         49.444 |
| Policy repair + escalation | gender      | Male                      | 2537 |      88.727 |    1.786 |         53.53  |
| Policy repair + escalation | age         | 0-35                      | 3291 |      90.641 |    1.949 |         52.252 |
| Policy repair + escalation | age         | 35+                       | 1209 |      92.556 |    1.972 |         50.176 |
| Policy repair + escalation | imd         | IMD 0-30% (most deprived) | 1861 |      91.564 |    2.03  |         51.936 |
| Policy repair + escalation | imd         | IMD 30-70%                | 1676 |      91.05  |    1.933 |         51.13  |
| Policy repair + escalation | imd         | IMD 70-100%               |  861 |      90.244 |    1.864 |         52.355 |
| Policy repair + escalation | imd         | IMD missing               |  102 |      93.137 |    1.704 |         50.658 |
| Policy repair + escalation | disability  | Disability: no            | 4097 |      91.335 |    1.958 |         51.785 |
| Policy repair + escalation | disability  | Disability: yes           |  403 |      89.33  |    1.925 |         50.653 |
| DiCE + full gate           | gender      | Female                    | 1963 |      60.061 |    1.929 |         48.865 |
| DiCE + full gate           | gender      | Male                      | 2537 |      78.952 |    1.728 |         50.506 |
| DiCE + full gate           | age         | 0-35                      | 3291 |      71.316 |    1.792 |         50.125 |
| DiCE + full gate           | age         | 35+                       | 1209 |      69.065 |    1.83  |         49.262 |
| DiCE + full gate           | imd         | IMD 0-30% (most deprived) | 1861 |      69.694 |    1.838 |         49.721 |
| DiCE + full gate           | imd         | IMD 30-70%                | 1676 |      70.167 |    1.79  |         49.824 |
| DiCE + full gate           | imd         | IMD 70-100%               |  861 |      71.893 |    1.752 |         50.277 |
| DiCE + full gate           | imd         | IMD missing               |  102 |      88.235 |    1.798 |         50.816 |
| DiCE + full gate           | disability  | Disability: no            | 4097 |      70.759 |    1.804 |         50.05  |
| DiCE + full gate           | disability  | Disability: yes           |  403 |      70.223 |    1.784 |         48.344 |
| Framework                  | gender      | Female                    | 1963 |      93.938 |    1.946 |         43.946 |
| Framework                  | gender      | Male                      | 2537 |      94.482 |    1.646 |         45.721 |
| Framework                  | age         | 0-35                      | 3291 |      93.953 |    1.763 |         45.105 |
| Framework                  | age         | 35+                       | 1209 |      95.037 |    1.812 |         44.528 |
| Framework                  | imd         | IMD 0-30% (most deprived) | 1861 |      93.928 |    1.821 |         45.052 |
| Framework                  | imd         | IMD 30-70%                | 1676 |      94.57  |    1.771 |         44.532 |
| Framework                  | imd         | IMD 70-100%               |  861 |      93.844 |    1.712 |         45.403 |
| Framework                  | imd         | IMD missing               |  102 |      98.039 |    1.617 |         46.082 |
| Framework                  | disability  | Disability: no            | 4097 |      94.313 |    1.778 |         45.005 |
| Framework                  | disability  | Disability: yes           |  403 |      93.548 |    1.762 |         44.374 |
| Framework + fallback       | gender      | Female                    | 1963 |      95.008 |    1.949 |         43.91  |
| Framework + fallback       | gender      | Male                      | 2537 |      95.27  |    1.653 |         45.683 |
| Framework + fallback       | age         | 0-35                      | 3291 |      94.926 |    1.769 |         45.062 |
| Framework + fallback       | age         | 35+                       | 1209 |      95.782 |    1.816 |         44.502 |
| Framework + fallback       | imd         | IMD 0-30% (most deprived) | 1861 |      94.841 |    1.824 |         45.013 |
| Framework + fallback       | imd         | IMD 30-70%                | 1676 |      95.465 |    1.777 |         44.498 |
| Framework + fallback       | imd         | IMD 70-100%               |  861 |      94.89  |    1.719 |         45.354 |
| Framework + fallback       | imd         | IMD missing               |  102 |      98.039 |    1.617 |         46.082 |
| Framework + fallback       | disability  | Disability: no            | 4097 |      95.143 |    1.783 |         44.97  |
| Framework + fallback       | disability  | Disability: yes           |  403 |      95.285 |    1.77  |         44.31  |

## B. Recourse gaps and tests (Holm-adjusted)
| method                     | attribute   |    n |   yield_gap_pp |   p_yield |   effort_gap |   effort_gap_rel_pct |   p_effort |   p_yield_holm |   p_effort_holm |
|:---------------------------|:------------|-----:|---------------:|----------:|-------------:|---------------------:|-----------:|---------------:|----------------:|
| CARE (bounded)             | gender      |  300 |        16.4706 |    0.0029 |       0.5772 |              33.6065 |     0.0025 |         0.0728 |          0.0534 |
| CARE (bounded)             | age         |  300 |         1.4205 |    0.9251 |       0.3714 |              22.054  |     0.045  |         1      |          0.6295 |
| CARE (bounded)             | imd         |  300 |        13.3333 |    0.8394 |       0.2535 |              15.9158 |     0.3381 |         1      |          1      |
| CARE (bounded)             | disability  |  300 |         0.3256 |    1      |       0.3526 |              20.2224 |     0.0816 |         1      |          1      |
| MCCE (bounded)             | gender      | 4500 |        10.1972 |    0      |       1.3328 |              54.6864 |     0      |         0      |          0      |
| MCCE (bounded)             | age         | 4500 |         3.6186 |    0.0333 |       0.3862 |              15.3898 |     0      |         0.7668 |          0      |
| MCCE (bounded)             | imd         | 4500 |         8.6903 |    0.3039 |       0.6699 |              29.4258 |     0      |         1      |          0      |
| MCCE (bounded)             | disability  | 4500 |         2.3616 |    0.3918 |       0.013  |               0.5364 |     0.7805 |         1      |          1      |
| NICE (bounded)             | gender      | 4500 |         5.859  |    0      |       0.0074 |               0.5995 |     0.8923 |         0      |          1      |
| NICE (bounded)             | age         | 4500 |         0.5252 |    0.5199 |       0.1461 |              12.1078 |     0.0157 |         1      |          0.2512 |
| NICE (bounded)             | imd         | 4500 |         3.9205 |    0.0036 |       0.1267 |              10.0673 |     0.1634 |         0.0866 |          1      |
| NICE (bounded)             | disability  | 4500 |         1.0578 |    0.415  |       0.0302 |               2.4493 |     0.934  |         1      |          1      |
| DiCE first candidate       | gender      | 4500 |        15.6731 |    0      |       0.1806 |              10.3937 |     0      |         0      |          0      |
| DiCE first candidate       | age         | 4500 |         3.0807 |    0.0586 |       0.0368 |               2.1482 |     0.0321 |         1      |          0.4816 |
| DiCE first candidate       | imd         | 4500 |        18.2966 |    0.0002 |       0.0701 |               4.1481 |     0.4484 |         0.0052 |          1      |
| DiCE first candidate       | disability  | 4500 |         0.0217 |    1      |       0.0208 |               1.2261 |     0.2303 |         1      |          1      |
| Policy repair + escalation | gender      | 4500 |         5.5676 |    0      |       0.3735 |              18.9269 |     0      |         0      |          0      |
| Policy repair + escalation | age         | 4500 |         1.9147 |    0.0517 |       0.0236 |               1.2017 |     0.3402 |         1      |          1      |
| Policy repair + escalation | imd         | 4500 |         2.8934 |    0.6167 |       0.3256 |              17.2945 |     0      |         1      |          0      |
| Policy repair + escalation | disability  | 4500 |         2.0051 |    0.2074 |       0.0332 |               1.7091 |     0.3004 |         1      |          1      |
| DiCE + full gate           | gender      | 4500 |        18.8904 |    0      |       0.2018 |              11.0356 |     0      |         0      |          0      |
| DiCE + full gate           | age         | 4500 |         2.2504 |    0.1517 |       0.0381 |               2.1059 |     0.0092 |         1      |          0.165  |
| DiCE + full gate           | imd         | 4500 |        18.5416 |    0.0007 |       0.0863 |               4.8101 |     0.0049 |         0.0195 |          0.099  |
| DiCE + full gate           | disability  | 4500 |         0.5358 |    0.8665 |       0.0197 |               1.0969 |     0.196  |         1      |          1      |
| Framework                  | gender      | 4500 |         0.5438 |    0.4763 |       0.3002 |              16.7132 |     0      |         1      |          0      |
| Framework                  | age         | 4500 |         1.084  |    0.1896 |       0.0486 |               2.7207 |     0.0076 |         1      |          0.1436 |
| Framework                  | imd         | 4500 |         4.1948 |    0.3038 |       0.2032 |              11.744  |     0      |         1      |          0      |
| Framework                  | disability  | 4500 |         0.7645 |    0.6054 |       0.0156 |               0.8815 |     0.5481 |         1      |          1      |
| Framework + fallback       | gender      | 4500 |         0.2624 |    0.7365 |       0.2963 |              16.4543 |     0      |         1      |          0      |
| Framework + fallback       | age         | 4500 |         0.8561 |    0.2682 |       0.0468 |               2.6123 |     0.0106 |         1      |          0.181  |
| Framework + fallback       | imd         | 4500 |         3.1977 |    0.437  |       0.2068 |              11.9238 |     0      |         1      |          0      |
| Framework + fallback       | disability  | 4500 |         0.1426 |    0.9955 |       0.0127 |               0.7174 |     0.6084 |         1      |          1      |

## C. Module x stage adjusted contrasts (cluster-robust by learner, Holm)
| method                     | attribute   | contrast                                | outcome   |    n |   raw_diff |   adj_diff |    ci_lo |   ci_hi |      p |   p_holm |
|:---------------------------|:------------|:----------------------------------------|:----------|-----:|-----------:|-----------:|---------:|--------:|-------:|---------:|
| CARE (bounded)             | gender      | Female - Male                           | yield_pp  |  300 |   -16.4706 |    -2.333  | -21.6694 | 17.0033 | 0.8131 |   1      |
| CARE (bounded)             | gender      | Female - Male                           | effort    |   88 |     0.5772 |     0.0588 |  -0.2678 |  0.3853 | 0.7244 |   1      |
| CARE (bounded)             | age         | 35+ - 0-35                              | yield_pp  |  300 |     1.4205 |    -0.9242 | -13.2732 | 11.4248 | 0.8834 |   1      |
| CARE (bounded)             | age         | 35+ - 0-35                              | effort    |   88 |     0.3714 |     0.1046 |  -0.1642 |  0.3735 | 0.4456 |   1      |
| CARE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  |  175 |    -4.3011 |    -5.3111 | -20.39   |  9.7679 | 0.49   |   1      |
| CARE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    |   53 |     0.2416 |     0.0397 |  -0.2013 |  0.2806 | 0.7469 |   1      |
| CARE (bounded)             | disability  | Disability: yes - Disability: no        | yield_pp  |  300 |     0.3256 |     5.0985 | -13.2327 | 23.4297 | 0.5857 |   1      |
| CARE (bounded)             | disability  | Disability: yes - Disability: no        | effort    |   88 |     0.3526 |     0.2075 |  -0.0554 |  0.4704 | 0.1218 |   1      |
| MCCE (bounded)             | gender      | Female - Male                           | yield_pp  | 4500 |    10.1972 |     1.7008 |  -3.3953 |  6.7969 | 0.513  |   1      |
| MCCE (bounded)             | gender      | Female - Male                           | effort    | 2036 |     1.3328 |    -0.0754 |  -0.2125 |  0.0616 | 0.2805 |   1      |
| MCCE (bounded)             | age         | 35+ - 0-35                              | yield_pp  | 4500 |     3.6186 |     1.3718 |  -2.6101 |  5.3536 | 0.4995 |   1      |
| MCCE (bounded)             | age         | 35+ - 0-35                              | effort    | 2036 |     0.3862 |     0.1007 |  -0.0112 |  0.2126 | 0.0777 |   1      |
| MCCE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2722 |     1.7459 |    -1.0653 |  -5.8196 |  3.6889 | 0.6605 |   1      |
| MCCE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    | 1237 |     0.3318 |    -0.0091 |  -0.1301 |  0.1119 | 0.883  |   1      |
| MCCE (bounded)             | disability  | Disability: yes - Disability: no        | yield_pp  | 4500 |     2.3616 |     4.1601 |  -2.021  | 10.3412 | 0.1871 |   1      |
| MCCE (bounded)             | disability  | Disability: yes - Disability: no        | effort    | 2036 |     0.013  |     0.0142 |  -0.1457 |  0.1742 | 0.8615 |   1      |
| NICE (bounded)             | gender      | Female - Male                           | yield_pp  | 4500 |    -5.859  |    -0.0267 |  -2.0248 |  1.9714 | 0.9791 |   1      |
| NICE (bounded)             | gender      | Female - Male                           | effort    |  222 |    -0.0074 |     0.0466 |  -0.0433 |  0.1365 | 0.3093 |   1      |
| NICE (bounded)             | age         | 35+ - 0-35                              | yield_pp  | 4500 |    -0.5252 |     0.2904 |  -1.3734 |  1.9542 | 0.7323 |   1      |
| NICE (bounded)             | age         | 35+ - 0-35                              | effort    |  222 |    -0.1461 |    -0.0641 |  -0.1117 | -0.0165 | 0.0083 |   0.5291 |
| NICE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2722 |    -3.046  |    -1.757  |  -3.8565 |  0.3426 | 0.101  |   1      |
| NICE (bounded)             | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    |  133 |     0.0062 |    -0.0181 |  -0.0832 |  0.047  | 0.5857 |   1      |
| NICE (bounded)             | disability  | Disability: yes - Disability: no        | yield_pp  | 4500 |    -1.0578 |    -0.853  |  -3.1511 |  1.445  | 0.4669 |   1      |
| NICE (bounded)             | disability  | Disability: yes - Disability: no        | effort    |  222 |    -0.0302 |    -0.0139 |  -0.0777 |  0.0499 | 0.6692 |   1      |
| DiCE first candidate       | gender      | Female - Male                           | yield_pp  | 4500 |   -15.6731 |     3.1931 |  -0.9201 |  7.3063 | 0.1281 |   1      |
| DiCE first candidate       | gender      | Female - Male                           | effort    | 1553 |     0.1806 |     0.0115 |  -0.059  |  0.0819 | 0.7497 |   1      |
| DiCE first candidate       | age         | 35+ - 0-35                              | yield_pp  | 4500 |    -3.0807 |    -0.5157 |  -3.9802 |  2.9488 | 0.7705 |   1      |
| DiCE first candidate       | age         | 35+ - 0-35                              | effort    | 1553 |     0.0368 |     0.0097 |  -0.0358 |  0.0551 | 0.6768 |   1      |
| DiCE first candidate       | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2722 |    -4.6497 |    -0.6173 |  -5.0101 |  3.7754 | 0.783  |   1      |
| DiCE first candidate       | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    |  903 |     0.0537 |     0.0013 |  -0.0534 |  0.056  | 0.9639 |   1      |
| DiCE first candidate       | disability  | Disability: yes - Disability: no        | yield_pp  | 4500 |    -0.0217 |    -0.761  |  -6.2249 |  4.7029 | 0.7849 |   1      |
| DiCE first candidate       | disability  | Disability: yes - Disability: no        | effort    | 1553 |    -0.0208 |    -0.022  |  -0.0913 |  0.0474 | 0.5346 |   1      |
| Policy repair + escalation | gender      | Female - Male                           | yield_pp  | 4500 |     5.5676 |    -0.1727 |  -2.6801 |  2.3347 | 0.8926 |   1      |
| Policy repair + escalation | gender      | Female - Male                           | effort    | 4102 |     0.3735 |    -0.064  |  -0.1427 |  0.0148 | 0.1117 |   1      |
| Policy repair + escalation | age         | 35+ - 0-35                              | yield_pp  | 4500 |     1.9147 |     0.5941 |  -1.2619 |  2.4502 | 0.5304 |   1      |
| Policy repair + escalation | age         | 35+ - 0-35                              | effort    | 4102 |     0.0236 |    -0.0464 |  -0.1071 |  0.0143 | 0.1341 |   1      |
| Policy repair + escalation | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2722 |     1.3198 |    -0.045  |  -2.4212 |  2.3312 | 0.9704 |   1      |
| Policy repair + escalation | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    | 2481 |     0.1662 |     0.0411 |  -0.0329 |  0.1152 | 0.2765 |   1      |
| Policy repair + escalation | disability  | Disability: yes - Disability: no        | yield_pp  | 4500 |    -2.0051 |    -0.9088 |  -4.2264 |  2.4089 | 0.5914 |   1      |
| Policy repair + escalation | disability  | Disability: yes - Disability: no        | effort    | 4102 |    -0.0332 |    -0.0062 |  -0.0989 |  0.0866 | 0.8964 |   1      |
| DiCE + full gate           | gender      | Female - Male                           | yield_pp  | 4500 |   -18.8904 |     0.0091 |  -4.6743 |  4.6925 | 0.997  |   1      |
| DiCE + full gate           | gender      | Female - Male                           | effort    | 3182 |     0.2018 |    -0.0416 |  -0.0961 |  0.0129 | 0.1348 |   1      |
| DiCE + full gate           | age         | 35+ - 0-35                              | yield_pp  | 4500 |    -2.2504 |     0.4231 |  -3.0343 |  3.8806 | 0.8104 |   1      |
| DiCE + full gate           | age         | 35+ - 0-35                              | effort    | 3182 |     0.0381 |     0.0055 |  -0.0324 |  0.0435 | 0.7749 |   1      |
| DiCE + full gate           | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2722 |    -2.1994 |     2.2454 |  -2.0512 |  6.542  | 0.3057 |   1      |
| DiCE + full gate           | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    | 1916 |     0.0863 |     0.0197 |  -0.0263 |  0.0657 | 0.4008 |   1      |
| DiCE + full gate           | disability  | Disability: yes - Disability: no        | yield_pp  | 4500 |    -0.5358 |    -0.4987 |  -5.396  |  4.3985 | 0.8418 |   1      |
| DiCE + full gate           | disability  | Disability: yes - Disability: no        | effort    | 3182 |    -0.0197 |    -0.0145 |  -0.0692 |  0.0401 | 0.6023 |   1      |
| Framework                  | gender      | Female - Male                           | yield_pp  | 4500 |    -0.5438 |     0.7924 |  -1.0821 |  2.667  | 0.4074 |   1      |
| Framework                  | gender      | Female - Male                           | effort    | 4241 |     0.3002 |    -0.0417 |  -0.1069 |  0.0236 | 0.2109 |   1      |
| Framework                  | age         | 35+ - 0-35                              | yield_pp  | 4500 |     1.084  |     0.5097 |  -0.9116 |  1.9309 | 0.4821 |   1      |
| Framework                  | age         | 35+ - 0-35                              | effort    | 4241 |     0.0486 |    -0.0118 |  -0.0605 |  0.0369 | 0.6353 |   1      |
| Framework                  | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2722 |     0.0836 |    -0.0484 |  -1.9692 |  1.8724 | 0.9606 |   1      |
| Framework                  | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    | 2556 |     0.1083 |     0.01   |  -0.0515 |  0.0715 | 0.749  |   1      |
| Framework                  | disability  | Disability: yes - Disability: no        | yield_pp  | 4500 |    -0.7645 |    -0.732  |  -3.176  |  1.7119 | 0.5571 |   1      |
| Framework                  | disability  | Disability: yes - Disability: no        | effort    | 4241 |    -0.0156 |    -0.0132 |  -0.085  |  0.0585 | 0.7177 |   1      |
| Framework + fallback       | gender      | Female - Male                           | yield_pp  | 4500 |    -0.2624 |     0.1296 |  -1.5535 |  1.8128 | 0.88   |   1      |
| Framework + fallback       | gender      | Female - Male                           | effort    | 4282 |     0.2963 |    -0.0447 |  -0.1097 |  0.0204 | 0.1785 |   1      |
| Framework + fallback       | age         | 35+ - 0-35                              | yield_pp  | 4500 |     0.8561 |     0.1519 |  -1.1602 |  1.464  | 0.8205 |   1      |
| Framework + fallback       | age         | 35+ - 0-35                              | effort    | 4282 |     0.0468 |    -0.0129 |  -0.0617 |  0.0359 | 0.6046 |   1      |
| Framework + fallback       | imd         | IMD 0-30% (most deprived) - IMD 70-100% | yield_pp  | 2722 |    -0.0482 |    -0.3791 |  -2.1274 |  1.3692 | 0.6708 |   1      |
| Framework + fallback       | imd         | IMD 0-30% (most deprived) - IMD 70-100% | effort    | 2582 |     0.1048 |     0.0081 |  -0.0533 |  0.0695 | 0.7969 |   1      |
| Framework + fallback       | disability  | Disability: yes - Disability: no        | yield_pp  | 4500 |     0.1426 |     0.1265 |  -2.0154 |  2.2683 | 0.9079 |   1      |
| Framework + fallback       | disability  | Disability: yes - Disability: no        | effort    | 4282 |    -0.0127 |    -0.0105 |  -0.0823 |  0.0613 | 0.7738 |   1      |