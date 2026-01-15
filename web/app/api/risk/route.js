export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const area = searchParams.get("area") || "default";

  // 1️⃣ Fetch satellite risk
  const satRes = await fetch(
    `${process.env.NEXT_PUBLIC_BASE_URL}/api/satellite?area=${area}`
  );
  const satelliteData = await satRes.json();
  const satelliteRisk = satelliteData.riskScore;

  let sensorRisk = null;
  let finalRisk = satelliteRisk;

  // 2️⃣ Fetch sensor risk ONLY if sensors exist
  try {
    const sensorRes = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/sensor?area=${area}`
    );
    const sensorData = await sensorRes.json();
    sensorRisk = sensorData.riskScore;

    // 3️⃣ FUSION LOGIC (THIS IS YOUR LINE)
    finalRisk =
      0.6 * satelliteRisk +
      0.4 * sensorRisk;
  } catch {
    // no sensors → satellite-only risk
    finalRisk = satelliteRisk;
  }

  // 4️⃣ Alert levels
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
