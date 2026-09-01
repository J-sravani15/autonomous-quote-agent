"""
Premium Advisor Service - Recommends premium adjustments.

Adjusts quoted premiums based on:
- Conversion probability (lower probability → discount to attract)
- Risk level (higher risk → premium increase)

This service implements business rules for competitive pricing
while maintaining risk-adjusted profitability.
"""


def adjust_premium(quoted_premium: float, probability: float, risk_level: str) -> float:
    """
    Adjust premium based on conversion probability and risk.
    
    Premium adjustment rules:
    1. Low probability (<0.4): 10% discount to improve competitiveness
    2. High probability (>0.7): 5% increase as customer is likely to convert
    3. High risk: 10% increase to account for risk profile
    
    The adjustments are applied in sequence, allowing for multiplicative effects.
    
    Args:
        quoted_premium: Original quoted premium (float, >= 0)
        probability: ML model's conversion probability (float, 0.0-1.0)
        risk_level: Risk classification from risk profiler ("LOW", "MEDIUM", "HIGH")
        
    Returns:
        Adjusted premium (float, rounded to 2 decimal places)
        
    Example:
        >>> adjust_premium(1000, 0.35, "HIGH")
        990.0  # 10% discount (low prob) + 10% increase (high risk) = net -1%
    """

    premium = quoted_premium

    # Rule 1: Conversion probability adjustment
    if probability < 0.4:
        premium = premium * 0.9  # 10% discount for low-probability quotes
    elif probability > 0.7:
        premium = premium * 1.05  # 5% increase for high-probability quotes

    # Rule 2: Risk-based adjustment
    if risk_level == "HIGH":
        premium = premium * 1.1  # 10% increase for high-risk profiles

    return round(premium, 2)