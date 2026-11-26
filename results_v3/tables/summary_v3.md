## Accepted yield (%)
|                               | dice_first   | posthoc_full_gate   | ocean      | ocean_joint   | ocean_joint_free   | dace        | dace_rule   | mace        | mace_rule   | framework   | repair      | repair_esc   | repair_sparse0   | repair_sparse   | exact       |   queries |   rule attainable % |
|:------------------------------|:-------------|:--------------------|:-----------|:--------------|:-------------------|:------------|:------------|:------------|:------------|:------------|:------------|:-------------|:-----------------|:----------------|:------------|----------:|--------------------:|
| ('ADULT', 'aligned', 'cat')   | 9.8 ± 2.9    | 26.3 ± 2.7          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 26.6 ± 2.8  | 0.3 ± 0.4   | 0.8 ± 0.9    | 0.3 ± 0.4        | 0.8 ± 0.9       | 30.7 ± 2.4  |      1000 |               100   |
| ('ADULT', 'aligned', 'lr')    | 3.9 ± 0.9    | 18.5 ± 3.4          | nan        | nan           | nan                | 11.7 ± 7.6  | 18.3 ± 10.4 | 20.0 ± 8.7  | 33.3 ± 5.8  | 18.7 ± 3.7  | 0.0 ± 0.0   | 0.0 ± 0.0    | 0.0 ± 0.0        | 0.0 ± 0.0       | 29.1 ± 1.8  |      1000 |               100   |
| ('ADULT', 'aligned', 'mlp')   | 7.7 ± 2.9    | 26.1 ± 4.7          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 26.4 ± 4.6  | 0.0 ± 0.0   | 0.1 ± 0.2    | 0.0 ± 0.0        | 0.1 ± 0.2       | 31.0 ± 4.2  |      1000 |               100   |
| ('ADULT', 'aligned', 'rf')    | 7.2 ± 2.1    | 26.9 ± 3.3          | 20.7 ± 2.9 | 27.8 ± 4.0    | 27.8 ± 4.0         | 10.0 ± 5.0  | 20.0 ± 21.8 | 20.0 ± 8.7  | 31.7 ± 22.5 | 27.1 ± 3.5  | 0.0 ± 0.0   | 0.2 ± 0.3    | 0.0 ± 0.0        | 0.2 ± 0.3       | 29.7 ± 3.4  |      1000 |               100   |
| ('GMSC', 'aligned', 'cat')    | 76.4 ± 2.3   | 97.4 ± 0.8          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 98.0 ± 0.8  | 9.9 ± 2.2   | 56.5 ± 4.0   | 9.9 ± 2.2        | 56.5 ± 4.0      | 98.5 ± 0.5  |      1000 |               100   |
| ('GMSC', 'aligned', 'lr')     | 52.3 ± 5.4   | 76.7 ± 4.8          | nan        | nan           | nan                | 48.3 ± 12.6 | 70.0 ± 13.2 | 45.0 ± 15.0 | 80.0 ± 10.0 | 80.6 ± 4.3  | 1.6 ± 1.4   | 4.3 ± 2.3    | 1.6 ± 1.4        | 4.3 ± 2.3       | 80.9 ± 4.3  |      1000 |               100   |
| ('GMSC', 'aligned', 'mlp')    | 46.7 ± 3.8   | 60.8 ± 3.0          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 62.2 ± 3.6  | 6.2 ± 1.8   | 23.1 ± 5.7   | 6.2 ± 1.8        | 23.1 ± 5.7      | 62.6 ± 3.3  |      1000 |               100   |
| ('GMSC', 'aligned', 'rf')     | 74.8 ± 8.1   | 98.0 ± 2.0          | 66.8 ± 8.3 | 83.6 ± 6.1    | 97.6 ± 2.2         | 0.0         | 0.0         | 30.0        | 50.0        | 98.4 ± 1.7  | 7.6 ± 1.7   | 60.8 ± 5.0   | 7.6 ± 1.7        | 60.8 ± 5.0      | 98.8 ± 1.8  |       250 |               100   |
| ('HMDA', 'aligned', 'cat')    | 86.2 ± 2.7   | 99.9 ± 0.2          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 99.9 ± 0.2  | 98.6 ± 0.8  | 99.8 ± 0.2   | 98.6 ± 0.8       | 99.8 ± 0.2      | 99.9 ± 0.2  |      1301 |               100   |
| ('HMDA', 'aligned', 'lr')     | 50.8 ± 8.8   | 100.0 ± 0.0         | nan        | nan           | nan                | 0.0 ± 0.0   | 88.3 ± 5.8  | 0.0 ± 0.0   | 100.0 ± 0.0 | 100.0 ± 0.0 | 100.0 ± 0.0 | 100.0 ± 0.0  | 100.0 ± 0.0      | 100.0 ± 0.0     | 100.0 ± 0.0 |       492 |               100   |
| ('HMDA', 'aligned', 'mlp')    | 78.2 ± 4.2   | 100.0 ± 0.0         | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 100.0 ± 0.0 | 99.8 ± 0.2  | 100.0 ± 0.0  | 99.8 ± 0.2       | 100.0 ± 0.0     | 100.0 ± 0.0 |      1235 |               100   |
| ('HMDA', 'aligned', 'rf')     | 88.8 ± 1.9   | 100.0 ± 0.0         | 0.1 ± 0.3  | 2.2 ± 0.5     | 100.0 ± 0.0        | 1.7 ± 2.9   | 68.3 ± 14.4 | 0.0 ± 0.0   | 100.0 ± 0.0 | 100.0 ± 0.0 | 99.9 ± 0.3  | 99.9 ± 0.3   | 99.9 ± 0.3       | 99.9 ± 0.3      | 100.0 ± 0.0 |      1357 |               100   |
| ('HMDA_OR', 'aligned', 'cat') | 79.8 ± 0.3   | 99.9 ± 0.2          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 100.0 ± 0.0 | 98.4 ± 1.1  | 100.0 ± 0.0  | 98.5 ± 0.9       | 100.0 ± 0.0     | 100.0 ± 0.0 |       808 |               100   |
| ('HMDA_OR', 'aligned', 'lr')  | 41.8 ± 3.4   | 99.2 ± 0.7          | nan        | nan           | nan                | 0.0 ± 0.0   | 88.3 ± 5.8  | 0.0 ± 0.0   | 100.0 ± 0.0 | 100.0 ± 0.0 | 100.0 ± 0.0 | 100.0 ± 0.0  | 100.0 ± 0.0      | 100.0 ± 0.0     | 100.0 ± 0.0 |       275 |               100   |
| ('HMDA_OR', 'aligned', 'mlp') | 71.7 ± 6.5   | 100.0 ± 0.0         | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 100.0 ± 0.0 | 99.7 ± 0.2  | 100.0 ± 0.0  | 99.7 ± 0.2       | 100.0 ± 0.0     | 100.0 ± 0.0 |       762 |               100   |
| ('HMDA_OR', 'aligned', 'rf')  | 82.8 ± 1.8   | 99.8 ± 0.4          | 0.2 ± 0.4  | 2.4 ± 0.4     | 100.0 ± 0.0        | nan         | nan         | 0.0 ± 0.0   | 100.0 ± 0.0 | 100.0 ± 0.0 | 99.8 ± 0.4  | 99.9 ± 0.2   | 99.8 ± 0.4       | 99.9 ± 0.2      | 100.0 ± 0.0 |       840 |               100   |
| ('HMDA_S', 'aligned', 'cat')  | 32.1 ± 1.6   | 87.8 ± 0.7          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 99.8 ± 0.4  | 98.1 ± 1.1  | 99.7 ± 0.6   | 98.2 ± 0.9       | 99.8 ± 0.4      | 99.8 ± 0.4  |       808 |               100   |
| ('HMDA_S', 'aligned', 'lr')   | 14.9 ± 5.6   | 77.3 ± 8.6          | nan        | nan           | nan                | 0.0 ± 0.0   | 91.7 ± 2.9  | 0.0 ± 0.0   | 100.0 ± 0.0 | 100.0 ± 0.0 | 100.0 ± 0.0 | 100.0 ± 0.0  | 100.0 ± 0.0      | 100.0 ± 0.0     | 100.0 ± 0.0 |       275 |               100   |
| ('HMDA_S', 'aligned', 'mlp')  | 28.7 ± 1.2   | 86.7 ± 3.1          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 100.0 ± 0.0 | 99.7 ± 0.2  | 100.0 ± 0.0  | 99.7 ± 0.2       | 100.0 ± 0.0     | 100.0 ± 0.0 |       762 |               100   |
| ('HMDA_S', 'aligned', 'rf')   | 30.6 ± 3.1   | 89.0 ± 2.7          | 0.0 ± 0.0  | 3.5 ± 0.6     | 99.5 ± 0.8         | nan         | nan         | 0.0 ± 0.0   | 100.0 ± 0.0 | 99.6 ± 0.6  | 99.5 ± 0.8  | 99.6 ± 0.6   | 99.5 ± 0.8       | 99.6 ± 0.6      | 99.6 ± 0.6  |       840 |                99.8 |
| ('OULAD', 'aligned', 'cat')   | 31.7 ± 4.6   | 69.7 ± 10.7         | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 96.0 ± 2.5  | 16.0 ± 9.2  | 91.3 ± 4.3   | 25.3 ± 10.8      | 92.0 ± 4.6      | 96.0 ± 2.5  |       300 |                96   |
| ('OULAD', 'aligned', 'lr')    | 75.3 ± 6.2   | 95.3 ± 2.2          | nan        | nan           | nan                | 49.2 ± 9.9  | 98.4 ± 2.7  | 0.0 ± 0.0   | 98.4 ± 2.7  | 95.3 ± 2.2  | 10.7 ± 4.5  | 95.3 ± 2.2   | 14.0 ± 1.9       | 93.3 ± 3.9      | 95.3 ± 2.2  |       300 |                95.3 |
| ('OULAD', 'aligned', 'mlp')   | 53.7 ± 13.2  | 93.0 ± 2.2          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 96.7 ± 1.2  | 10.0 ± 10.9 | 94.0 ± 3.0   | 13.0 ± 10.9      | 92.0 ± 3.0      | 96.7 ± 1.2  |       300 |                96.7 |
| ('OULAD', 'aligned', 'rf')    | 52.8 ± 9.2   | 91.7 ± 1.7          | 11.1 ± 2.5 | 62.2 ± 6.7    | 96.7 ± 0.0         | 0.0         | 0.0         | 0.0         | 66.7        | 96.7 ± 0.0  | 21.1 ± 10.7 | 95.6 ± 1.9   | 16.1 ± 4.2       | 95.0 ± 1.7      | 96.7 ± 0.0  |       180 |                96.7 |
| ('OULAD', 'floor', 'cat')     | 8.0 ± 1.4    | 22.7 ± 4.2          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 96.0 ± 2.5  | 18.3 ± 6.2  | 91.3 ± 4.3   | 15.0 ± 5.3       | 92.0 ± 4.6      | 96.0 ± 2.5  |       300 |                96   |
| ('OULAD', 'floor', 'lr')      | 19.3 ± 3.8   | 28.0 ± 3.0          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 95.3 ± 2.2  | 14.0 ± 3.8  | 95.3 ± 2.2   | 10.7 ± 2.5       | 93.3 ± 3.9      | 95.3 ± 2.2  |       300 |                95.3 |
| ('OULAD', 'floor', 'mlp')     | 14.3 ± 2.8   | 26.7 ± 3.1          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 96.7 ± 1.2  | 11.3 ± 4.9  | 94.0 ± 3.0   | 10.7 ± 5.3       | 92.0 ± 3.0      | 96.7 ± 1.2  |       300 |                96.7 |
| ('OULAD', 'floor', 'rf')      | 13.9 ± 1.9   | 28.3 ± 1.7          | 7.2 ± 2.5  | 85.6 ± 4.2    | 96.7 ± 0.0         | nan         | nan         | nan         | nan         | 96.7 ± 0.0  | 9.4 ± 1.0   | 95.6 ± 1.9   | 10.0 ± 2.9       | 95.0 ± 1.7      | 96.7 ± 0.0  |       180 |                96.7 |
| ('PIMA', 'aligned', 'cat')    | 45.3 ± 4.4   | 95.9 ± 1.9          | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 100.0 ± 0.0 | 44.5 ± 10.6 | 100.0 ± 0.0  | 44.5 ± 10.6      | 100.0 ± 0.0     | 100.0 ± 0.0 |       461 |               100   |
| ('PIMA', 'aligned', 'lr')     | 44.2 ± 8.3   | 95.6 ± 3.5          | nan        | nan           | nan                | 6.7 ± 7.6   | 100.0 ± 0.0 | 5.0 ± 5.0   | 100.0 ± 0.0 | 100.0 ± 0.0 | 62.4 ± 8.6  | 100.0 ± 0.0  | 62.4 ± 8.6       | 100.0 ± 0.0     | 100.0 ± 0.0 |       427 |               100   |
| ('PIMA', 'aligned', 'mlp')    | 46.1 ± 7.6   | 89.0 ± 11.3         | nan        | nan           | nan                | nan         | nan         | nan         | nan         | 98.1 ± 5.7  | 52.6 ± 24.8 | 91.8 ± 20.4  | 52.6 ± 24.8      | 91.8 ± 20.4     | 98.5 ± 4.6  |       292 |               100   |
| ('PIMA', 'aligned', 'rf')     | 44.9 ± 9.5   | 97.7 ± 2.5          | 16.6 ± 6.6 | 49.9 ± 10.0   | 98.4 ± 1.6         | 13.3 ± 2.9  | 51.7 ± 18.9 | 5.0 ± 5.0   | 96.7 ± 2.9  | 100.0 ± 0.0 | 52.0 ± 10.8 | 100.0 ± 0.0  | 52.0 ± 10.8      | 100.0 ± 0.0     | 100.0 ± 0.0 |       467 |               100   |

## Exact solver: status (%) and time (s)
|                               |   optimal |   infeasible |   time_limit |   sec_median |   sec_p95 |   sec_max |   binaries |
|:------------------------------|----------:|-------------:|-------------:|-------------:|----------:|----------:|-----------:|
| ('ADULT', 'aligned', 'cat')   |      30.7 |         69.3 |          0   |         0.02 |       0.1 |       0.4 |       86   |
| ('ADULT', 'aligned', 'lr')    |      29.1 |         70.9 |          0   |         0    |       0   |       0   |        2   |
| ('ADULT', 'aligned', 'mlp')   |      31   |         69   |          0   |         0.03 |       0.2 |       0.4 |       34   |
| ('ADULT', 'aligned', 'rf')    |      29.7 |         70.3 |          0   |         0.02 |       0.2 |       0.5 |      167   |
| ('GMSC', 'aligned', 'cat')    |      98.5 |          1.5 |          0   |         0.91 |       4.2 |       9.6 |      214.5 |
| ('GMSC', 'aligned', 'lr')     |      80.9 |         19.1 |          0   |         0.01 |       0   |       0   |        3   |
| ('GMSC', 'aligned', 'mlp')    |      62.6 |         37.4 |          0   |         0.01 |       0.1 |       0.4 |       15   |
| ('GMSC', 'aligned', 'rf')     |      98.8 |          1.2 |          0   |        26.48 |      76.6 |     112.8 |     3959   |
| ('HMDA', 'aligned', 'cat')    |      99.9 |          0.1 |          0   |         0.13 |       0.5 |       0.7 |       96   |
| ('HMDA', 'aligned', 'lr')     |     100   |          0   |          0   |         0    |       0   |       0   |        2   |
| ('HMDA', 'aligned', 'mlp')    |     100   |          0   |          0   |         0.02 |       0   |       0.1 |       36   |
| ('HMDA', 'aligned', 'rf')     |     100   |          0   |          0   |         0.53 |       1   |       1.2 |      483   |
| ('HMDA_OR', 'aligned', 'cat') |     100   |          0   |          0   |         0.11 |       0.4 |       0.6 |       99.5 |
| ('HMDA_OR', 'aligned', 'lr')  |     100   |          0   |          0   |         0    |       0   |       0   |        4   |
| ('HMDA_OR', 'aligned', 'mlp') |     100   |          0   |          0   |         0.03 |       0   |       0.1 |       38   |
| ('HMDA_OR', 'aligned', 'rf')  |     100   |          0   |          0   |         0.6  |       1.2 |       1.3 |      473   |
| ('HMDA_S', 'aligned', 'cat')  |      99.8 |          0.2 |          0   |         0.24 |       0.6 |       0.8 |      122.5 |
| ('HMDA_S', 'aligned', 'lr')   |     100   |          0   |          0   |         0    |       0   |       0   |        2   |
| ('HMDA_S', 'aligned', 'mlp')  |     100   |          0   |          0   |         0.03 |       0   |       0.1 |       37   |
| ('HMDA_S', 'aligned', 'rf')   |      99.6 |          0.4 |          0   |         0.64 |       1.1 |       1.3 |      581   |
| ('OULAD', 'aligned', 'cat')   |      96   |          4   |          0   |        16.65 |      44.1 |      58.6 |      462   |
| ('OULAD', 'aligned', 'lr')    |      95.3 |          4.7 |          0   |         0.01 |       0   |       0   |        4   |
| ('OULAD', 'aligned', 'mlp')   |      96.7 |          3.3 |          0   |         0.32 |       2.6 |       9.2 |       40   |
| ('OULAD', 'aligned', 'rf')    |      91.7 |          3.3 |          5   |        18.5  |      58.8 |      60.4 |     2384   |
| ('OULAD', 'floor', 'cat')     |      94.7 |          4   |          1.3 |         8.93 |      55   |      61.7 |      383.5 |
| ('OULAD', 'floor', 'lr')      |      95.3 |          4.7 |          0   |         0.01 |       0   |       0   |        4   |
| ('OULAD', 'floor', 'mlp')     |      96.7 |          3.3 |          0   |         0.13 |       0.4 |       0.6 |       36.5 |
| ('OULAD', 'floor', 'rf')      |      80   |          3.3 |         16.7 |        22.68 |      60.2 |      61.5 |     1964   |
| ('PIMA', 'aligned', 'cat')    |     100   |          0   |          0   |         0.32 |       0.9 |       3.6 |      193   |
| ('PIMA', 'aligned', 'lr')     |     100   |          0   |          0   |         0    |       0   |       0   |        3   |
| ('PIMA', 'aligned', 'mlp')    |      98.6 |          1.4 |          0   |         0.04 |       0.4 |       1   |       37   |
| ('PIMA', 'aligned', 'rf')     |     100   |          0   |          0   |         0.55 |       2.3 |       4.8 |      430   |

## Cost relative to the exact optimum (queries accepted by both)
| dataset   | regime   | model   | method            |    n |   cost_method |   cost_exact |   excess_pct |   optimal_pct |   effort_method |   effort_exact |
|:----------|:---------|:--------|:------------------|-----:|--------------:|-------------:|-------------:|--------------:|----------------:|---------------:|
| ADULT     | aligned  | cat     | dice_first        |   98 |         1.899 |        1.194 |         59.1 |           0   |           0.94  |          0.49  |
| ADULT     | aligned  | cat     | posthoc_full_gate |  263 |         1.891 |        1.213 |         55.9 |           0   |           0.937 |          0.5   |
| ADULT     | aligned  | cat     | framework         |  266 |         1.688 |        1.22  |         38.4 |           0   |           0.779 |          0.504 |
| ADULT     | aligned  | cat     | repair            |    3 |         0.554 |        0.554 |         -0   |         100   |           0.054 |          0.054 |
| ADULT     | aligned  | cat     | repair_esc        |    8 |         0.596 |        0.549 |          8.5 |          37.5 |           0.096 |          0.049 |
| ADULT     | aligned  | cat     | repair_sparse0    |    3 |         0.554 |        0.554 |          0   |         100   |           0.054 |          0.054 |
| ADULT     | aligned  | cat     | repair_sparse     |    8 |         0.596 |        0.549 |          8.5 |          37.5 |           0.096 |          0.049 |
| ADULT     | aligned  | lr      | dice_first        |   39 |         1.854 |        1.001 |         85.2 |           0   |           0.879 |          0.463 |
| ADULT     | aligned  | lr      | posthoc_full_gate |  185 |         1.863 |        1.099 |         69.5 |           0   |           0.914 |          0.502 |
| ADULT     | aligned  | lr      | dace              |    7 |         1.54  |        1.136 |         35.6 |           0   |           0.611 |          0.636 |
| ADULT     | aligned  | lr      | dace_rule         |   11 |         1.663 |        1.385 |         20.1 |           0   |           0.709 |          0.704 |
| ADULT     | aligned  | lr      | mace              |   12 |         1.495 |        1.16  |         28.9 |           8.3 |           0.662 |          0.66  |
| ADULT     | aligned  | lr      | mace_rule         |   20 |         1.711 |        1.444 |         18.5 |          20   |           0.761 |          0.744 |
| ADULT     | aligned  | lr      | framework         |  187 |         1.742 |        1.11  |         57   |           0   |           0.814 |          0.508 |
| ADULT     | aligned  | mlp     | dice_first        |   77 |         1.811 |        1.07  |         69.2 |           0   |           0.856 |          0.434 |
| ADULT     | aligned  | mlp     | posthoc_full_gate |  261 |         1.867 |        1.141 |         63.6 |           0   |           0.902 |          0.498 |
| ADULT     | aligned  | mlp     | framework         |  264 |         1.659 |        1.147 |         44.6 |           0   |           0.767 |          0.5   |
| ADULT     | aligned  | mlp     | repair_esc        |    1 |         0.561 |        0.533 |          5.3 |           0   |           0.061 |          0.033 |
| ADULT     | aligned  | mlp     | repair_sparse     |    1 |         0.561 |        0.533 |          5.3 |           0   |           0.061 |          0.033 |
| ADULT     | aligned  | rf      | dice_first        |   72 |         1.926 |        1.249 |         54.3 |           0   |           0.968 |          0.596 |
| ADULT     | aligned  | rf      | posthoc_full_gate |  269 |         1.951 |        1.352 |         44.3 |           0   |           0.99  |          0.667 |
| ADULT     | aligned  | rf      | ocean             |  207 |         1.255 |        1.208 |          3.9 |          87.4 |           0.644 |          0.629 |
| ADULT     | aligned  | rf      | ocean_joint       |  278 |         1.375 |        1.334 |          3.1 |          88.8 |           0.675 |          0.659 |
| ADULT     | aligned  | rf      | ocean_joint_free  |  278 |         1.375 |        1.334 |          3.1 |          88.8 |           0.675 |          0.659 |
| ADULT     | aligned  | rf      | dace              |    6 |         1.46  |        1.279 |         14.2 |          33.3 |           0.71  |          0.696 |
| ADULT     | aligned  | rf      | dace_rule         |   12 |         1.688 |        1.604 |          5.2 |          75   |           0.855 |          0.812 |
| ADULT     | aligned  | rf      | mace              |   12 |         1.633 |        1.377 |         18.6 |          16.7 |           0.675 |          0.71  |
| ADULT     | aligned  | rf      | mace_rule         |   19 |         1.68  |        1.518 |         10.7 |          10.5 |           0.733 |          0.754 |
| ADULT     | aligned  | rf      | framework         |  271 |         1.839 |        1.357 |         35.6 |           0   |           0.904 |          0.668 |
| ADULT     | aligned  | rf      | repair_esc        |    2 |         0.781 |        0.77  |          1.3 |           0   |           0.281 |          0.27  |
| ADULT     | aligned  | rf      | repair_sparse     |    2 |         0.781 |        0.77  |          1.3 |           0   |           0.281 |          0.27  |
| GMSC      | aligned  | cat     | dice_first        |  764 |         2.207 |        0.959 |        130.2 |           0.8 |           1.293 |          0.421 |
| GMSC      | aligned  | cat     | posthoc_full_gate |  974 |         2.216 |        0.97  |        128.5 |           0.6 |           1.297 |          0.427 |
| GMSC      | aligned  | cat     | framework         |  980 |         1.495 |        0.972 |         53.8 |           0.8 |           0.795 |          0.429 |
| GMSC      | aligned  | cat     | repair            |   99 |         0.956 |        0.956 |          0   |         100   |           0.456 |          0.456 |
| GMSC      | aligned  | cat     | repair_esc        |  565 |         1.029 |        0.887 |         16   |          19.1 |           0.529 |          0.377 |
| GMSC      | aligned  | cat     | repair_sparse0    |   99 |         0.956 |        0.956 |          0   |         100   |           0.456 |          0.456 |
| GMSC      | aligned  | cat     | repair_sparse     |  565 |         1.029 |        0.887 |         16   |          19.1 |           0.529 |          0.377 |
| GMSC      | aligned  | lr      | dice_first        |  523 |         2.321 |        1.111 |        108.8 |           0.2 |           1.374 |          0.509 |
| GMSC      | aligned  | lr      | posthoc_full_gate |  767 |         2.411 |        1.318 |         82.9 |           0.1 |           1.444 |          0.604 |
| GMSC      | aligned  | lr      | dace              |   29 |         1.795 |        1.001 |         79.3 |           3.4 |           0.812 |          0.398 |
| GMSC      | aligned  | lr      | dace_rule         |   42 |         1.941 |        1.262 |         53.8 |           2.4 |           0.893 |          0.548 |
| GMSC      | aligned  | lr      | mace              |   27 |         1.146 |        0.806 |         42.1 |          11.1 |           0.312 |          0.306 |
| GMSC      | aligned  | lr      | mace_rule         |   48 |         1.597 |        1.255 |         27.2 |          18.8 |           0.545 |          0.537 |
| GMSC      | aligned  | lr      | framework         |  806 |         1.828 |        1.351 |         35.3 |           0.2 |           1.016 |          0.621 |
| GMSC      | aligned  | lr      | repair            |   16 |         1.102 |        1.102 |          0   |         100   |           0.602 |          0.602 |
| GMSC      | aligned  | lr      | repair_esc        |   43 |         1.097 |        0.901 |         21.7 |          37.2 |           0.597 |          0.378 |
| GMSC      | aligned  | lr      | repair_sparse0    |   16 |         1.102 |        1.102 |          0   |         100   |           0.602 |          0.602 |
| GMSC      | aligned  | lr      | repair_sparse     |   43 |         1.097 |        0.901 |         21.7 |          37.2 |           0.597 |          0.378 |
| GMSC      | aligned  | mlp     | dice_first        |  467 |         2.356 |        1.33  |         77.1 |           0   |           1.418 |          0.698 |
| GMSC      | aligned  | mlp     | posthoc_full_gate |  608 |         2.368 |        1.33  |         78   |           0   |           1.418 |          0.69  |
| GMSC      | aligned  | mlp     | framework         |  622 |         1.756 |        1.338 |         31.3 |           0   |           0.99  |          0.693 |
| GMSC      | aligned  | mlp     | repair            |   62 |         1.04  |        1.04  |          0   |         100   |           0.54  |          0.54  |
| GMSC      | aligned  | mlp     | repair_esc        |  231 |         1.073 |        0.969 |         10.7 |          27.3 |           0.573 |          0.467 |
| GMSC      | aligned  | mlp     | repair_sparse0    |   62 |         1.04  |        1.04  |          0   |         100   |           0.54  |          0.54  |
| GMSC      | aligned  | mlp     | repair_sparse     |  231 |         1.073 |        0.969 |         10.7 |          27.3 |           0.573 |          0.467 |
| GMSC      | aligned  | rf      | dice_first        |  187 |         2.378 |        1.113 |        113.7 |           0   |           1.394 |          0.527 |
| GMSC      | aligned  | rf      | posthoc_full_gate |  245 |         2.359 |        1.122 |        110.2 |           0   |           1.385 |          0.534 |
| GMSC      | aligned  | rf      | ocean             |  167 |         1.361 |        1.065 |         27.8 |          40.7 |           0.594 |          0.478 |
| GMSC      | aligned  | rf      | ocean_joint       |  209 |         1.433 |        1.104 |         29.8 |          33.5 |           0.617 |          0.513 |
| GMSC      | aligned  | rf      | ocean_joint_free  |  244 |         1.451 |        1.121 |         29.4 |          30.7 |           0.621 |          0.535 |
| GMSC      | aligned  | rf      | mace              |    6 |         1.374 |        0.813 |         69   |          16.7 |           0.541 |          0.23  |
| GMSC      | aligned  | rf      | mace_rule         |   10 |         1.484 |        0.865 |         71.5 |          20   |           0.434 |          0.365 |
| GMSC      | aligned  | rf      | framework         |  246 |         1.67  |        1.124 |         48.7 |           0   |           0.924 |          0.536 |
| GMSC      | aligned  | rf      | repair            |   19 |         0.984 |        0.984 |         -0   |         100   |           0.484 |          0.484 |
| GMSC      | aligned  | rf      | repair_esc        |  152 |         1.174 |        0.952 |         23.4 |          13.2 |           0.674 |          0.442 |
| GMSC      | aligned  | rf      | repair_sparse0    |   19 |         0.984 |        0.984 |         -0   |         100   |           0.484 |          0.484 |
| GMSC      | aligned  | rf      | repair_sparse     |  152 |         1.174 |        0.952 |         23.4 |          13.2 |           0.674 |          0.442 |
| HMDA      | aligned  | cat     | dice_first        | 1121 |         1.688 |        0.772 |        118.6 |           0.3 |           0.934 |          0.252 |
| HMDA      | aligned  | cat     | posthoc_full_gate | 1300 |         1.702 |        0.785 |        117   |           0.2 |           0.939 |          0.25  |
| HMDA      | aligned  | cat     | framework         | 1300 |         0.959 |        0.785 |         22.2 |           1   |           0.42  |          0.25  |
| HMDA      | aligned  | cat     | repair            | 1282 |         0.785 |        0.785 |         -0   |         100   |           0.25  |          0.25  |
| HMDA      | aligned  | cat     | repair_esc        | 1298 |         0.791 |        0.784 |          0.9 |          98.8 |           0.253 |          0.249 |
| HMDA      | aligned  | cat     | repair_sparse0    | 1282 |         0.785 |        0.785 |          0   |         100   |           0.25  |          0.25  |
| HMDA      | aligned  | cat     | repair_sparse     | 1298 |         0.791 |        0.784 |          0.9 |          98.8 |           0.253 |          0.249 |
| HMDA      | aligned  | lr      | dice_first        |  255 |         1.715 |        0.857 |        100.2 |           0   |           0.984 |          0.337 |
| HMDA      | aligned  | lr      | posthoc_full_gate |  492 |         1.72  |        0.871 |         97.4 |           0   |           0.972 |          0.339 |
| HMDA      | aligned  | lr      | dace_rule         |   53 |         1.092 |        0.886 |         23.3 |          58.5 |           0.385 |          0.339 |
| HMDA      | aligned  | lr      | mace_rule         |   60 |         0.88  |        0.88  |          0   |          98.3 |           0.338 |          0.338 |
| HMDA      | aligned  | lr      | framework         |  492 |         1.14  |        0.871 |         30.9 |           0.6 |           0.587 |          0.339 |
| HMDA      | aligned  | lr      | repair            |  492 |         0.871 |        0.871 |         -0   |         100   |           0.339 |          0.339 |
| HMDA      | aligned  | lr      | repair_esc        |  492 |         0.871 |        0.871 |         -0   |         100   |           0.339 |          0.339 |
| HMDA      | aligned  | lr      | repair_sparse0    |  492 |         0.871 |        0.871 |          0   |         100   |           0.339 |          0.339 |
| HMDA      | aligned  | lr      | repair_sparse     |  492 |         0.871 |        0.871 |          0   |         100   |           0.339 |          0.339 |
| HMDA      | aligned  | mlp     | dice_first        |  970 |         1.717 |        0.78  |        119.9 |           0.3 |           0.96  |          0.258 |
| HMDA      | aligned  | mlp     | posthoc_full_gate | 1235 |         1.747 |        0.805 |        117.1 |           0.2 |           0.978 |          0.257 |
| HMDA      | aligned  | mlp     | framework         | 1235 |         1.006 |        0.805 |         25   |           1.5 |           0.455 |          0.257 |
| HMDA      | aligned  | mlp     | repair            | 1232 |         0.805 |        0.805 |         -0   |         100   |           0.257 |          0.257 |
| HMDA      | aligned  | mlp     | repair_esc        | 1235 |         0.805 |        0.805 |          0   |          99.8 |           0.258 |          0.257 |
| HMDA      | aligned  | mlp     | repair_sparse0    | 1232 |         0.805 |        0.805 |          0   |         100   |           0.257 |          0.257 |
| HMDA      | aligned  | mlp     | repair_sparse     | 1235 |         0.805 |        0.805 |          0   |          99.8 |           0.258 |          0.257 |
| HMDA      | aligned  | rf      | dice_first        | 1205 |         1.698 |        0.772 |        119.9 |           0.2 |           0.941 |          0.247 |
| HMDA      | aligned  | rf      | posthoc_full_gate | 1357 |         1.708 |        0.787 |        117.1 |           0.1 |           0.945 |          0.247 |
| HMDA      | aligned  | rf      | ocean             |    2 |         1.51  |        1.51  |         -0   |         100   |           0.51  |          0.51  |
| HMDA      | aligned  | rf      | ocean_joint       |   30 |         1.278 |        0.742 |         72.4 |           6.7 |           0.278 |          0.208 |
| HMDA      | aligned  | rf      | ocean_joint_free  | 1357 |         0.811 |        0.787 |          3   |          96.2 |           0.252 |          0.247 |
| HMDA      | aligned  | rf      | dace              |    1 |         0.643 |        0.643 |         -0   |         100   |           0.143 |          0.143 |
| HMDA      | aligned  | rf      | dace_rule         |   41 |         1.032 |        0.736 |         40.3 |          51.2 |           0.325 |          0.236 |
| HMDA      | aligned  | rf      | mace_rule         |   60 |         0.966 |        0.79  |         22.3 |          55   |           0.25  |          0.249 |
| HMDA      | aligned  | rf      | framework         | 1357 |         0.954 |        0.787 |         21.2 |           1   |           0.41  |          0.247 |
| HMDA      | aligned  | rf      | repair            | 1355 |         0.786 |        0.786 |         -0   |         100   |           0.246 |          0.246 |
| HMDA      | aligned  | rf      | repair_esc        | 1355 |         0.786 |        0.786 |         -0   |         100   |           0.246 |          0.246 |
| HMDA      | aligned  | rf      | repair_sparse0    | 1355 |         0.786 |        0.786 |          0   |         100   |           0.246 |          0.246 |
| HMDA      | aligned  | rf      | repair_sparse     | 1355 |         0.786 |        0.786 |          0   |         100   |           0.246 |          0.246 |
| HMDA_OR   | aligned  | cat     | dice_first        |  645 |         1.739 |        0.836 |        108.1 |           0.3 |           0.977 |          0.318 |
| HMDA_OR   | aligned  | cat     | posthoc_full_gate |  807 |         1.783 |        0.857 |        108   |           0.2 |           1.005 |          0.323 |
| HMDA_OR   | aligned  | cat     | framework         |  808 |         1.053 |        0.858 |         22.8 |           0.5 |           0.51  |          0.323 |
| HMDA_OR   | aligned  | cat     | repair            |  795 |         0.867 |        0.859 |          0.9 |          97.9 |           0.321 |          0.324 |
| HMDA_OR   | aligned  | cat     | repair_esc        |  808 |         0.872 |        0.858 |          1.7 |          96.4 |           0.325 |          0.323 |
| HMDA_OR   | aligned  | cat     | repair_sparse0    |  796 |         0.859 |        0.859 |          0   |         100   |           0.324 |          0.324 |
| HMDA_OR   | aligned  | cat     | repair_sparse     |  808 |         0.864 |        0.858 |          0.7 |          98.6 |           0.327 |          0.323 |
| HMDA_OR   | aligned  | lr      | dice_first        |  116 |         1.764 |        0.932 |         89.3 |           0   |           1.022 |          0.415 |
| HMDA_OR   | aligned  | lr      | posthoc_full_gate |  273 |         1.8   |        0.959 |         87.6 |           0.7 |           1.041 |          0.426 |
| HMDA_OR   | aligned  | lr      | dace_rule         |   53 |         1.208 |        0.976 |         23.8 |          54.7 |           0.482 |          0.429 |
| HMDA_OR   | aligned  | lr      | mace_rule         |   60 |         1.183 |        0.971 |         21.9 |          65   |           0.483 |          0.429 |
| HMDA_OR   | aligned  | lr      | framework         |  275 |         1.248 |        0.961 |         29.9 |           0   |           0.683 |          0.427 |
| HMDA_OR   | aligned  | lr      | repair            |  275 |         0.963 |        0.961 |          0.2 |          99.6 |           0.427 |          0.427 |
| HMDA_OR   | aligned  | lr      | repair_esc        |  275 |         0.963 |        0.961 |          0.2 |          99.6 |           0.427 |          0.427 |
| HMDA_OR   | aligned  | lr      | repair_sparse0    |  275 |         0.961 |        0.961 |          0   |         100   |           0.427 |          0.427 |
| HMDA_OR   | aligned  | lr      | repair_sparse     |  275 |         0.961 |        0.961 |          0   |         100   |           0.427 |          0.427 |
| HMDA_OR   | aligned  | mlp     | dice_first        |  550 |         1.757 |        0.846 |        107.7 |           0.5 |           1.003 |          0.324 |
| HMDA_OR   | aligned  | mlp     | posthoc_full_gate |  762 |         1.811 |        0.879 |        105.9 |           0.4 |           1.038 |          0.333 |
| HMDA_OR   | aligned  | mlp     | framework         |  762 |         1.093 |        0.879 |         24.3 |           1   |           0.535 |          0.333 |
| HMDA_OR   | aligned  | mlp     | repair            |  760 |         0.886 |        0.879 |          0.7 |          98.6 |           0.332 |          0.333 |
| HMDA_OR   | aligned  | mlp     | repair_esc        |  762 |         0.887 |        0.879 |          0.9 |          98.3 |           0.332 |          0.333 |
| HMDA_OR   | aligned  | mlp     | repair_sparse0    |  760 |         0.879 |        0.879 |          0   |         100   |           0.333 |          0.333 |
| HMDA_OR   | aligned  | mlp     | repair_sparse     |  762 |         0.88  |        0.879 |          0.1 |          99.7 |           0.334 |          0.333 |
| HMDA_OR   | aligned  | rf      | dice_first        |  696 |         1.749 |        0.835 |        109.6 |           0.1 |           0.986 |          0.311 |
| HMDA_OR   | aligned  | rf      | posthoc_full_gate |  838 |         1.781 |        0.855 |        108.3 |           0.1 |           1.009 |          0.317 |
| HMDA_OR   | aligned  | rf      | ocean             |    2 |         1.51  |        1.51  |         -0   |         100   |           0.51  |          0.51  |
| HMDA_OR   | aligned  | rf      | ocean_joint       |   20 |         1.292 |        0.79  |         63.5 |          10   |           0.292 |          0.24  |
| HMDA_OR   | aligned  | rf      | ocean_joint_free  |  840 |         0.883 |        0.856 |          3.1 |          95.2 |           0.32  |          0.317 |
| HMDA_OR   | aligned  | rf      | mace_rule         |   60 |         1.008 |        0.843 |         19.6 |          63.3 |           0.317 |          0.302 |
| HMDA_OR   | aligned  | rf      | framework         |  840 |         1.036 |        0.856 |         21   |           0.5 |           0.49  |          0.317 |
| HMDA_OR   | aligned  | rf      | repair            |  838 |         0.861 |        0.855 |          0.7 |          98.6 |           0.316 |          0.317 |
| HMDA_OR   | aligned  | rf      | repair_esc        |  839 |         0.863 |        0.855 |          0.9 |          98.5 |           0.317 |          0.317 |
| HMDA_OR   | aligned  | rf      | repair_sparse0    |  838 |         0.855 |        0.855 |          0   |         100   |           0.317 |          0.317 |
| HMDA_OR   | aligned  | rf      | repair_sparse     |  839 |         0.857 |        0.855 |          0.1 |          99.9 |           0.318 |          0.317 |
| HMDA_S    | aligned  | cat     | dice_first        |  259 |         1.117 |        0.75  |         48.9 |           0   |           0.617 |          0.25  |
| HMDA_S    | aligned  | cat     | posthoc_full_gate |  709 |         1.115 |        0.746 |         49.4 |           0.4 |           0.615 |          0.246 |
| HMDA_S    | aligned  | cat     | framework         |  806 |         1.002 |        0.8   |         25.3 |           2.5 |           0.453 |          0.252 |
| HMDA_S    | aligned  | cat     | repair            |  792 |         0.797 |        0.797 |         -0   |         100   |           0.252 |          0.252 |
| HMDA_S    | aligned  | cat     | repair_esc        |  805 |         0.807 |        0.799 |          1   |          98.5 |           0.256 |          0.252 |
| HMDA_S    | aligned  | cat     | repair_sparse0    |  793 |         0.797 |        0.797 |         -0   |         100   |           0.252 |          0.252 |
| HMDA_S    | aligned  | cat     | repair_sparse     |  806 |         0.808 |        0.8   |          1   |          98.5 |           0.256 |          0.252 |
| HMDA_S    | aligned  | lr      | dice_first        |   42 |         1.134 |        0.833 |         36.1 |           0   |           0.634 |          0.333 |
| HMDA_S    | aligned  | lr      | posthoc_full_gate |  212 |         1.155 |        0.833 |         38.6 |           0   |           0.655 |          0.333 |
| HMDA_S    | aligned  | lr      | dace_rule         |   55 |         0.833 |        0.833 |         -0   |         100   |           0.333 |          0.333 |
| HMDA_S    | aligned  | lr      | mace_rule         |   60 |         0.956 |        0.88  |          8.6 |          83.3 |           0.339 |          0.338 |
| HMDA_S    | aligned  | lr      | framework         |  275 |         1.137 |        0.874 |         30.1 |           0.4 |           0.593 |          0.339 |
| HMDA_S    | aligned  | lr      | repair            |  275 |         0.874 |        0.874 |         -0   |         100   |           0.339 |          0.339 |
| HMDA_S    | aligned  | lr      | repair_esc        |  275 |         0.874 |        0.874 |         -0   |         100   |           0.339 |          0.339 |
| HMDA_S    | aligned  | lr      | repair_sparse0    |  275 |         0.874 |        0.874 |          0   |         100   |           0.339 |          0.339 |
| HMDA_S    | aligned  | lr      | repair_sparse     |  275 |         0.874 |        0.874 |          0   |         100   |           0.339 |          0.339 |
| HMDA_S    | aligned  | mlp     | dice_first        |  219 |         1.129 |        0.769 |         46.9 |           0   |           0.629 |          0.269 |
| HMDA_S    | aligned  | mlp     | posthoc_full_gate |  662 |         1.132 |        0.754 |         50.1 |           0.2 |           0.632 |          0.254 |
| HMDA_S    | aligned  | mlp     | framework         |  762 |         1.029 |        0.804 |         28   |           0.7 |           0.479 |          0.257 |
| HMDA_S    | aligned  | mlp     | repair            |  760 |         0.804 |        0.804 |         -0   |         100   |           0.257 |          0.257 |
| HMDA_S    | aligned  | mlp     | repair_esc        |  762 |         0.805 |        0.804 |          0.1 |          99.7 |           0.257 |          0.257 |
| HMDA_S    | aligned  | mlp     | repair_sparse0    |  760 |         0.804 |        0.804 |          0   |         100   |           0.257 |          0.257 |
| HMDA_S    | aligned  | mlp     | repair_sparse     |  762 |         0.805 |        0.804 |          0.1 |          99.7 |           0.257 |          0.257 |
| HMDA_S    | aligned  | rf      | dice_first        |  257 |         1.116 |        0.75  |         48.9 |           0   |           0.616 |          0.25  |
| HMDA_S    | aligned  | rf      | posthoc_full_gate |  748 |         1.109 |        0.741 |         49.8 |           0.5 |           0.609 |          0.241 |
| HMDA_S    | aligned  | rf      | ocean_joint       |   29 |         0.942 |        0.938 |          0.4 |          96.6 |           0.287 |          0.283 |
| HMDA_S    | aligned  | rf      | ocean_joint_free  |  836 |         0.789 |        0.789 |          0   |          99.9 |           0.247 |          0.247 |
| HMDA_S    | aligned  | rf      | mace_rule         |   60 |         0.922 |        0.804 |         14.7 |          50   |           0.255 |          0.254 |
| HMDA_S    | aligned  | rf      | framework         |  837 |         0.987 |        0.79  |         24.9 |           2.3 |           0.444 |          0.247 |
| HMDA_S    | aligned  | rf      | repair            |  836 |         0.789 |        0.789 |         -0   |         100   |           0.247 |          0.247 |
| HMDA_S    | aligned  | rf      | repair_esc        |  837 |         0.79  |        0.79  |          0   |          99.9 |           0.248 |          0.247 |
| HMDA_S    | aligned  | rf      | repair_sparse0    |  836 |         0.789 |        0.789 |          0   |         100   |           0.247 |          0.247 |
| HMDA_S    | aligned  | rf      | repair_sparse     |  837 |         0.79  |        0.79  |          0   |          99.9 |           0.248 |          0.247 |
| OULAD     | aligned  | cat     | dice_first        |   95 |         2.67  |        2.056 |         29.8 |           0   |           1.68  |          1.172 |
| OULAD     | aligned  | cat     | posthoc_full_gate |  209 |         2.893 |        2.364 |         22.4 |           0   |           1.833 |          1.364 |
| OULAD     | aligned  | cat     | framework         |  288 |         2.966 |        2.636 |         12.5 |          16.3 |           1.803 |          1.522 |
| OULAD     | aligned  | cat     | repair            |   48 |         2.584 |        2.584 |         -0   |         100   |           1.521 |          1.521 |
| OULAD     | aligned  | cat     | repair_esc        |  274 |         3.258 |        2.626 |         24.1 |          17.5 |           2.008 |          1.525 |
| OULAD     | aligned  | cat     | repair_sparse0    |   76 |         2.735 |        2.735 |          0   |         100   |           1.597 |          1.597 |
| OULAD     | aligned  | cat     | repair_sparse     |  276 |         3.059 |        2.625 |         16.5 |          27.5 |           1.865 |          1.526 |
| OULAD     | aligned  | lr      | dice_first        |  226 |         3.449 |        2.679 |         28.7 |           0   |           2.201 |          1.63  |
| OULAD     | aligned  | lr      | posthoc_full_gate |  286 |         3.609 |        2.788 |         29.5 |           0   |           2.307 |          1.688 |
| OULAD     | aligned  | lr      | dace              |   31 |         3.418 |        2.371 |         44.1 |           0   |           1.644 |          1.452 |
| OULAD     | aligned  | lr      | dace_rule         |   62 |         3.802 |        2.88  |         32   |           0   |           1.963 |          1.751 |
| OULAD     | aligned  | lr      | mace_rule         |   62 |         4.754 |        2.88  |         65.1 |           3.2 |           2.77  |          1.751 |
| OULAD     | aligned  | lr      | framework         |  286 |         3.091 |        2.788 |         10.9 |           0.7 |           1.918 |          1.688 |
| OULAD     | aligned  | lr      | repair            |   32 |         2.162 |        2.162 |         -0   |         100   |           1.209 |          1.209 |
| OULAD     | aligned  | lr      | repair_esc        |  286 |         3.141 |        2.788 |         12.7 |          11.2 |           1.921 |          1.688 |
| OULAD     | aligned  | lr      | repair_sparse0    |   42 |         2.301 |        2.301 |          0   |         100   |           1.301 |          1.301 |
| OULAD     | aligned  | lr      | repair_sparse     |  280 |         3.162 |        2.784 |         13.6 |          15   |           1.923 |          1.683 |
| OULAD     | aligned  | mlp     | dice_first        |  161 |         3.214 |        2.543 |         26.4 |           0   |           2.052 |          1.505 |
| OULAD     | aligned  | mlp     | posthoc_full_gate |  279 |         3.319 |        2.671 |         24.3 |           0   |           2.122 |          1.585 |
| OULAD     | aligned  | mlp     | framework         |  290 |         3.033 |        2.696 |         12.5 |           0.7 |           1.879 |          1.603 |
| OULAD     | aligned  | mlp     | repair            |   30 |         2.169 |        2.169 |         -0   |         100   |           1.252 |          1.252 |
| OULAD     | aligned  | mlp     | repair_esc        |  282 |         3.184 |        2.67  |         19.2 |          10.6 |           1.961 |          1.587 |
| OULAD     | aligned  | mlp     | repair_sparse0    |   39 |         2.092 |        2.092 |          0   |         100   |           1.182 |          1.182 |
| OULAD     | aligned  | mlp     | repair_sparse     |  276 |         3.171 |        2.666 |         19   |          14.1 |           1.943 |          1.58  |
| OULAD     | aligned  | rf      | dice_first        |   95 |         2.749 |        2.258 |         21.8 |           5.3 |           1.728 |          1.311 |
| OULAD     | aligned  | rf      | posthoc_full_gate |  165 |         3.017 |        2.549 |         18.4 |           3.6 |           1.905 |          1.485 |
| OULAD     | aligned  | rf      | ocean             |   20 |         2.35  |        2.165 |          8.6 |          65   |           1.25  |          1.24  |
| OULAD     | aligned  | rf      | ocean_joint       |  112 |         5.139 |        2.865 |         79.3 |          12.5 |           2.782 |          1.678 |
| OULAD     | aligned  | rf      | ocean_joint_free  |  174 |         4.084 |        2.599 |         57.1 |          32.2 |           2.227 |          1.513 |
| OULAD     | aligned  | rf      | mace_rule         |   14 |         3.477 |        2.468 |         40.9 |           7.1 |           1.62  |          1.433 |
| OULAD     | aligned  | rf      | framework         |  174 |         2.836 |        2.599 |          9.1 |           8.6 |           1.724 |          1.513 |
| OULAD     | aligned  | rf      | repair            |   38 |         2.853 |        2.853 |         -0   |         100   |           1.669 |          1.669 |
| OULAD     | aligned  | rf      | repair_esc        |  172 |         3.147 |        2.6   |         21   |          22.1 |           1.929 |          1.516 |
| OULAD     | aligned  | rf      | repair_sparse0    |   29 |         2.248 |        2.248 |          0   |         100   |           1.334 |          1.334 |
| OULAD     | aligned  | rf      | repair_sparse     |  171 |         3.056 |        2.601 |         17.5 |          17   |           1.875 |          1.516 |
| OULAD     | floor    | cat     | dice_first        |   24 |         3.432 |        2.526 |         35.9 |           4.2 |           2.495 |          1.63  |
| OULAD     | floor    | cat     | posthoc_full_gate |   68 |         3.663 |        2.83  |         29.4 |           1.5 |           2.685 |          1.83  |
| OULAD     | floor    | cat     | framework         |  288 |         7.435 |        6.415 |         15.9 |           0.3 |           4.876 |          3.842 |
| OULAD     | floor    | cat     | repair            |   55 |         5.336 |        5.336 |         -0   |         100   |           3.245 |          3.245 |
| OULAD     | floor    | cat     | repair_esc        |  274 |         7.2   |        6.549 |          9.9 |          20.4 |           4.608 |          3.916 |
| OULAD     | floor    | cat     | repair_sparse0    |   45 |         3.302 |        3.302 |         -0   |         100   |           2.058 |          2.058 |
| OULAD     | floor    | cat     | repair_sparse     |  276 |         7.175 |        6.528 |          9.9 |          16.7 |           4.595 |          3.907 |
| OULAD     | floor    | lr      | dice_first        |   58 |         3.918 |        3.214 |         21.9 |           1.7 |           2.866 |          2.283 |
| OULAD     | floor    | lr      | posthoc_full_gate |   84 |         3.807 |        3.1   |         22.8 |           1.2 |           2.777 |          2.154 |
| OULAD     | floor    | lr      | framework         |  286 |         7.502 |        6.525 |         15   |           0.3 |           4.989 |          4.027 |
| OULAD     | floor    | lr      | repair            |   42 |         5.146 |        5.146 |         -0   |         100   |           3.181 |          3.181 |
| OULAD     | floor    | lr      | repair_esc        |  286 |         6.741 |        6.525 |          3.3 |          15.4 |           4.243 |          4.027 |
| OULAD     | floor    | lr      | repair_sparse0    |   32 |         3.437 |        3.437 |          0   |         100   |           2.171 |          2.171 |
| OULAD     | floor    | lr      | repair_sparse     |  280 |         6.777 |        6.575 |          3.1 |          11.8 |           4.247 |          4.044 |
| OULAD     | floor    | mlp     | dice_first        |   43 |         3.644 |        2.863 |         27.3 |           0   |           2.621 |          1.945 |
| OULAD     | floor    | mlp     | posthoc_full_gate |   80 |         3.636 |        2.902 |         25.3 |           0   |           2.63  |          1.952 |
| OULAD     | floor    | mlp     | framework         |  290 |         7.362 |        6.379 |         15.4 |           0.3 |           4.885 |          3.906 |
| OULAD     | floor    | mlp     | repair            |   34 |         5.197 |        5.197 |         -0   |         100   |           3.123 |          3.123 |
| OULAD     | floor    | mlp     | repair_esc        |  282 |         6.733 |        6.43  |          4.7 |          12.1 |           4.244 |          3.928 |
| OULAD     | floor    | mlp     | repair_sparse0    |   32 |         4.563 |        4.563 |          0   |         100   |           2.75  |          2.75  |
| OULAD     | floor    | mlp     | repair_sparse     |  276 |         6.752 |        6.481 |          4.2 |          11.6 |           4.231 |          3.948 |
| OULAD     | floor    | rf      | dice_first        |   25 |         3.715 |        2.772 |         34   |           0   |           2.715 |          1.832 |
| OULAD     | floor    | rf      | posthoc_full_gate |   51 |         3.727 |        2.86  |         30.3 |           0   |           2.727 |          1.899 |
| OULAD     | floor    | rf      | ocean             |   13 |         3.028 |        3.007 |          0.7 |          84.6 |           2.066 |          2.007 |
| OULAD     | floor    | rf      | ocean_joint       |  154 |         7.352 |        6.768 |          8.6 |          20.1 |           4.725 |          4.08  |
| OULAD     | floor    | rf      | ocean_joint_free  |  174 |         6.848 |        6.337 |          8.1 |          25.9 |           4.417 |          3.852 |
| OULAD     | floor    | rf      | framework         |  174 |         7.074 |        6.337 |         11.6 |           4   |           4.643 |          3.852 |
| OULAD     | floor    | rf      | repair            |   17 |         2.938 |        2.938 |         -0   |         100   |           1.849 |          1.849 |
| OULAD     | floor    | rf      | repair_esc        |  172 |         6.892 |        6.372 |          8.2 |          13.4 |           4.453 |          3.872 |
| OULAD     | floor    | rf      | repair_sparse0    |   18 |         2.962 |        2.962 |         -0   |         100   |           1.879 |          1.879 |
| OULAD     | floor    | rf      | repair_sparse     |  171 |         7.173 |        6.39  |         12.3 |          14   |           4.726 |          3.881 |
| PIMA      | aligned  | cat     | dice_first        |  209 |         2.074 |        1.214 |         70.8 |           0   |           1.141 |          0.504 |
| PIMA      | aligned  | cat     | posthoc_full_gate |  442 |         2.158 |        1.353 |         59.5 |           0   |           1.207 |          0.558 |
| PIMA      | aligned  | cat     | framework         |  461 |         1.778 |        1.37  |         29.8 |           0   |           0.923 |          0.566 |
| PIMA      | aligned  | cat     | repair            |  203 |         1.382 |        1.382 |         -0   |         100   |           0.552 |          0.552 |
| PIMA      | aligned  | cat     | repair_esc        |  461 |         1.553 |        1.37  |         13.4 |          44.3 |           0.666 |          0.566 |
| PIMA      | aligned  | cat     | repair_sparse0    |  203 |         1.382 |        1.382 |          0   |         100   |           0.552 |          0.552 |
| PIMA      | aligned  | cat     | repair_sparse     |  461 |         1.553 |        1.37  |         13.4 |          44.3 |           0.666 |          0.566 |
| PIMA      | aligned  | lr      | dice_first        |  190 |         2.213 |        1.307 |         69.3 |           0   |           1.266 |          0.544 |
| PIMA      | aligned  | lr      | posthoc_full_gate |  410 |         2.225 |        1.437 |         54.9 |           0   |           1.267 |          0.59  |
| PIMA      | aligned  | lr      | dace              |    4 |         2.216 |        1.049 |        111.2 |           0   |           0.716 |          0.424 |
| PIMA      | aligned  | lr      | dace_rule         |   60 |         2.08  |        1.486 |         40   |           0   |           0.772 |          0.594 |
| PIMA      | aligned  | lr      | mace              |    3 |         1.214 |        0.879 |         38   |          33.3 |           0.38  |          0.379 |
| PIMA      | aligned  | lr      | mace_rule         |   60 |         1.599 |        1.486 |          7.6 |          28.3 |           0.599 |          0.594 |
| PIMA      | aligned  | lr      | framework         |  427 |         1.854 |        1.447 |         28.1 |           0   |           0.97  |          0.595 |
| PIMA      | aligned  | lr      | repair            |  262 |         1.418 |        1.418 |         -0   |         100   |           0.565 |          0.565 |
| PIMA      | aligned  | lr      | repair_esc        |  427 |         1.549 |        1.447 |          7.1 |          61.4 |           0.661 |          0.595 |
| PIMA      | aligned  | lr      | repair_sparse0    |  262 |         1.418 |        1.418 |          0   |         100   |           0.565 |          0.565 |
| PIMA      | aligned  | lr      | repair_sparse     |  427 |         1.549 |        1.447 |          7.1 |          61.4 |           0.661 |          0.595 |
| PIMA      | aligned  | mlp     | dice_first        |  130 |         2.163 |        1.269 |         70.4 |           0   |           1.224 |          0.561 |
| PIMA      | aligned  | mlp     | posthoc_full_gate |  261 |         2.246 |        1.427 |         57.4 |           0   |           1.287 |          0.611 |
| PIMA      | aligned  | mlp     | framework         |  287 |         1.884 |        1.474 |         27.9 |           0   |           0.999 |          0.639 |
| PIMA      | aligned  | mlp     | repair            |  148 |         1.418 |        1.418 |         -0   |         100   |           0.567 |          0.567 |
| PIMA      | aligned  | mlp     | repair_esc        |  272 |         1.613 |        1.452 |         11.1 |          54.4 |           0.716 |          0.619 |
| PIMA      | aligned  | mlp     | repair_sparse0    |  148 |         1.418 |        1.418 |          0   |         100   |           0.567 |          0.567 |
| PIMA      | aligned  | mlp     | repair_sparse     |  272 |         1.613 |        1.452 |         11.1 |          54.4 |           0.716 |          0.619 |
| PIMA      | aligned  | rf      | dice_first        |  211 |         2.123 |        1.169 |         81.6 |           0   |           1.182 |          0.458 |
| PIMA      | aligned  | rf      | posthoc_full_gate |  456 |         2.189 |        1.327 |         65   |           0   |           1.23  |          0.535 |
| PIMA      | aligned  | rf      | ocean             |   79 |         0.875 |        0.862 |          1.5 |          93.7 |           0.362 |          0.362 |
| PIMA      | aligned  | rf      | ocean_joint       |  235 |         1.562 |        1.235 |         26.5 |          34.5 |           0.664 |          0.496 |
| PIMA      | aligned  | rf      | ocean_joint_free  |  460 |         1.639 |        1.338 |         22.4 |          36.3 |           0.693 |          0.542 |
| PIMA      | aligned  | rf      | dace              |    8 |         2.71  |        1.374 |         97.2 |          25   |           1.523 |          0.562 |
| PIMA      | aligned  | rf      | dace_rule         |   31 |         2.046 |        1.329 |         53.9 |          19.4 |           0.74  |          0.523 |
| PIMA      | aligned  | rf      | mace              |    3 |         0.857 |        0.682 |         25.5 |          33.3 |           0.19  |          0.182 |
| PIMA      | aligned  | rf      | mace_rule         |   58 |         1.615 |        1.392 |         16.1 |          25.9 |           0.564 |          0.564 |
| PIMA      | aligned  | rf      | framework         |  467 |         1.773 |        1.338 |         32.5 |           0   |           0.935 |          0.541 |
| PIMA      | aligned  | rf      | repair            |  241 |         1.36  |        1.36  |         -0   |         100   |           0.539 |          0.539 |
| PIMA      | aligned  | rf      | repair_esc        |  467 |         1.515 |        1.338 |         13.2 |          51.6 |           0.643 |          0.541 |
| PIMA      | aligned  | rf      | repair_sparse0    |  241 |         1.36  |        1.36  |          0   |         100   |           0.539 |          0.539 |
| PIMA      | aligned  | rf      | repair_sparse     |  467 |         1.515 |        1.338 |         13.2 |          51.6 |           0.643 |          0.541 |

## Paired yield: exact vs baselines (McNemar, Holm)
| dataset   | regime   | model   | baseline          |    n |   diff_pp |   only_exact |   only_baseline |      p |   p_holm |
|:----------|:---------|:--------|:------------------|-----:|----------:|-------------:|----------------:|-------:|---------:|
| ADULT     | aligned  | cat     | framework         | 1000 |      4.1  |           41 |               0 | 0      |   0      |
| ADULT     | aligned  | cat     | repair_esc        | 1000 |     29.9  |          299 |               0 | 0      |   0      |
| ADULT     | aligned  | cat     | repair_sparse     | 1000 |     29.9  |          299 |               0 | 0      |   0      |
| ADULT     | aligned  | cat     | posthoc_full_gate | 1000 |      4.4  |           44 |               0 | 0      |   0      |
| ADULT     | aligned  | lr      | framework         | 1000 |     10.4  |          104 |               0 | 0      |   0      |
| ADULT     | aligned  | lr      | repair_esc        | 1000 |     29.1  |          291 |               0 | 0      |   0      |
| ADULT     | aligned  | lr      | repair_sparse     | 1000 |     29.1  |          291 |               0 | 0      |   0      |
| ADULT     | aligned  | lr      | posthoc_full_gate | 1000 |     10.6  |          106 |               0 | 0      |   0      |
| ADULT     | aligned  | lr      | dace_rule         |   60 |     15    |            9 |               0 | 0.0039 |   0.418  |
| ADULT     | aligned  | lr      | mace_rule         |   60 |      0    |            0 |               0 | 1      |   1      |
| ADULT     | aligned  | mlp     | framework         | 1000 |      4.6  |           46 |               0 | 0      |   0      |
| ADULT     | aligned  | mlp     | repair_esc        | 1000 |     30.9  |          309 |               0 | 0      |   0      |
| ADULT     | aligned  | mlp     | repair_sparse     | 1000 |     30.9  |          309 |               0 | 0      |   0      |
| ADULT     | aligned  | mlp     | posthoc_full_gate | 1000 |      4.9  |           49 |               0 | 0      |   0      |
| ADULT     | aligned  | rf      | framework         | 1000 |      2.6  |           26 |               0 | 0      |   0.0001 |
| ADULT     | aligned  | rf      | repair_esc        | 1000 |     29.5  |          295 |               0 | 0      |   0      |
| ADULT     | aligned  | rf      | repair_sparse     | 1000 |     29.5  |          295 |               0 | 0      |   0      |
| ADULT     | aligned  | rf      | posthoc_full_gate | 1000 |      2.8  |           28 |               0 | 0      |   0      |
| ADULT     | aligned  | rf      | ocean_joint       | 1000 |      1.9  |           19 |               0 | 0      |   0.0005 |
| ADULT     | aligned  | rf      | ocean_joint_free  | 1000 |      1.9  |           19 |               0 | 0      |   0.0005 |
| ADULT     | aligned  | rf      | dace_rule         |   60 |     11.67 |            7 |               0 | 0.0156 |   1      |
| ADULT     | aligned  | rf      | mace_rule         |   60 |      0    |            0 |               0 | 1      |   1      |
| GMSC      | aligned  | cat     | framework         | 1000 |      0.5  |            5 |               0 | 0.0625 |   1      |
| GMSC      | aligned  | cat     | repair_esc        | 1000 |     42    |          420 |               0 | 0      |   0      |
| GMSC      | aligned  | cat     | repair_sparse     | 1000 |     42    |          420 |               0 | 0      |   0      |
| GMSC      | aligned  | cat     | posthoc_full_gate | 1000 |      1.1  |           11 |               0 | 0.001  |   0.1084 |
| GMSC      | aligned  | lr      | framework         | 1000 |      0.3  |            3 |               0 | 0.25   |   1      |
| GMSC      | aligned  | lr      | repair_esc        | 1000 |     76.6  |          766 |               0 | 0      |   0      |
| GMSC      | aligned  | lr      | repair_sparse     | 1000 |     76.6  |          766 |               0 | 0      |   0      |
| GMSC      | aligned  | lr      | posthoc_full_gate | 1000 |      4.2  |           42 |               0 | 0      |   0      |
| GMSC      | aligned  | lr      | dace_rule         |   60 |     10    |            6 |               0 | 0.0312 |   1      |
| GMSC      | aligned  | lr      | mace_rule         |   60 |      0    |            0 |               0 | 1      |   1      |
| GMSC      | aligned  | mlp     | framework         | 1000 |      0.4  |            4 |               0 | 0.125  |   1      |
| GMSC      | aligned  | mlp     | repair_esc        | 1000 |     39.5  |          395 |               0 | 0      |   0      |
| GMSC      | aligned  | mlp     | repair_sparse     | 1000 |     39.5  |          395 |               0 | 0      |   0      |
| GMSC      | aligned  | mlp     | posthoc_full_gate | 1000 |      1.8  |           18 |               0 | 0      |   0.0009 |
| GMSC      | aligned  | rf      | framework         |  250 |      0.4  |            1 |               0 | 1      |   1      |
| GMSC      | aligned  | rf      | repair_esc        |  250 |     38    |           95 |               0 | 0      |   0      |
| GMSC      | aligned  | rf      | repair_sparse     |  250 |     38    |           95 |               0 | 0      |   0      |
| GMSC      | aligned  | rf      | posthoc_full_gate |  250 |      0.8  |            2 |               0 | 0.5    |   1      |
| GMSC      | aligned  | rf      | ocean_joint       |  250 |     15.2  |           38 |               0 | 0      |   0      |
| GMSC      | aligned  | rf      | ocean_joint_free  |  250 |      1.2  |            3 |               0 | 0.25   |   1      |
| GMSC      | aligned  | rf      | dace_rule         |   20 |    100    |           20 |               0 | 0      |   0.0002 |
| GMSC      | aligned  | rf      | mace_rule         |   20 |     50    |           10 |               0 | 0.002  |   0.2109 |
| HMDA      | aligned  | cat     | framework         | 1301 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | cat     | repair_esc        | 1301 |      0.15 |            2 |               0 | 0.5    |   1      |
| HMDA      | aligned  | cat     | repair_sparse     | 1301 |      0.15 |            2 |               0 | 0.5    |   1      |
| HMDA      | aligned  | cat     | posthoc_full_gate | 1301 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | lr      | framework         |  492 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | lr      | repair_esc        |  492 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | lr      | repair_sparse     |  492 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | lr      | posthoc_full_gate |  492 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | lr      | dace_rule         |   60 |     11.67 |            7 |               0 | 0.0156 |   1      |
| HMDA      | aligned  | lr      | mace_rule         |   60 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | mlp     | framework         | 1235 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | mlp     | repair_esc        | 1235 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | mlp     | repair_sparse     | 1235 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | mlp     | posthoc_full_gate | 1235 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | rf      | framework         | 1357 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | rf      | repair_esc        | 1357 |      0.15 |            2 |               0 | 0.5    |   1      |
| HMDA      | aligned  | rf      | repair_sparse     | 1357 |      0.15 |            2 |               0 | 0.5    |   1      |
| HMDA      | aligned  | rf      | posthoc_full_gate | 1357 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | rf      | ocean_joint       | 1357 |     97.79 |         1327 |               0 | 0      |   0      |
| HMDA      | aligned  | rf      | ocean_joint_free  | 1357 |      0    |            0 |               0 | 1      |   1      |
| HMDA      | aligned  | rf      | dace_rule         |   60 |     31.67 |           19 |               0 | 0      |   0.0005 |
| HMDA      | aligned  | rf      | mace_rule         |   60 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | cat     | framework         |  808 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | cat     | repair_esc        |  808 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | cat     | repair_sparse     |  808 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | cat     | posthoc_full_gate |  808 |      0.12 |            1 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | lr      | framework         |  275 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | lr      | repair_esc        |  275 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | lr      | repair_sparse     |  275 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | lr      | posthoc_full_gate |  275 |      0.73 |            2 |               0 | 0.5    |   1      |
| HMDA_OR   | aligned  | lr      | dace_rule         |   60 |     11.67 |            7 |               0 | 0.0156 |   1      |
| HMDA_OR   | aligned  | lr      | mace_rule         |   60 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | mlp     | framework         |  762 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | mlp     | repair_esc        |  762 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | mlp     | repair_sparse     |  762 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | mlp     | posthoc_full_gate |  762 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | rf      | framework         |  840 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | rf      | repair_esc        |  840 |      0.12 |            1 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | rf      | repair_sparse     |  840 |      0.12 |            1 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | rf      | posthoc_full_gate |  840 |      0.24 |            2 |               0 | 0.5    |   1      |
| HMDA_OR   | aligned  | rf      | ocean_joint       |  840 |     97.62 |          820 |               0 | 0      |   0      |
| HMDA_OR   | aligned  | rf      | ocean_joint_free  |  840 |      0    |            0 |               0 | 1      |   1      |
| HMDA_OR   | aligned  | rf      | mace_rule         |   60 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | cat     | framework         |  808 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | cat     | repair_esc        |  808 |      0.12 |            1 |               0 | 1      |   1      |
| HMDA_S    | aligned  | cat     | repair_sparse     |  808 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | cat     | posthoc_full_gate |  808 |     12    |           97 |               0 | 0      |   0      |
| HMDA_S    | aligned  | lr      | framework         |  275 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | lr      | repair_esc        |  275 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | lr      | repair_sparse     |  275 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | lr      | posthoc_full_gate |  275 |     22.91 |           63 |               0 | 0      |   0      |
| HMDA_S    | aligned  | lr      | dace_rule         |   60 |      8.33 |            5 |               0 | 0.0625 |   1      |
| HMDA_S    | aligned  | lr      | mace_rule         |   60 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | mlp     | framework         |  762 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | mlp     | repair_esc        |  762 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | mlp     | repair_sparse     |  762 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | mlp     | posthoc_full_gate |  762 |     13.12 |          100 |               0 | 0      |   0      |
| HMDA_S    | aligned  | rf      | framework         |  840 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | rf      | repair_esc        |  840 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | rf      | repair_sparse     |  840 |      0    |            0 |               0 | 1      |   1      |
| HMDA_S    | aligned  | rf      | posthoc_full_gate |  840 |     10.6  |           89 |               0 | 0      |   0      |
| HMDA_S    | aligned  | rf      | ocean_joint       |  840 |     96.19 |          808 |               0 | 0      |   0      |
| HMDA_S    | aligned  | rf      | ocean_joint_free  |  840 |      0.12 |            1 |               0 | 1      |   1      |
| HMDA_S    | aligned  | rf      | mace_rule         |   60 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | aligned  | cat     | framework         |  300 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | aligned  | cat     | repair_esc        |  300 |      4.67 |           14 |               0 | 0.0001 |   0.0143 |
| OULAD     | aligned  | cat     | repair_sparse     |  300 |      4    |           12 |               0 | 0.0005 |   0.0552 |
| OULAD     | aligned  | cat     | posthoc_full_gate |  300 |     26.33 |           79 |               0 | 0      |   0      |
| OULAD     | aligned  | lr      | framework         |  300 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | aligned  | lr      | repair_esc        |  300 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | aligned  | lr      | repair_sparse     |  300 |      2    |            6 |               0 | 0.0312 |   1      |
| OULAD     | aligned  | lr      | posthoc_full_gate |  300 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | aligned  | lr      | dace_rule         |   63 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | aligned  | lr      | mace_rule         |   63 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | aligned  | mlp     | framework         |  300 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | aligned  | mlp     | repair_esc        |  300 |      2.67 |            8 |               0 | 0.0078 |   0.8203 |
| OULAD     | aligned  | mlp     | repair_sparse     |  300 |      4.67 |           14 |               0 | 0.0001 |   0.0143 |
| OULAD     | aligned  | mlp     | posthoc_full_gate |  300 |      3.67 |           11 |               0 | 0.001  |   0.1084 |
| OULAD     | aligned  | rf      | framework         |  180 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | aligned  | rf      | repair_esc        |  180 |      1.11 |            2 |               0 | 0.5    |   1      |
| OULAD     | aligned  | rf      | repair_sparse     |  180 |      1.67 |            3 |               0 | 0.25   |   1      |
| OULAD     | aligned  | rf      | posthoc_full_gate |  180 |      5    |            9 |               0 | 0.0039 |   0.418  |
| OULAD     | aligned  | rf      | ocean_joint       |  180 |     34.44 |           62 |               0 | 0      |   0      |
| OULAD     | aligned  | rf      | ocean_joint_free  |  180 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | aligned  | rf      | dace_rule         |   21 |     95.24 |           20 |               0 | 0      |   0.0002 |
| OULAD     | aligned  | rf      | mace_rule         |   21 |     28.57 |            6 |               0 | 0.0312 |   1      |
| OULAD     | floor    | cat     | framework         |  300 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | floor    | cat     | repair_esc        |  300 |      4.67 |           14 |               0 | 0.0001 |   0.0143 |
| OULAD     | floor    | cat     | repair_sparse     |  300 |      4    |           12 |               0 | 0.0005 |   0.0552 |
| OULAD     | floor    | cat     | posthoc_full_gate |  300 |     73.33 |          220 |               0 | 0      |   0      |
| OULAD     | floor    | lr      | framework         |  300 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | floor    | lr      | repair_esc        |  300 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | floor    | lr      | repair_sparse     |  300 |      2    |            6 |               0 | 0.0312 |   1      |
| OULAD     | floor    | lr      | posthoc_full_gate |  300 |     67.33 |          202 |               0 | 0      |   0      |
| OULAD     | floor    | mlp     | framework         |  300 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | floor    | mlp     | repair_esc        |  300 |      2.67 |            8 |               0 | 0.0078 |   0.8203 |
| OULAD     | floor    | mlp     | repair_sparse     |  300 |      4.67 |           14 |               0 | 0.0001 |   0.0143 |
| OULAD     | floor    | mlp     | posthoc_full_gate |  300 |     70    |          210 |               0 | 0      |   0      |
| OULAD     | floor    | rf      | framework         |  180 |      0    |            0 |               0 | 1      |   1      |
| OULAD     | floor    | rf      | repair_esc        |  180 |      1.11 |            2 |               0 | 0.5    |   1      |
| OULAD     | floor    | rf      | repair_sparse     |  180 |      1.67 |            3 |               0 | 0.25   |   1      |
| OULAD     | floor    | rf      | posthoc_full_gate |  180 |     68.33 |          123 |               0 | 0      |   0      |
| OULAD     | floor    | rf      | ocean_joint       |  180 |     11.11 |           20 |               0 | 0      |   0.0002 |
| OULAD     | floor    | rf      | ocean_joint_free  |  180 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | cat     | framework         |  461 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | cat     | repair_esc        |  461 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | cat     | repair_sparse     |  461 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | cat     | posthoc_full_gate |  461 |      4.12 |           19 |               0 | 0      |   0.0005 |
| PIMA      | aligned  | lr      | framework         |  427 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | lr      | repair_esc        |  427 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | lr      | repair_sparse     |  427 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | lr      | posthoc_full_gate |  427 |      3.98 |           17 |               0 | 0      |   0.0018 |
| PIMA      | aligned  | lr      | dace_rule         |   60 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | lr      | mace_rule         |   60 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | mlp     | framework         |  292 |      0.34 |            1 |               0 | 1      |   1      |
| PIMA      | aligned  | mlp     | repair_esc        |  292 |      5.48 |           16 |               0 | 0      |   0.0036 |
| PIMA      | aligned  | mlp     | repair_sparse     |  292 |      5.48 |           16 |               0 | 0      |   0.0036 |
| PIMA      | aligned  | mlp     | posthoc_full_gate |  292 |      9.25 |           27 |               0 | 0      |   0.0001 |
| PIMA      | aligned  | rf      | framework         |  467 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | rf      | repair_esc        |  467 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | rf      | repair_sparse     |  467 |      0    |            0 |               0 | 1      |   1      |
| PIMA      | aligned  | rf      | posthoc_full_gate |  467 |      2.36 |           11 |               0 | 0.001  |   0.1084 |
| PIMA      | aligned  | rf      | ocean_joint       |  467 |     49.68 |          232 |               0 | 0      |   0      |
| PIMA      | aligned  | rf      | ocean_joint_free  |  467 |      1.5  |            7 |               0 | 0.0156 |   1      |
| PIMA      | aligned  | rf      | dace_rule         |   60 |     48.33 |           29 |               0 | 0      |   0      |
| PIMA      | aligned  | rf      | mace_rule         |   60 |      3.33 |            2 |               0 | 0.5    |   1      |

## Main rejection reasons
|                                  | reason                                                                     |
|:---------------------------------|:---------------------------------------------------------------------------|
| ('ADULT', 'dace')                | no_candidate 67%; below_policy_threshold 26%; out_of_bounds 6%             |
| ('ADULT', 'dace_rule')           | no_candidate 98%; out_of_bounds 1%; classifier_target_not_met 1%           |
| ('ADULT', 'dice_first')          | no_candidate 62%; below_policy_threshold 38%                               |
| ('ADULT', 'exact')               | no_candidate 100%                                                          |
| ('ADULT', 'framework')           | no_candidate 100%                                                          |
| ('ADULT', 'mace')                | no_candidate 51%; below_policy_threshold 38%; out_of_bounds 11%            |
| ('ADULT', 'mace_rule')           | no_candidate 100%                                                          |
| ('ADULT', 'ocean')               | no_candidate 79%; below_policy_threshold 11%; out_of_bounds 10%            |
| ('ADULT', 'ocean_joint')         | no_candidate 86%; classifier_target_not_met 13%; below_policy_threshold 1% |
| ('ADULT', 'ocean_joint_free')    | no_candidate 86%; classifier_target_not_met 14%                            |
| ('ADULT', 'posthoc_full_gate')   | no_candidate 100%                                                          |
| ('ADULT', 'repair')              | classifier_target_not_met 100%                                             |
| ('ADULT', 'repair_esc')          | classifier_target_not_met 100%                                             |
| ('ADULT', 'repair_sparse')       | classifier_target_not_met 100%                                             |
| ('ADULT', 'repair_sparse0')      | classifier_target_not_met 100%                                             |
| ('GMSC', 'dace')                 | no_candidate 75%; below_policy_threshold 25%                               |
| ('GMSC', 'dace_rule')            | no_candidate 100%                                                          |
| ('GMSC', 'dice_first')           | below_policy_threshold 48%; no_candidate 45%; out_of_bounds 7%             |
| ('GMSC', 'exact')                | no_candidate 100%                                                          |
| ('GMSC', 'framework')            | no_candidate 100%                                                          |
| ('GMSC', 'mace')                 | below_policy_threshold 53%; no_candidate 47%                               |
| ('GMSC', 'mace_rule')            | no_candidate 100%                                                          |
| ('GMSC', 'ocean')                | below_policy_threshold 93%; no_candidate 7%                                |
| ('GMSC', 'ocean_joint')          | below_policy_threshold 85%; no_candidate 15%                               |
| ('GMSC', 'ocean_joint_free')     | no_candidate 100%                                                          |
| ('GMSC', 'posthoc_full_gate')    | no_candidate 100%                                                          |
| ('GMSC', 'repair')               | classifier_target_not_met 99%; no_candidate 1%                             |
| ('GMSC', 'repair_esc')           | classifier_target_not_met 98%; no_candidate 2%                             |
| ('GMSC', 'repair_sparse')        | classifier_target_not_met 100%                                             |
| ('GMSC', 'repair_sparse0')       | classifier_target_not_met 100%                                             |
| ('HMDA', 'dace')                 | policy_violated 57%; no_candidate 43%                                      |
| ('HMDA', 'dace_rule')            | no_candidate 100%                                                          |
| ('HMDA', 'dice_first')           | policy_violated 100%; no_candidate 0%                                      |
| ('HMDA', 'exact')                | no_candidate 100%                                                          |
| ('HMDA', 'framework')            | no_candidate 100%                                                          |
| ('HMDA', 'mace')                 | policy_violated 98%; no_candidate 2%                                       |
| ('HMDA', 'ocean')                | policy_violated 100%                                                       |
| ('HMDA', 'ocean_joint')          | policy_violated 100%                                                       |
| ('HMDA', 'posthoc_full_gate')    | no_candidate 100%                                                          |
| ('HMDA', 'repair')               | classifier_target_not_met 100%                                             |
| ('HMDA', 'repair_esc')           | classifier_target_not_met 100%                                             |
| ('HMDA', 'repair_sparse')        | classifier_target_not_met 100%                                             |
| ('HMDA', 'repair_sparse0')       | classifier_target_not_met 100%                                             |
| ('HMDA_OR', 'dace')              | policy_violated 88%; no_candidate 12%                                      |
| ('HMDA_OR', 'dace_rule')         | no_candidate 100%                                                          |
| ('HMDA_OR', 'dice_first')        | policy_violated 100%                                                       |
| ('HMDA_OR', 'mace')              | policy_violated 98%; no_candidate 2%                                       |
| ('HMDA_OR', 'ocean')             | policy_violated 100%                                                       |
| ('HMDA_OR', 'ocean_joint')       | policy_violated 100%                                                       |
| ('HMDA_OR', 'posthoc_full_gate') | no_candidate 100%                                                          |
| ('HMDA_OR', 'repair')            | classifier_target_not_met 100%                                             |
| ('HMDA_OR', 'repair_esc')        | classifier_target_not_met 100%                                             |
| ('HMDA_OR', 'repair_sparse')     | classifier_target_not_met 100%                                             |
| ('HMDA_OR', 'repair_sparse0')    | classifier_target_not_met 100%                                             |
| ('HMDA_S', 'dace')               | policy_violated 100%                                                       |
| ('HMDA_S', 'dace_rule')          | no_candidate 100%                                                          |
| ('HMDA_S', 'dice_first')         | inconsistent 69%; policy_violated 31%                                      |
| ('HMDA_S', 'exact')              | no_candidate 100%                                                          |
| ('HMDA_S', 'framework')          | no_candidate 100%                                                          |
| ('HMDA_S', 'mace')               | policy_violated 98%; no_candidate 2%                                       |
| ('HMDA_S', 'ocean')              | policy_violated 100%; inconsistent 0%                                      |
| ('HMDA_S', 'ocean_joint')        | policy_violated 100%; classifier_target_not_met 0%                         |
| ('HMDA_S', 'ocean_joint_free')   | policy_violated 75%; classifier_target_not_met 25%                         |
| ('HMDA_S', 'posthoc_full_gate')  | no_candidate 100%                                                          |
| ('HMDA_S', 'repair')             | classifier_target_not_met 82%; inconsistent 9%; policy_violated 9%         |
| ('HMDA_S', 'repair_esc')         | classifier_target_not_met 50%; policy_violated 33%; inconsistent 17%       |
| ('HMDA_S', 'repair_sparse')      | no_candidate 80%; classifier_target_not_met 20%                            |
| ('HMDA_S', 'repair_sparse0')     | classifier_target_not_met 81%; no_candidate 19%                            |
| ('OULAD', 'dace')                | below_policy_threshold 51%; no_candidate 40%; out_of_bounds 9%             |
| ('OULAD', 'dace_rule')           | no_candidate 100%                                                          |
| ('OULAD', 'dice_first')          | below_policy_threshold 67%; out_of_bounds 32%; no_candidate 1%             |
| ('OULAD', 'exact')               | no_candidate 100%                                                          |
| ('OULAD', 'framework')           | no_candidate 100%                                                          |
| ('OULAD', 'mace')                | below_policy_threshold 80%; no_candidate 19%; out_of_bounds 1%             |
| ('OULAD', 'mace_rule')           | no_candidate 100%                                                          |
| ('OULAD', 'ocean')               | below_policy_threshold 98%; out_of_bounds 2%                               |
| ('OULAD', 'ocean_joint')         | below_policy_threshold 95%; classifier_target_not_met 5%                   |
| ('OULAD', 'ocean_joint_free')    | below_policy_threshold 100%                                                |
| ('OULAD', 'posthoc_full_gate')   | no_candidate 100%                                                          |
| ('OULAD', 'repair')              | classifier_target_not_met 95%; below_policy_threshold 5%                   |
| ('OULAD', 'repair_esc')          | below_policy_threshold 64%; classifier_target_not_met 36%                  |
| ('OULAD', 'repair_sparse')       | no_candidate 55%; classifier_target_not_met 45%                            |
| ('OULAD', 'repair_sparse0')      | classifier_target_not_met 95%; no_candidate 5%                             |
| ('PIMA', 'dace')                 | policy_violated 95%; out_of_bounds 4%; no_candidate 1%                     |
| ('PIMA', 'dace_rule')            | policy_violated 55%; no_candidate 45%                                      |
| ('PIMA', 'dice_first')           | policy_violated 100%; out_of_bounds 0%; no_candidate 0%                    |
| ('PIMA', 'exact')                | no_candidate 100%                                                          |
| ('PIMA', 'framework')            | no_candidate 100%                                                          |
| ('PIMA', 'mace')                 | policy_violated 83%; no_candidate 17%                                      |
| ('PIMA', 'mace_rule')            | no_candidate 100%                                                          |
| ('PIMA', 'ocean')                | policy_violated 100%; classifier_target_not_met 0%                         |
| ('PIMA', 'ocean_joint')          | policy_violated 98%; classifier_target_not_met 2%                          |
| ('PIMA', 'ocean_joint_free')     | classifier_target_not_met 100%                                             |
| ('PIMA', 'posthoc_full_gate')    | no_candidate 100%                                                          |
| ('PIMA', 'repair')               | classifier_target_not_met 100%                                             |
| ('PIMA', 'repair_esc')           | classifier_target_not_met 100%                                             |
| ('PIMA', 'repair_sparse')        | classifier_target_not_met 100%                                             |
| ('PIMA', 'repair_sparse0')       | classifier_target_not_met 100%                                             |
