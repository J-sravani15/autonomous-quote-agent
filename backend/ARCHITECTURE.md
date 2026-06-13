# Autonomous Quote Agent - Architecture Documentation

## Overview

The Autonomous Quote Agent is a multi-agent AI system that automates insurance quote analysis and decision-making. Version 2.0 introduces the Decision Analysis layer for enhanced explainability and reasoning.

## System Architecture

### Multi-Agent Pipeline (v2.0)

```
User Input (QuoteInput)
         ↓
    Risk Profiler (Agent 1)
    Analyzes driver/vehicle risk
         ↓
Conversion Predictor (Agent 2)
    ML model predicts probability
         ↓
 Premium Advisor (Agent 3)
   Adjusts premiums dynamically
         ↓
Decision Router (Agent 4)
Routes to AUTO/FOLLOW-UP/ESCALATE
         ↓
Decision Analysis (Agent 5) ← NEW v2.0
Generates reasoning & confidence
         ↓
  PredictionResponse
   Complete structured output
```

## Services Architecture

### Layer 1: Prediction Pipeline Services

#### 1. Risk Profiler (`risk_profiler.py`)
**Purpose**: Calculates risk classification based on driver history

**Algorithm**:
```
score = (Prev_Accidents × 3) + (Prev_Citations × 2)

Risk Level:
  score < 3    → LOW
  3 ≤ score < 6 → MEDIUM
  score ≥ 6    → HIGH
```

**Key Method**: `calculate_risk(data: QuoteInput) → str`

---

#### 2. Conversion Predictor (`predict_service.py`)
**Purpose**: ML-based conversion probability estimation

**Features**:
- Loads pre-trained scikit-learn model from `models/conversion_model.pkl`
- Auto-handles missing features (fills with 0)
- Returns binary prediction + probability

**Key Method**: `predict_conversion(data: dict) → Tuple[int, float]`

**Returns**:
- `prediction`: 0 or 1 (binary classification)
- `probability`: 0.0-1.0 (conversion likelihood)

---

#### 3. Premium Advisor (`premium_advisor.py`)
**Purpose**: Dynamic premium adjustment based on risk and probability

**Rules**:
```
IF probability < 0.4:
    premium *= 0.9    (10% discount - improve competitiveness)
ELSE IF probability > 0.7:
    premium *= 1.05   (5% increase - capture high-probability value)

IF risk_level == "HIGH":
    premium *= 1.1    (10% increase - risk adjustment)
```

**Key Method**: `adjust_premium(quoted_premium: float, probability: float, risk_level: str) → float`

---

#### 4. Decision Router (`decision_router.py`)
**Purpose**: Route decision based on probability and risk

**Rules** (evaluated in order):
```
IF probability > 0.7 AND risk_level == "LOW":
    return "AUTO APPROVE"
ELSE IF probability > 0.4:
    return "AGENT FOLLOW-UP"
ELSE:
    return "ESCALATE TO UNDERWRITER"
```

**Key Method**: `route_decision(probability: float, risk_level: str) → str`

---

### Layer 2: Decision Analysis Service (NEW v2.0)

#### Decision Analysis (`decision_analysis.py`)
**Purpose**: Comprehensive analysis with reasoning, confidence, and recommendations

**Key Responsibilities**:
1. **Confidence Scoring**: 0.0-1.0 based on ML certainty + risk alignment
2. **Risk Factor Identification**: Extracts actionable risk drivers
3. **Reasoning Generation**: Business-friendly explanation of decisions
4. **Recommended Actions**: Specific next steps for each decision
5. **Override Detection**: Identifies edge cases requiring special handling

**Main Function**: `analyze_decision(...) → DecisionAnalysis`

**Confidence Calculation** (weighted):
- ML Probability Certainty: 40%
- Risk-Probability Alignment: 40%
- Decision Consistency: 20%

**Override Rules**:
1. Multiple incidents (HIGH risk + 5+ incidents) → Force escalation
2. Extremely high probability (>0.95) + escalation → Consider override
3. Very low probability (<0.3) + auto-approve → Flag as override

**Output**: `DecisionAnalysis` object with:
- decision
- risk_level
- confidence_score (0.0-1.0)
- confidence_level (VERY_LOW/LOW/MEDIUM/HIGH/VERY_HIGH)
- reasoning (business explanation)
- recommended_action (specific next steps)
- risk_factors (identified issues)
- alternative_decision (if override needed)

---

### Layer 3: API & Schema Services

#### Request/Response Schemas

**`QuoteInput`** (Request):
```python
- Driver_Age: int (16-100)
- Driving_Exp: int (0-70)
- Prev_Accidents: int (≥0)
- Prev_Citations: int (≥0)
- Coverage: int (≥1)
- Veh_Usage: int (≥1)
- Annual_Miles_Range: int (≥0)
- Vehicl_Cost_Range: int (≥0)
- Sal_Range: int (≥0)
- Quoted_Premium: float (≥0)
```

**`PredictionResponse`** (Response - v2.0):
```python
- risk_level: RiskLevelEnum
- prediction: int (0 or 1)
- conversion_probability: float
- recommended_premium: float
- decision: DecisionEnum
- analysis: DecisionAnalysis (NEW v2.0)
  ├── confidence_score
  ├── reasoning
  ├── recommended_action
  ├── risk_factors
  └── override_triggered
- processing_time_ms: float
- model_version: str
```

---

#### Ollama Service (`ollama_service.py`)
**Purpose**: LLM-based natural language explanations

**Features**:
- Uses Ollama API for local LLM inference
- Fallback explanation if Ollama unavailable
- Temperature=0.2 for consistent, deterministic output

**Key Method**: `explain_decision(payload: dict) → str`

---

## API Endpoints

### POST /predict
**Main prediction endpoint**

**Request**: QuoteInput
**Response**: PredictionResponse (v2.0 with decision analysis)

**Example Response**:
```json
{
  "risk_level": "MEDIUM",
  "prediction": 1,
  "conversion_probability": 0.68,
  "recommended_premium": 950.00,
  "decision": "AGENT FOLLOW-UP",
  "analysis": {
    "decision": "AGENT FOLLOW-UP",
    "risk_level": "MEDIUM",
    "confidence_score": 0.742,
    "confidence_level": "HIGH",
    "reasoning": "Risk Assessment: Customer classified as MEDIUM risk. Key factors: Previous citations: 2. Conversion Analysis: ML model shows moderate conversion potential. Premium adjusted -5.0% to improve competitiveness. Decision: Agent follow-up recommended for review and personalization.",
    "recommended_action": "Agent should contact within 24 hours. Emphasize competitive premium positioning.",
    "conversion_probability": 0.68,
    "risk_factors": ["Previous citations: 2"],
    "premium_adjustment_reason": "Premium reduced 5.0% to enhance competitiveness",
    "alternative_decision": null,
    "override_triggered": false,
    "override_reason": null
  },
  "processing_time_ms": 45.23,
  "model_version": "1.0"
}
```

### POST /explain
**Natural language explanation endpoint**

**Request**: ExplainInput (full prediction context)
**Response**: `{"explanation": "natural language explanation"}`

### GET /
**Health check endpoint**

**Response**: Status message

### GET /health
**Detailed health check**

**Response**: Service health details

---

## Data Flow Diagram

```
┌─────────────┐
│ Frontend    │
│ (JS/HTML)   │
└──────┬──────┘
       │ POST /predict (QuoteInput)
       ▼
┌─────────────────────────────────┐
│  FastAPI App (main.py)          │
│ - CORS middleware               │
│ - Request validation            │
│ - Error handling                │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────┐
│ Predict Router (predict.py)             │
│ Orchestrates multi-agent pipeline       │
└──────┬──────────────────────────────────┘
       │
       ├──► Agent 1: Risk Profiler
       │    └─► calculate_risk()
       │
       ├──► Agent 2: Prediction Service
       │    └─► predict_conversion()
       │
       ├──► Agent 3: Premium Advisor
       │    └─► adjust_premium()
       │
       ├──► Agent 4: Decision Router
       │    └─► route_decision()
       │
       └──► Agent 5: Decision Analysis (NEW)
            └─► analyze_decision()
                ├─► _calculate_confidence_score()
                ├─► _identify_risk_factors()
                ├─► _generate_reasoning()
                ├─► _generate_recommended_action()
                └─► _check_override_conditions()
       │
       ▼
┌──────────────────────────────────┐
│ Response Builder                 │
│ - PredictionResponse             │
│ - Combines all agent outputs     │
│ - Includes decision analysis     │
└──────┬───────────────────────────┘
       │ JSON
       ▼
┌──────────────────┐
│ Frontend Display │
│ (Result shown)   │
└──────────────────┘
```

---

## Design Patterns Used

### 1. Multi-Agent Pattern
Each service is a specialized agent with single responsibility:
- Risk Profiler: Risk assessment
- Predictor: Probability estimation
- Premium Advisor: Business rules
- Decision Router: Action routing
- Decision Analysis: Explainability

### 2. Layered Architecture
- **API Layer**: FastAPI endpoints
- **Schema Layer**: Pydantic validation
- **Service Layer**: Business logic
- **Database Layer**: SQLAlchemy ORM

### 3. Service Injection
Router orchestrates services in pipeline:
```python
risk = calculate_risk(data)
probability = predict_conversion(data)
premium = adjust_premium(data, probability, risk)
decision = route_decision(probability, risk)
analysis = analyze_decision(...)
```

### 4. Enum-Based Type Safety
Response objects use enums:
```python
class RiskLevelEnum(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
```

---

## File Structure

```
backend/
├── app/
│   ├── main.py                          # FastAPI app entry point
│   ├── db/
│   │   ├── database.py                  # SQLAlchemy config
│   │   └── models.py                    # ORM models
│   ├── routers/
│   │   └── predict.py                   # Main API endpoints
│   ├── schemas/
│   │   ├── predict_schema.py            # Input schemas
│   │   └── decision_schema.py           # Response schemas (v2.0)
│   └── services/
│       ├── risk_profiler.py             # Agent 1
│       ├── predict_service.py           # Agent 2 (ML)
│       ├── premium_advisor.py           # Agent 3
│       ├── decision_router.py           # Agent 4
│       ├── decision_analysis.py         # Agent 5 (NEW v2.0)
│       ├── ollama_service.py            # LLM service
│       ├── ml_service.py                # Deprecated
│       └── conversion_predictor.py      # Deprecated
├── models/
│   └── conversion_model.pkl             # Pre-trained model
├── Dockerfile
├── requirements.txt
└── ARCHITECTURE.md                      # This file
```

---

## Production Considerations

### Security
- [ ] Enable CORS restrictions (specify frontend origin)
- [ ] Add authentication/authorization
- [ ] Validate all inputs at API boundary
- [ ] Use HTTPS for all endpoints
- [ ] Implement rate limiting

### Performance
- [ ] Cache model in memory (already done with joblib)
- [ ] Consider async/await for I/O operations
- [ ] Add request timeout limits
- [ ] Monitor inference time

### Scalability
- [ ] Database: Migrate from SQLite to PostgreSQL
- [ ] Queue system for async processing (Celery + Redis)
- [ ] Model serving: Consider TensorFlow Serving or Seldon
- [ ] Containerization: Docker + Kubernetes

### Monitoring
- [ ] Add structured logging (loguru configured)
- [ ] Track prediction performance metrics
- [ ] Monitor model drift
- [ ] Alert on decision anomalies

### Testing
- [ ] Unit tests for each service
- [ ] Integration tests for full pipeline
- [ ] Load testing
- [ ] Edge case validation

---

## Configuration

### Environment Variables
```bash
# Ollama configuration
OLLAMA_MODEL=llama3.1

# Database
DATABASE_URL=sqlite:///./hackathon.db

# FastAPI
ENVIRONMENT=development  # or production
DEBUG=true              # Disable in production
```

### Model Loading
The model is loaded from `../models/conversion_model.pkl` relative to the service file.
Ensure this path is correct or update `MODEL_PATH` in `predict_service.py`.

---

## Version History

### v2.0 (Current)
- ✅ Added Decision Analysis layer (Agent 5)
- ✅ Structured confidence scoring
- ✅ Risk factor identification
- ✅ Business reasoning generation
- ✅ Override rule detection
- ✅ Enhanced schemas with enums
- ✅ Comprehensive logging
- ✅ Improved documentation

### v1.0 (Previous)
- Basic 4-agent pipeline
- Unstructured responses
- Limited explainability

---

## Bugs Fixed / Issues Resolved

### v1.0 Issues
1. ❌ **Broken imports in quote_router.py** - References non-existent services
   - ✅ **Fixed**: Services properly implemented, quote_router deprecated

2. ❌ **Duplicate service files** - conversion_predictor.py unused
   - ✅ **Fixed**: Consolidated into predict_service.py

3. ❌ **Hardcoded model path** - predict_service.py uses relative path
   - ✅ **Fixed**: Dynamic path resolution with error handling

4. ❌ **No response standardization** - Different endpoints return different formats
   - ✅ **Fixed**: Unified PredictionResponse schema with TypedDict enums

5. ❌ **Missing error handling** - No validation for edge cases
   - ✅ **Fixed**: Added try-catch in router, validation in schemas

---

## Future Enhancements

### Short Term
- [ ] Add A/B testing framework for decision rules
- [ ] Implement decision logging/audit trail
- [ ] Add performance metrics endpoint
- [ ] Create admin dashboard

### Medium Term
- [ ] Multi-model ensemble (reduce single-model dependency)
- [ ] Feature importance analysis
- [ ] Dynamic rule engine (vs. hardcoded rules)
- [ ] Feedback loop for model retraining

### Long Term
- [ ] Real-time model monitoring and drift detection
- [ ] Explainable AI (SHAP/LIME integration)
- [ ] Custom LLM fine-tuning for domain-specific explanations
- [ ] Decision analytics and business intelligence

---

## Support & Maintenance

### Known Limitations
1. **SQLite database**: Not suitable for production; migrate to PostgreSQL
2. **Single-threaded model loading**: Consider thread pooling
3. **Ollama dependency**: Requires local Ollama instance for explanations
4. **Fixed decision rules**: Not configurable via UI (yet)

### Contact & Questions
- Architecture Lead: [Your Name]
- Last Updated: 2025
- Status: Production v2.0
