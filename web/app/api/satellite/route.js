import fs from "fs";
import path from "path";

function readJSON(p) {
  if (!fs.existsSync(p)) {
    throw new Error("Missing file: " + p);
  }
  return JSON.parse(fs.readFileSync(p, "utf-8"));
}

const gridData = readJSON(
  path.join(process.cwd(), "public/data/grid_features_ml.json")
);

const riskGeo = readJSON(
  path.join(process.cwd(), "public/data/grid_risk_collab.geojson")
);

const satelliteData = {
  noney: { R: 0.90, V: 0.30, S: 0.80, E: 0.90, P: 0.10 },
  ukhrul: { R: 0.70, V: 0.20, S: 0.90, E: 0.90, P: 0.20 },
  tamenglong: { R: 0.85, V: 0.45, S: 0.80, E: 0.60, P: 0.50 },
  default: { R: 0.60, V: 0.70, S: 0.60, E: 0.70, P: 0.25 },
};

export async function GET(request) {

  try {

    const { searchParams } = new URL(request.url);
    const area = searchParams.get("area");
    const grid_uid = searchParams.get("grid_uid")?.trim();

    // ================= GRID MODE =================

    if (grid_uid) {

      const row = gridData.find(r =>
        String(r.grid_uid).trim() === grid_uid
      );

      if (!row) {
        return Response.json(
          { error: "Grid not found: " + grid_uid },
          { status: 404 }
        );
      }

      const features = {
        R: row.rain_7d / 200,
        V: row.ndvi,
        S: row.slope / 30,
        E: row.elevation / 2000,
        P: row.soil_moisture
      };

      const rawFeatures = {
        elevation: row.elevation,
        slope: row.slope,
        ndvi: row.ndvi,
        rain_1d: row.rain_1d,
        rain_7d: row.rain_7d,
        rain_30d: row.rain_30d,
        soil_moisture: row.soil_moisture,
        soil_type: row.soil_type,
        population: row.population
      };

      const riskFeature = riskGeo.features.find(f =>
        String(f.properties.grid_uid).trim() === grid_uid
      );

      const riskScore = riskFeature?.properties?.risk ?? 0;

      let decision = "NO_DEPLOYMENT";
      if (riskScore >= 0.7) decision = "DEPLOY_SENSORS";
      else if (riskScore >= 0.4) decision = "MONITOR";

      // ================= EXPLAINABILITY =================

      const contributions = {
        rainfall: features.R * 0.30,
        slope: features.S * 0.30,
        vegetation: (1 - features.V) * 0.20,
        soil: features.P * 0.20
      };

      const sorted = Object.entries(contributions)
        .sort((a, b) => b[1] - a[1]);

      const topDrivers = sorted.slice(0, 2).map(x => x[0]);


      return Response.json({
        target: grid_uid,
        mode: "grid",
        features,
        rawFeatures,
        riskScore,
        riskPercent: Math.round(riskScore * 100),
        decision,
        drivers: topDrivers,        // ⭐ NEW
        contributions,              // ⭐ NEW
        model: "Grid ML Inference"
      });
    }

    // ================= AREA MODE =================

    const f = satelliteData[area] || satelliteData.default;

    const response = await fetch(
      "http://127.0.0.1:8000/predict/satellite",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ features: [f.R, f.V, f.S, f.E, f.P] }),
      }
    );

    const ml = await response.json();

    return Response.json({
      target: area,
      mode: "area",
      features: f,
      riskScore: ml.riskScore,
      riskPercent: ml.riskPercent,
      decision: ml.riskScore >= 0.7 ? "DEPLOY_SENSORS"
               : ml.riskScore >= 0.4 ? "MONITOR"
               : "NO_DEPLOYMENT",
      model: "Satellite Logistic Model"
    });

  } catch (err) {

    console.error("Satellite API crash:", err);

    return Response.json(
      { error: "API crash", detail: String(err) },
      { status: 500 }
    );
  }
}
