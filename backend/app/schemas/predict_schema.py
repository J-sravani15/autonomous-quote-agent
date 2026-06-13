from pydantic import BaseModel, Field
from typing import Optional


class QuoteInput(BaseModel):
    """
    Insurance Quote Input Schema - Request model for prediction endpoint.
    
    Contains all driver, vehicle, and quote information needed for
    the multi-agent analysis pipeline.
    """
    Driver_Age: int = Field(..., ge=16, le=100, description="Driver age in years")
    Driving_Exp: int = Field(..., ge=0, le=70, description="Years of driving experience")
    Prev_Accidents: int = Field(..., ge=0, description="Number of previous accidents")
    Prev_Citations: int = Field(..., ge=0, description="Number of previous citations")
    Coverage: int = Field(..., ge=1, description="Coverage level selected")
    Veh_Usage: int = Field(..., ge=1, description="Vehicle usage category")
    Annual_Miles_Range: int = Field(..., ge=0, description="Annual miles range value")
    Vehicl_Cost_Range: int = Field(..., ge=0, description="Vehicle cost range value")
    Sal_Range: int = Field(..., ge=0, description="Salary range value")
    Quoted_Premium: float = Field(..., ge=0, description="Originally quoted premium")


class ExplainInput(QuoteInput):
    """
    Extended Input for Explanation Endpoint.
    
    Combines quote input with prediction outputs for explanation generation.
    """
    risk_level: str = Field(..., description="Risk level from analysis")
    prediction: int = Field(..., ge=0, le=1, description="Binary prediction")
    conversion_probability: float = Field(..., ge=0, le=1, description="Conversion probability")
    recommended_premium: float = Field(..., ge=0, description="Recommended premium")
    decision: str = Field(..., description="Final decision")
