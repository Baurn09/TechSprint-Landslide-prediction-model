from fastapi import FastAPI
import pickle
import numpy as np

app = FastAPI()

with open("../training/satellite_gbt_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("../training/satellite_scaler.pkl", "rb") as f:
    scaler = pickle.load(f)

@app.post("/predict/satellite")
def predict_satellite(data: dict):
    X = np.array([data["features"]])
    X_scaled = scaler.transform(X)

    risk = model.predict_proba(X_scaled)[0][1]

    return {
        "riskScore": float(risk)
    }
