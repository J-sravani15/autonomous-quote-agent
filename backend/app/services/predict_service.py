"""
Prediction Service - ML-based conversion prediction.

Loads the pre-trained scikit-learn model and generates:
- Binary prediction (0 = won't convert, 1 = will convert)
- Conversion probability (0.0-1.0)

The model expects features aligned with the training dataset.
Missing features are filled with 0, extra features are ignored.
"""

import joblib
import pandas as pd
import os
from pathlib import Path
import sklearn  # Required for unpickling sklearn models

# Model loading with path resolution
MODEL_PATH = os.path.join(
    Path(__file__).parent.parent.parent, "models", "conversion_model.pkl"
)

print(f"Loading model from: {MODEL_PATH}")
print(f"Model exists: {os.path.exists(MODEL_PATH)}")

model = None

def _load_model():
    """Lazy load the model on first use."""
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            # Fallback to relative path
            fallback_path = "models/conversion_model.pkl"
            if os.path.exists(fallback_path):
                actual_path = fallback_path
            else:
                raise RuntimeError(
                    f"Conversion model not found. Tried: {MODEL_PATH} and {fallback_path}"
                )
        else:
            actual_path = MODEL_PATH
            
        try:
            print(f"Loading model from: {actual_path}")
            import sklearn  # Ensure sklearn is imported for unpickling
            model = joblib.load(actual_path)
            print(f"✓ Model loaded successfully")
        except Exception as e:
            print(f"✗ Error loading model: {str(e)}")
            raise RuntimeError(f"Error loading model: {str(e)}")
    return model


def predict_conversion(data: dict) -> tuple:
    """
    Predict conversion probability using ML model.
    
    Process:
    1. Convert input dict to DataFrame
    2. Add missing features (filled with 0)
    3. Reorder columns to match training
    4. Convert to numeric, fill NaN with 0
    5. Generate prediction and probability
    
    Args:
        data: Dictionary with quote features
        
    Returns:
        Tuple of (prediction, probability)
        - prediction: int (0 or 1, binary classification)
        - probability: float (0.0-1.0, probability of conversion)
        
    Raises:
        ValueError: If model inference fails
    """
    
    ml_model = _load_model()

    df = pd.DataFrame([data])

    # Expected model features
    expected_features = ml_model.feature_names_in_

    # Add missing columns (fill with 0)
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0

    # Reorder columns exactly like training
    df = df[expected_features]

    # Ensure numeric values
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

    # Model prediction
    prediction = ml_model.predict(df)[0]

    # Probability of conversion (class 1)
    probability = ml_model.predict_proba(df)[0][1]

    # DEBUG logging
    print("INPUT DATA →")
    print(df)
    print("MODEL PREDICTION →", prediction)
    print("MODEL PROBABILITY →", probability)

    return int(prediction), float(probability)