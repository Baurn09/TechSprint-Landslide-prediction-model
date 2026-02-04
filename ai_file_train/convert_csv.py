import json
import pandas as pd

with open("new_500_pts_landslides.geojson") as f:
    data = json.load(f)

rows = []
for feat in data["features"]:
    lon, lat = feat["geometry"]["coordinates"]
    props = feat["properties"]
    rows.append({
        "longitude": lon,
        "latitude": lat,
        "date": props["date"],
        "name": props["name"]
    })

df = pd.DataFrame(rows)
df.to_csv("new_500_pts_landslides.csv", index=False)

print("Saved CSV:", len(df))
