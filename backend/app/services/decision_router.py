def route_decision(probability, risk_level, recommended_premium):
    """
    Final decision based on outputs of previous agents.
    """

    if probability > 0.70 and risk_level == "LOW" and recommended_premium < 50000:
        return "AUTO APPROVE"

    elif probability > 0.40 and risk_level != "HIGH":
        return "AGENT FOLLOW-UP"

    else:
        return "ESCALATE TO UNDERWRITER"
