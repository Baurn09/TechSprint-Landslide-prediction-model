export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const area = searchParams.get("area") || "default";

  const baseUrl = process.env.NEXT_PUBLIC_BASE_URL || "http://localhost:3000";

  /* ---------- satellite risk ---------- */
  const satRes = await fetch(`${baseUrl}/api/satellite?area=${area}`);
  const satData = await satRes.json();
  const satelliteRisk = satData.riskScore;

  let sensorRisk = null;
  let finalRisk = satelliteRisk;

  /* ---------- sensor risk (if deployed) ---------- */
  try {
    const sensorRes = await fetch(`${baseUrl}/api/sensor?area=${area}`);
    const sensorData = await sensorRes.json();
    sensorRisk = sensorData.riskScore;

    // Dense sensor deployment → sensor dominates
    finalRisk = 0.3 * satelliteRisk + 0.7 * sensorRisk;
  } catch {
    finalRisk = satelliteRisk;
  }

  /* ---------- alert level ---------- */
  let alertLevel = "GREEN";
  if (finalRisk >= 0.75) alertLevel = "RED";
  else if (finalRisk >= 0.45) alertLevel = "YELLOW";

  return Response.json({
    area,
    satelliteRisk,
    sensorRisk,
    finalRisk: Number(finalRisk.toFixed(2)),
    alertLevel,
    model: "Satellite (GBDT) + Sensor (RF) Fusion",
  });
}
