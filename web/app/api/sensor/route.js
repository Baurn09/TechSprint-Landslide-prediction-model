// app/api/sensor/route.js

// Persistent state (simulates continuous sensor readings)
let state = {
  soilMoisture: 55, // %
  motion: {
    x: 0.02,
    y: 0.02,
    z: 0.01,
  },
};

// ---------- helpers ----------

// simulate slow soil moisture change
function updateSoilMoisture(areaFactor) {
  const delta =
    Math.random() < 0.6
      ? Math.random() * 1.5 // slow drying
      : Math.random() * 3.5; // wetting event

  state.soilMoisture += delta * areaFactor;
  state.soilMoisture = Math.min(
    Math.max(state.soilMoisture, 40),
    95
  );
}

// simulate 3-axis motion sensor
function updateMotion(areaFactor) {
  // slow tilt drift (slope movement)
  state.motion.x += (Math.random() - 0.5) * 0.01 * areaFactor;
  state.motion.y += (Math.random() - 0.5) * 0.01 * areaFactor;

  // vertical vibration (micro slips / tremors)
  state.motion.z =
    Math.abs((Math.random() - 0.5) * 0.05 * areaFactor);

  // clamp values
  state.motion.x = Math.max(
    Math.min(state.motion.x, 0.4),
    -0.4
  );
  state.motion.y = Math.max(
    Math.min(state.motion.y, 0.4),
    -0.4
  );
}

// derive metrics from raw motion
function deriveMotionMetrics() {
  const { x, y, z } = state.motion;

  const tilt = Math.sqrt(x * x + y * y);
  const vibration = Math.abs(z);
  const magnitude = Math.sqrt(
    x * x + y * y + z * z
  );

  return {
    x,
    y,
    z,
    tilt,
    vibration,
    magnitude,
  };
}

// ---------- main ----------

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const area = searchParams.get("area") || "default";

  // hilly zones behave worse
  const areaFactor =
    area === "tamenglong" ||
    area === "ukhrul" ||
    area === "noney"
      ? 1.4
      : 1.0;

  updateSoilMoisture(areaFactor);
  updateMotion(areaFactor);

  const motion = deriveMotionMetrics();

  return Response.json({
    area,
    timestamp: new Date().toISOString(),
    soilMoisture: Number(state.soilMoisture.toFixed(1)),
    motion: {
      x: Number(motion.x.toFixed(3)),
      y: Number(motion.y.toFixed(3)),
      z: Number(motion.z.toFixed(3)),
      tilt: Number(motion.tilt.toFixed(3)),
      vibration: Number(motion.vibration.toFixed(3)),
      magnitude: Number(motion.magnitude.toFixed(3)),
    },
  });
}
