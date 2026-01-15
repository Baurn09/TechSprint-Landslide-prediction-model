from fastapi import FastAPI
import pickle
import numpy as np

app = FastAPI()

# Load models ONCE
with open("../training/satellite_gbt_model.pkl", "rb") as f:
    satellite_model = pickle.load(f)

with open("../training/satellite_scaler.pkl", "rb") as f:
    satellite_scaler = pickle.load(f)

@app.post("/predict/satellite")
def predict_satellite(data: dict):
    features = np.array([data["features"]])
    features_scaled = satellite_scaler.transform(features)
    prediction = satellite_model.predict(features_scaled)

    return {
        "risk": int(prediction[0])
    }
