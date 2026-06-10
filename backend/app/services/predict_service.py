import joblib
import pandas as pd

model = joblib.load("models/conversion_model.pkl")

def predict_conversion(data):

    df = pd.DataFrame([data])

    # Expected model features
    expected_features = model.feature_names_in_

    # Add missing columns
    for col in expected_features:
        if col not in df.columns:
            df[col] = 0

    # Reorder columns exactly like training
    df = df[expected_features]

    # Ensure numeric values
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

    # Model prediction
    prediction = model.predict(df)[0]

    # Probability of conversion
    probability = model.predict_proba(df)[0][1]

    # DEBUG (very important for you now)
    print("INPUT DATA →")
    print(df)

    print("MODEL PREDICTION →", prediction)
    print("MODEL PROBABILITY →", probability)

    return int(prediction), float(probability)