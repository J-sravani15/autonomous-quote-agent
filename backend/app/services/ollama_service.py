import json
import os
import subprocess
import socket
import traceback


def _get_available_models() -> list:
    """Get list of available Ollama models."""
    try:
        result = subprocess.run(
            ["ollama", "list"], capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            # Parse the output - first model is usually the best
            lines = result.stdout.strip().split("\n")[1:]  # Skip header
            models = []
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]
                    models.append(model_name)
            print(f"✓ Found Ollama models: {models}")
            return models
        else:
            print(f"✗ Ollama command failed: {result.stderr}")
            return []
    except FileNotFoundError:
        print("✗ Ollama not found in PATH - make sure it's installed and running")
        return []
    except Exception as e:
        print(f"✗ Error detecting Ollama models: {str(e)}")
        return []


def _test_ollama_connection():
    """Test if Ollama is accessible on localhost:11434"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(("127.0.0.1", 11434))
        sock.close()
        if result == 0:
            print(f"OK Ollama server is accessible on port 11434")
            return True
        else:
            print(
                f"! Cannot connect to Ollama on 127.0.0.1:11434 - port not responding"
            )
            return False
    except Exception as e:
        print(f"! Error testing Ollama connection: {str(e)}")
        return False


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

    explanation = (
        f"This quote was marked {risk_level} because the risk profiler found the customer profile consistent with that risk band. "
        f"The premium was {premium_direction} based on the model output and risk rules. "
        f"The conversion probability was {probability:.2f}, so the final decision was {decision.lower()}."
    )
    print(f"OK Using fallback explanation (Ollama unavailable)")
    return explanation


def explain_decision(payload: dict) -> str:
    """Generate explanation using Ollama LLM."""

    print("=" * 80)
    print("EXPLANATION REQUEST STARTED")
    print("=" * 80)

    # Try to get model from environment, or use default llama3
    model_name = os.getenv("OLLAMA_MODEL", "llama3.2")  # Default to llama3
    print(f"[STEP 1] Checking environment variable OLLAMA_MODEL")
    print(f"  > OLLAMA_MODEL value: {model_name}")

    # Model is set from environment or uses default llama3
    print(f"  OK Using model: {model_name}")

    print(f"\n[STEP 3] Building prompt...")
    prompt = f"""
You are an insurance underwriting assistant.

Explain the quote decision ONLY using the provided data.
Do not invent facts.
Do not assume information not present.
Use simple business language.

Include:

1. Customer Profile
2. Risk Assessment
3. Conversion Analysis
4. Premium Adjustment
5. Final Decision

Quote Data:
{json.dumps(payload, indent=2)}
"""
    print(f"  > Prompt length: {len(prompt)} characters")
    print(f"  > Prompt first 100 chars: {prompt[:100]}...")

    try:
        print(f"\n[STEP 4] Importing ollama library...")
        import ollama

        print(f"  OK Ollama library imported successfully")
        print(f"  > Ollama module: {ollama.__file__}")

        print(f"\n[STEP 5] Testing Ollama connection on localhost:11434...")
        if not _test_ollama_connection():
            print(f"  ! Connection test failed - will use fallback")
            print("=" * 80)
            return _fallback_explanation(payload)
        print(f"  OK Ollama connection successful")

        print(f"\n[STEP 6] Preparing ollama.chat() call...")
        print(f"  > Model name: {model_name}")
        print(f"  > Messages: 2 (system + user)")
        print(f"  > Options: temperature=0.2")

        print(f"\n[STEP 7] Calling ollama.chat()...")
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

        print(f"  OK ollama.chat() returned successfully")
        print(f"\n[STEP 8] Analyzing response...")
        print(f"  > Raw response type: {type(response)}")

        # ChatResponse object has message attribute, not dict access
        if hasattr(response, "message"):
            message = response.message.get("content", "").strip()
            print(f"  > Extracted from response.message object")
        elif isinstance(response, dict):
            message = response.get("message", {}).get("content", "").strip()
            print(f"  > Extracted from dict response")
        else:
            message = ""
            print(f"  ! Could not extract message from response")
        print(f"\n[STEP 9] Extracting message content...")
        print(f"  > Message length: {len(message)} characters")
        print(f"  > Message first 150 chars: {message[:150]}...")

        if message:
            print(f"\nOK EXPLANATION GENERATED SUCCESSFULLY")
            print(f"  > Generated {len(message)} characters of explanation")
            print("=" * 80)
            return message
        else:
            print(f"\n! Empty message in response - using fallback")
            print("=" * 80)
            return _fallback_explanation(payload)

    except ImportError as e:
        print(f"\n! ERROR Ollama Python library not installed")
        print(f"  > Error: {str(e)}")
        print(f"  > Fix: pip install ollama")
        print("=" * 80)
        return _fallback_explanation(payload)

    except ConnectionRefusedError as e:
        print(f"\n! ERROR Connection refused - Ollama not responding")
        print(f"  > Error: {str(e)}")
        print("=" * 80)
        return _fallback_explanation(payload)

    except Exception as e:
        print(f"\n! ERROR Unexpected error during ollama.chat() call")
        print(f"  > Error type: {type(e).__name__}")
        print(f"  > Error message: {str(e)}")
        print(f"  > Model being used: {model_name}")
        print("=" * 80)
        return _fallback_explanation(payload)
