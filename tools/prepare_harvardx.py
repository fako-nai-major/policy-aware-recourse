"""Build data/HarvardX/harvardx-cs250.csv from the HarvardX-MITx person-course data.

Source: HarvardX-MITx Person-Course Academic Year 2013 De-Identified dataset,
version 2.0 (Harvard Dataverse, https://doi.org/10.7910/DVN/26147).

Usage (from the repository root):
    python tools/prepare_harvardx.py path/to/person_course.csv
The input can be the full person-course file or a file already restricted to
HarvardX/CS50x/2012. Output: data/HarvardX/harvardx-cs250.csv (11,023 learners).
"""
import os
import sys
import pandas as pd

COURSE = 'HarvardX/CS50x/2012'
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'HarvardX', 'harvardx-cs250.csv')


def main(path):
    pc = pd.read_csv(path, low_memory=False)
    d = pc[pc.course_id == COURSE]                      # 1. one course: CS50x (2012)
    d = d[d.explored == 1].copy()                       # 2. learners who explored > half the chapters
    d['userid'] = d.userid_di.str[5:].astype('int64')   # 3. 'MHxPC130471418' -> 130471418
    d = d[['certified', 'nevents', 'ndays_act', 'nchapters', 'userid']]  # 4. outcome + engagement
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    d.to_csv(OUT)                                       # index kept to match the file used in the paper
    print(f'{len(d):,} learners, {int(d.certified.sum()):,} certified ({d.certified.mean():.1%}) -> {OUT}')


if __name__ == '__main__':
    main(sys.argv[1])
