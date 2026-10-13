"""Build data/HMDA/hmda_purchase.csv from a CFPB HMDA Data Browser export.

Keeps conventional, first-lien, home-purchase, owner-occupied, single-unit,
site-built, non-business, closed-end, non-reverse mortgage applications that were
either originated (action_taken 1 -> approved = 1) or denied (3 -> approved = 0).

Columns kept for modelling: loan_amount, income (thousands), property_value,
loan_term, dti (debt-to-income, %), cltv (combined loan-to-value, %).
HMDA reports DTI in bands outside 36-49%; bands are mapped to their midpoints
(<20 -> 15, 20-<30 -> 25, 30-<36 -> 33, 50-60 -> 55, >60 -> 65).
Applicant sex, race, ethnicity and age are kept only for the group audit and are
never model features.  Rows with missing or exempt model fields are dropped.

Usage:  python tools/prepare_hmda.py path/to/hmda_export.csv
"""
import os, sys
import numpy as np, pandas as pd

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'HMDA', 'hmda_purchase.csv')
DTI_BANDS = {'<20%': 15.0, '20%-<30%': 25.0, '30%-<36%': 33.0, '50%-60%': 55.0, '>60%': 65.0}


def main(path):
    d = pd.read_csv(path, low_memory=False)
    d = d[d.action_taken.isin([1, 3]) & (d.loan_type == 1) & (d.loan_purpose == 1) & (d.lien_status == 1)
          & (d.occupancy_type == 1) & (d.total_units.astype(str) == '1')
          & (d.derived_dwelling_category == 'Single Family (1-4 Units):Site-Built')
          & (d.business_or_commercial_purpose == 2) & (d['open-end_line_of_credit'] == 2) & (d.reverse_mortgage == 2)].copy()
    d['approved'] = (d.action_taken == 1).astype(int)
    dti = d.debt_to_income_ratio.astype(str)
    d['dti'] = pd.to_numeric(dti.map(DTI_BANDS).fillna(dti), errors='coerce')
    d['cltv'] = pd.to_numeric(d.loan_to_value_ratio, errors='coerce')
    for c in ['loan_amount', 'income', 'property_value', 'loan_term']:
        d[c] = pd.to_numeric(d[c], errors='coerce')
    model = ['loan_amount', 'income', 'property_value', 'loan_term', 'dti', 'cltv']
    d = d.dropna(subset=model)
    d = d[(d.income > 0) & (d.cltv > 0) & (d.cltv <= 150) & (d.property_value > 0)]
    keep = ['activity_year', 'county_code', 'approved', 'denial_reason-1'] + model + \
           ['derived_sex', 'derived_race', 'derived_ethnicity', 'applicant_age']
    d = d[keep].reset_index(drop=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    d.to_csv(OUT, index=False)
    print(f'{len(d):,} applications ({d.approved.mean():.1%} approved) -> {OUT}')
    print('denied with DTI as first reason:', int((d['denial_reason-1'] == 1).sum()), 'of', int((d.approved == 0).sum()))


if __name__ == '__main__':
    main(sys.argv[1])
