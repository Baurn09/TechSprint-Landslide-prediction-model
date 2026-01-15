from pathlib import Path
import pickle
import numpy as np
from fastapi import FastAPI

BASE_DIR = Path(__file__).resolve().parent
TRAINING_DIR = BASE_DIR.parent / "training"

app = FastAPI()

<<<<<<< HEAD
with open(TRAINING_DIR / "satellite_gbt_model.pkl", "rb") as f:
    model = pickle.load(f)

with open(TRAINING_DIR / "satellite_scaler.pkl", "rb") as f:
    scaler = pickle.load(f)



=======
with open("../training/satellite_gbt_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("../training/satellite_scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
>>>>>>> 697a574495f79e7122473ba2ebe4fd0c478e7934

@app.post("/predict/satellite")
def predict_satellite(data: dict):
    X = np.array([data["features"]])
    X_scaled = scaler.transform(X)

    risk = model.predict_proba(X_scaled)[0][1]

    return {
        "riskScore": float(risk)
    }
