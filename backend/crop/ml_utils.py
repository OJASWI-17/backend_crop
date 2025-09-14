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

def predict_crop(data):
    # If frontend sends "features" as a list
    features = [data["features"]]

    # Scale
    features_scaled = scaler.transform(features)

    # Predict
    prediction = model.predict(features_scaled)

    # Decode to label
    crop = label_encoder.inverse_transform(prediction)[0]

    return crop

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
