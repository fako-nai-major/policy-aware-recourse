## (a) Bound validity (Prop. 4.1)
queries: 20812; LB_R > exact cost: 0; model dual bound > exact cost: 0

## Certified abstention (Theorem 2)
exact infeasible: 3472; of which rule-infeasible (R empty): 88; rule-feasible but A empty: 3384

## (b) Rule-binding queries (OPT = LB_R) and repair optimality (Props. 4.2, 5)
| dataset   | regime   | model   |    n |   rule_binding_pct |   repair0_accepted_by_f |   repair0_is_opt_pct |   repair_esc_opt_pct |
|:----------|:---------|:--------|-----:|-------------------:|------------------------:|---------------------:|---------------------:|
| ADULT     | aligned  | cat     |  307 |                1   |                       3 |                  nan |                 37.5 |
| ADULT     | aligned  | lr      |  291 |                0   |                       0 |                  nan |                  0   |
| ADULT     | aligned  | mlp     |  310 |                0   |                       0 |                  nan |                  0   |
| ADULT     | aligned  | rf      |  297 |                0   |                       0 |                  nan |                  0   |
| GMSC      | aligned  | cat     |  985 |               10.1 |                      99 |                  nan |                 19.1 |
| GMSC      | aligned  | lr      |  809 |                2   |                      16 |                  nan |                 37.2 |
| GMSC      | aligned  | mlp     |  626 |                9.9 |                      62 |                  nan |                 27.3 |
| GMSC      | aligned  | rf      |  247 |                7.7 |                      19 |                  nan |                 13.2 |
| HMDA      | aligned  | cat     | 1300 |               98.7 |                    1282 |                  100 |                 98.8 |
| HMDA      | aligned  | lr      |  492 |              100   |                     492 |                  100 |                100   |
| HMDA      | aligned  | mlp     | 1235 |               99.8 |                    1232 |                  100 |                 99.8 |
| HMDA      | aligned  | rf      | 1357 |               99.9 |                    1355 |                  100 |                100   |
| HMDA_OR   | aligned  | cat     |  808 |               98.5 |                     795 |                  nan |                 96.4 |
| HMDA_OR   | aligned  | lr      |  275 |              100   |                     275 |                  nan |                 99.6 |
| HMDA_OR   | aligned  | mlp     |  762 |               99.7 |                     760 |                  nan |                 98.3 |
| HMDA_OR   | aligned  | rf      |  840 |               99.8 |                     838 |                  nan |                 98.5 |
| HMDA_S    | aligned  | cat     |  806 |               98.4 |                     793 |                  nan |                 98.5 |
| HMDA_S    | aligned  | lr      |  275 |              100   |                     275 |                  nan |                100   |
| HMDA_S    | aligned  | mlp     |  762 |               99.7 |                     760 |                  nan |                 99.7 |
| HMDA_S    | aligned  | rf      |  837 |               99.9 |                     836 |                  nan |                 99.9 |
| OULAD     | aligned  | cat     |  288 |               75.3 |                      48 |                  nan |                 17.5 |
| OULAD     | aligned  | lr      |  286 |               24.5 |                      32 |                  nan |                 11.2 |
| OULAD     | aligned  | mlp     |  290 |               37.2 |                      30 |                  nan |                 10.6 |
| OULAD     | aligned  | rf      |  174 |               80.5 |                      38 |                  nan |                 22.1 |
| OULAD     | floor    | cat     |  288 |               38.9 |                      55 |                  nan |                 20.4 |
| OULAD     | floor    | lr      |  286 |               14.7 |                      42 |                  nan |                 15.4 |
| OULAD     | floor    | mlp     |  290 |               18.3 |                      34 |                  nan |                 12.1 |
| OULAD     | floor    | rf      |  174 |               36.8 |                      17 |                  nan |                 13.4 |
| PIMA      | aligned  | cat     |  461 |               44   |                     203 |                  100 |                 44.3 |
| PIMA      | aligned  | lr      |  427 |               61.4 |                     262 |                  100 |                 61.4 |
| PIMA      | aligned  | mlp     |  288 |               51.4 |                     148 |                  100 |                 54.4 |
| PIMA      | aligned  | rf      |  467 |               51.6 |                     241 |                  100 |                 51.6 |

## (c) Escalation end-point test, linear models (Theorem 7.2)
| dataset   | regime   | subset   |   n |   esc_success_pct |   end_point_ok_pct |   agreement_pct |   esc_fail_but_end_ok |   esc_ok_but_end_fail |
|:----------|:---------|:---------|----:|------------------:|-------------------:|----------------:|----------------------:|----------------------:|
| HMDA      | aligned  | all      | 492 |             100   |              100   |             100 |                     0 |                     0 |
| HMDA      | aligned  | seed 0   |  74 |             100   |              100   |             100 |                     0 |                     0 |
| HMDA      | aligned  | seed 1   | 109 |             100   |              100   |             100 |                     0 |                     0 |
| HMDA      | aligned  | seed 2   |  92 |             100   |              100   |             100 |                     0 |                     0 |
| HMDA      | aligned  | seed 3   |  99 |             100   |              100   |             100 |                     0 |                     0 |
| HMDA      | aligned  | seed 4   | 118 |             100   |              100   |             100 |                     0 |                     0 |
| OULAD     | aligned  | all      | 300 |              95.3 |               95.3 |             100 |                     0 |                     0 |
| OULAD     | aligned  | seed 0   |  60 |              95   |               95   |             100 |                     0 |                     0 |
| OULAD     | aligned  | seed 1   |  60 |              96.7 |               96.7 |             100 |                     0 |                     0 |
| OULAD     | aligned  | seed 2   |  60 |              96.7 |               96.7 |             100 |                     0 |                     0 |
| OULAD     | aligned  | seed 3   |  60 |              91.7 |               91.7 |             100 |                     0 |                     0 |
| OULAD     | aligned  | seed 4   |  60 |              96.7 |               96.7 |             100 |                     0 |                     0 |
| OULAD     | floor    | all      | 300 |              95.3 |               95.3 |             100 |                     0 |                     0 |
| OULAD     | floor    | seed 0   |  60 |              95   |               95   |             100 |                     0 |                     0 |
| OULAD     | floor    | seed 1   |  60 |              96.7 |               96.7 |             100 |                     0 |                     0 |
| OULAD     | floor    | seed 2   |  60 |              96.7 |               96.7 |             100 |                     0 |                     0 |
| OULAD     | floor    | seed 3   |  60 |              91.7 |               91.7 |             100 |                     0 |                     0 |
| OULAD     | floor    | seed 4   |  60 |              96.7 |               96.7 |             100 |                     0 |                     0 |
| PIMA      | aligned  | all      | 427 |             100   |              100   |             100 |                     0 |                     0 |
| PIMA      | aligned  | seed 0   |  50 |             100   |              100   |             100 |                     0 |                     0 |
| PIMA      | aligned  | seed 1   |  36 |             100   |              100   |             100 |                     0 |                     0 |
| PIMA      | aligned  | seed 2   |  31 |             100   |              100   |             100 |                     0 |                     0 |
| PIMA      | aligned  | seed 3   |  53 |             100   |              100   |             100 |                     0 |                     0 |
| PIMA      | aligned  | seed 4   |  42 |             100   |              100   |             100 |                     0 |                     0 |
| PIMA      | aligned  | seed 5   |  40 |             100   |              100   |             100 |                     0 |                     0 |
| PIMA      | aligned  | seed 6   |  43 |             100   |              100   |             100 |                     0 |                     0 |
| PIMA      | aligned  | seed 7   |  32 |             100   |              100   |             100 |                     0 |                     0 |
| PIMA      | aligned  | seed 8   |  53 |             100   |              100   |             100 |                     0 |                     0 |
| PIMA      | aligned  | seed 9   |  47 |             100   |              100   |             100 |                     0 |                     0 |

## (d) Price of compliance: OPT - LB_F (both proven optimal)
| dataset   | regime   | model   |    n |   cost_exact |   cost_model_only |   poc_mean |   poc_pct |   rule_free_pct |
|:----------|:---------|:--------|-----:|-------------:|------------------:|-----------:|----------:|----------------:|
| ADULT     | aligned  | cat     |  307 |        1.267 |             0.985 |      0.282 |      28.6 |            45   |
| ADULT     | aligned  | lr      |  291 |        1.269 |             0.762 |      0.507 |      66.5 |            13.4 |
| ADULT     | aligned  | mlp     |  310 |        1.21  |             1.027 |      0.183 |      17.8 |            56.8 |
| ADULT     | aligned  | rf      |  297 |        1.37  |             1.234 |      0.136 |      11   |            77.1 |
| GMSC      | aligned  | cat     |  985 |        0.98  |             0.852 |      0.128 |      15   |            69   |
| GMSC      | aligned  | lr      |  809 |        1.36  |             1.027 |      0.333 |      32.5 |            57.5 |
| GMSC      | aligned  | mlp     |  626 |        1.346 |             1.185 |      0.161 |      13.6 |            64.2 |
| GMSC      | aligned  | rf      |   48 |        1.112 |             0.959 |      0.152 |      15.9 |            68.8 |
| HMDA      | aligned  | cat     | 1300 |        0.785 |             0.678 |      0.107 |      15.8 |             1.5 |
| HMDA      | aligned  | lr      |  492 |        0.871 |             0.53  |      0.341 |      64.3 |             0   |
| HMDA      | aligned  | mlp     | 1235 |        0.805 |             0.639 |      0.166 |      26   |             0.2 |
| HMDA      | aligned  | rf      | 1357 |        0.787 |             0.684 |      0.103 |      15.1 |             0.1 |
| HMDA_OR   | aligned  | cat     |  808 |        0.858 |             0.678 |      0.18  |      26.6 |             1.6 |
| HMDA_OR   | aligned  | lr      |  275 |        0.961 |             0.525 |      0.436 |      83   |             0   |
| HMDA_OR   | aligned  | mlp     |  762 |        0.879 |             0.633 |      0.246 |      38.9 |             0.3 |
| HMDA_OR   | aligned  | rf      |  840 |        0.856 |             0.682 |      0.174 |      25.5 |             0.2 |
| HMDA_S    | aligned  | cat     |  806 |        0.8   |             0.69  |      0.11  |      15.9 |             1.6 |
| HMDA_S    | aligned  | lr      |  275 |        0.874 |             0.525 |      0.349 |      66.4 |             0   |
| HMDA_S    | aligned  | mlp     |  762 |        0.804 |             0.634 |      0.17  |      26.8 |             0.3 |
| HMDA_S    | aligned  | rf      |  837 |        0.79  |             0.687 |      0.103 |      14.9 |             0.1 |
| OULAD     | aligned  | cat     |   11 |        2.207 |             1.871 |      0.336 |      18   |             0   |
| OULAD     | aligned  | lr      |  286 |        2.788 |             2.743 |      0.044 |       1.6 |            75.9 |
| OULAD     | aligned  | mlp     |   57 |        2.828 |             2.696 |      0.131 |       4.9 |            61.4 |
| OULAD     | aligned  | rf      |    2 |        1.237 |             1.044 |      0.193 |      18.5 |             0   |
| OULAD     | floor    | cat     |   36 |        5.671 |             5.455 |      0.216 |       4   |            47.2 |
| OULAD     | floor    | lr      |  286 |        6.525 |             6.514 |      0.012 |       0.2 |            88.1 |
| OULAD     | floor    | mlp     |   58 |        6.662 |             6.645 |      0.017 |       0.3 |            89.7 |
| OULAD     | floor    | rf      |   17 |        3.267 |             3.11  |      0.157 |       5.1 |            41.2 |
| PIMA      | aligned  | cat     |  461 |        1.37  |             0.872 |      0.498 |      57.1 |            14.1 |
| PIMA      | aligned  | lr      |  427 |        1.447 |             0.876 |      0.571 |      65.2 |             8.4 |
| PIMA      | aligned  | mlp     |  288 |        1.482 |             0.872 |      0.609 |      69.9 |            14.2 |
| PIMA      | aligned  | rf      |  467 |        1.338 |             0.833 |      0.505 |      60.6 |            11.3 |

## (e) A-posteriori gap certificate (Prop. 4.3): mean true vs certified gap
| dataset   | regime   | model   | method     |    n |   true_gap |   certified_gap |   certificate_tight_pct |
|:----------|:---------|:--------|:-----------|-----:|-----------:|----------------:|------------------------:|
| ADULT     | aligned  | cat     | repair_esc |    8 |      0.047 |           0.054 |                    87.5 |
| ADULT     | aligned  | cat     | framework  |  266 |      0.468 |           0.711 |                    48.9 |
| ADULT     | aligned  | lr      | framework  |  187 |      0.632 |           1.024 |                    19.8 |
| ADULT     | aligned  | mlp     | repair_esc |    1 |      0.028 |           0.028 |                   100   |
| ADULT     | aligned  | mlp     | framework  |  264 |      0.511 |           0.661 |                    62.5 |
| ADULT     | aligned  | rf      | repair_esc |    2 |      0.01  |           0.018 |                    50   |
| ADULT     | aligned  | rf      | framework  |  271 |      0.482 |           0.617 |                    77.1 |
| GMSC      | aligned  | cat     | repair_esc |  565 |      0.142 |           0.181 |                    76.8 |
| GMSC      | aligned  | cat     | framework  |  980 |      0.523 |           0.577 |                    79.1 |
| GMSC      | aligned  | lr      | repair_esc |   43 |      0.196 |           0.277 |                    72.1 |
| GMSC      | aligned  | lr      | framework  |  806 |      0.477 |           0.766 |                    59.3 |
| GMSC      | aligned  | mlp     | repair_esc |  231 |      0.104 |           0.159 |                    70.6 |
| GMSC      | aligned  | mlp     | framework  |  622 |      0.418 |           0.534 |                    74.1 |
| GMSC      | aligned  | rf      | repair_esc |  152 |      0.222 |           0.653 |                    23.7 |
| GMSC      | aligned  | rf      | framework  |  246 |      0.547 |           1.135 |                    20.7 |
| HMDA      | aligned  | cat     | repair_esc | 1298 |      0.007 |           0.007 |                   100   |
| HMDA      | aligned  | cat     | framework  | 1300 |      0.175 |           0.175 |                   100   |
| HMDA      | aligned  | lr      | repair_esc |  492 |     -0     |          -0     |                   100   |
| HMDA      | aligned  | lr      | framework  |  492 |      0.269 |           0.269 |                   100   |
| HMDA      | aligned  | mlp     | repair_esc | 1235 |      0     |           0     |                   100   |
| HMDA      | aligned  | mlp     | framework  | 1235 |      0.201 |           0.201 |                   100   |
| HMDA      | aligned  | rf      | repair_esc | 1355 |     -0     |          -0     |                   100   |
| HMDA      | aligned  | rf      | framework  | 1357 |      0.167 |           0.167 |                   100   |
| HMDA_OR   | aligned  | cat     | repair_esc |  808 |      0.014 |           0.014 |                   100   |
| HMDA_OR   | aligned  | cat     | framework  |  808 |      0.196 |           0.196 |                   100   |
| HMDA_OR   | aligned  | lr      | repair_esc |  275 |      0.002 |           0.002 |                   100   |
| HMDA_OR   | aligned  | lr      | framework  |  275 |      0.287 |           0.287 |                   100   |
| HMDA_OR   | aligned  | mlp     | repair_esc |  762 |      0.008 |           0.008 |                   100   |
| HMDA_OR   | aligned  | mlp     | framework  |  762 |      0.214 |           0.214 |                   100   |
| HMDA_OR   | aligned  | rf      | repair_esc |  839 |      0.008 |           0.008 |                   100   |
| HMDA_OR   | aligned  | rf      | framework  |  840 |      0.18  |           0.18  |                   100   |
| HMDA_S    | aligned  | cat     | repair_esc |  805 |      0.008 |           0.008 |                   100   |
| HMDA_S    | aligned  | cat     | framework  |  806 |      0.202 |           0.202 |                   100   |
| HMDA_S    | aligned  | lr      | repair_esc |  275 |     -0     |          -0     |                   100   |
| HMDA_S    | aligned  | lr      | framework  |  275 |      0.263 |           0.263 |                   100   |
| HMDA_S    | aligned  | mlp     | repair_esc |  762 |      0.001 |           0.001 |                   100   |
| HMDA_S    | aligned  | mlp     | framework  |  762 |      0.225 |           0.225 |                   100   |
| HMDA_S    | aligned  | rf      | repair_esc |  837 |      0     |           0     |                   100   |
| HMDA_S    | aligned  | rf      | framework  |  837 |      0.197 |           0.197 |                   100   |
| OULAD     | aligned  | cat     | repair_esc |  274 |      0.633 |           0.692 |                    78.5 |
| OULAD     | aligned  | cat     | framework  |  288 |      0.33  |           0.408 |                    75.3 |
| OULAD     | aligned  | lr      | repair_esc |  286 |      0.354 |           0.354 |                   100   |
| OULAD     | aligned  | lr      | framework  |  286 |      0.303 |           0.303 |                   100   |
| OULAD     | aligned  | mlp     | repair_esc |  282 |      0.514 |           0.662 |                    50.4 |
| OULAD     | aligned  | mlp     | framework  |  290 |      0.336 |           0.511 |                    49.3 |
| OULAD     | aligned  | rf      | repair_esc |  169 |      0.556 |           0.596 |                    82.8 |
| OULAD     | aligned  | rf      | framework  |  171 |      0.265 |           0.31  |                    81.9 |
| OULAD     | floor    | cat     | repair_esc |  270 |      0.647 |           0.8   |                    46.3 |
| OULAD     | floor    | cat     | framework  |  284 |      1.025 |           1.194 |                    44.7 |
| OULAD     | floor    | lr      | repair_esc |  286 |      0.216 |           0.216 |                   100   |
| OULAD     | floor    | lr      | framework  |  286 |      0.976 |           0.976 |                   100   |
| OULAD     | floor    | mlp     | repair_esc |  282 |      0.303 |           0.563 |                    36.9 |
| OULAD     | floor    | mlp     | framework  |  290 |      0.984 |           1.267 |                    36.2 |
| OULAD     | floor    | rf      | repair_esc |  142 |      0.529 |           0.631 |                    50   |
| OULAD     | floor    | rf      | framework  |  144 |      0.765 |           0.872 |                    49.3 |
| PIMA      | aligned  | cat     | repair_esc |  461 |      0.183 |           0.236 |                    58.1 |
| PIMA      | aligned  | cat     | framework  |  461 |      0.408 |           0.461 |                    58.1 |
| PIMA      | aligned  | lr      | repair_esc |  427 |      0.102 |           0.148 |                    69.8 |
| PIMA      | aligned  | lr      | framework  |  427 |      0.407 |           0.453 |                    69.8 |
| PIMA      | aligned  | mlp     | repair_esc |  272 |      0.161 |           0.244 |                    66.9 |
| PIMA      | aligned  | mlp     | framework  |  287 |      0.411 |           0.516 |                    65.9 |
| PIMA      | aligned  | rf      | repair_esc |  467 |      0.177 |           0.214 |                    62.7 |
| PIMA      | aligned  | rf      | framework  |  467 |      0.435 |           0.472 |                    62.7 |
