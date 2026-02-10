import pandas as pd

df = pd.read_csv("../grid_gen/grid_features_ml.csv")
df.to_json("../web/public/data/grid_features_ml.json", orient="records")

print("✅ JSON created")