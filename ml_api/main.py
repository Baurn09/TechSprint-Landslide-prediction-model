from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import os

# ================= SENSOR IMPORTS =================
from ml_api.serial_reader import start_serial_thread, latest_sensor_data

# ================= APP =================
app = FastAPI()


prev_soil = None
prev_tilt = None

# ==================================================
# START SERIAL ON API STARTUP  ✅ CRITICAL
# ==================================================

@app.on_event("startup")
def startup_event():
    start_serial_thread()
    print("✅ Serial reader started")

# ==================================================
# BASIC ROUTES
# ==================================================

@app.get("/")
def home():
    return {"message": "Landslide Prediction API is running"}

@app.get("/data")
def get_sensor_data():
    # Sends latest live sensor data
    return latest_sensor_data


# ==================================================
# SENSOR-BASED PREDICTION
# ==================================================

@app.post("/predict/sensor")
def predict_sensor():

    soil = latest_sensor_data["soil"]
    tilt = latest_sensor_data["tilt"]
    vib  = latest_sensor_data["vibration"]

    if soil is None:
        return {
            "soil": None,
            "tilt": None,
            "vibration": None,
            "riskScore": 0,
            "riskPercent": 0,
            "status": "NO SENSOR DATA"
        }

    global prev_soil, prev_tilt

    if prev_soil is None:
        prev_soil, prev_tilt = soil, tilt
        return {
            "soil": soil,
            "tilt": tilt,
            "vibration": vib,
            "riskScore": 0,
            "riskPercent": 0,
            "status": "CALIBRATING"
        }

    soil_rate = soil - prev_soil
    tilt_rate = tilt - prev_tilt

    prev_soil, prev_tilt = soil, tilt

    # Must match training features exactly
    feature_vector = np.array([[
        soil,
        soil_rate,
        tilt,
        tilt_rate,
        abs(vib)
    ]])

    # IsolationForest inference
    anomaly_label = sensor_model.predict(feature_vector)[0]
    anomaly_score = sensor_model.decision_function(feature_vector)[0]

    # Convert anomaly score to 0–1 risk
    risk = 1 - (anomaly_score + 0.5)
    risk = max(0, min(risk, 1))

    status = (
        "HIGH" if risk > 0.7
        else "MODERATE" if risk > 0.4
        else "LOW"
    )

    return {
        "soil": round(float(soil), 2),
        "tilt": round(float(tilt), 4),
        "vibration": round(float(vib), 4),
        "riskScore": float(risk),
        "riskPercent": int(risk * 100),
        "status": status
    }

# ==================================================
# SATELLITE MODEL
# ==================================================

BASE_DIR = os.path.dirname(__file__)

# ==================================================
# SENSOR ML MODEL
# ==================================================

sensor_model = joblib.load(
    os.path.join(BASE_DIR, "../training/sensor_anomaly_model.pkl")
)

# If you used a scaler during training, also load:
# sensor_scaler = joblib.load(
#     os.path.join(BASE_DIR, "../training/sensor_scaler.pkl")
# )


sat_model = joblib.load(
    os.path.join(BASE_DIR, "../training/landslide_logistic_model.pkl")
)
sat_scaler = joblib.load(
    os.path.join(BASE_DIR, "../training/landslide_scaler.pkl")
)

class SatelliteInput(BaseModel):
    features: list  # [R, V, S, E, P]

@app.post("/predict/satellite")
def predict_satellite(data: SatelliteInput):

    R, V, S, E, P = data.features

    rain_1d = R * 100
    rain_7d = R * 200
    rain_30d = R * 500

    soil_moisture = R * 0.4
    soil_type = 3
    population = P * 100
    elevation = E * 1000
    slope = S * 6

    rain_slope_interaction = rain_7d * slope
    rain_intensity_ratio = rain_1d / (rain_30d + 1e-6)
    bare_soil_index = 1 - V
    saturation_index = rain_30d * soil_moisture

    rainfall_stress = 0.5 * rain_1d + 0.3 * rain_7d + 0.2 * rain_30d
    slope_factor = 0.6