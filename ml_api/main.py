from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
from collections import deque

# ================= SENSOR IMPORTS =================
from ml_api.serial_reader import start_serial_thread, latest_sensor_data

# ================= APP =================
app = FastAPI()

# ==================================================
# START SERIAL (UNCHANGED)
# ==================================================

@app.on_event("startup")
def startup_event():
    print("🚀 FastAPI starting...")
    start_serial_thread()

# ==================================================
# SENSOR CONFIG (UNCHANGED)
# ==================================================

WINDOW = 120  # calibration samples
SOIL_RATE_TH = 0.02
TILT_RATE_TH = 0.05
VIB_TH = 1.5

soil_buf = deque(maxlen=WINDOW)
tilt_buf = deque(maxlen=WINDOW)
vib_buf  = deque(maxlen=WINDOW)

prev_soil = None
prev_tilt = None

# ==================================================
# SENSOR ENDPOINT (UNCHANGED)
# ==================================================

@app.post("/predict/sensor")
def predict_sensor():
    global prev_soil, prev_tilt

    print("🧠 main.py sees:", latest_sensor_data)

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

    soil_buf.append(soil)
    tilt_buf.append(tilt)
    vib_buf.append(abs(vib))

    if len(soil_buf) < WINDOW:
        return {
            "soil": soil,
            "tilt": tilt,
            "vibration": vib,
            "riskScore": 0,
            "riskPercent": 0,
            "status": "CALIBRATING"
        }

    soil_mean, soil_std = np.mean(soil_buf), np.std(soil_buf)
    tilt_mean, tilt_std = np.mean(tilt_buf), np.std(tilt_buf)
    vib_mean, vib_std   = np.mean(vib_buf), np.std(vib_buf)

    soil_z = abs((soil - soil_mean) / (soil_std + 1e-6))
    tilt_z = abs((tilt - tilt_mean) / (tilt_std + 1e-6))
    vib_z  = abs((vib  - vib_mean)  / (vib_std  + 1e-6))

    anomaly_score = soil_z + tilt_z + vib_z

    if prev_soil is None:
        prev_soil, prev_tilt = soil, tilt
        return {
            "soil": soil,
            "tilt": tilt,
            "vibration": vib,
            "riskScore": 0,
            "riskPercent": 0,
            "status": "NORMAL"
        }

    soil_rate = soil - prev_soil
    tilt_rate = tilt - prev_tilt

    prev_soil, prev_tilt = soil, tilt

    physics_trigger = (
        soil_rate > SOIL_RATE_TH and
        abs(tilt_rate) > TILT_RATE_TH and
        vib > VIB_TH
    )

    risk = min(anomaly_score / 10, 1.0)

    status = (
        "HIGH" if (risk > 0.7 and physics_trigger)
        else "MODERATE" if risk > 0.4
        else "LOW"
    )

    return {
        "soil": round(float(soil), 2),
        "tilt": round(float(tilt), 4),
        "vibration": round(float(vib), 4),
        "riskScore": round(float(risk), 3),
        "riskPercent": int(risk * 100),
        "status": status
    }

# ==================================================
# SATELLITE MODEL (NEW – DOES NOT TOUCH SENSOR)
# ==================================================

import joblib
import os

BASE_DIR = os.path.dirname(__file__)

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


    # ---- derive training features ----

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

    # ================= DASHBOARD INDICATORS =================

    # 1. Rainfall Stress
    rainfall_stress = (
        0.5 * rain_1d +
        0.3 * rain_7d +
        0.2 * rain_30d
    )

    # 2. Slope Factor
    slope_factor = (
        0.6 * slope +
        0.4 * rain_slope_interaction
    )

    # 3. Soil Saturation
    soil_saturation = (
        0.5 * soil_moisture +
        0.5 * saturation_index
    )

    # 4. Vegetation Protection
    vegetation_protection = (
        0.7 * V -
        0.3 * bare_soil_index
    )

    # 5. Terrain Context
    terrain_context = elevation

    # 6. Human Exposure
    human_exposure = population


    feature_vector = [[
        elevation,
        V,
        population,
        rain_1d,
        rain_7d,
        rain_30d,
        slope,
        soil_moisture,
        soil_type,
        rain_slope_interaction,
        rain_intensity_ratio,
        bare_soil_index,
        saturation_index
    ]]

    X = np.array(feature_vector)

    X_scaled = sat_scaler.transform(X)
    prob = sat_model.predict_proba(X_scaled)[0][1]

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
# GRID BATCH MODEL INFERENCE (NEW)
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

        # -------- base inputs from GEE --------

        elevation = row.elevation
        V = row.ndvi
        population = row.population * 100
        rain_1d = row.rain_1d
        rain_7d = row.rain_7d
        rain_30d = row.rain_30d
        slope = row.slope
        soil_moisture = row.soil_moisture
        soil_type = row.soil_type

        # -------- derived features (MATCH TRAINING) --------

        rain_slope_interaction = rain_7d * slope
        rain_intensity_ratio = rain_1d / (rain_30d + 1e-6)
        bare_soil_index = 1.0 - V
        saturation_index = rain_30d * soil_moisture

        feature_vector = [[
            elevation,
            V,
            population,
            rain_1d,
            rain_7d,
            rain_30d,
            slope,
            soil_moisture,
            soil_type,
            rain_slope_interaction,
            rain_intensity_ratio,
            bare_soil_index,
            saturation_index
        ]]

        print("Sample feature vector:", feature_vector)
        X = np.array(feature_vector)

        X_scaled = sat_scaler.transform(X)

        prob = sat_model.predict_proba(X_scaled)[0][1]
        print("prob:", prob)
        if slope < 5 or elevation < 600:
            prob = 0

        results.append({
            "grid_uid": row.grid_uid,
            "risk": float(prob)
        })

    return {"results": results}
