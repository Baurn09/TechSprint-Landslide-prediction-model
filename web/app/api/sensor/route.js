import { sensorRiskRandomForest } from "../../lib/sensorRandomForest";

/* ---------- persistent sensor state ---------- */
let state = {
  soilMoisture: 55,
  motion: { x: 0.02, y: 0.02, z: 0.01 },
};

/* ---------- helpers ---------- */

function updateSoilMoisture(areaFactor) {
  const delta =
    Math.random() < 0.6
      ? Math.random() * 1.5
      : Math.random() * 3.5;

  state.soilMoisture += delta * areaFactor;
  state.soilMoisture = Math.min(Math.max(state.soilMoisture, 40), 95);
}

function updateMotion(areaFactor) {
  state.motion.x += (Math.random() - 0.5) * 0.01 * areaFactor;
  state.motion.y += (Math.random() - 0.5) * 0.01 * areaFactor;
  state.motion.z = Math.abs((Math.random() - 0.5) * 0.05 * areaFactor);

  state.motion.x = Math.max(Math.min(state.motion.x, 0.4), -0.4);
  state.motion.y = Math.max(Math.min(state.motion.y, 0.4), -0.4);
}

function deriveMotionMetrics() {
  const { x, y, z } = state.motion;
  return {
    tilt: Math.sqrt(x * x + y * y),
    vibration: Math.abs(z),
    magnitude: Math.sqrt(x * x + y * y + z * z),
  };
}

/* ---------- API ---------- */

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const area = searchParams.get("area") || "default";

  const areaFactor =
    area === "noney" || area === "ukhrul" || area === "tamenglong"
      ? 1.4
      : 1.0;

  updateSoilMoisture(areaFactor);
  updateMotion(areaFactor);

  const motion = deriveMotionMetrics();

  const features = {
    soilMoisture: state.soilMoisture,
    tilt: motion.tilt,
    vibration: motion.vibration,
    magnitude: motion.magnitude,
  };

  // 🔹 ML inference
  const riskScore = sensorRiskRandomForest(features);

  return Response.json({
    area,
    timestamp: new Date().toISOString(),
    features: {
      soilMoisture: Number(features.soilMoisture.toFixed(1)),
      tilt: Number(features.tilt.toFixed(3)),
      vibration: Number(features.vibration.toFixed(3)),
      magnitude: Number(features.magnitude.toFixed(3)),
    },
    riskScore,
    model: "Random Forest (Ground Sensors)",
  });
}
