import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# ==================================================
# STEP 1: LOAD & PREPARE DATA
# ==================================================
print("\n--- Loading Ground Sensor Dataset ---")

df = pd.read_csv("sensor_training_data.csv")
print(f"Dataset Loaded | Shape: {df.shape}")

# Remove duplicates & handle missing values
df.drop_duplicates(inplace=True)
df.fillna(df.median(), inplace=True)

# Define features and target
FEATURES = ["soilMoisture", "tilt", "vibration", "magnitude"]
TARGET = "unstable"

X = df[FEATURES].clip(lower=0)
y = df[TARGET]

# ==================================================
# STEP 2: TRAIN–TEST SPLIT
# ==================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==================================================
# STEP 3: FEATURE SCALING
# ==================================================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, "sensor_scaler.pkl")
print("Scaler saved successfully.")

# ==================================================
# STEP 4: RANDOM FOREST TRAINING
# ==================================================
print("\n--- Training Random Forest Model ---")

rf_model = RandomForestClassifier(
    n_estimators=400,
    max_depth=6,
    min_samples_split=5,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1
)

rf_model.fit(X_train_scaled, y_train)

joblib.dump(rf_model, "sensor_random_forest.pkl")
print("Random Forest model trained & saved.")

# ==================================================
# STEP 5: MODEL EVALUATION
# ==================================================
print("\n--- Model Evaluation ---")

y_pred = rf_model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
accuracy_percent = int(round(accuracy * 100))

print(f"\n✅ Model Accuracy: {accuracy_percent}%\n")

print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=["Safe", "Danger"]))

# ==================================================
# STEP 6: REAL-WORLD SCENARIO TESTING
# ==================================================
print("\n--- Real-World Simulation ---")

test_samples = np.array([
    [45.0, 0.02, 0.01, 0.05],   # Normal conditions
    [90.0, 0.35, 0.04, 0.30]    # High-risk conditions
])

test_samples_scaled = scaler.transform(test_samples)
probabilities = rf_model.predict_proba(test_samples_scaled)

for i, prob in enumerate(probabilities):
    risk = int(round(prob[1] * 100))
    status = "🚨 HIGH RISK" if prob[1] > 0.5 else "✅ SAFE"
    print(f"Scenario {i + 1}: {risk}% → {status}")
