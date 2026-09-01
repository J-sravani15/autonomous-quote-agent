<<<<<<< HEAD
def route_decision(probability, risk_level, recommended_premium):
    """
    Final decision based on outputs of previous agents.
=======
"""
Decision Router Service - Routes quotes to appropriate actions.

Makes the final routing decision based on conversion probability and risk level.
Determines whether a quote should be:
- AUTO APPROVE: Automatically issued (high probability, low risk)
- AGENT FOLLOW-UP: Requires agent contact for review
- ESCALATE TO UNDERWRITER: Complex case requiring specialist review

This service implements the core business logic for automatic decision-making.
"""


def route_decision(probability: float, risk_level: str) -> str:
    """
    Decide what action to take for the insurance quote.
    
    Decision rules (applied in order):
    1. probability > 0.7 AND risk_level == "LOW" → AUTO APPROVE
    2. probability > 0.4 → AGENT FOLLOW-UP
    3. Otherwise → ESCALATE TO UNDERWRITER
    
    Args:
        probability: Conversion probability from ML model (0.0-1.0)
        risk_level: Risk classification ("LOW", "MEDIUM", "HIGH")
        
    Returns:
        Decision string: "AUTO APPROVE", "AGENT FOLLOW-UP", or "ESCALATE TO UNDERWRITER"
        
    Examples:
        >>> route_decision(0.8, "LOW")
        'AUTO APPROVE'
        >>> route_decision(0.6, "MEDIUM")
        'AGENT FOLLOW-UP'
        >>> route_decision(0.3, "HIGH")
        'ESCALATE TO UNDERWRITER'
>>>>>>> fb7fc542cf06a6e1c388ce1b21c7662a88659a8e
    """

    if probability > 0.70 and risk_level == "LOW" and recommended_premium < 50000:
        return "AUTO APPROVE"

    elif probability > 0.40 and risk_level != "HIGH":
        return "AGENT FOLLOW-UP"

    else:
        return "ESCALATE TO UNDERWRITER"
