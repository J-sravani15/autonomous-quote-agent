def route_decision(probability, risk_level):
    """
    Decide what action to take for the insurance quote.
    """

    if probability > 0.7 and risk_level == "LOW":
        return "AUTO APPROVE"

    elif probability > 0.4:
        return "AGENT FOLLOW-UP"

    else:
        return "ESCALATE TO UNDERWRITER"