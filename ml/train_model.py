import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# 🔥 READ WITH CORRECT ENCODING
data = pd.read_csv("landslide_data.csv", encoding="utf-16")

# 🔥 CLEAN HEADERS
data.columns = data.columns.str.strip().str.lower().str.replace(" ", "_")
print(data.columns)

X = data[['soil_moisture', 'tilt', 'vibration', 'rainfall', 'slope', 'ndvi']]
y = data['risk']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Accuracy:", accuracy_score(y_test, model.predict(X_test)))

joblib.dump(model, "landslide_model.pkl")
print("Model saved successfully")
