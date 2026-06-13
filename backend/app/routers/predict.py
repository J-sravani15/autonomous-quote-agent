from fastapi import APIRouter
from app.schemas.predict_schema import QuoteInput, ExplainInput

from app.services.risk_profiler import calculate_risk
from app.services.predict_service import predict_conversion
from app.services.premium_advisor import adjust_premium
from app.services.decision_router import route_decision
from app.services.ollama_service import explain_decision

router = APIRouter()


@router.post("/predict")
def predict(data: QuoteInput):

    # Agent 1: Risk Profiler
    risk_level = calculate_risk(data)

    # Agent 2: Conversion Predictor (ML)
    prediction, probability = predict_conversion(data.dict())

    # TRUE AGENT CHAINING
    # Agent 2 now depends on Agent 1 output
    if risk_level == "HIGH":
        probability *= 0.85
    elif risk_level == "MEDIUM":
        probability *= 0.95

    probability = round(probability, 4)

    # Agent 3: Premium Advisor
    # Depends on Agent 1 + Agent 2
    recommended_premium = adjust_premium(data.Quoted_Premium, probability, risk_level)

    # Agent 4: Decision Router
    # Depends on Agent 1 + Agent 2 + Agent 3
    decision = route_decision(probability, risk_level, recommended_premium)

    return {
        "risk_level": risk_level,
        "prediction": int(prediction),
        "conversion_probability": float(probability),
        "recommended_premium": recommended_premium,
        "decision": decision,
    }


@router.post("/explain")
def explain(data: ExplainInput):
    payload = data.dict()
    return {"explanation": explain_decision(payload)}
