from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import os
from ml_api.serial_reader import start_serial_thread, latest_sensor_data


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

@app.on_event("startup")
def startup_event():
    start_serial_thread()


from collections import deque

# ------------------ GROUND SENSOR (NO TRAINING) ------------------

WINDOW = 120  # calibration samples (~2 min)
SOIL_RATE_TH = 0.02
TILT_RATE_TH = 0.05
VIB_TH = 1.5

soil_buf = deque(maxlen=WINDOW)
tilt_buf = deque(maxlen=WINDOW)
vib_buf = deque(maxlen=WINDOW)

prev_soil = None
prev_tilt = None

class SensorRequest(BaseModel):
    # order: soil_moisture, tilt, vibration
    features: list[float]

@app.post("/predict/sensor")
def predict_sensor(data: SensorRequest):
    global prev_soil, prev_tilt

    soil = latest_sensor_data["soil"]
    tilt = latest_sensor_data["tilt"]
    vib  = latest_sensor_data["vibration"]

    if soil is None:
        return {
            "status": "NO SENSOR DATA",
            "riskScore": 0,
            "riskPercent": 0
        }

    soil_buf.append(soil)
    tilt_buf.append(tilt)
    vib_buf.append(abs(vib))

    # ---------------- Calibration phase ----------------
    if len(soil_buf) < WINDOW:
        return {
            "status": "CALIBRATING",
            "riskScore": 0.0,
            "riskPercent": 0
        }

    soil_mean, soil_std = np.mean(soil_buf), np.std(soil_buf)
    tilt_mean, tilt_std = np.mean(tilt_buf), np.std(tilt_buf)
    vib_mean, vib_std = np.mean(vib_buf), np.std(vib_buf)

    soil_z = abs((soil - soil_mean) / (soil_std + 1e-6))
    tilt_z = abs((tilt - tilt_mean) / (tilt_std + 1e-6))
    vib_z  = abs((vib - vib_mean) / (vib_std + 1e-6))

    anomaly_score = soil_z + tilt_z + vib_z

    # ---------------- Rate-based physics ----------------
    if prev_soil is None:
        prev_soil, prev_tilt = soil, tilt
        return {
            "status": "NORMAL",
            "riskScore": 0.0,
            "riskPercent": 0
        }

    soil_rate = soil - prev_soil
    tilt_rate = tilt - prev_tilt

    prev_soil, prev_tilt = soil, tilt

    physics_trigger = (
        soil_rate > SOIL_RATE_TH and
        abs(tilt_rate) > TILT_RATE_TH and
        vib > VIB_TH
    )

    # ---------------- Risk calculation ----------------
    risk = min(anomaly_score / 10, 1.0)

    status = (
        "HIGH" if (risk > 0.7 and physics_trigger)
        else "MODERATE" if risk > 0.4
        else "LOW"
    )

    return {
        "riskScore": round(float(risk), 3),
        "riskPercent": int(risk * 100),
        "status": status
    }
