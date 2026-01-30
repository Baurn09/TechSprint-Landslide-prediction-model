import joblib
import pandas as pd

# Load model
model = joblib.load("landslide_model.pkl")

# Example live sensor + satellite input
sample = {
    "soil_moisture": 82,
    "tilt": 3.8,
    "vibration": 1.1,
    "rainfall": 75,
    "slope": 40,
    "ndvi": 0.22
}

df = pd.DataFrame([sample])

prediction = model.predict(df)
print("Predicted Landslide Risk:", prediction[0])
