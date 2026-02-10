import pandas as pd
import geopandas as gpd
import requests
import os
import sys

# =========================================
# PATHS
# =========================================

BASE_DIR = os.path.dirname(__file__)

FEATURE_CSV = os.path.join(BASE_DIR, "grid_features_ml.csv")
GRID_GEOJSON = os.path.join(BASE_DIR, "../web/public/data/grid_features_geojson.geojson")

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
# CHECK FILES
# =========================================

if not os.path.exists(FEATURE_CSV):
    print("❌ Feature CSV not found")
    sys.exit(1)

if not os.path.exists(GRID_GEOJSON):
    print("❌ Grid GeoJSON not found")
    sys.exit(1)


# =========================================
# LOAD FEATURE CSV
# =========================================

print("📂 Loading feature CSV...")
df = pd.read_csv(FEATURE_CSV)

print("Rows:", len(df))

# Clean NaN for JSON safety
df = df.replace([float("inf"), -float("inf")], 0)
df = df.fillna(0)

# =========================================
# DERIVED FEATURES (MUST MATCH TRAINING)
# =========================================

df["rain_slope_interaction"] = df["rain_7d"] * df["slope"]

df["rain_intensity_ratio"] = df["rain_1d"] / (df["rain_30d"] + 1e-6)

df["bare_soil_index"] = 1.0 - df["ndvi"]

df["saturation_index"] = df["rain_30d"] * df["soil_moisture"]



# =========================================
# REQUIRED ML FEATURES
# =========================================

REQUIRED = [
    "grid_uid",
    "elevation",
    "ndvi",
    "bare_soil_index",
    "population",
    "rain_1d",
    "rain_7d",
    "rain_30d",
    "rain_intensity_ratio",
    "slope",
    "rain_slope_interaction",
    "soil_moisture",
    "saturation_index",
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

data = resp.json()
print("API keys:", data.keys())
print("First row:", data["results"][0])
print("✅ Predictions received")


# =========================================
# LOAD REAL GRID POLYGONS
# =========================================

print("🗺️ Loading grid polygons...")
gdf = gpd.read_file(GRID_GEOJSON)

print("Polygons:", len(gdf))

print("CSV grid_uids:", len(set(risk_df["grid_uid"])))
print("GeoJSON grid_uids:", len(set(gdf["grid_uid"])))

common = set(risk_df["grid_uid"]) & set(gdf["grid_uid"])
print("Common IDs:", len(common))

# =========================================
# MERGE RISK INTO POLYGONS
# =========================================

gdf = gdf.merge(risk_df, on="grid_uid", how="left")
gdf["risk"] = gdf["risk"].fillna(0)


# =========================================
# SAVE FINAL RISK MAP
# =========================================

os.makedirs(os.path.dirname(OUTPUT_GEOJSON), exist_ok=True)

gdf.to_file(OUTPUT_GEOJSON, driver="GeoJSON")

print("✅ Saved risk map:")
print(OUTPUT_GEOJSON)

print("🚀 Grid inference complete")
