"""
Decision Analysis Schema - Response models for decision analysis layer.

This module defines the response schemas for the decision analysis layer,
providing structured, typed responses with reasoning and recommendations.
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class RiskLevelEnum(str, Enum):
    """Risk classification levels."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class DecisionEnum(str, Enum):
    """Possible decisions from the decision router."""
    AUTO_APPROVE = "AUTO APPROVE"
    AGENT_FOLLOW_UP = "AGENT FOLLOW-UP"
    ESCALATE_TO_UNDERWRITER = "ESCALATE TO UNDERWRITER"


class ConfidenceLevel(str, Enum):
    """Confidence level classifications."""
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    VERY_HIGH = "VERY_HIGH"


class DecisionAnalysis(BaseModel):
    """
    Decision Analysis Result - Comprehensive analysis of the quote decision.
    
    Provides structured reasoning, confidence metrics, and actionable recommendations.
    """
    
    decision: DecisionEnum = Field(
        ...,
        description="The recommended action for this quote"
    )
    
    risk_level: RiskLevelEnum = Field(
        ...,
        description="Risk classification of the driver/vehicle"
    )
    
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in the decision (0.0-1.0)"
    )
    
    confidence_level: ConfidenceLevel = Field(
        ...,
        description="Categorical confidence level"
    )
    
    reasoning: str = Field(
        ...,
        description="Detailed explanation of why this decision was made"
    )
    
    recommended_action: str = Field(
        ...,
        description="Specific next steps to take based on this decision"
    )
    
    conversion_probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="ML model's estimated probability of conversion"
    )
    
    risk_factors: List[str] = Field(
        default_factory=list,
        description="Key risk factors identified"
    )
    
    premium_adjustment_reason: str = Field(
        ...,
        description="Explanation for premium adjustment decision"
    )
    
    alternative_decision: Optional[DecisionEnum] = Field(
        default=None,
        description="Alternative decision if primary fails"
    )
    
    override_triggered: bool = Field(
        default=False,
        description="Whether any override rules were triggered"
    )
    
    override_reason: Optional[str] = Field(
        default=None,
        description="Reason for override if triggered"
    )


class PredictionResponse(BaseModel):
    """
    Complete Prediction Response - Combines all agent outputs and decision analysis.
    
    This is the unified response format for the /predict endpoint.
    """
    
    # Original agent outputs
    risk_level: RiskLevelEnum = Field(
        ...,
        description="Risk classification from Risk Profiler agent"
    )
    
    prediction: int = Field(
        ...,
        ge=0,
        le=1,
        description="Binary prediction from ML model (0 or 1)"
    )
    
    conversion_probability: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Probability of conversion from ML model"
    )
    
    recommended_premium: float = Field(
        ...,
        ge=0.0,
        description="Premium recommended by Premium Advisor agent"
    )
    
    decision: DecisionEnum = Field(
        ...,
        description="Action decided by Decision Router agent"
    )
    
    # New decision analysis layer
    analysis: DecisionAnalysis = Field(
        ...,
        description="Comprehensive decision analysis with reasoning"
    )
    
    # Metadata
    processing_time_ms: Optional[float] = Field(
        default=None,
        description="Processing time in milliseconds"
    )
    
    model_version: str = Field(
        default="1.0",
        description="Version of the prediction model"
    )


class ExplainInputExtended(BaseModel):
    """Extended input for explanation endpoint including decision analysis."""
    
    driver_age: int
    driving_exp: int
    prev_accidents: int
    prev_citations: int
    coverage: int
    veh_usage: int
    annual_miles_range: int
    vehicl_cost_range: int
    sal_range: int
    quoted_premium: float
    risk_level: RiskLevelEnum
    prediction: int
    conversion_probability: float
    recommended_premium: float
    decision: DecisionEnum
    analysis: Optional[DecisionAnalysis] = None
