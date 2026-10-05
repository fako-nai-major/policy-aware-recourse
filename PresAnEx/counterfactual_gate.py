"""Final acceptance checks for complete counterfactual feature vectors.

This gate rejects the selected output; it does not search for a replacement.
Checks describe the encoded policy and bounds, not causal feasibility.
"""
import numpy as np
import pandas as pd


def apply_hard_gate(candidate, original, *, feature_columns, actionable_features,
                    feature_bounds, assessment_weights, institutional_threshold,
                    predict, desired_class=1):
    """Return (accepted candidate or None, audit) after fresh final-vector checks.

    `predict` must accept a DataFrame in feature_columns order. Prediction errors
    propagate: a model/configuration failure is not ordinary recourse rejection.
    Non-finite/missing inputs fail closed. All non-actionable features are fixed.
    """
    if not callable(predict):
        raise ValueError('A prediction callable is required by the hard gate')
    if not np.isfinite(institutional_threshold):
        raise ValueError('Institutional threshold must be finite')
    columns = list(feature_columns)
    if not columns or len(set(columns)) != len(columns):
        raise ValueError('Model feature columns must be nonempty and unique')
    if not set(actionable_features).issubset(columns) or not set(assessment_weights).issubset(columns):
        raise ValueError('Policy and actionable features must be model features')
    for feature in actionable_features:
        low, high = feature_bounds[feature]
        if not np.isfinite([low, high]).all() or low > high:
            raise ValueError(f'Invalid bounds for {feature}')
    if not assessment_weights or not np.isfinite(list(assessment_weights.values())).all():
        raise ValueError('Policy weights must be nonempty and finite')
    audit = dict(accepted=False, policy_valid=False, classifier_valid=False,
                 feasible=False, policy_score=None, prediction=None, reasons=[])
    if candidate is None:
        audit['reasons'].append('no_candidate')
        return None, audit
    missing = [f for f in columns if f not in candidate or f not in original]
    if missing:
        audit['reasons'].append('missing_features:' + ','.join(missing))
        return None, audit
    for feature in columns:
        value = candidate[feature]
        if pd.isna(value) or (isinstance(value, (int, float, np.number)) and not np.isfinite(value)):
            audit['reasons'].append(f'nonfinite_feature:{feature}')
    if audit['reasons']:
        return None, audit
    try:
        score = sum(float(candidate[f]) * w for f, w in assessment_weights.items())
        out_of_bounds = [f for f in actionable_features
                         if not feature_bounds[f][0] <= float(candidate[f]) <= feature_bounds[f][1]]
    except (TypeError, ValueError):
        audit['reasons'].append('nonnumeric_policy_or_actionable_feature')
        return None, audit
    if not np.isfinite(score):
        audit['reasons'].append('nonfinite_policy_score')
        return None, audit
    # Exact preservation, including categorical values and identifiers.
    changed = [f for f in columns if f not in actionable_features
               and (pd.isna(original[f]) or candidate[f] != original[f])]
    audit['policy_score'] = float(score)
    audit['policy_valid'] = bool(score >= institutional_threshold)
    audit['feasible'] = not out_of_bounds and not changed
    if not audit['policy_valid']:
        audit['reasons'].append('below_policy_threshold')
    audit['reasons'].extend('out_of_bounds:' + f for f in out_of_bounds)
    audit['reasons'].extend('immutable_changed:' + f for f in changed)
    prediction = np.asarray(predict(pd.DataFrame([candidate[columns].to_dict()], columns=columns))).reshape(-1)
    if len(prediction) != 1:
        raise ValueError('Expected one classifier prediction for the selected vector')
    audit['prediction'] = prediction[0].item() if isinstance(prediction[0], np.generic) else prediction[0]
    audit['classifier_valid'] = bool(prediction[0] == desired_class)
    if not audit['classifier_valid']:
        audit['reasons'].append('classifier_target_not_met')
    audit['accepted'] = audit['policy_valid'] and audit['feasible'] and audit['classifier_valid']
    if not audit['accepted']:
        return None, audit
    accepted = candidate.copy()
    accepted['predicted_score'] = score
    accepted['predicted_result'] = 1
    accepted['policy_penalty'] = 0.0
    accepted['feasibility_penalty'] = 0.0
    return accepted, audit
