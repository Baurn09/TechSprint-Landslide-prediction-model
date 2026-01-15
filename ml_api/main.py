from pathlib import Path
import pickle
import numpy as np
from fastapi import FastAPI

BASE_DIR = Path(__file__).resolve().parent
TRAINING_DIR = BASE_DIR.parent / "training"

app = FastAPI()

with open(TRAINING_DIR / "satellite_gbt_model.pkl", "rb") as f:
    model = pickle.load(f)

with open(TRAINING_DIR / "satellite_scaler.pkl", "rb") as f:
    scaler = pickle.load(f)




@app.post("/predict/satellite")
def predict_satellite(data: dict):
    features = np.array([data["features"]])
    features_scaled = satellite_scaler.transform(features)
    prediction = satellite_model.predict(features_scaled)

    return {
        "risk": int(prediction[0])
    }
