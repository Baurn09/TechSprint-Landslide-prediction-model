import { satelliteRiskGBM } from "@/lib/satelliteGBM";

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const area = searchParams.get("area") || "default";

  const d = satelliteData[area] || satelliteData.default;

  // Build feature vector explicitly
  const featureVector = {
    R: d.rainfall,
    V: d.vegetation,
    S: d.slope,
    E: d.elevation ?? 0.5, // fallback if missing
    P: d.soil,
    H: d.history,
  };

  const riskScore = satelliteRiskGBM(featureVector);

  let decision = "NO_DEPLOYMENT";
  if (riskScore >= 0.7) decision = "DEPLOY_SENSORS";
  else if (riskScore >= 0.4) decision = "MONITOR";

  return Response.json({
    area,
    features: featureVector,
    riskScore,
    decision,
    model: "Gradient Boosted Trees (Satellite-Based)",
  });
}
