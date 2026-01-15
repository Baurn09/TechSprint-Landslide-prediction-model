import { satelliteRiskGBM } from "../../lib/satelliteGBM";

const satelliteData = {
  noney: {
    R: 0.78, // rainfall
    V: 0.42, // vegetation (NDVI)
    S: 0.85, // slope
    E: 0.66, // elevation
    P: 0.71, // soil proxy
    H: 0.80, // historical susceptibility
  },
  ukhrul: {
    R: 0.65,
    V: 0.45,
    S: 0.90,
    E: 0.70,
    P: 0.75,
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
    R: 0.50,
    V: 0.55,
    S: 0.60,
    E: 0.50,
    P: 0.45,
    H: 0.30,
  },
};

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const area = searchParams.get("area") || "default";

  const features = satelliteData[area] || satelliteData.default;

  // 🔹 ML inference
  const riskScore = satelliteRiskGBM(features);

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
