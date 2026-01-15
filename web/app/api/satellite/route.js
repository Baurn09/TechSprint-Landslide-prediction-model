import { satelliteRiskGBM } from "../../lib/satelliteGBM";

const satelliteData = {
  noney: {
    R: 0.90, // rainfall
    V: 0.30, // vegetation (NDVI)
    S: 0.80, // slope
    E: 0.90, // elevation
    P: 0.10, // soil proxy
    H: 0.90, // historical susceptibility
  },
  ukhrul: {
    R: 0.70,
    V: 0.20,
    S: 0.90,
    E: 0.90,
    P: 0.20,
    H: 0.85,
  },
  tamenglong: {
    R: 0.85,
    V: 0.45,
    S: 0.80,
    E: 0.60,
    P: 0.50,
    H: 0.70,
  },
  default: {
    R: 0.80,
    V: 0.90,
    S: 0.80,
    E: 0.70,
    P: 0.25,
    H: 0.90,
  },
};

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const area = searchParams.get("area") || "default";

  const features = satelliteData[area] || satelliteData.default;

  // 🔹 ML inference
  const riskScore =   satelliteRiskGBM(features);

  let decision = "NO_DEPLOYMENT";
  if (riskScore >= 0.7) decision = "DEPLOY_SENSORS";
  else if (riskScore >= 0.4) decision = "MONITOR";

  return Response.json({
    area,
    features,
    riskScore,
    decision,
    model: "Gradient Boosted Trees (Satellite)",
  });
}
