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


# Lending with a structural action model (v3).  The applicant acts on the loan amount
# (larger down payment) and on other monthly debt; the combined loan-to-value ratio
# follows the loan amount exactly, and lowering the loan lowers the mortgage payment
# and hence the debt-to-income ratio:
#   cltv - cltv0 = 100 (loan - loan0) / property_value                      (equality)
#   dti  <= dti0 - k (loan0 - loan),  k = 100 * pay(r, n) / monthly income   (other debt may fall further)
# pay(r, n) = monthly payment per dollar of a fixed-rate loan, r = 6.5 %/yr (2025 level).
RATE = 0.065


def _pay(n_months):
    rm = RATE / 12.0
    return rm / (1.0 - (1.0 + rm) ** (-float(n_months)))


def _hmda_links(row):
    from recourse.core import Constraint
    pv, l0, c0, d0 = float(row['property_value']), float(row['loan_amount']), float(row['cltv']), float(row['dti'])
    # amounts in $ thousands: payment (k$/month) per k$ of loan = pay(); income in k$/yr
    k = 100.0 * _pay(row['loan_term']) / (float(row['income']) / 12.0)
    return [Constraint({'cltv': 1.0, 'loan_amount': -100.0 / pv}, '==', c0 - 100.0 * l0 / pv, 'cltv_follows_loan'),
            Constraint({'dti': 1.0, 'loan_amount': -k}, '<=', d0 - k * l0, 'dti_follows_loan')]


def _hmda_k(df):
    # loan amount and property value in $ thousands (keeps DiCE's post-hoc sparsity search tractable)
    df = df.copy(); df['loan_amount'] = df.loan_amount / 1000.0; df['property_value'] = df.property_value / 1000.0
    return df


HMDA_S = dict(HMDA, name='HMDA_S', tau_sweep=[], prepare=_hmda_k,
              actionable=dict(loan_amount=dict(direction='decrease', lo=lambda r: 0.6 * float(r['loan_amount']), hi=1e12),
                              dti=dict(direction='decrease', lo=20.0, hi=65.0),
                              cltv=dict(direction='decrease',
                                        lo=lambda r: max(0.0, float(r['cltv']) - 40.0 * float(r['loan_amount']) / float(r['property_value'])),
                                        hi=150.0)),
              links=_hmda_links, derived=('cltv',))

# Lending with a disjunctive (compensating-factor) rule, illustrative of how eligibility
# matrices trade one ratio against another:  CLTV <= 97  and  (DTI <= 45  or  (DTI <= 50 and CLTV <= 80)).
HMDA_OR = dict(HMDA, name='HMDA_OR', tau_sweep=[],
               policy=[dict(weights={'cltv': 1.0}, op='<=', tau=97.0, name='cltv')],
               any_of=[[dict(weights={'dti': 1.0}, op='<=', tau=45.0, name='dti45')],
                       [dict(weights={'dti': 1.0}, op='<=', tau=50.0, name='dti50'),
                        dict(weights={'cltv': 1.0}, op='<=', tau=80.0, name='cltv80')]],
               any_of_name='dti_or_compensating')

# ---------------------------------------------------------------- standard benchmarks (v3)
# Both files are the CARLA versions (Pawelczyk et al., 2021; github.com/carla-recourse/cf-data):
# missing values removed, categorical attributes binarised, outcome coded 1 = desired.

def _adult(df):
    df = df.copy()
    bins = {'workclass': 'Private', 'marital-status': 'Married', 'occupation': 'Managerial-Specialist',
            'relationship': 'Husband', 'race': 'White', 'sex': 'Male', 'native-country': 'US'}
    for c, v in bins.items():
        df[c] = (df[c] == v).astype(float)
    df.columns = [c.replace('-', '_') for c in df.columns]
    return df


# Employment: Adult (1994 US Census).  Rule (policy scenario): EU Working Time Directive
# 2003/88/EC, Art. 6(b) -- average weekly working time, including overtime, at most 48 hours.
# Actions: more education (at most 4 further years, i.e. about one degree) and a change of hours.
ADULT = dict(
    name='ADULT', path='ADULT/adult.csv', y='income', group=None, prepare=_adult,
    features=['age', 'workclass', 'fnlwgt', 'education_num', 'marital_status', 'occupation', 'relationship',
              'race', 'sex', 'capital_gain', 'capital_loss', 'hours_per_week', 'native_country'],
    actionable=dict(education_num=dict(direction='increase', lo=1.0, hi=lambda r: min(16.0, float(r['education_num']) + 4.0)),
                    hours_per_week=dict(direction='both', lo=1.0, hi=99.0)),
    policy=[dict(weights={'hours_per_week': 1.0}, op='<=', tau=48.0, name='working_time')],
)


def _gmsc(df):
    # DebtRatio = monthly debt payments / monthly gross income; extreme values (> 5) are data errors
    df = df[(df.DebtRatio <= 5.0) & (df.RevolvingUtilizationOfUnsecuredLines <= 2.0)].copy()
    df.columns = [c.replace('-', '_') for c in df.columns]
    return df


# Consumer credit: Give Me Some Credit (Kaggle 2011).  Rule: debt-to-income at most 43 %
# (CFPB Ability-to-Repay / Qualified Mortgage rule, 12 CFR 1026.43(e)(2)(vi), in force 2014-2021).
GMSC = dict(
    name='GMSC', path='GMSC/gmsc.csv', y='SeriousDlqin2yrs', group=None, prepare=_gmsc,
    features=['RevolvingUtilizationOfUnsecuredLines', 'age', 'NumberOfTime30_59DaysPastDueNotWorse', 'DebtRatio',
              'MonthlyIncome', 'NumberOfOpenCreditLinesAndLoans', 'NumberOfTimes90DaysLate',
              'NumberRealEstateLoansOrLines', 'NumberOfTime60_89DaysPastDueNotWorse', 'NumberOfDependents'],
    actionable=dict(DebtRatio=dict(direction='decrease', lo=0.0, hi=5.0),
                    RevolvingUtilizationOfUnsecuredLines=dict(direction='decrease', lo=0.0, hi=2.0),
                    NumberOfOpenCreditLinesAndLoans=dict(direction='decrease', lo=0.0, hi=24.0)),
    policy=[dict(weights={'DebtRatio': 1.0}, op='<=', tau=0.43, name='dti')],
)

for cfg in [HMDA, PIMA, HMDA_S, HMDA_OR, ADULT, GMSC]:
    if os.path.exists(os.path.join(DATA, cfg['path'])):
        register(cfg)
