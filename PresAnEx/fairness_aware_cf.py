"""
fairness_aware_cf.py

Module for generating and selecting diverse policy-aware counterfactuals with support
for institutional policy constraints, effort-weighted proximity, sparsity, and feasibility.

Functions:
    generate_diverse_policy_aware_cfs: Generate diverse policy-aware counterfactuals similar to DiCE
    select_best_counterfactual: Select the best counterfactual from a set of candidates.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import euclidean_distances
import os
import warnings

from PresAnEx.course_data import course_catalog


DEFAULT_ASSIGNMENT_FEATURE_MAP = {
    "Assignment 1": ["Test_1", "Test_2"],
    "Assignment 2": ["Test_3"],
    "Assignment 3": ["Test_4"],
    "Final project": ["Test_5", "final_exam"],
}


def assessmentLevel(content):
    from ContentRecomVal.assessment_level import assessmentLevel as _assessment_level

    return _assessment_level(content)


def suggest_learning_content(*args, **kwargs):
    from ContentRecomVal.content_recommendation import (
        suggest_learning_content as _suggest_learning_content,
    )

    return _suggest_learning_content(*args, **kwargs)


def get_course_by_code(course_code):
    normalized_code = str(course_code).strip().upper()
    for course in course_catalog:
        if str(course.get("course_code", "")).strip().upper() == normalized_code:
            return course
    raise ValueError(f"Unknown course_code '{course_code}'.")


def build_assignment_feature_map(assignment_feature_map=None):
    raw_mapping = assignment_feature_map or DEFAULT_ASSIGNMENT_FEATURE_MAP
    normalized_mapping = {}

    for assignment_name, features in raw_mapping.items():
        if isinstance(features, str):
            feature_list = [features]
        else:
            feature_list = [str(feature).strip() for feature in features if str(feature).strip()]

        if feature_list:
            normalized_mapping[str(assignment_name).strip()] = feature_list

    return normalized_mapping


def _changed_feature_names(original_instance, best_cf):
    changed_features = []
    for feature_name in best_cf.index:
        if feature_name not in original_instance.index:
            continue
        try:
            if not np.isclose(best_cf[feature_name], original_instance[feature_name]):
                changed_features.append(feature_name)
        except Exception:
            if best_cf[feature_name] != original_instance[feature_name]:
                changed_features.append(feature_name)
    return changed_features


def _mapped_feature_names(assignment_feature_map):
    mapped_features = []
    seen = set()
    for features in assignment_feature_map.values():
        for feature_name in features:
            normalized = str(feature_name).strip()
            if not normalized or normalized in seen:
                continue
            seen.add(normalized)
            mapped_features.append(normalized)
    return mapped_features


def _ordered_assignment_feature_pairs(course, assignment_feature_map):
    ordered_pairs = []
    for assignment_name in course.get("assignments", {}).keys():
        for feature_name in assignment_feature_map.get(assignment_name, []):
            ordered_pairs.append((assignment_name, feature_name))
    return ordered_pairs


def _dedupe_preserving_order(items):
    ordered = []
    seen = set()
    for item in items:
        normalized = str(item).strip()
        if not normalized:
            continue
        lowered = normalized.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        ordered.append(normalized)
    return ordered


def derive_assignment_gap_analysis(
    original_instance,
    best_cf,
    course_code,
    assignment_feature_map=None,
):
    course = get_course_by_code(course_code)
    resolved_mapping = build_assignment_feature_map(assignment_feature_map)
    mapped_features = _mapped_feature_names(resolved_mapping)
    changed_features = [
        feature_name
        for feature_name in _changed_feature_names(original_instance, best_cf)
        if feature_name in mapped_features
    ]
    assignment_items = []

    for assignment_name, assignment_outcomes in course.get("assignments", {}).items():
        mapped_features = resolved_mapping.get(assignment_name, [])
        improved_features = []
        unchanged_features = []

        for feature_name in mapped_features:
            if feature_name not in original_instance.index or feature_name not in best_cf.index:
                continue

            if best_cf[feature_name] > original_instance[feature_name] and not np.isclose(
                best_cf[feature_name], original_instance[feature_name]
            ):
                improved_features.append(feature_name)
            else:
                unchanged_features.append(feature_name)

        assignment_items.append(
            {
                "assignment_name": assignment_name,
                "mapped_features": mapped_features,
                "improved_features": improved_features,
                "unchanged_features": unchanged_features,
                "impacted": bool(improved_features),
                "missing_objectives": list(assignment_outcomes),
            }
        )

    impacted_assignments = [
        item["assignment_name"] for item in assignment_items if item["impacted"]
    ]

    return {
        "course_code": course["course_code"],
        "course_title": course["course_title"],
        "changed_features": changed_features,
        "assignment_feature_map": resolved_mapping,
        "ordered_feature_sequence": [
            {"assignment_name": assignment_name, "feature_name": feature_name}
            for assignment_name, feature_name in _ordered_assignment_feature_pairs(
                course, resolved_mapping
            )
        ],
        "assignments": assignment_items,
        "impacted_assignments": impacted_assignments,
    }


def build_missing_objectives_from_assignments(assignment_gap_analysis):
    missing_objectives = []

    for assignment in assignment_gap_analysis.get("assignments", []):
        if not assignment.get("impacted"):
            continue
        missing_objectives.extend(assignment.get("missing_objectives", []))

    return _dedupe_preserving_order(missing_objectives)


def _derive_assessment_level(missing_objectives):
    if not missing_objectives:
        return None

    # Assessment-level lookup depends on Mongo-backed verb groups.
    # When MongoDB is not configured, skip this step quietly and let
    # content recommendation proceed without a level hint.
    if not os.getenv("MONGODB_URI"):
        return None

    try:
        derived_level = assessmentLevel(" ".join(missing_objectives))
    except Exception:
        return None

    normalized_level = str(derived_level).strip() if derived_level is not None else ""
    return normalized_level or None


def _empty_recommendation_response(course, missing_objectives, assessment_level, providers):
    provider_list = [provider.lower() for provider in (providers or ["coursera", "udemy"])]
    return {
        "category": course.get("recommendation_category"),
        "sub_category": course.get("recommendation_sub_category"),
        "assessment_level": assessment_level,
        "missing_objectives": missing_objectives,
        "providers": provider_list,
        "suggestion_count": 0,
        "suggestions": [],
    }


def _build_recommendation_response(course, missing_objectives, assessment_level, providers):
    selected_providers = providers or ["coursera", "udemy"]
    if not missing_objectives:
        return _empty_recommendation_response(
            course=course,
            missing_objectives=[],
            assessment_level=assessment_level,
            providers=selected_providers,
        )

    return suggest_learning_content(
        missing_objectives=missing_objectives,
        category=course.get("recommendation_category"),
        level=assessment_level,
        sub_category=course.get("recommendation_sub_category"),
        providers=selected_providers,
    )


def build_sequential_recommendations_from_assignments(
    assignment_gap_analysis,
    course_code,
    providers=None,
):
    course = get_course_by_code(course_code)
    sequential_recommendations = []
    cumulative_objectives = []
    assignment_lookup = {
        assignment["assignment_name"]: assignment
        for assignment in assignment_gap_analysis.get("assignments", [])
    }

    for sequence_index, stage in enumerate(
        assignment_gap_analysis.get("ordered_feature_sequence", []), start=1
    ):
        assignment_name = stage["assignment_name"]
        feature_name = stage["feature_name"]
        assignment = assignment_lookup.get(assignment_name)
        if assignment is None or feature_name not in assignment.get("improved_features", []):
            continue

        stage_objectives = _dedupe_preserving_order(assignment.get("missing_objectives", []))
        cumulative_objectives.extend(stage_objectives)
        cumulative_missing_objectives = _dedupe_preserving_order(cumulative_objectives)
        assessment_level = _derive_assessment_level(cumulative_missing_objectives)

        sequential_recommendations.append(
            {
                "sequence_index": sequence_index,
                "assignment_name": assignment_name,
                "feature_name": feature_name,
                "improved_features": [feature_name],
                "stage_missing_objectives": stage_objectives,
                "cumulative_missing_objectives": cumulative_missing_objectives,
                "assessment_level": assessment_level,
                "recommendation_response": _build_recommendation_response(
                    course=course,
                    missing_objectives=cumulative_missing_objectives,
                    assessment_level=assessment_level,
                    providers=providers,
                ),
            }
        )

    return sequential_recommendations


def recommend_learning_materials_from_gaps(
    original_instance,
    best_cf,
    course_code,
    assignment_feature_map=None,
    providers=None,
):
    course = get_course_by_code(course_code)
    gap_analysis = derive_assignment_gap_analysis(
        original_instance=original_instance,
        best_cf=best_cf,
        course_code=course_code,
        assignment_feature_map=assignment_feature_map,
    )
    missing_objectives = build_missing_objectives_from_assignments(gap_analysis)
    assessment_level = _derive_assessment_level(missing_objectives)
    recommendation_response = _build_recommendation_response(
        course=course,
        missing_objectives=missing_objectives,
        assessment_level=assessment_level,
        providers=providers,
    )
    sequential_recommendations = build_sequential_recommendations_from_assignments(
        assignment_gap_analysis=gap_analysis,
        course_code=course_code,
        providers=providers,
    )

    recommendation_payload = {
        "course_code": course["course_code"],
        "course_title": course["course_title"],
        "assignment_feature_map": gap_analysis["assignment_feature_map"],
        "changed_features": gap_analysis["changed_features"],
        "impacted_assignments": gap_analysis["impacted_assignments"],
        "missing_objectives": missing_objectives,
        "assessment_level": assessment_level,
        "sequential_recommendations": sequential_recommendations,
        "recommendation_response": recommendation_response,
    }

    return gap_analysis, recommendation_payload


def generate_diverse_policy_aware_cfs(
    original_instance: pd.Series,
    model,
    institutional_threshold: float,
    actionable_features: list,
    immutable_features: list,
    assessment_weights: dict,
    feature_bounds: dict,
    feature_ranges: dict,
    num_diverse_cfs: int = 10,
    diversity_weight: float = 0.5,
    mutation_rate: float = 0.1,
    max_iterations: int = 100,
    seed: int = None,
    debug: bool = False
):
    """
    Generate diverse policy-aware counterfactuals similar to DiCE methodology.
    
    This function uses an iterative optimization approach with diversity constraints
    to generate multiple valid counterfactuals that satisfy institutional policies.
    
    Parameters:
        original_instance (pd.Series): Original instance to explain.
        model: Trained model with predict_proba or predict method.
        institutional_threshold (float): Score needed to pass.
        actionable_features (list): Features that can be changed.
        immutable_features (list): Features that cannot be changed.
        assessment_weights (dict): {feature: weight} for score computation.
        feature_bounds (dict): {feature: (min, max)} bounds.
        feature_ranges (dict): {feature: (min, max)} for normalization.
        num_diverse_cfs (int): Number of diverse counterfactuals to generate.
        diversity_weight (float): Weight for diversity penalty (0-1).
        mutation_rate (float): Probability of mutating each feature.
        max_iterations (int): Maximum iterations for generation.
        seed (int): Random seed for reproducibility.
    
    Returns:
        pd.DataFrame: Generated diverse counterfactuals with metrics.
    """
    if seed is not None:
        np.random.seed(seed)
    
    def compute_score(x_row, feature_weights):
        """Compute weighted sum score."""
        return sum(x_row[feat] * weight for feat, weight in feature_weights.items() if feat in x_row)
    
    def is_policy_valid(x_cf):
        """Check if counterfactual satisfies policy threshold."""
        score = compute_score(x_cf, assessment_weights)
        return score >= institutional_threshold
    
    def is_feasible(x_cf):
        """Check if counterfactual is feasible (within bounds and respects immutability)."""
        for feat in actionable_features:
            lb, ub = feature_bounds[feat]
            if not (lb <= x_cf[feat] <= ub):
                return False
        for feat in immutable_features:
            if not np.isclose(x_cf[feat], original_instance[feat]):
                return False
        return True
    
    def compute_proximity(x_cf):
        """Compute proximity distance."""
        return sum([
            abs(x_cf[f] - original_instance[f]) / feature_ranges[f]
            for f in actionable_features if f in x_cf
        ])
    
    def compute_sparsity(x_cf):
        """Compute sparsity (number of changed features)."""
        return sum([
            not np.isclose(x_cf[f], original_instance[f])
            for f in actionable_features if f in x_cf
        ])
    
    def compute_diversity_penalty(cf_list, new_cf):
        """Compute penalty based on distance from existing counterfactuals."""
        if len(cf_list) == 0:
            return 0
        cf_array = np.array([cf[actionable_features].values for cf in cf_list])
        new_cf_array = np.array([new_cf[actionable_features].values])
        distances = euclidean_distances(new_cf_array, cf_array)
        return 1.0 / (1.0 + np.mean(distances))  # Penalty decreases with distance
    
    def mutate_instance(x_current, mutation_rate):
        """Create a mutated copy by randomly changing features."""
        x_new = x_current.copy()
        for feat in actionable_features:
            if np.random.random() < mutation_rate:
                lb, ub = feature_bounds[feat]
                x_new[feat] = np.random.uniform(lb, ub)
        return x_new
    
    # Initialize population
    generated_cfs = []
    attempts = []
    iteration = 0
    
    while len(generated_cfs) < num_diverse_cfs and iteration < max_iterations:
        # Generate candidate
        candidate = mutate_instance(original_instance, mutation_rate)
        
        # Enforce immutability
        for feat in immutable_features:
            candidate[feat] = original_instance[feat]
        
        # Check feasibility
        if not is_feasible(candidate):
            iteration += 1
            continue
        
        # Check policy validity
        if is_policy_valid(candidate):
            # Compute diversity
            diversity_penalty = compute_diversity_penalty(generated_cfs, candidate)
            attempts.append({
                'iteration': iteration,
                'candidate': candidate.copy(),
                'score': compute_score(candidate, assessment_weights),
                'feasible': is_feasible(candidate),
                'policy_valid': True,
                'diversity_penalty': diversity_penalty
            })
            
            # Accept if sufficiently diverse or if we need more samples
            if len(generated_cfs) < num_diverse_cfs // 2 or diversity_penalty < 0.7:
                generated_cfs.append(candidate)
        
        iteration += 1
    
    # If we haven't generated enough, use random exploration
    while len(generated_cfs) < num_diverse_cfs:
        candidate = original_instance.copy()
        for feat in actionable_features:
            lb, ub = feature_bounds[feat]
            candidate[feat] = np.random.uniform(lb, ub)
        
        for feat in immutable_features:
            candidate[feat] = original_instance[feat]
        
        if is_feasible(candidate) and is_policy_valid(candidate):
            diversity_penalty = compute_diversity_penalty(generated_cfs, candidate)
            attempts.append({
                'iteration': iteration,
                'candidate': candidate.copy(),
                'score': compute_score(candidate, assessment_weights),
                'feasible': True,
                'policy_valid': True,
                'diversity_penalty': diversity_penalty
            })
            if diversity_penalty < 0.7:
                generated_cfs.append(candidate)
    
    # Convert to DataFrame and compute metrics
    cfs_df = pd.DataFrame(generated_cfs)
    
    # Compute metrics for each CF
    metrics = []
    for _, cf in cfs_df.iterrows():
        score = compute_score(cf, assessment_weights)
        proximity = compute_proximity(cf)
        sparsity = compute_sparsity(cf)
        diversity_pen = compute_diversity_penalty(
            [cfs_df.iloc[i] for i in range(len(metrics))],
            cf
        )
        
        metrics.append({
            'predicted_score': score,
            'predicted_result': 1 if score >= institutional_threshold else 0,
            'proximity_distance': proximity,
            'sparsity': sparsity,
            'diversity_penalty': diversity_pen,
            'feasible': is_feasible(cf),
            'policy_valid': is_policy_valid(cf)
        })
    
    metrics_df = pd.DataFrame(metrics)
    cfs_df = pd.concat([cfs_df.reset_index(drop=True), metrics_df.reset_index(drop=True)], axis=1)
    
    if debug:
        return cfs_df, attempts
    return cfs_df


def generate_diverse_policy_aware_cfs_optimized(
    original_instance: pd.Series,
    model,
    institutional_threshold: float,
    actionable_features: list,
    immutable_features: list,
    assessment_weights: dict,
    feature_bounds: dict,
    feature_ranges: dict,
    effort_weights: dict = None,
    num_diverse_cfs: int = 10,
    lambda_policy: float = 1000,
    lambda_feas: float = 1000,
    lambda_prox: float = 1,
    lambda_spar: float = 0.5,
    lambda_diversity: float = 100,
    learning_rate: float = 0.01,
    max_iterations: int = 500,
    seed: int = None,
    debug: bool = False
):
    """
    Generate diverse policy-aware counterfactuals using optimization-based approach.
    
    Uses gradient-based optimization with diversity constraints to generate multiple
    valid counterfactuals that satisfy institutional policies, inspired by DiCE.
    
    Parameters:
        original_instance (pd.Series): Original instance to explain.
        model: Trained model with predict_proba or predict method.
        institutional_threshold (float): Score needed to pass.
        actionable_features (list): Features that can be changed.
        immutable_features (list): Features that cannot be changed.
        assessment_weights (dict): {feature: weight} for score computation.
        feature_bounds (dict): {feature: (min, max)} bounds.
        feature_ranges (dict): {feature: (min, max)} for normalization.
        effort_weights (dict): {feature: effort} weights (default: uniform).
        num_diverse_cfs (int): Number of diverse counterfactuals to generate.
        lambda_policy (float): Weight for policy validity penalty.
        lambda_feas (float): Weight for feasibility penalty.
        lambda_prox (float): Weight for proximity penalty.
        lambda_spar (float): Weight for sparsity penalty.
        lambda_diversity (float): Weight for diversity penalty.
        learning_rate (float): Learning rate for optimization.
        max_iterations (int): Maximum iterations per CF generation.
        seed (int): Random seed for reproducibility.
    
    Returns:
        pd.DataFrame: Generated diverse counterfactuals with metrics.
    """
    if seed is not None:
        np.random.seed(seed)
    
    if effort_weights is None:
        effort_weights = {f: 1.0 for f in actionable_features}
    
    def compute_score(x_row):
        """Compute weighted sum score."""
        return sum(x_row.get(feat, 0) * weight for feat, weight in assessment_weights.items())
    
    def policy_penalty(x_cf):
        """Policy constraint penalty."""
        s = compute_score(x_cf)
        return max(0, institutional_threshold - s) / institutional_threshold
    
    def feasibility_penalty(x_cf):
        """Feasibility constraint penalty."""
        penalty = 0
        for feat in actionable_features:
            lb, ub = feature_bounds[feat]
            if x_cf.get(feat, 0) < lb or x_cf.get(feat, 0) > ub:
                penalty += 1
        for feat in immutable_features:
            if not np.isclose(x_cf.get(feat, 0), original_instance.get(feat, 0)):
                penalty += 1
        return penalty
    
    def proximity_distance(x_cf):
        """Proximity distance."""
        dist = 0
        for f in actionable_features:
            if f in feature_ranges:
                dist += effort_weights[f] * abs(x_cf.get(f, 0) - original_instance.get(f, 0)) / feature_ranges[f]
        return dist
    
    def sparsity(x_cf):
        """Sparsity (number of changed features)."""
        return sum([1 for f in actionable_features if not np.isclose(x_cf.get(f, 0), original_instance.get(f, 0))])
    
    def diversity_penalty(cf_list, new_cf):
        """Diversity penalty based on distance from existing CFs."""
        if not cf_list:
            return 0
        cf_vectors = np.array([[cf.get(f, 0) for f in actionable_features] for cf in cf_list])
        new_cf_vector = np.array([[new_cf.get(f, 0) for f in actionable_features]])
        distances = euclidean_distances(new_cf_vector, cf_vectors)
        min_distance = np.min(distances)
        return 1.0 / (1.0 + min_distance)
    
    def objective_function(x_cf, cf_list):
        """Combined objective function."""
        pol = policy_penalty(x_cf)
        feas = feasibility_penalty(x_cf)
        prox = proximity_distance(x_cf)
        spar = sparsity(x_cf)
        div = diversity_penalty(cf_list, x_cf)
        
        return (lambda_policy * pol +
                lambda_feas * feas +
                lambda_prox * prox +
                lambda_spar * spar +
                lambda_diversity * div)
    
    generated_cfs = []
    attempts = []
    
    for cf_idx in range(num_diverse_cfs):
        # Initialize candidate
        x_current = original_instance.copy()
        
        # Random perturbation
        for feat in actionable_features:
            lb, ub = feature_bounds[feat]
            x_current[feat] = np.random.uniform(lb, ub)
        
        # Enforce immutability
        for feat in immutable_features:
            x_current[feat] = original_instance[feat]
        
        # Gradient-free optimization using random search
        best_x = x_current.copy()
        best_obj = objective_function(best_x, generated_cfs)
        
        for iteration in range(max_iterations):
            # Generate perturbed candidate
            x_new = best_x.copy()
            
            for feat in actionable_features:
                if np.random.random() < 0.3:  # 30% chance to perturb each feature
                    lb, ub = feature_bounds[feat]
                    perturbation = np.random.normal(0, learning_rate)
                    x_new[feat] = np.clip(best_x[feat] + perturbation, lb, ub)
            
            # Enforce immutability
            for feat in immutable_features:
                x_new[feat] = original_instance[feat]
            
            # Evaluate
            obj_new = objective_function(x_new, generated_cfs)
            
            # Accept if better
            if obj_new < best_obj:
                best_x = x_new.copy()
                best_obj = obj_new
            # log attempt
            if debug:
                attempts.append({
                    'cf_idx': cf_idx,
                    'iteration': iteration,
                    'candidate': x_new.copy(),
                    'obj': obj_new,
                    'policy_penalty': policy_penalty(x_new),
                    'feasibility_penalty': feasibility_penalty(x_new),
                    'proximity': proximity_distance(x_new),
                    'sparsity': sparsity(x_new)
                })
        
        # Only add if policy-valid
        if policy_penalty(best_x) < 0.01:  # Nearly policy-valid
            generated_cfs.append(best_x)
        else:
            if debug:
                attempts.append({
                    'cf_idx': cf_idx,
                    'iteration': max_iterations,
                    'candidate': best_x.copy(),
                    'obj': best_obj,
                    'policy_penalty': policy_penalty(best_x),
                    'feasibility_penalty': feasibility_penalty(best_x),
                    'proximity': proximity_distance(best_x),
                    'sparsity': sparsity(best_x),
                    'accepted': False
                })
    
    # Convert to DataFrame and compute metrics
    cfs_df = pd.DataFrame(generated_cfs)
    
    # Compute metrics for each CF
    metrics = []
    for _, cf in cfs_df.iterrows():
        score = compute_score(cf)
        proximity = proximity_distance(cf)
        spar = sparsity(cf)
        
        metrics.append({
            'predicted_score': score,
            'predicted_result': 1 if score >= institutional_threshold else 0,
            'proximity_distance': proximity,
            'sparsity': spar,
            'objective_score': objective_function(cf, []),
            'feasible': feasibility_penalty(cf) == 0,
            'policy_valid': policy_penalty(cf) < 0.01
        })
    
    metrics_df = pd.DataFrame(metrics)
    cfs_df = pd.concat([cfs_df.reset_index(drop=True), metrics_df.reset_index(drop=True)], axis=1)
    
    if debug:
        return cfs_df, attempts
    return cfs_df


def select_best_counterfactual(
    original_instance: pd.Series,
    cf_examples: pd.DataFrame,
    institutional_threshold: float,
    actionable_features: list,
    immutable_features: list,
    assessment_weights: dict,
    feature_bounds: dict,
    effort_weights: dict,
    feature_ranges: dict,
    lambda_policy=1000,
    lambda_feas=1000,
    lambda_prox=1,
    lambda_spar=0.5,
    plot_scores=True,
    *,
    edit_zero_features=True
):
    """
    Returns the best counterfactual + logs + objective score distribution based on fairness-aware objective.

    Parameters:
        original_instance (pd.Series): Original student instance.
        cf_examples (pd.DataFrame): Counterfactual examples (rows).
        institutional_threshold (float): Score needed to pass (e.g. 0.4).
        actionable_features (list): Features that can be changed.
        immutable_features (list): Features that must remain fixed.
        feature_bounds (dict): {feature: (min, max)}
        effort_weights (dict): {feature: weight}
        feature_ranges (dict): {feature: normalization range}
        lambda_policy, lambda_feas, lambda_prox, lambda_spar (float): Loss weights.
        edit_zero_features (bool): Apply zero-feature replacements after ranking.
            Disable to isolate selection from feature editing in matched ablations.

    Returns:
        pd.Series: Returns the best counterfactual with minimal objective score + logs.
        pd.DataFrame: Counterfactuals DataFrame with penalty and objective columns.
    """

    def policy_penalty(x_cf):
        #s = score_fn(x_cf)
        s = compute_score(x_cf, assessment_weights)
        return max(0, institutional_threshold - s) / institutional_threshold

    def feasibility_penalty(x_cf):
        feas_penalty = 0
        reasons = []
        for feat in actionable_features:
            lb, ub = feature_bounds[feat]
            if not lb <= x_cf[feat] <= ub:
                feas_penalty += 1
                reasons.append(f"{feat} out of bounds")
        for feat in immutable_features:
            if not np.isclose(x_cf[feat], original_instance[feat]):
                feas_penalty += 1
                reasons.append(f"{feat} changed (immutable)")
        return feas_penalty, reasons

    def proximity_distance(x_cf):
        return sum([
            effort_weights[f] * abs(x_cf[f] - original_instance[f]) / feature_ranges[f]
            for f in actionable_features if f in x_cf
        ])

    def sparsity(x_cf):
        return sum([
            not np.isclose(x_cf[f], original_instance[f])
            for f in actionable_features if f in x_cf
        ])
    
    def compute_score(x_row, feature_weights):
        """
        Computes a weighted sum score for the given row using feature_weights.
        Args:
            x_row (pd.Series): The instance (counterfactual or original).
            feature_weights (dict): Mapping from feature name to weight.
        Returns:
            float: Weighted sum score.
        """
        return sum(x_row[feat] * weight for feat, weight in feature_weights.items() if feat in x_row)

    # Containers
    policy_scores = []
    feas_scores = []
    prox_scores = []
    spar_scores = []
    obj_scores = []
    reason_logs = []

    for _, x_cf in cf_examples.iterrows():
        pol = policy_penalty(x_cf)
        feas, reasons = feasibility_penalty(x_cf)
        prox = proximity_distance(x_cf)
        spar = sparsity(x_cf)
        obj = (lambda_policy * pol +
               lambda_feas * feas +
               lambda_prox * prox +
               lambda_spar * spar)

        policy_scores.append(pol)
        feas_scores.append(feas)
        prox_scores.append(prox)
        spar_scores.append(spar)
        obj_scores.append(obj)
        reason_logs.append("; ".join(reasons) if reasons else "OK")

    # Update DataFrame with metrics
    cf_examples = cf_examples.copy()
    cf_examples["predicted_score"] = compute_score(cf_examples, assessment_weights)
    cf_examples["predicted_result"] = cf_examples["predicted_score"].apply(lambda x: 1 if x >= institutional_threshold else 0)
    cf_examples["policy_penalty"] = policy_scores
    cf_examples["feasibility_penalty"] = feas_scores
    cf_examples["proximity_distance"] = prox_scores
    cf_examples["sparsity"] = spar_scores
    cf_examples["objective_score"] = obj_scores
    # Ensure reason_log column is object dtype before assigning string values to avoid
    # pandas FutureWarning about assigning incompatible dtypes to existing numeric columns.
    cf_examples["reason_log"] = pd.Series(reason_logs, index=cf_examples.index, dtype=object)

    # Select best CF with lowest objective score
    min_obj = min(obj_scores)
    tolerance = 1e-3  # Allow minimal difference in objective score
    candidates = [
        (i, cf_examples.iloc[i]) for i, obj in enumerate(obj_scores)
        if abs(obj - min_obj) <= tolerance
    ]

    # Among equally good candidates, prefer:
    #  - lowest number of changed features (sparsity)
    #  - lowest total distance (proximity)
    #  - lowest sum of changed feature values (magnitude)
    def nonzero_metric(cf):
        sparsity_score = sum(
            not np.isclose(cf[f], original_instance[f])
            for f in actionable_features
        )
        proximity_score = sum(
            abs(cf[f] - original_instance[f])
            for f in actionable_features
        )
        nonzero_total = sum(
            cf[f] for f in actionable_features if not np.isclose(cf[f], 0)
        )
        return sparsity_score, proximity_score, nonzero_total

    sorted_candidates = sorted(
        candidates,
        key=lambda tup: nonzero_metric(tup[1])
    )

    best_index, best_cf = sorted_candidates[0]
    best_cf = best_cf.copy()  # Make editable copy

    # Optional feature editing; every final vector still needs the hard gate.
    for feat in (actionable_features if edit_zero_features else []):
        if best_cf[feat] == 0:
            lb, ub = feature_bounds[feat]
            candidate_values = np.linspace(lb, ub, num=10)
            valid_candidates = []
            for val in candidate_values:
                temp_cf = best_cf.copy()
                temp_cf[feat] = val
                within_bounds = lb <= val <= ub
                unchanged_immutable = all(
                    np.isclose(temp_cf[imm], original_instance[imm])
                    for imm in immutable_features
                )
                prox = effort_weights[feat] * abs(val - original_instance[feat]) / feature_ranges[feat]
                #pol_penalty = max(0, institutional_threshold - score_fn(temp_cf)) / institutional_threshold
                pol_penalty = max(0, institutional_threshold - compute_score(temp_cf, assessment_weights)) / institutional_threshold
                if within_bounds and unchanged_immutable and pol_penalty == 0:
                    obj_val = (
                        lambda_policy * pol_penalty +
                        lambda_feas * 0 +
                        lambda_prox * prox +
                        lambda_spar * (not np.isclose(val, original_instance[feat]))
                    )
                    valid_candidates.append((val, obj_val))
            if valid_candidates:
                suggested_val = sorted(valid_candidates, key=lambda x: x[1])[0][0]
                best_cf[feat] = suggested_val

    # Return a complete feature vector, not a sparse display of changes.
    # Refresh every metric after the optional feature replacements above.
    best_cf["predicted_score"] = compute_score(best_cf, assessment_weights)
    best_cf["predicted_result"] = int(best_cf["predicted_score"] >= institutional_threshold)
    best_cf["policy_penalty"] = policy_penalty(best_cf)
    best_cf["feasibility_penalty"], final_reasons = feasibility_penalty(best_cf)
    best_cf["proximity_distance"] = proximity_distance(best_cf)
    best_cf["sparsity"] = sparsity(best_cf)
    best_cf["objective_score"] = (
        lambda_policy * best_cf["policy_penalty"]
        + lambda_feas * best_cf["feasibility_penalty"]
        + lambda_prox * best_cf["proximity_distance"]
        + lambda_spar * best_cf["sparsity"]
    )
    best_cf["reason_log"] = "; ".join(final_reasons) if final_reasons else "OK"

    # Plot objective score distribution
    if plot_scores:
        plt.figure(figsize=(10, 5))
        plt.hist(cf_examples["objective_score"], bins=20, color='skyblue', edgecolor='black')
        plt.axvline(obj_scores[best_index], color='red', linestyle='--', label='Best CF')
        plt.title("Objective Score Distribution Across Counterfactuals")
        plt.xlabel("Objective Score")
        plt.ylabel("Number of Counterfactuals")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    # Get minimal unique nonzero suggestions for each actionable feature
    min_feature_suggestions = min_unique_nonzero_features(cf_examples, actionable_features, feature_bounds)

    # --- Add metrics for min_feature_suggestions as a DataFrame row ---
    min_suggestion_row = {}
    for feat in cf_examples.columns:
        if feat in min_feature_suggestions:
            min_suggestion_row[feat] = min_feature_suggestions[feat]
        elif feat in original_instance:
            min_suggestion_row[feat] = original_instance[feat]
        else:
            min_suggestion_row[feat] = np.nan

    # Compute metrics for the suggestion row
    min_suggestion_row = pd.Series(min_suggestion_row)
    # Policy penalty
    min_suggestion_row["policy_penalty"] = max(0, institutional_threshold - compute_score(min_suggestion_row, assessment_weights)) / institutional_threshold
    # Feasibility penalty
    feas_penalty, reasons = 0, []
    for feat in actionable_features:
        lb, ub = feature_bounds[feat]
        if not lb <= min_suggestion_row[feat] <= ub:
            feas_penalty += 1
            reasons.append(f"{feat} out of bounds")
    for feat in immutable_features:
        if not np.isclose(min_suggestion_row[feat], original_instance[feat]):
            feas_penalty += 1
            reasons.append(f"{feat} changed (immutable)")
    min_suggestion_row["feasibility_penalty"] = feas_penalty
    # Proximity distance
    min_suggestion_row["proximity_distance"] = sum([
        effort_weights[f] * abs(min_suggestion_row[f] - original_instance[f]) / feature_ranges[f]
        for f in actionable_features if f in min_suggestion_row
    ])
    # Sparsity
    min_suggestion_row["sparsity"] = sum([
        not np.isclose(min_suggestion_row[f], original_instance[f])
        for f in actionable_features if f in min_suggestion_row
    ])
    # Predicted score
    min_suggestion_row["predicted_score"] = compute_score(min_suggestion_row, assessment_weights)
    min_suggestion_row["predicted_result"] =  1 if min_suggestion_row["predicted_score"] >= institutional_threshold else 0

    # Objective score
    min_suggestion_row["objective_score"] = (
        lambda_policy * min_suggestion_row["policy_penalty"] +
        lambda_feas * min_suggestion_row["feasibility_penalty"] +
        lambda_prox * min_suggestion_row["proximity_distance"] +
        lambda_spar * min_suggestion_row["sparsity"]
    )
    # Cast the series to object dtype so we can safely store string logs without dtype warnings
    min_suggestion_row = min_suggestion_row.astype(object)
    min_suggestion_row["reason_log"] = "; ".join(reasons) if reasons else "OK"

    # Convert to DataFrame for display consistency
    min_feature_suggestions_df = pd.DataFrame([min_suggestion_row])

    return best_cf, cf_examples, min_feature_suggestions_df


def select_best_counterfactual_with_recommendations(
    original_instance: pd.Series,
    cf_examples: pd.DataFrame,
    institutional_threshold: float,
    actionable_features: list,
    immutable_features: list,
    assessment_weights: dict,
    feature_bounds: dict,
    effort_weights: dict,
    feature_ranges: dict,
    course_code,
    assignment_feature_map=None,
    providers=None,
    lambda_policy=1000,
    lambda_feas=1000,
    lambda_prox=1,
    lambda_spar=0.5,
    plot_scores=True,
    gate_predict=None,
    gate_feature_columns=None,
):
    best_cf, cf_examples_with_meta, min_feature_suggestions = select_best_counterfactual(
        original_instance=original_instance,
        cf_examples=cf_examples,
        institutional_threshold=institutional_threshold,
        actionable_features=actionable_features,
        immutable_features=immutable_features,
        assessment_weights=assessment_weights,
        feature_bounds=feature_bounds,
        effort_weights=effort_weights,
        feature_ranges=feature_ranges,
        lambda_policy=lambda_policy,
        lambda_feas=lambda_feas,
        lambda_prox=lambda_prox,
        lambda_spar=lambda_spar,
        plot_scores=plot_scores,
    )

    gate_audit = None
    if gate_predict is not None:
        from PresAnEx.counterfactual_gate import apply_hard_gate
        best_cf, gate_audit = apply_hard_gate(
            best_cf, original_instance, feature_columns=gate_feature_columns,
            actionable_features=actionable_features, feature_bounds=feature_bounds,
            assessment_weights=assessment_weights,
            institutional_threshold=institutional_threshold, predict=gate_predict,
        )
        # Auxiliary suggestions are not independently gated; never expose them
        # as accepted recommendations through the gated path.
        min_feature_suggestions = pd.DataFrame()
        if best_cf is None:
            return {"best_cf": None, "cf_examples": cf_examples_with_meta,
                    "min_feature_suggestions": min_feature_suggestions,
                    "gate_audit": gate_audit, "content_recommendations": {}}

    course = get_course_by_code(course_code)
    assignment_gap_analysis, content_recommendations = recommend_learning_materials_from_gaps(
        original_instance=original_instance,
        best_cf=best_cf,
        course_code=course_code,
        assignment_feature_map=assignment_feature_map,
        providers=providers,
    )

    return {
        "gate_audit": gate_audit,
        "best_cf": best_cf,
        "cf_examples": cf_examples_with_meta,
        "min_feature_suggestions": min_feature_suggestions,
        "course_context": {
            "course_code": course["course_code"],
            "course_title": course["course_title"],
            "institution": course.get("institution"),
            "overview": course.get("overview"),
            "outcomes": list(course.get("outcomes", [])),
            "objectives": list(course.get("objectives", [])),
            "recommendation_category": course.get("recommendation_category"),
            "recommendation_sub_category": course.get("recommendation_sub_category"),
        },
        "assignment_gap_analysis": assignment_gap_analysis,
        "content_recommendations": content_recommendations,
    }

def min_unique_nonzero_features(cf_examples: pd.DataFrame, actionable_features: list, feature_bounds: dict):
    """
    For each actionable feature, select the minimum unique non-zero value across all counterfactuals,
    clipped to the feature's permitted bounds.
    Returns a dict {feature: min_nonzero_value_within_bounds}
    """
    suggestions = {}
    for feat in actionable_features:
        vals = np.unique(cf_examples[feat].values)
        nonzero_vals = [v for v in vals if not np.isclose(v, 0)]
        if len(vals) == 1:
            # Only one unique value (could be zero or nonzero)
            min_val = vals[0]
        elif nonzero_vals:
            min_val = np.min(nonzero_vals)
        else:
            min_val = 0
        # Apply feature bounds
        lb, ub = feature_bounds[feat]
        min_val = np.clip(min_val, lb, ub)
        suggestions[feat] = min_val
    return suggestions


def analyze_diverse_counterfactuals(
    diverse_cfs: pd.DataFrame,
    original_instance: pd.Series,
    actionable_features: list,
    metric_columns: list = None,
    plot=True
):
    """
    Analyze and visualize the generated diverse counterfactuals.
    
    Parameters:
        diverse_cfs (pd.DataFrame): DataFrame of diverse counterfactuals with metrics.
        original_instance (pd.Series): Original instance.
        actionable_features (list): List of actionable features.
        metric_columns (list): Columns to analyze (default: all metric columns).
        plot (bool): Whether to plot the analysis.
    
    Returns:
        dict: Analysis summary including diversity metrics.
    """
    if metric_columns is None:
        metric_columns = ['predicted_score', 'proximity_distance', 'sparsity', 'objective_score']
    
    available_metrics = [m for m in metric_columns if m in diverse_cfs.columns]
    
    analysis = {
        'num_cfs_generated': len(diverse_cfs),
        'num_policy_valid': diverse_cfs['policy_valid'].sum() if 'policy_valid' in diverse_cfs.columns else 0,
        'num_feasible': diverse_cfs['feasible'].sum() if 'feasible' in diverse_cfs.columns else 0,
    }
    
    # Compute metrics statistics
    for metric in available_metrics:
        analysis[f'{metric}_mean'] = diverse_cfs[metric].mean()
        analysis[f'{metric}_std'] = diverse_cfs[metric].std()
        analysis[f'{metric}_min'] = diverse_cfs[metric].min()
        analysis[f'{metric}_max'] = diverse_cfs[metric].max()
    
    # Feature usage analysis
    feature_changes = {}
    for feat in actionable_features:
        if feat in diverse_cfs.columns:
            num_changed = sum(~np.isclose(diverse_cfs[feat], original_instance[feat]))
            avg_change = (diverse_cfs[feat] - original_instance[feat]).abs().mean()
            feature_changes[feat] = {
                'num_changed': num_changed,
                'avg_change': avg_change,
                'max_change': (diverse_cfs[feat] - original_instance[feat]).abs().max()
            }
    analysis['feature_changes'] = feature_changes
    
    # Plotting
    if plot and len(available_metrics) > 0:
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Diverse Policy-Aware Counterfactuals Analysis', fontsize=16)
        
        for idx, metric in enumerate(available_metrics[:4]):
            ax = axes[idx // 2, idx % 2]
            ax.hist(diverse_cfs[metric], bins=15, color='steelblue', edgecolor='black', alpha=0.7)
            ax.set_xlabel(metric)
            ax.set_ylabel('Frequency')
            ax.set_title(f'Distribution of {metric}')
            ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    return analysis
