#!/usr/bin/env python
"""Minimal test of Ollama integration"""

import sys
sys.path.insert(0, 'app')

from services.ollama_service import explain_decision

payload = {
    'risk_level': 'LOW',
    'prediction': 0,
    'conversion_probability': 0.39,
    'decision': 'ESCALATE',
}

print("\nCalling explain_decision()...\n")
result = explain_decision(payload)

print("\n" + "=" * 80)
print(f"RESULT: {len(result)} characters")
print("=" * 80)
print(f"First 500 chars:\n{result[:500]}")
