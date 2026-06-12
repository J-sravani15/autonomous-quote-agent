import json
import os


def _fallback_explanation(payload: dict) -> str:
    risk_level = payload.get("risk_level", "UNKNOWN")
    probability = float(payload.get("conversion_probability", 0))
    recommended_premium = payload.get("recommended_premium", 0)
    quoted_premium = payload.get("Quoted_Premium", 0)
    decision = payload.get("decision", "REVIEW")

    premium_direction = (
        "increased"
        if recommended_premium > quoted_premium
        else "reduced or kept stable"
    )

    return (
        f"This quote was marked {risk_level} because the risk profiler found the customer profile consistent with that risk band. "
        f"The premium was {premium_direction} based on the model output and risk rules. "
        f"The conversion probability was {probability:.2f}, so the final decision was {decision.lower()}."
    )


def explain_decision(payload: dict) -> str:
    model_name = os.getenv("OLLAMA_MODEL", "llama3.1")
    prompt = (
        "Explain this insurance quote decision in simple language. "
        "Cover why the customer was assigned the risk level, why the premium changed, "
        "and why the final decision was made. Keep it concise and business-friendly.\n\n"
        f"Quote data:\n{json.dumps(payload, indent=2)}"
    )

    try:
        import ollama

        response = ollama.chat(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are an insurance underwriting explanation assistant.",
                },
                {"role": "user", "content": prompt},
            ],
            options={"temperature": 0.2},
        )

        message = response.get("message", {}).get("content", "").strip()
        if message:
            return message
    except Exception:
        pass

    return _fallback_explanation(payload)
