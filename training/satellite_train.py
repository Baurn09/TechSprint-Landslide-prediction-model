import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from sklearn.linear_model import LogisticRegression

<<<<<<< HEAD
# ==================================================
# STEP 1: LOADING & PREPROCESSING
# ==================================================
print("\n--- Loading Satellite Training Data ---")
=======

print("\n--- Loading Landslide Training Data ---")
>>>>>>> 3bdec942a1cdffe2d2197998236f016e849c13b1

df = pd.read_csv("landslide_dataset.csv")
print(f"Dataset Loaded | Shape: {df.shape}")

# ==================================================
# STEP 1: BASIC CLEANING
# ==================================================

df.drop(columns=["system:index", "date", ".geo"], inplace=True, errors="ignore")
df.drop_duplicates(inplace=True)
<<<<<<< HEAD
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
=======
df.fillna(df.median(numeric_only=True), inplace=True)
>>>>>>> 3bdec942a1cdffe2d2197998236f016e849c13b1

# ==================================================
# STEP 2: FEATURE ENGINEERING (PHYSICS-AWARE)
# ==================================================

<<<<<<< HEAD
# NOTE: The template clipped values to 1.0. 
# Since raw satellite data (Elevation/Rain) exceeds 1.0, 
# we skip clipping here to preserve data variance for the Scaler.
# df[["R", "V", "S", "E", "P", "H"]].clip(0.0, 1.0, inplace=True)
=======
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
>>>>>>> 3bdec942a1cdffe2d2197998236f016e849c13b1

TARGET = "landslide"

X = df[FEATURES]
y = df[TARGET]

# ==================================================
<<<<<<< HEAD
# STEP 2: DATA SPLITTING & SCALING
# ==================================================
=======
# STEP 4: TRAIN / TEST SPLIT
# ==================================================

>>>>>>> 3bdec942a1cdffe2d2197998236f016e849c13b1
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

<<<<<<< HEAD
=======
# ==================================================
# STEP 5: SCALING (VERY IMPORTANT FOR LOGISTIC)
# ==================================================

>>>>>>> 3bdec942a1cdffe2d2197998236f016e849c13b1
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, "landslide_scaler.pkl")
print("Scaler saved.")

# ==================================================
<<<<<<< HEAD
# STEP 3: GRADIENT BOOSTED TREE MODEL
=======
# STEP 6: LOGISTIC REGRESSION MODEL
>>>>>>> 3bdec942a1cdffe2d2197998236f016e849c13b1
# ==================================================

<<<<<<< HEAD
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
=======
print("\n--- Training Logistic Regression Model ---")

model = LogisticRegression(
    max_iter=2000,
    class_weight="balanced",  # important for rare landslides
    solver="lbfgs",
    random_state=42
>>>>>>> 3bdec942a1cdffe2d2197998236f016e849c13b1
)

model.fit(X_train_scaled, y_train)

joblib.dump(model, "landslide_logistic_model.pkl")
print("Landslide Logistic Regression model trained & saved.")

# ==================================================
<<<<<<< HEAD
# STEP 4: MODEL EVALUATION
=======
# STEP 7: EVALUATION
>>>>>>> 3bdec942a1cdffe2d2197998236f016e849c13b1
# ==================================================

print("\n--- Model Evaluation ---")

y_pred = model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
print(f"\n✅ Model Accuracy: {accuracy * 100:.2f}%\n")

print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=["No Landslide", "Landslide"]))

# ==================================================
<<<<<<< HEAD
# STEP 5: REAL-WORLD SCENARIO TEST
=======
# STEP 8: REAL-WORLD SCENARIO TEST
>>>>>>> 3bdec942a1cdffe2d2197998236f016e849c13b1
# ==================================================

print("\n--- Real-World Scenario Simulation ---")

# Example input values based on dataset scales
# Format: [Rain, NDVI, Slope, Elevation, Population, SoilMoisture, Interaction]
test_samples = np.array([
<<<<<<< HEAD
    [5.0, 0.5, 2.0, 100.0, 10.0, 0.1, 10.0],    # Low risk (low rain, low slope)
    [80.0, 0.2, 35.0, 800.0, 50.0, 0.4, 2800.0] # High risk (heavy rain, steep slope)
=======
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
>>>>>>> 3bdec942a1cdffe2d2197998236f016e849c13b1
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

<<<<<<< HEAD
    print(f"Scenario {i + 1}: {risk}% → {status}")
=======

    print(f"Scenario {i + 1}: {risk}% → {status}")
>>>>>>> 3bdec942a1cdffe2d2197998236f016e849c13b1
