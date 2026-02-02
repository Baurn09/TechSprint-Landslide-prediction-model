import pandas as pd
import numpy as np
import xgboost as xgb
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

# ==================================================
# STEP 1: LOADING & PREPROCESSING
# ==================================================
print("\n--- Loading Satellite Training Data ---")

df = pd.read_csv("satellite_training_data.csv")
print(f"Dataset Loaded | Shape: {df.shape}")

# Basic cleaning
df.drop_duplicates(inplace=True)
# Select only numeric columns for median calculation to avoid errors with date/.geo
numeric_cols = df.select_dtypes(include=[np.number]).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

# Mapping CSV columns to the logic in your template
# R=rain_7d, V=ndvi, S=slope, E=elevation, P=population, H=soil_moisture
df['R'] = df['rain_7d']
df['V'] = df['ndvi']
df['S'] = df['slope']
df['E'] = df['elevation']
df['P'] = df['population']
df['H'] = df['soil_moisture']

# Feature engineering (rainfall on slope interaction)
df["Rain_on_Slope"] = df["R"] * df["S"]

# NOTE: The template clipped values to 1.0. 
# Since raw satellite data (Elevation/Rain) exceeds 1.0, 
# we skip clipping here to preserve data variance for the Scaler.
# df[["R", "V", "S", "E", "P", "H"]].clip(0.0, 1.0, inplace=True)

# Features & target
FEATURES = ["R", "V", "S", "E", "P", "H", "Rain_on_Slope"]
TARGET = "landslide"

X = df[FEATURES]
y = df[TARGET]

# ==================================================
# STEP 2: DATA SPLITTING & SCALING
# ==================================================
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, "satellite_scaler.pkl")
print("Scaler saved.")

# ==================================================
# STEP 3: GRADIENT BOOSTED TREE MODEL
# ==================================================
print("\n--- Training Gradient Boosted Tree (XGBoost) ---")

gbt_model = XGBClassifier(
    n_estimators=800,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)

gbt_model.fit(X_train_scaled, y_train)

joblib.dump(gbt_model, "satellite_gbt_model.pkl")
print("Satellite GBT model trained & saved.")

# ==================================================
# STEP 4: MODEL EVALUATION
# ==================================================
print("\n--- Model Evaluation ---")

y_pred = gbt_model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
accuracy_percent = int(round(accuracy * 100))

print(f"\n✅ Satellite Model Accuracy: {accuracy_percent}%\n")

print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=["No Landslide", "Landslide"]))

# ==================================================
# STEP 5: REAL-WORLD SCENARIO TEST
# ==================================================
print("\n--- Real-World Scenario Simulation ---")

# Example input values based on dataset scales
# Format: [Rain, NDVI, Slope, Elevation, Population, SoilMoisture, Interaction]
test_samples = np.array([
    [5.0, 0.5, 2.0, 100.0, 10.0, 0.1, 10.0],    # Low risk (low rain, low slope)
    [80.0, 0.2, 35.0, 800.0, 50.0, 0.4, 2800.0] # High risk (heavy rain, steep slope)
])

test_samples_scaled = scaler.transform(test_samples)
probs = gbt_model.predict_proba(test_samples_scaled)

for i, p in enumerate(probs):
    risk = int(round(p[1] * 100))

    if risk < 40:
        status = "✅ LOW RISK"
    elif risk < 70:
        status = "🟠 MODERATE RISK"
    else:
        status = "🚨 HIGH RISK"

    print(f"Scenario {i + 1}: {risk}% → {status}")