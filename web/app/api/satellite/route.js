const satelliteData = {
  noney: {
    R: 0.90,
    V: 0.30,
    S: 0.80,
    E: 0.90,
    P: 0.10,
    H: 0.90,
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

  const f = satelliteData[area] || satelliteData.default;

  // ✅ MATCH TRAINING FEATURE ORDER (Logistic Regression – Satellite)
  const featureVector = [
    f.R,
    f.V,
    f.S,
    f.E,
    f.P,
    f.H,
    f.R * f.S, // Rain_on_Slope
  ];

  // 🔥 CALL FASTAPI (REAL MODEL)
  const response = await fetch("http://127.0.0.1:8000/predict/satellite", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      features: featureVector,
    }),
  });

  if (!response.ok) {
    return Response.json(
      { error: "ML service unavailable" },
      { status: 500 }
    );
  }

  const mlResult = await response.json();

  let decision = "NO_DEPLOYMENT";
  if (mlResult.riskScore >= 0.7) decision = "DEPLOY_SENSORS";
  else if (mlResult.riskScore >= 0.4) decision = "MONITOR";

  return Response.json({
    area,
    features: f,
    riskScore: mlResult.riskScore,
    riskPercent: mlResult.riskPercent,
    decision,
    model: "Logistic Regression (Satellite)",
  });
}
