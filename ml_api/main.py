from fastapi import FastAPI
import numpy as np
from collections import deque
from ml_api.serial_reader import start_serial_thread, latest_sensor_data

app = FastAPI()

# ------------------ START SERIAL ------------------

@app.on_event("startup")
def startup_event():
    print("🚀 FastAPI starting...")
    start_serial_thread()

# ------------------ SENSOR CONFIG ------------------

WINDOW = 120  # calibration samples
SOIL_RATE_TH = 0.02
TILT_RATE_TH = 0.05
VIB_TH = 1.5

soil_buf = deque(maxlen=WINDOW)
tilt_buf = deque(maxlen=WINDOW)
vib_buf  = deque(maxlen=WINDOW)

prev_soil = None
prev_tilt = None

# ------------------ SENSOR ENDPOINT ------------------

@app.post("/predict/sensor")
def predict_sensor():
    global prev_soil, prev_tilt

    # 🔍 DEBUG: check if data reaches main.py
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

    # ---------------- CALIBRATION ----------------
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

    # ---------------- PHYSICS ----------------
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
