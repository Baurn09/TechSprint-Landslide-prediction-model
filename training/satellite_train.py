import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import joblib

# ---------------------------
# Load dataset
# ---------------------------
# Columns:
# R, V, S, E, P, H, landslide
data = pd.read_csv("satellite_training_data.csv")

X = data[["R", "V", "S", "E", "P", "H"]]
y = data["landslide"]  # 0 or 1

# ---------------------------
# Train / test split
# ---------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------------------
# Model
# ---------------------------
model = xgb.XGBClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric="logloss"
)

model.fit(X_train, y_train)

# ---------------------------
# Evaluation
# ---------------------------
pred = model.predict_proba(X_test)[:, 1]
print("Satellite Model AUC:", roc_auc_score(y_test, pred))

# ---------------------------
# Save model
# ---------------------------
joblib.dump(model, "satellite_model.pkl")
print("Satellite model saved")
