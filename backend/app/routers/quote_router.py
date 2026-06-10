from fastapi import APIRouter
from app.schemas.quote_schema import QuoteInput

from app.services.risk_agent import calculate_risk
from app.services.premium_agent import calculate_premium
from app.services.conversion_agent import predict_conversion
from app.services.decision_agent import final_decision

router = APIRouter()

@router.post("/generate-quote")
def generate_quote(data: QuoteInput):

    risk = calculate_risk(data.accidents)

    premium = calculate_premium(risk)

    conversion = predict_conversion(premium)

    decision = final_decision(risk)

    return {
        "risk": risk,
        "premium": premium,
        "conversion_probability": conversion,
        "decision": decision
    }