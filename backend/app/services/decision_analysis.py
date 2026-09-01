"""
Decision Analysis Service - Comprehensive analysis layer for insurance quote decisions.

This service provides detailed reasoning, confidence scoring, and recommendations
for every insurance quote decision. It sits between the Decision Router and API response,
enriching the decision with explainability and structured analysis.

Design principles:
- Analyze all agent outputs holistically
- Generate high-confidence, business-friendly reasoning
- Detect edge cases and anomalies
- Suggest alternatives for risky decisions
- Track confidence levels explicitly
"""

from schemas.decision_schema import (
    DecisionAnalysis,
    DecisionEnum,
    RiskLevelEnum,
    ConfidenceLevel,
)
from typing import List, Tuple


def _calculate_confidence_score(
    probability: float,
    risk_level: RiskLevelEnum,
    decision_aligned: bool = True,
) -> float:
    """
    Calculate confidence score for the decision.
    
    Confidence factors:
    - ML probability: 40% weight (how sure the model is)
    - Risk alignment: 40% weight (how well decision aligns with risk)
    - Decision consistency: 20% weight (internal coherence)
    
    Args:
        probability: Conversion probability from ML model
        risk_level: Risk level classification
        decision_aligned: Whether decision aligns with risk/probability
        
    Returns:
        Confidence score between 0.0 and 1.0
    """
    
    # ML probability confidence (normalized)
    if probability > 0.8 or probability < 0.2:
        prob_confidence = 0.9  # High certainty at extremes
    elif probability > 0.6 or probability < 0.4:
        prob_confidence = 0.7  # Medium certainty in outer ranges
    else:
        prob_confidence = 0.5  # Lower certainty near 0.5 (indecisive)
    
    # Risk-probability alignment confidence
    if risk_level == RiskLevelEnum.LOW and probability > 0.6:
        alignment_confidence = 0.95  # Very well aligned
    elif risk_level == RiskLevelEnum.HIGH and probability < 0.4:
        alignment_confidence = 0.95  # Very well aligned
    elif risk_level == RiskLevelEnum.MEDIUM and 0.4 <= probability <= 0.7:
        alignment_confidence = 0.85  # Well aligned
    else:
        alignment_confidence = 0.65  # Misalignment reduces confidence
    
    # Decision consistency
    consistency_confidence = 0.9 if decision_aligned else 0.6
    
    # Weighted average
    final_score = (
        (prob_confidence * 0.4)
        + (alignment_confidence * 0.4)
        + (consistency_confidence * 0.2)
    )
    
    return round(final_score, 3)


def _confidence_to_level(score: float) -> ConfidenceLevel:
    """Convert numeric confidence score to categorical level."""
    if score >= 0.85:
        return ConfidenceLevel.VERY_HIGH
    elif score >= 0.70:
        return ConfidenceLevel.HIGH
    elif score >= 0.55:
        return ConfidenceLevel.MEDIUM
    elif score >= 0.40:
        return ConfidenceLevel.LOW
    else:
        return ConfidenceLevel.VERY_LOW


def _identify_risk_factors(
    prev_accidents: int,
    prev_citations: int,
    annual_miles: int,
    vehicle_cost: int,
) -> List[str]:
    """
    Identify and list specific risk factors from quote data.
    
    Args:
        prev_accidents: Number of previous accidents
        prev_citations: Number of previous citations
        annual_miles: Annual miles range
        vehicle_cost: Vehicle cost range
        
    Returns:
        List of identified risk factors as strings
    """
    factors: List[str] = []
    
    if prev_accidents > 0:
        factors.append(f"Previous accidents: {prev_accidents}")
    
    if prev_citations > 0:
        factors.append(f"Previous citations: {prev_citations}")
    
    if annual_miles > 15000:  # Assuming range, adjust threshold as needed
        factors.append("High annual mileage exposure")
    
    if vehicle_cost > 30000:  # High-value vehicle
        factors.append("High-value vehicle")
    
    return factors


def _generate_reasoning(
    risk_level: RiskLevelEnum,
    probability: float,
    decision: DecisionEnum,
    risk_factors: List[str],
    quoted_premium: float,
    recommended_premium: float,
) -> str:
    """
    Generate business-friendly reasoning for the decision.
    
    Args:
        risk_level: Risk classification
        probability: Conversion probability
        decision: Final decision made
        risk_factors: Identified risk factors
        quoted_premium: Premium quoted
        recommended_premium: Premium recommended
        
    Returns:
        Formatted reasoning string
    """
    
    # Start with risk assessment
    reasoning_parts = [
        f"Risk Assessment: Customer classified as {risk_level.value} risk."
    ]
    
    if risk_factors:
        reasoning_parts.append(
            f"Key factors: {', '.join(risk_factors)}."
        )
    
    # Add conversion insight
    prob_insight = ""
    if probability > 0.7:
        prob_insight = "ML model indicates high conversion likelihood"
    elif probability > 0.4:
        prob_insight = "ML model shows moderate conversion potential"
    else:
        prob_insight = "ML model predicts low conversion likelihood"
    
    reasoning_parts.append(f"Conversion Analysis: {prob_insight}.")
    
    # Premium adjustment
    if abs(recommended_premium - quoted_premium) > 0.01:
        percent_change = round(
            ((recommended_premium - quoted_premium) / quoted_premium) * 100, 1
        )
        if percent_change > 0:
            reasoning_parts.append(
                f"Premium adjusted +{percent_change}% due to risk profile."
            )
        else:
            reasoning_parts.append(
                f"Premium adjusted {percent_change}% to improve competitiveness."
            )
    
    # Final decision justification
    if decision == DecisionEnum.AUTO_APPROVE:
        reasoning_parts.append(
            "Decision: Auto-approve due to low risk and high conversion probability."
        )
    elif decision == DecisionEnum.AGENT_FOLLOW_UP:
        reasoning_parts.append(
            "Decision: Agent follow-up recommended for review and personalization."
        )
    else:  # ESCALATE
        reasoning_parts.append(
            "Decision: Escalate to underwriter for specialized review."
        )
    
    return " ".join(reasoning_parts)


def _generate_recommended_action(
    decision: DecisionEnum,
    risk_level: RiskLevelEnum,
    probability: float,
    confidence_score: float,
) -> str:
    """
    Generate specific, actionable next steps.
    
    Args:
        decision: Final decision
        risk_level: Risk level
        probability: Conversion probability
        confidence_score: Confidence in the decision
        
    Returns:
        Formatted action string
    """
    
    actions = {
        DecisionEnum.AUTO_APPROVE: (
            "Issue quote immediately. Monitor for policy activation within 24 hours."
        ),
        DecisionEnum.AGENT_FOLLOW_UP: (
            f"Agent should contact within 24 hours. Emphasize competitive premium positioning. "
            f"Highlight {' and '.join(['low risk profile' if risk_level == RiskLevelEnum.LOW else 'detailed coverage']) if risk_level else 'coverage options'}."
        ),
        DecisionEnum.ESCALATE_TO_UNDERWRITER: (
            f"Route to underwriting queue for review. Flag as {'high-risk case' if risk_level == RiskLevelEnum.HIGH else 'complex case'} requiring specialist assessment."
        ),
    }
    
    base_action = actions.get(
        decision,
        "Review quote status and determine next steps."
    )
    
    # Add confidence caveat if low
    if confidence_score < 0.6:
        base_action += (
            " ⚠️ Low confidence in this decision - manual review recommended."
        )
    
    return base_action


def _check_override_conditions(
    risk_level: RiskLevelEnum,
    probability: float,
    decision: DecisionEnum,
    prev_accidents: int,
    prev_citations: int,
) -> Tuple[bool, str]:
    """
    Check if any override rules should trigger.
    
    Override rules:
    - Escalate if high-risk + multiple incidents
    - Downgrade escalation if probability is extremely high
    - Special handling for edge cases
    
    Args:
        risk_level: Risk classification
        probability: Conversion probability
        decision: Current decision
        prev_accidents: Number of accidents
        prev_citations: Number of citations
        
    Returns:
        Tuple of (override_triggered, reason)
    """
    
    # Override 1: Multiple incidents in high-risk category should escalate
    if risk_level == RiskLevelEnum.HIGH and (prev_accidents + prev_citations) > 5:
        if decision != DecisionEnum.ESCALATE_TO_UNDERWRITER:
            return True, "Multiple incidents require mandatory underwriter review"
    
    # Override 2: Extremely high probability can override escalation
    if probability > 0.95 and decision == DecisionEnum.ESCALATE_TO_UNDERWRITER:
        return True, "Exceptionally high conversion probability warrants reconsideration"
    
    # Override 3: Very low probability auto-approvals should be escalated
    if probability < 0.3 and decision == DecisionEnum.AUTO_APPROVE:
        return True, "Low conversion probability contradicts auto-approval"
    
    return False, ""


def analyze_decision(
    risk_level: str,
    prediction: int,
    conversion_probability: float,
    recommended_premium: float,
    decision: str,
    quoted_premium: float,
    prev_accidents: int = 0,
    prev_citations: int = 0,
    annual_miles: int = 10000,
    vehicle_cost: int = 25000,
) -> DecisionAnalysis:
    """
    Analyze a quote decision and generate comprehensive reasoning.
    
    This is the main entry point for the decision analysis service.
    It takes all inputs from the prediction pipeline and produces
    a detailed analysis object suitable for business users and logs.
    
    Args:
        risk_level: Risk level from risk profiler ("LOW", "MEDIUM", "HIGH")
        prediction: Binary prediction from ML model (0 or 1)
        conversion_probability: Probability from ML model (0.0-1.0)
        recommended_premium: Premium recommended by advisor
        decision: Decision from router ("AUTO APPROVE", "AGENT FOLLOW-UP", "ESCALATE TO UNDERWRITER")
        quoted_premium: Original quoted premium
        prev_accidents: Number of previous accidents
        prev_citations: Number of previous citations
        annual_miles: Annual miles range value
        vehicle_cost: Vehicle cost range value
        
    Returns:
        DecisionAnalysis object with structured decision reasoning
    """
    
    # Convert string enums to typed enums
    risk_enum = RiskLevelEnum(risk_level)
    decision_enum = DecisionEnum(decision)
    
    # Identify risk factors
    risk_factors = _identify_risk_factors(
        prev_accidents, prev_citations, annual_miles, vehicle_cost
    )
    
    # Calculate confidence
    decision_aligned = (
        (risk_enum == RiskLevelEnum.LOW and conversion_probability > 0.6)
        or (risk_enum == RiskLevelEnum.HIGH and conversion_probability < 0.4)
        or (risk_enum == RiskLevelEnum.MEDIUM and 0.4 <= conversion_probability <= 0.7)
    )
    
    confidence_score = _calculate_confidence_score(
        conversion_probability, risk_enum, decision_aligned
    )
    confidence_level = _confidence_to_level(confidence_score)
    
    # Generate reasoning
    reasoning = _generate_reasoning(
        risk_enum,
        conversion_probability,
        decision_enum,
        risk_factors,
        quoted_premium,
        recommended_premium,
    )
    
    # Generate recommended action
    recommended_action = _generate_recommended_action(
        decision_enum, risk_enum, conversion_probability, confidence_score
    )
    
    # Premium adjustment reason
    percent_change = round(
        ((recommended_premium - quoted_premium) / quoted_premium) * 100, 1
    )
    if abs(percent_change) < 0.5:
        premium_adjustment_reason = "Premium held stable based on risk profile"
    elif percent_change > 0:
        premium_adjustment_reason = f"Premium increased {abs(percent_change)}% due to risk factors"
    else:
        premium_adjustment_reason = f"Premium reduced {abs(percent_change)}% to enhance competitiveness"
    
    # Check override conditions
    override_triggered, override_reason = _check_override_conditions(
        risk_enum,
        conversion_probability,
        decision_enum,
        prev_accidents,
        prev_citations,
    )
    
    alternative_decision = None
    if override_triggered and override_reason:
        # Suggest alternative if override needed
        if decision_enum != DecisionEnum.ESCALATE_TO_UNDERWRITER:
            alternative_decision = DecisionEnum.ESCALATE_TO_UNDERWRITER
    
    # Build final analysis
    analysis = DecisionAnalysis(
        decision=decision_enum,
        risk_level=risk_enum,
        confidence_score=confidence_score,
        confidence_level=confidence_level,
        reasoning=reasoning,
        recommended_action=recommended_action,
        conversion_probability=conversion_probability,
        risk_factors=risk_factors,
        premium_adjustment_reason=premium_adjustment_reason,
        alternative_decision=alternative_decision,
        override_triggered=override_triggered,
        override_reason=override_reason if override_triggered else None,
    )
    
    return analysis
