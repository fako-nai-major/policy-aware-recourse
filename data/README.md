# Data

`datasets.py` reads three files from this folder; set the `PAR_DATA` environment variable to use another folder with the same layout.

| Path | Included | Source |
|---|---|---|
| `OULAD/OULAD_coursework.csv` | yes | Built from the raw Open University Learning Analytics Dataset by `tools/prepare_oulad.py` |
| `HarvardX/harvardx-cs250.csv` | no | HarvardX-MITx person-course data (CS50x, 2012); download and run `tools/prepare_harvardx.py` |
| `AUC/assignment_grades_cleaned.csv` | no | Institutional course records from Athabasca University; not publicly available |
| `OULAD/studentInfo.csv` | no | Raw OULAD file; needed only by `fairness.py` (and, with the other raw tables, by `tools/prepare_oulad.py`) |

## OULAD

One row per learner and module presentation for modules AAA, BBB, EEE and FFF (19,353 rows; 13,714 after `datasets.py` drops withdrawn learners), built from the raw OULAD tables by `tools/prepare_oulad.py`:

- `id_student`, `code_module`, `code_presentation`, `final_result`;
- `sum_click`: total VLE clicks of the learner in the presentation (from `studentVle.csv`);
- `Test_1` … `Test_11`: the contribution of the k-th weighted coursework assessment (TMA or CMA with weight > 0, ordered by due date; examinations excluded) to the coursework score, i.e. score × weight / 100. A missing submission contributes 0;
- `W_1` … `W_11`: the weight of that assessment in the presentation, used as its upper bound. Assessments that do not exist in a presentation have weight 0.

In every presentation the coursework weights sum to 100, so Σ Test_k is the 0–100 coursework score to which the Open University's 40% threshold applies. This threshold is necessary but not sufficient for passing, because the modules also have an examination. To rebuild the file, download the raw tables from https://analyse.kmi.open.ac.uk/open_dataset and run `python tools/prepare_oulad.py path/to/raw_folder`.

OULAD is © The Open University and released under CC BY 4.0. Please cite Kuzilek, J., Hlosta, M., & Zdrahal, Z. (2017). Open University Learning Analytics dataset. *Scientific Data*, 4, 170171. https://doi.org/10.1038/sdata.2017.171

The raw tables, including `studentInfo.csv` for the group-level audit, are available at https://analyse.kmi.open.ac.uk/open_dataset.

## HarvardX

`harvardx-cs250.csv` has the columns `certified`, `nevents`, `ndays_act`, `nchapters` and `userid` (one row per learner, 11,023 rows; 1,282 certified, 11.6%).

**Source.** HarvardX-MITx Person-Course Academic Year 2013 De-Identified dataset, version 2.0 (HarvardX & MITx, 2014), Harvard Dataverse, https://doi.org/10.7910/DVN/26147. We use the records for the course `HarvardX/CS50x/2012` (169,621 registrants). The file name keeps an internal label ("cs250"); the course is CS50x.

**Preparation** (`tools/prepare_harvardx.py` rebuilds the file from the person-course CSV):

1. Keep the rows with `course_id == "HarvardX/CS50x/2012"`.
2. Keep learners with `explored == 1`, i.e. who accessed more than half of the course chapters (11,023 learners).
3. Derive `userid` from `userid_di` by dropping its `MHxPC` prefix (`MHxPC130471418` → `130471418`).
4. Keep `certified` (the outcome) and the engagement counts `nevents`, `ndays_act` and `nchapters`. Demographic fields, dates, `grade`, `viewed` and `explored` are dropped; `nplay_video` and `nforum_posts` are dropped because they are 0 for every learner in this extract.

The data are de-identified but subject to the provider's terms of use, so they are not redistributed here.

## AUC

`assignment_grades_cleaned.csv` has one row per learner (670 rows) with the columns `id_student`, `date_accessed`, `sum_click`, `Test_1` … `Test_5`, `final_exam`, `final_grade` and `final_result`. The label is `final_result = 1` if `final_grade = 0.25 × (Test_1 + … + Test_4) > 15`.

These are institutional records that cannot be shared. [State access conditions, e.g. "available from the corresponding author on reasonable request, subject to approval by …"]

The released AUC per-query results contain pseudonymous learner codes (`L0001`…) instead of student IDs. The counterfactual feature vectors have been removed from them.
