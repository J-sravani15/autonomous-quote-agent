"""
Decision Router Service - Routes quotes to appropriate actions.
"""
# Demo threshold chosen because trained conversion model
# produces probabilities mostly in the 0.28–0.43 range.
# Allows demonstration of AUTO APPROVE workflow.


def route_decision(
    probability: float, risk_level: str, recommended_premium: float
) -> str:
    """
    Decide what action to take for the insurance quote.
    """

    if probability > 0.42 and risk_level == "LOW" and recommended_premium < 50000:
        return "AUTO APPROVE"
    elif probability > 0.40 and risk_level != "HIGH":
        return "AGENT FOLLOW-UP"
    else:
        return "ESCALATE TO UNDERWRITER"
