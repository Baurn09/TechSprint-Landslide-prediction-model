from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import os

app = FastAPI()

# ------------------ PATH SETUP ------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "training")

SCALER_PATH = os.path.join(MODEL_DIR, "satellite_scaler.pkl")
MODEL_PATH = os.path.join(MODEL_DIR, "satellite_gbt_model.pkl")

# ------------------ LOAD MODEL ON STARTUP ------------------

scaler = joblib.load(SCALER_PATH)
model = joblib.load(MODEL_PATH)

print("✅ Satellite model & scaler loaded successfully")

# ------------------ INPUT SCHEMA ------------------

class SatelliteRequest(BaseModel):
    # Must be in the SAME ORDER as training FEATURES
    features: list[float]  # length = 7

# ------------------ PREDICTION ENDPOINT ------------------

@app.post("/predict/satellite")
def predict_satellite(data: SatelliteRequest):
    X = np.array([data.features])

    X_scaled = scaler.transform(X)

    # Probability of landslide (class 1)
    risk_prob = model.predict_proba(X_scaled)[0][1]

    return {
        "riskScore": round(float(risk_prob), 4),
        "riskPercent": int(round(risk_prob * 100)),
        "status": (
            "LOW" if risk_prob < 0.4
            else "MODERATE" if risk_prob < 0.7
            else "HIGH"
        )
    }
#Ground sensor part 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "training")

SENSOR_SCALER = os.path.join(MODEL_DIR, "sensor_scaler.pkl")
SENSOR_MODEL = os.path.join(MODEL_DIR, "sensor_random_forest.pkl")

sensor_scaler = joblib.load(SENSOR_SCALER)
sensor_model = joblib.load(SENSOR_MODEL)

print("✅ Ground sensor model loaded")

class SensorRequest(BaseModel):
    features: list[float]  # [soilMoisture, tilt, vibration, magnitude]

@app.post("/predict/sensor")
def predict_sensor(data: SensorRequest):
    X = np.array([data.features])
    X_scaled = sensor_scaler.transform(X)

    prob = sensor_model.predict_proba(X_scaled)[0][1]

    return {
        "riskScore": round(float(prob), 4),
        "riskPercent": int(round(prob * 100)),
        "status": (
            "HIGH" if prob >= 0.7
            else "MODERATE" if prob >= 0.4
            else "LOW"
        )
    }
