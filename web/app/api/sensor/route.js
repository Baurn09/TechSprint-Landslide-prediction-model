export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const area = searchParams.get("area") || "default";

  let backend;

  try {
    backend = await fetch("http://127.0.0.1:8000/predict/sensor", {
      method: "POST",
    });
  } catch (err) {
    return Response.json(
      { error: "Backend unreachable" },
      { status: 500 }
    );
  }

  if (!backend.ok) {
    return Response.json(
      { error: "Sensor service unavailable" },
      { status: 500 }
    );
  }

  const ml = await backend.json();

  return Response.json({
    area,
    timestamp: new Date().toISOString(),

    // 👇 REAL SENSOR VALUES (from FastAPI)
    features: {
      soilMoisture: ml.soil,
      tilt: ml.tilt,
      vibration: ml.vibration,
    },

    riskScore: ml.riskScore,
    riskPercent: ml.riskPercent,
    status: ml.status,

    model: "Ground Sensor (Hardware)",
  });
}
