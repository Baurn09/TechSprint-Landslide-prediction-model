from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import joblib
import os

# ================= SENSOR IMPORTS =================
from ml_api.serial_reader import start_serial_thread, latest_sensor_data

# ================= APP =================
app = FastAPI()

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

    # ================= ML INFERENCE =================

    feature_vector = np.array([[soil, tilt, vib]])

    # If you used scaler:
    # X_scaled = sensor_scaler.transform(feature_vector)
    # prob = sensor_model.predict_proba(X_scaled)[0][1]

    prob = sensor_model.predict_proba(feature_vector)[0][1]

    status = (
        "HIGH" if prob > 0.7
        else "MODERATE" if prob > 0.4
        else "LOW"
    )

    return {
        "soil": round(float(soil), 2),
        "tilt": round(float(tilt), 4),
        "vibration": round(float(vib), 4),
        "riskScore": float(prob),
        "riskPercent": int(prob * 100),
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
    slope_factor = 0.6 * slope + 0.4 * rain_slope_interaction
    soil_saturation = 0.5 * soil_moisture + 0.5 * saturation_index
    vegetation_protection = 0.7 * V - 0.3 * bare_soil_index
    terrain_context = elevation
    human_exposure = population

    feature_vector = [[
        elevation, V, population,
        rain_1d, rain_7d, rain_30d,
        slope, soil_moisture, soil_type,
        rain_slope_interaction,
        rain_intensity_ratio,
        bare_soil_index,
        saturation_index
    ]]

    X = sat_scaler.transform(np.array(feature_vector))
    prob = sat_model.predict_proba(X)[0][1]

    return {
        "riskScore": float(prob),
        "riskPercent": int(prob * 100),
        "indicators": {
            "rainfallStress": round(float(rainfall_stress), 2),
            "slopeFactor": round(float(slope_factor), 2),
            "soilSaturation": round(float(soil_saturation), 3),
            "vegetationProtection": round(float(vegetation_protection), 3),
            "terrainContext": round(float(terrain_context), 1),
            "humanExposure": int(human_exposure)
        }
    }

# ==================================================
# GRID BATCH MODEL
# ==================================================

class GridRow(BaseModel):
    grid_uid: str
    ndvi: float
    population: float
    rain_1d: float
    rain_7d: float
    rain_30d: float
    slope: float
    soil_moisture: float
    soil_type: float
    elevation: float

class GridBatchInput(BaseModel):
    rows: list[GridRow]

@app.post("/predict/grid")
def predict_grid(data: GridBatchInput):

    results = []

    for row in data.rows:

        rain_slope_interaction = row.rain_7d * row.slope
        rain_intensity_ratio = row.rain_1d / (row.rain_30d + 1e-6)
        bare_soil_index = 1.0 - row.ndvi
        saturation_index = row.rain_30d * row.soil_moisture

        feature_vector = [[
            row.elevation,
            row.ndvi,
            bare_soil_index,
            row.population * 100,
            row.rain_1d,
            row.rain_7d,
            row.rain_30d,
            rain_intensity_ratio,
            row.slope,
            rain_slope_interaction,
            row.soil_moisture,
            saturation_index,
            row.soil_type
        ]]

        X = sat_scaler.transform(np.array(feature_vector))
        prob = sat_model.predict_proba(X)[0][1]

        if row.slope < 5 or row.elevation < 600:
            prob = 0

        results.append({
            "grid_uid": row.grid_uid,
            "risk": float(prob)
        })

    return {"results": results}