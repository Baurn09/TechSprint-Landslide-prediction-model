import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression


print("\n--- Loading Landslide Training Data ---")

df = pd.read_csv("landslide_dataset.csv")
print(f"Dataset Loaded | Shape: {df.shape}")

# ==================================================
# STEP 1: BASIC CLEANING
# ==================================================

df.drop(columns=["system:index", "date", ".geo"], inplace=True, errors="ignore")
df.drop_duplicates(inplace=True)
df.fillna(df.median(numeric_only=True), inplace=True)

# ==================================================
# STEP 1.5: DATASET BALANCING (UNDERSAMPLING)
# ==================================================

pos = df[df.landslide == 1]
neg = df[df.landslide == 0].sample(len(pos), random_state=42)

df = pd.concat([pos, neg]).sample(frac=1, random_state=42).reset_index(drop=True)

print(f"Balanced Dataset | Landslide: {len(pos)} | No Landslide: {len(neg)}")


# ==================================================
# STEP 2: FEATURE ENGINEERING (PHYSICS-AWARE)
# ==================================================

# Rainfall + slope interaction
df["rain_slope_interaction"] = df["rain_7d"] * df["slope"]

# Short vs long rainfall accumulation ratio
df["rain_intensity_ratio"] = df["rain_1d"] / (df["rain_30d"] + 1e-6)

# Vegetation protection inverse
df["bare_soil_index"] = 1.0 - df["ndvi"]

# Soil saturation effect (VERY IMPORTANT)
df["saturation_index"] = df["rain_30d"] * df["soil_moisture"]


# ==================================================
# STEP 3: FEATURE SELECTION
# ==================================================

FEATURES = [
    "elevation",
    "ndvi",
    "population",
    "rain_1d",
    "rain_7d",
    "rain_30d",
    "slope",
    "soil_moisture",
    "soil_type",
    "rain_slope_interaction",
    "rain_intensity_ratio",
    "bare_soil_index",
    "saturation_index"
]

TARGET = "landslide"

X = df[FEATURES]
y = df[TARGET]

# ==================================================
# STEP 4: TRAIN / TEST SPLIT
# ==================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==================================================
# STEP 5: SCALING (VERY IMPORTANT FOR LOGISTIC)
# ==================================================

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, "landslide_scaler.pkl")
print("Scaler saved.")

# ==================================================
# STEP 6: LOGISTIC REGRESSION MODEL
# ==================================================

print("\n--- Training Logistic Regression Model ---")

model = LogisticRegression(
    max_iter=2000,
    solver="lbfgs",
    random_state=42
)

model.fit(X_train_scaled, y_train)

joblib.dump(model, "landslide_logistic_model.pkl")
print("Landslide Logistic Regression model trained & saved.")

# ==================================================
# STEP 7: EVALUATION
# ==================================================

print("\n--- Model Evaluation ---")

y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Model Accuracy: {accuracy * 100:.2f}%\n")

print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=["No Landslide", "Landslide"]))

# ==================================================
# STEP 8: REAL-WORLD SCENARIO TEST
# ==================================================

print("\n--- Real-World Scenario Simulation ---")

test_samples = np.array([
    # HIGH RISK
    [
    900,        # elevation
    0.15,       # ndvi (very sparse vegetation)
    15.0,       # population
    120.0,      # rain_1d (extreme rainfall)
    220.0,      # rain_7d (persistent heavy rain)
    560.0,      # rain_30d (fully saturated month)
    5.5,        # slope (very steep)
    0.40,       # soil_moisture (near saturation)
    2,          # soil_type (weak / loose soil)
    220.0 * 5.5,# rain_slope_interaction
    120.0 / 560.0, # rain_intensity_ratio
    1 - 0.15,   # bare_soil_index
    560.0 * 0.40   # saturation_index
    ],

    # LOW RISK
    [
    520,        # elevation
    0.85,       # ndvi (dense vegetation)
    85.0,       # population
    0.8,        # rain_1d (almost no rain)
    3.0,        # rain_7d (very low rain)
    40.0,       # rain_30d (dry month)
    0.9,        # slope (almost flat)
    0.04,       # soil_moisture (very dry)
    4,          # soil_type (stable soil)
    3.0 * 0.9,  # rain_slope_interaction
    0.8 / 40.0, # rain_intensity_ratio
    1 - 0.85,    # bare_soil_index
    40.0 * 0.04   # saturation_index
    ]
])

test_samples_scaled = scaler.transform(test_samples)
probs = model.predict_proba(test_samples_scaled)

for i, p in enumerate(probs):
    risk = int(round(p[1] * 100))

    if risk < 35:
        status = "✅ LOW RISK"
    elif risk < 60:
        status = "🟠 MODERATE RISK"
    else:
        status = "🚨 HIGH RISK"


    print(f"Scenario {i + 1}: {risk}% → {status}")
