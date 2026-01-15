// app/api/satellite/route.js

const satelliteData = {
  noney: {
    slope: 0.85,
    rainfall: 0.78,
    vegetation: 0.40,
    soil: 0.70,
    history: 0.80,
  },
  ukhrul: {
    slope: 0.90,
    rainfall: 0.65,
    vegetation: 0.45,
    soil: 0.75,
    history: 0.85,
  },
  tamenglong: {
    slope: 0.80,
    rainfall: 0.85,
    vegetation: 0.45,
    soil: 0.50,
    history: 0.70,
  },
  default: {
    slope: 0.60,
    rainfall: 0.90,
    vegetation: 0.50,
    soil: 0.40,
    history: 0.30,
  },
};

function calculateRisk(d) {
  return Number(
    (
      0.3 * d.slope +
      0.25 * d.rainfall +
      0.2 * (1 - d.vegetation) +
      0.15 * d.soil +
      0.1 * d.history
    ).toFixed(2)
  );
}

function generateTrend(base) {
  return Array.from({ length: 10 }, () =>
    Number((base + (Math.random() - 0.5) * 0.1).toFixed(2))
  );
}


export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const area = searchParams.get("area") || "default";

  const data = satelliteData[area] || satelliteData.default;
  const riskScore = calculateRisk(data);

  let decision = "NO_DEPLOYMENT";
  if (riskScore >= 0.5) decision = "DEPLOY_SENSORS";
  else if (riskScore >= 0.5) decision = "MONITOR";

  return Response.json({
    area,
    ...data,
    riskScore,
    decision,
    trends: {
      slope: generateTrend(data.slope),
      rainfall: generateTrend(data.rainfall),
      vegetation: generateTrend(data.vegetation),
      soil: generateTrend(data.soil),
      history: generateTrend(data.history),
    },
  });

}
