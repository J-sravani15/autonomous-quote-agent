# Quick Start Guide - Autonomous Quote Agent v2.0

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start the Backend
```bash
cd app
uvicorn main:app --reload
```

**Backend runs at**: `http://127.0.0.1:8000`

### Step 3: View API Documentation
Open in browser: `http://127.0.0.1:8000/docs`

---

## 📤 Test the Prediction Endpoint

### Using curl:
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Driver_Age": 35,
    "Driving_Exp": 10,
    "Prev_Accidents": 0,
    "Prev_Citations": 0,
    "Coverage": 1,
    "Veh_Usage": 1,
    "Annual_Miles_Range": 10000,
    "Vehicl_Cost_Range": 25000,
    "Sal_Range": 50000,
    "Quoted_Premium": 1000
  }'
```

### Using Python:
```python
import requests

payload = {
    "Driver_Age": 35,
    "Driving_Exp": 10,
    "Prev_Accidents": 0,
    "Prev_Citations": 0,
    "Coverage": 1,
    "Veh_Usage": 1,
    "Annual_Miles_Range": 10000,
    "Vehicl_Cost_Range": 25000,
    "Sal_Range": 50000,
    "Quoted_Premium": 1000
}

response = requests.post("http://127.0.0.1:8000/predict", json=payload)
result = response.json()

print(f"Decision: {result['decision']}")
print(f"Confidence: {result['analysis']['confidence_score']}")
print(f"Reasoning: {result['analysis']['reasoning']}")
```

### Using JavaScript:
```javascript
const payload = {
    Driver_Age: 35,
    Driving_Exp: 10,
    Prev_Accidents: 0,
    Prev_Citations: 0,
    Coverage: 1,
    Veh_Usage: 1,
    Annual_Miles_Range: 10000,
    Vehicl_Cost_Range: 25000,
    Sal_Range: 50000,
    Quoted_Premium: 1000
};

fetch('http://127.0.0.1:8000/predict', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload)
})
.then(r => r.json())
.then(data => {
    console.log('Decision:', data.decision);
    console.log('Analysis:', data.analysis);
});
```

---

## 📊 Response Structure (v2.0)

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
    "reasoning": "Risk Assessment: Customer classified as MEDIUM risk...",
    "recommended_action": "Agent should contact within 24 hours...",
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

---

## 📚 Key Concepts

### Decision Types
| Decision | Meaning | Action |
|----------|---------|--------|
| `AUTO APPROVE` | High probability + Low risk | Issue immediately |
| `AGENT FOLLOW-UP` | Moderate probability | Contact for review |
| `ESCALATE TO UNDERWRITER` | Low probability or High risk | Specialist review |

### Risk Levels
| Level | Meaning | Threshold |
|-------|---------|-----------|
| `LOW` | Clean history | Score < 3 |
| `MEDIUM` | Some incidents | Score 3-6 |
| `HIGH` | Multiple incidents | Score ≥ 6 |

**Risk Score = (Accidents × 3) + (Citations × 2)**

### Confidence Levels
| Level | Range | Meaning |
|-------|-------|---------|
| `VERY_HIGH` | 0.85-1.0 | Very confident |
| `HIGH` | 0.70-0.85 | Confident |
| `MEDIUM` | 0.55-0.70 | Moderate |
| `LOW` | 0.40-0.55 | Low confidence |
| `VERY_LOW` | 0.0-0.40 | Very low confidence |

---

## 🔧 File Structure

```
backend/
├── app/
│   ├── main.py                      ← FastAPI app
│   ├── routers/
│   │   └── predict.py              ← API endpoints
│   ├── services/
│   │   ├── decision_analysis.py    ← NEW: Analysis engine
│   │   ├── risk_profiler.py
│   │   ├── predict_service.py      ← ML predictions
│   │   ├── premium_advisor.py
│   │   └── decision_router.py
│   └── schemas/
│       ├── predict_schema.py       ← Input/Output types
│       └── decision_schema.py      ← NEW: Response types
├── models/
│   └── conversion_model.pkl        ← ML model
├── requirements.txt
├── ARCHITECTURE.md                 ← Full documentation
├── IMPLEMENTATION_SUMMARY.md       ← What changed
└── QUICK_START.md                 ← This file
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'app'"
**Solution**: Make sure you're running from the `backend/app` directory:
```bash
cd backend/app
uvicorn main:app --reload
```

### Issue: "Model file not found"
**Solution**: Ensure `models/conversion_model.pkl` exists in `backend/models/`

### Issue: Ollama errors (for /explain endpoint)
**Solution**: Install Ollama and run: `ollama serve`
Or set model name: `OLLAMA_MODEL=llama3`

### Issue: Port 8000 already in use
**Solution**: Use different port:
```bash
uvicorn main:app --port 8001
```

---

## 🎯 Common Tasks

### Add New Prediction Field
1. Add field to `QuoteInput` in `schemas/predict_schema.py`
2. Add processing logic to relevant service
3. Include in response

### Modify Decision Rules
Edit the thresholds in:
- `services/decision_router.py` - Decision routing logic
- `services/decision_analysis.py` - Override rules

### Change Risk Scoring
Edit `services/risk_profiler.py`:
```python
score = data.Prev_Accidents * 3 + data.Prev_Citations * 2  # Modify multipliers
```

### Add Risk Factor
Add to `_identify_risk_factors()` in `services/decision_analysis.py`:
```python
if vehicle_type == "MOTORCYCLE":
    factors.append("High-risk vehicle type")
```

---

## 🔐 Production Setup

### Before Deploying
- [ ] Set `CORS` origins (don't use `["*"]`)
- [ ] Add authentication/authorization
- [ ] Set `DEBUG=false`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Enable HTTPS
- [ ] Setup monitoring/logging

### Environment Variables
```bash
# Development
ENVIRONMENT=development
DEBUG=true

# Production
ENVIRONMENT=production
DEBUG=false
OLLAMA_MODEL=llama3.1
DATABASE_URL=postgresql://user:pass@localhost/quotes
```

---

## 📖 Learn More

- **Full Architecture**: See `ARCHITECTURE.md`
- **What Changed**: See `IMPLEMENTATION_SUMMARY.md`
- **API Docs**: Visit `http://127.0.0.1:8000/docs`
- **Code**: Check docstrings in each service

---

## 🆘 Need Help?

### Common Questions

**Q: How do I customize the decision rules?**
A: Edit `services/decision_router.py` and `services/decision_analysis.py`

**Q: Can I add more risk factors?**
A: Yes, modify `_identify_risk_factors()` in `services/decision_analysis.py`

**Q: How accurate is the ML model?**
A: Depends on training data. Check `models/conversion_model.pkl` details.

**Q: Can I use a different ML model?**
A: Yes, replace `conversion_model.pkl` with your model. Ensure feature names match.

**Q: How do I monitor the system?**
A: Check logs in `logs/app.log`. Add monitoring via `/health` endpoint.

---

## ✅ What's New in v2.0

- ✅ Decision Analysis layer (Agent 5)
- ✅ Confidence scoring
- ✅ Structured reasoning
- ✅ Risk factor identification
- ✅ Recommended actions
- ✅ Override detection
- ✅ Enhanced documentation
- ✅ Type-safe responses
- ✅ Structured logging
- ✅ Better error handling

---

## 🎓 Example Use Cases

### Use Case 1: Low-Risk, High-Probability Quote
```
Input: 35yo, 10yrs exp, no accidents, no citations, $1000 premium
→ Risk: LOW
→ Probability: 0.85
→ Decision: AUTO APPROVE
→ Confidence: VERY_HIGH
→ Action: Issue immediately
```

### Use Case 2: High-Risk, Moderate-Probability Quote
```
Input: 45yo, 5yrs exp, 2 accidents, 3 citations, $1500 premium
→ Risk: HIGH
→ Probability: 0.55
→ Decision: ESCALATE TO UNDERWRITER
→ Confidence: HIGH
→ Action: Specialist review required
```

### Use Case 3: Edge Case (Very High Probability, High Risk)
```
Input: 50yo, 20yrs exp, 0 accidents, 0 citations, $800 premium
→ Risk: LOW
→ Probability: 0.92
→ Decision: AUTO APPROVE
→ Confidence: VERY_HIGH
→ Override: None
→ Action: Auto-approve - excellent profile + high conversion
```

---

## 🚀 Next Steps

1. ✅ Run the backend
2. ✅ Test with curl/Python/JavaScript
3. ✅ Check API docs at `/docs`
4. ✅ Read full architecture docs
5. ✅ Deploy to production when ready

---

**Happy coding! 🎉**
