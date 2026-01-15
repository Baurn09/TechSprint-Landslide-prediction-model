// app/api/sensors/route.js

let state = {
  soilMoisture: 55, // %
  rainfall: 0,      // mm/hr
  tilt: 0.02,       // degrees
  phase: "DRY",     // DRY → RAIN → SATURATED
};

function simulateRainfall() {
  const chance = Math.random();

  if (chance < 0.2) {
    return 0; // no rain
  }
  if (chance < 0.6) {
    return Math.floor(5 + Math.random() * 10); // light rain
  }
  return Math.floor(15 + Math.random() * 20); // heavy rain
}

function updateState(area) {
  const areaFactor =
    area === "tamenglong" || area === "ukhrul" || area === "noney"
      ? 1.3 // hilly zones
      : 1.0; // moderate zones

  state.rainfall = simulateRainfall() * areaFactor;

  if (state.rainfall > 0) {
    state.soilMoisture += state.rainfall * 0.3;
  } else {
    state.soilMoisture -= 1;
  }

  state.soilMoisture = Math.min(Math.max(state.soilMoisture, 40), 95);

  if (state.soilMoisture < 65) state.phase = "DRY";
  else if (state.soilMoisture < 80) state.phase = "RAIN";
  else state.phase = "SATURATED";

  if (state.phase === "SATURATED") {
    state.tilt += Math.random() * 0.03 * areaFactor;
  } else {
    state.tilt -= 0.005;
  }

  state.tilt = Math.max(state.tilt, 0.01);
}


function calculateRisk(area) {
  const reasons = [];

  if (state.soilMoisture > 65) reasons.push("High soil moisture");
  if (state.rainfall > 10) reasons.push("Heavy rainfall");
  if (state.tilt > 0.15) reasons.push("Accelerating ground tilt");

  let riskLevel = "SAFE";

  if (
    state.soilMoisture > 80 &&
    state.rainfall > 15 &&
    state.tilt > 0.18
  ) {
    riskLevel = "CRITICAL";
  } else if (state.soilMoisture > 65) {
    riskLevel = "WARNING";
  }

  return { riskLevel, reasons };
}


export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const area = searchParams.get("area") || "default";

  updateState(area);

  const { riskLevel, reasons } = calculateRisk(area);

  return Response.json({
    area,
    timestamp: new Date().toISOString(),
    soilMoisture: Number(state.soilMoisture.toFixed(1)),
    rainfall: state.rainfall,
    tilt: Number(state.tilt.toFixed(3)),
    phase: state.phase,
    riskLevel,
    reasons,
  });
}

