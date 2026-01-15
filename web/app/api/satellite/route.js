import { satelliteRiskGBM } from "../../lib/satelliteGBM";

const satelliteData = {
  noney: {
    slope: 0.85,
    rainfall: 0.78,
    vegetation: 0.40,
    soil: 0.70,
    history: 0.80,
    elevation: 0.65,
  },
  ukhrul: {
    slope: 0.90,
    rainfall: 0.65,
    vegetation: 0.45,
    soil: 0.75,
    history: 0.85,
    elevation: 0.70,
  },
  tamenglong: {
    slope: 0.80,
    rainfall: 0.85,
    vegetation: 0.45,
    soil: 0.50,
    history: 0.70,
    elevation: 0.60,
  },
  default: {
    slope: 0.60,
    rainfall: 0.50,
    vegetation: 0.55,
    soil: 0.45,
    history: 0.30,
    elevation: 0.50,
  },
};

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const area = searchParams.get("area") || "default";

  const d = satelliteData[area] || satelliteData.default;

  const features = {
    R: d.rainfall,
    V: d.vegetation,
    S: d.slope,
    E: d.elevation,
    P: d.soil,
    H: d.history,
  };

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
