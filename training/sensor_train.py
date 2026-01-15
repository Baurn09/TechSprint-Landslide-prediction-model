import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# ---------------------------
# Load dataset
# ---------------------------
# Columns:
# soilMoisture, tilt, vibration, magnitude, unstable
data = pd.read_csv("sensor_training_data.csv")

X = data[[
    "soilMoisture",
    "tilt",
    "vibration",
    "magnitude"
]]

y = data["unstable"]  # 0 or 1

# ---------------------------
# Train / test split
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------
# Model
# ---------------------------
rf = RandomForestClassifier(
    n_estimators=400,
    max_depth=6,
    min_samples_split=5,
    random_state=42
)

rf.fit(X_train, y_train)

# ---------------------------
# Evaluation
# ---------------------------
pred = rf.predict(X_test)
print("Sensor Model Accuracy:", accuracy_score(y_test, pred))

# ---------------------------
# Save model
# ---------------------------
joblib.dump(rf, "sensor_model.pkl")
print("Sensor model saved")
