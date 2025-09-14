# home/ml_utils.py (utility file for ML)
import os
import joblib
from django.conf import settings

# Path to the ml_models folder
MODEL_DIR = os.path.join(settings.BASE_DIR, "crop", "ml_models")

# Load once (don’t reload on every request)
model = joblib.load(os.path.join(MODEL_DIR, "crop_recommendation_model.pkl"))
scaler = joblib.load(os.path.join(MODEL_DIR, "crop_recommendation_scaler.pkl"))
label_encoder = joblib.load(os.path.join(MODEL_DIR, "crop_recommendation_label_encoder.pkl"))


import pandas as pd
import numpy as np

def predict_crop(data):
    print(f"=== NEW PREDICTION ===")
    print(f"Raw features received: {data['features']}")
    
    features = [data["features"]]
    print(f"Features before scaling: {features}")
    
    # Scale features
    features_scaled = scaler.transform(features)
    print(f"Features after scaling: {features_scaled}")

    # Get probabilities for all crops
    probabilities = model.predict_proba(features_scaled)[0]
    print(f"Raw probabilities: {probabilities}")
    print(f"Probability sum: {sum(probabilities)}")
    print(f"Max probability index: {np.argmax(probabilities)}")

    # Map probabilities to crop names
    crop_probs = {
        label_encoder.inverse_transform([i])[0]: float(prob)
        for i, prob in enumerate(probabilities)
    }
    print(f"Mapped probabilities: {crop_probs}")

    # Best crop (highest probability)
    prediction = model.predict(features_scaled)
    print(f"Raw prediction: {prediction}")
    
    best_crop = label_encoder.inverse_transform(prediction)[0]
    print(f"Best crop: {best_crop}")

    return best_crop, crop_probs


# def predict_crop(data):
#     # If frontend sends "features" as a list
#     features = [data["features"]]
    

#     # Scale
#     features_scaled = scaler.transform(features)

#     # Predict
#     prediction = model.predict(features_scaled)

#     # Decode to label
#     crop = label_encoder.inverse_transform(prediction)[0] #inverse_transform() → method that converts numeric labels back to original string labels.

#     return crop


# def predict_crop(data):
#     """
#     data: dict containing N, P, K, temperature, humidity, ph, rainfall
#     """
#     features = [[
#         data["N"], data["P"], data["K"],
#         data["temperature"], data["humidity"],
#         data["ph"], data["rainfall"]
#     ]]
#     # Scale input
#     features_scaled = scaler.transform(features)
#     # Predict
#     prediction = model.predict(features_scaled)
#     # Decode label
#     crop = label_encoder.inverse_transform(prediction)[0]
#     return crop
