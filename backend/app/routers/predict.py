from fastapi import APIRouter
from app.schemas.predict_schema import QuoteInput

from app.services.risk_profiler import calculate_risk
from app.services.predict_service import predict_conversion
from app.services.premium_advisor import adjust_premium
from app.services.decision_router import route_decision

router = APIRouter()

@router.post("/predict")
def predict(data: QuoteInput):

    # Agent 1: Risk Profiler
    risk_level = calculate_risk(data)

    # Agent 2: Conversion Predictor (ML)
    prediction, probability = predict_conversion(data.dict())

    # Agent 3: Premium Advisor
    recommended_premium = adjust_premium(
        data.Quoted_Premium,
        probability,
        risk_level
    )

    # Agent 4: Decision Router
    decision = route_decision(
        probability,
        risk_level
    )

    return {
        "risk_level": risk_level,
        "prediction": int(prediction),
        "conversion_probability": float(probability),
        "recommended_premium": recommended_premium,
        "decision": decision
    }