def adjust_premium(quoted_premium, probability, risk_level):
    """
    Adjust premium based on conversion probability and risk.
    """

    premium = quoted_premium

    # If probability is low → reduce premium to attract customer
    if probability < 0.4:
        premium = premium * 0.9

    # If probability is very high → increase premium slightly
    elif probability > 0.7:
        premium = premium * 1.05

    # If risk is high → increase premium
    if risk_level == "HIGH":
        premium = premium * 1.1

    return round(premium, 2)