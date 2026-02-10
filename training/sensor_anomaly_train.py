import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import IsolationForest
from filterpy.kalman import KalmanFilter

DATA_PATH = "sensor_training_data.csv"
MODEL_PATH = "sensor_anomaly_model.pkl"

df = pd.read_csv(DATA_PATH)

#Kalman Filter (tilt smoothing)
kf = KalmanFilter(dim_x=2, dim_z=1)
kf.x = np.array([[0.], [0.]])
kf.F = np.array([[1., 1.],[0., 1.]])
kf.H = np.array([[1., 0.]])
kf.P *= 1000
kf.R = 0.05
kf.Q = 0.01

features = []
prev_soil, prev_tilt = None, None

for _, row in df.iterrows():
    soil = row["soil_moisture"]
    tilt_raw = row["tilt"]
    vib = row["vibration"]

    kf.predict()
    kf.update(tilt_raw)
    tilt = kf.x[0, 0]

    if prev_soil is None:
        prev_soil, prev_tilt = soil, tilt
        continue

    features.append([
        soil,
        soil - prev_soil,
        tilt,
        tilt - prev_tilt,
        abs(vib)
    ])

    prev_soil, prev_tilt = soil, tilt

X = np.array(features)

#Isolation Forest
model = IsolationForest(
    n_estimators=150,
    contamination=0.05,
    random_state=42
)

model.fit(X)

joblib.dump(model, MODEL_PATH)
print("✅ Sensor anomaly model trained and saved")
