import { sensorRiskRandomForest } from "@/lib/sensorRandomForest";

export async function GET(request) {
  ...
  const motion = deriveMotionMetrics();

  const features = {
    soilMoisture: state.soilMoisture,
    tilt: motion.tilt,
    vibration: motion.vibration,
    magnitude: motion.magnitude,
  };

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
