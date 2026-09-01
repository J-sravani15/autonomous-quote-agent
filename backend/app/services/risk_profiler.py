"""
Risk Profiler Service - Analyzes driver and vehicle risk factors.

This service assigns risk levels based on driver history and vehicle information.
Used by the multi-agent pipeline to inform premium adjustments and routing decisions.

Risk Scoring:
- Accidents weighted heavily (×3) as they indicate actual incidents
- Citations weighted moderately (×2) as they indicate behavior patterns
- Risk bands: LOW (<3), MEDIUM (3-6), HIGH (≥6)
"""


def calculate_risk(data) -> str:
    """
    Calculate risk level from driver/vehicle data.
    
    Uses a simple scoring algorithm:
    - 3 points per previous accident
    - 2 points per previous citation
    
    Risk levels:
    - LOW: score < 3 (excellent history)
    - MEDIUM: 3 <= score < 6 (moderate history)
    - HIGH: score >= 6 (significant history)
    
    Args:
        data: QuoteInput object with driver history
        
    Returns:
        Risk level string: "LOW", "MEDIUM", or "HIGH"
    """

    score = data.Prev_Accidents * 3 + data.Prev_Citations * 2

    if score < 3:
        return "LOW"
    elif score < 6:
        return "MEDIUM"
    else:
        return "HIGH"