import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
from xgboost import XGBClassifier

# ==================================================
# STEP 1: LOAD & CLEAN DATA
# ==================================================
print("\n--- Loading Satellite Training Data ---")

df = pd.read_csv("satellite_training_data.csv")
print(f"Dataset Loaded | Shape: {df.shape}")

# Basic cleaning
df.drop_duplicates(inplace=True)
df.fillna(df.median(), inplace=True)

# Feature engineering (rainfall on slope interaction)
df["Rain_on_Slope"] = df["R"] * df["S"]

# Clip values to physical bounds
cols_to_clip = ["R", "V", "S", "E", "P", "H"]
df[cols_to_clip] = df[cols_to_clip].clip(0.0, 1.0)

# Features & target
FEATURES = ["R", "V", "S", "E", "P", "H", "Rain_on_Slope"]
TARGET = "landslide"

X = df[FEATURES]
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
# STEP 3: SCALING (Optional for tree models)
# ==================================================
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, "satellite_scaler.pkl")
print("Scaler saved.")

# ==================================================
# STEP 4: GRADIENT BOOSTED TREE MODEL
# ==================================================
print("\n--- Training Gradient Boosted Tree (XGBoost) ---")

gbt_model = XGBClassifier(
    n_estimators=300,
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
# STEP 5: MODEL EVALUATION
# ==================================================
print("\n--- Model Evaluation ---")

y_pred = gbt_model.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
accuracy_percent = int(round(accuracy * 100))

print(f"\n✅ Satellite Model Accuracy: {accuracy_percent}%\n")

print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=["No Landslide", "Landslide"]))

# ==================================================
# STEP 6: REAL-WORLD SCENARIO TEST
# ==================================================
print("\n--- Real-World Scenario Simulation ---")

test_samples = np.array([
    [0.30, 0.70, 0.40, 0.50, 0.40, 0.20, 0.12],  # Low risk
    [0.85, 0.35, 0.90, 0.70, 0.75, 0.85, 0.85 * 0.90]   # High risk
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
