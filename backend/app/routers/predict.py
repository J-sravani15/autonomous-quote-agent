"""
Prediction Router - Main API endpoints for insurance quote analysis.

This router orchestrates the multi-agent pipeline:
1. Risk Profiler - Analyzes driver/vehicle risk
2. Conversion Predictor - ML-based probability estimation  
3. Premium Advisor - Adjusts premiums based on risk/probability
4. Decision Router - Determines action (auto-approve/follow-up/escalate)
5. Decision Analysis - NEW: Comprehensive analysis and reasoning layer

All endpoints integrate with the decision analysis layer for explainability.
"""

from fastapi import APIRouter, HTTPException
from schemas.predict_schema import QuoteInput, ExplainInput
from schemas.decision_schema import PredictionResponse

from services.risk_profiler import calculate_risk
from services.predict_service import predict_conversion
from services.premium_advisor import adjust_premium
from services.decision_router import route_decision
from services.decision_analysis import analyze_decision
from services.ollama_service import explain_decision

import time
import sys
from typing import Optional
from loguru import logger

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
def predict(data: QuoteInput) -> PredictionResponse:
    """
    Main prediction endpoint - Analyzes insurance quotes through multi-agent pipeline.
    
    Pipeline flow:
    1. Risk Profiler: Calculate risk score from driver/vehicle history
    2. Conversion Predictor: ML model predicts conversion probability
    3. Premium Advisor: Adjusts premium based on risk and probability
    4. Decision Router: Determines action (auto-approve/follow-up/escalate)
    5. Decision Analysis: Generates reasoning, confidence, and recommendations
    
    Args:
        data: QuoteInput with driver and vehicle information
        
    Returns:
        PredictionResponse with complete analysis and decision reasoning
        
    Raises:
        HTTPException: If prediction fails or data validation errors
    """
    
    start_time = time.time()
    
    try:
        logger.info(f"Processing quote for driver age {data.Driver_Age}")
        
        # Agent 1: Risk Profiler
        risk_level = calculate_risk(data)
        logger.info(f"Risk Level: {risk_level}")

        # Agent 2: Conversion Predictor (ML)
        prediction, probability = predict_conversion(data.dict())
        logger.info(f"Conversion Probability: {probability:.2f}")

        # Agent 3: Premium Advisor
        recommended_premium = adjust_premium(
            data.Quoted_Premium, probability, risk_level
        )
        logger.info(f"Recommended Premium: {recommended_premium}")

        # Agent 4: Decision Router
        decision = route_decision(probability, risk_level)
        logger.info(f"Decision: {decision}")

        # Agent 5: Decision Analysis (NEW) - Enriches decision with reasoning
        analysis = analyze_decision(
            risk_level=risk_level,
            prediction=prediction,
            conversion_probability=probability,
            recommended_premium=recommended_premium,
            decision=decision,
            quoted_premium=data.Quoted_Premium,
            prev_accidents=data.Prev_Accidents,
            prev_citations=data.Prev_Citations,
            annual_miles=data.Annual_Miles_Range,
            vehicle_cost=data.Vehicl_Cost_Range,
        )
        logger.info(f"Analysis confidence: {analysis.confidence_score}")

        # Calculate processing time
        processing_time_ms = round((time.time() - start_time) * 1000, 2)
        logger.info(f"Processing completed in {processing_time_ms}ms")

        # Build unified response
        response = PredictionResponse(
            risk_level=risk_level,
            prediction=int(prediction),
            conversion_probability=float(probability),
            recommended_premium=recommended_premium,
            decision=decision,
            analysis=analysis,
            processing_time_ms=processing_time_ms,
        )

        return response

    except Exception as e:
        # Log the error and return 500
        logger.error(f"ERROR in /predict endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@router.post("/explain")
def explain(data: ExplainInput):
    """
    Explanation endpoint - Generates AI-powered explanation for decisions.
    
    Uses Ollama LLM to generate natural language explanation based on
    all prediction pipeline outputs and analysis results.
    
    Args:
        data: ExplainInput with full prediction context
        
    Returns:
        Dict with 'explanation' field containing natural language explanation
    """
    import sys
    sys.stderr.write("\n" + "=" * 80 + "\n")
    sys.stderr.write("[ENDPOINT] POST /explain - REQUEST RECEIVED\n")
    sys.stderr.write("=" * 80 + "\n")
    sys.stderr.write(f"[INPUT] ExplainInput received with risk_level={data.risk_level}, decision={data.decision}\n")
    
    try:
        sys.stderr.write("[STEP 1] Converting ExplainInput to dict...\n")
        payload = data.dict()
        sys.stderr.write(f"  OK Payload size: {len(payload)} fields\n")
        
        sys.stderr.write("[STEP 2] Calling explain_decision()...\n")
        explanation = explain_decision(payload)
        
        sys.stderr.write(f"[STEP 3] Got response with {len(explanation)} characters\n")
        
        response_data = {"explanation": explanation}
        sys.stderr.write("[SUCCESS] Returning explanation\n")
        sys.stderr.write("=" * 80 + "\n")
        logger.info("Explanation generated successfully")
        return response_data
        
    except Exception as e:
        sys.stderr.write(f"\n[ERROR] Exception: {type(e).__name__}: {str(e)}\n")
        import traceback
        traceback.print_exc(file=sys.stderr)
        
        error_response = {"explanation": f"Error: Could not generate explanation - {str(e)}"}
        sys.stderr.write("[RESPONSE] Returning error\n")
        sys.stderr.write("=" * 80 + "\n")
        
        logger.error(f"Error generating explanation: {str(e)}", exc_info=True)
        return error_response
