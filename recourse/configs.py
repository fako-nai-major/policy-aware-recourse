"""Non-education domains (registered when their prepared data file exists)."""
import os
from datasets import DATA
from recourse.domains import register

# Lending: HMDA home-purchase applications (prepared by tools/prepare_hmda.py).
# Rule: Fannie Mae Selling Guide B3-6-02, maximum total DTI 50% for loans underwritten
# with Desktop Underwriter; maximum combined loan-to-value 97% (Eligibility Matrix).
HMDA = dict(
    name='HMDA', path='HMDA/hmda_purchase.csv', y='approved', group=None,
    features=['loan_amount', 'income', 'property_value', 'loan_term', 'dti', 'cltv'],
    actionable=dict(dti=dict(direction='decrease', lo=20.0, hi=65.0),
                    cltv=dict(direction='decrease', lo=60.0, hi=150.0)),
    policy=[dict(weights={'dti': 1.0}, op='<=', tau=50.0, name='dti'),
            dict(weights={'cltv': 1.0}, op='<=', tau=97.0, name='cltv')],
    tau_sweep=[43.0, 45.0, 50.0],
)



def _pima(df):
    # Original NIDDK data (768 women): 0 codes a missing measurement.  Insulin (374 missing)
    # and skin thickness (227 missing) are dropped; rows with missing glucose, blood
    # pressure or BMI are removed (no imputation, so no outcome-dependent filling).
    df = df[(df.Glucose > 0) & (df.BloodPressure > 0) & (df.BMI > 0)].copy()
    df['no_diabetes'] = 1 - df.Outcome          # desired class = no diabetes onset within 5 years
    return df


# Health: Pima Indians Diabetes (NIDDK).  Glucose is the 2-hour plasma glucose of an
# oral glucose tolerance test.  Rule: ADA normal range (2-h glucose < 140 mg/dL) and
# WHO non-obese BMI (< 30 kg/m2).
PIMA = dict(
    name='PIMA', path='PIMA/diabetes.csv', y='no_diabetes', group=None, prepare=_pima,
    features=['Pregnancies', 'Glucose', 'BloodPressure', 'BMI', 'DiabetesPedigreeFunction', 'Age'],
    actionable=dict(Glucose=dict(direction='decrease', lo=70.0, hi=199.0),
                    BMI=dict(direction='decrease', lo=18.5, hi=67.1),
                    BloodPressure=dict(direction='decrease', lo=60.0, hi=122.0)),
    policy=[dict(weights={'Glucose': 1.0}, op='<=', tau=139.0, name='glucose'),
            dict(weights={'BMI': 1.0}, op='<=', tau=29.9, name='bmi')],
    tau_sweep=[125.0, 139.0],
)

for cfg in [HMDA, PIMA]:
    if os.path.exists(os.path.join(DATA, cfg['path'])):
        register(cfg)
