import pandas as pd
import requests
import json
import os
import sys

# =========================================
# PATHS
# =========================================

BASE_DIR = os.path.dirname(__file__)

GRID_CSV = os.path.join(BASE_DIR, "grid_features_ml.csv")

OUTPUT_GEOJSON = os.path.join(
    BASE_DIR,
    "..",
    "web",
    "public",
    "data",
    "grid_risk.geojson"
)

API_URL = "http://localhost:8000/predict/grid"


# =========================================
# CHECK FILE
# =========================================

if not os.path.exists(GRID_CSV):
    print("❌ grid csv not found")
    sys.exit(1)

print("📂 Loading grid CSV...")
df = pd.read_csv(GRID_CSV)
print("✅ Rows:", len(df))

df = df.replace([float("inf"), -float("inf")], 0)
df = df.fillna(0)


# =========================================
# REQUIRED ML FEATURES
# =========================================

REQUIRED = [
    "grid_uid",
    "elevation",
    "ndvi",
    "population",
    "rain_1d",
    "rain_7d",
    "rain_30d",
    "slope",
    "soil_moisture",
    "soil_type"
]

missing = [c for c in REQUIRED if c not in df.columns]

if missing:
    print("❌ Missing required columns:", missing)
    sys.exit(1)


# =========================================
# CALL FASTAPI GRID MODEL
# =========================================

print("🧠 Sending rows to FastAPI model...")

rows = df[REQUIRED].to_dict("records")

resp = requests.post(API_URL, json={"rows": rows})

if resp.status_code != 200:
    print("❌ API error:", resp.text)
    sys.exit(1)

risk_df = pd.DataFrame(resp.json()["results"])

print("✅ Predictions received")


# =========================================
# MERGE RISK
# =========================================

df = df.merge(risk_df, on="grid_uid", how="left")
df["risk"] = df["risk"].fillna(0)


# =========================================
# CHECK LAT/LON EXIST
# =========================================

if "lat" not in df.columns or "lon" not in df.columns:
    print("❌ lat/lon missing — re-export grid with centroid coords from GEE")
    sys.exit(1)


# =========================================
# BUILD GEOJSON POLYGONS (3km visual cells)
# =========================================

print("🗺️ Building GeoJSON polygons...")

features = []

cell_half_deg = 0.015   # ~3km visual size

for _, row in df.iterrows():

    lat = row["lat"]
    lon = row["lon"]

    poly = [
        [lon-cell_half_deg, lat-cell_half_deg],
        [lon+cell_half_deg, lat-cell_half_deg],
        [lon+cell_half_deg, lat+cell_half_deg],
        [lon-cell_half_deg, lat+cell_half_deg],
        [lon-cell_half_deg, lat-cell_half_deg]
    ]

    features.append({
        "type": "Feature",
        "properties": {
            "grid_uid": row["grid_uid"],
            "risk": float(row["risk"])
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [poly]
        }
    })


geojson = {
    "type": "FeatureCollection",
    "features": features
}


# =========================================
# SAVE
# =========================================

os.makedirs(os.path.dirname(OUTPUT_GEOJSON), exist_ok=True)

with open(OUTPUT_GEOJSON, "w") as f:
    json.dump(geojson, f)

print("✅ Saved:", OUTPUT_GEOJSON)
print("🚀 Grid inference complete")
