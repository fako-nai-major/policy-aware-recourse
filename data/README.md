# Data

`datasets.py` reads three files from this folder; set the `PAR_DATA` environment variable to use another folder with the same layout.

| Path | Included | Source |
|---|---|---|
| `OULAD/OULAD_All_Courses.csv` | yes | Derived from the Open University Learning Analytics Dataset |
| `HarvardX/harvardx-cs250.csv` | no | HarvardX person-course data; download and prepare as described below |
| `AUC/assignment_grades_cleaned.csv` | no | Institutional course records from Athabasca University; not publicly available |
| `OULAD/studentInfo.csv` | no | Raw OULAD file; needed only by `fairness.py` |

## OULAD

One row per learner and module presentation (30,121 rows; all seven modules, 2013B–2014J), built from the raw OULAD tables. The columns are:

- `id_student`, `code_module`, `code_presentation`;
- `date_accessed`, `sum_click` (total VLE clicks);
- for each `Test_1` … `Test_6`: the weighted contribution of the k-th assessment to the course score, plus its due date (`Test_k_due`) and submission date (`Test_k_submit`);
- `final_exam`;
- `final_result`.

`NULL` marks an assessment that does not exist or was not submitted. `datasets.py` keeps modules AAA, BBB, EEE and FFF, drops withdrawn learners, and treats `Pass` and `Distinction` as passing.

OULAD is © The Open University and released under CC BY 4.0. Please cite Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). Open University Learning Analytics dataset. *Scientific Data*, 4, 170171. https://doi.org/10.1038/sdata.2017.171

The raw tables, including `studentInfo.csv` for the group-level audit, are available at https://analyse.kmi.open.ac.uk/open_dataset.

## HarvardX

`harvardx-cs250.csv` has the columns `certified`, `nevents`, `ndays_act`, `nchapters` and `userid` (one row per learner, 11,023 rows). It comes from the HarvardX person-course data:

- Source: [dataset citation, DOI and course filter]
- Preparation: [steps used to create the extract]

The data are de-identified but subject to the provider's terms of use, so they are not redistributed here.

## AUC

`assignment_grades_cleaned.csv` has one row per learner (670 rows) with the columns `id_student`, `date_accessed`, `sum_click`, `Test_1` … `Test_5`, `final_exam`, `final_grade` and `final_result`. The label is `final_result = 1` if `final_grade = 0.25 × (Test_1 + … + Test_4) > 15`.

These are institutional records that cannot be shared. [State access conditions, e.g. "available from the corresponding author on reasonable request, subject to approval by …"]

The released AUC per-query results contain pseudonymous learner codes (`L0001`…) instead of student IDs. The counterfactual feature vectors have been removed from them.
