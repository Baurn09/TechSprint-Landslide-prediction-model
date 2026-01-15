// Random Forest for Ground Sensor Risk Estimation

const trees = [
  // Tree 1: Soil saturation focused
  (f) =>
    f.soilMoisture > 85
      ? 0.9
      : f.soilMoisture > 70
      ? 0.6
      : 0.2,

  // Tree 2: Tilt-based instability
  (f) =>
    f.tilt > 0.25
      ? 0.85
      : f.tilt > 0.15
      ? 0.55
      : 0.2,

  // Tree 3: Vibration detection
  (f) =>
    f.vibration > 0.03
      ? 0.8
      : f.vibration > 0.015
      ? 0.5
      : 0.2,

  // Tree 4: Acceleration magnitude
  (f) =>
    f.magnitude > 0.35
      ? 0.75
      : f.magnitude > 0.2
      ? 0.45
      : 0.2,

  // Tree 5: Combined failure pattern
  (f) =>
    f.soilMoisture > 75 &&
    f.tilt > 0.18 &&
    f.vibration > 0.02
      ? 0.95
      : 0.3,
];

export function sensorRiskRandomForest(features) {
  const scores = trees.map((tree) => tree(features));
  const avg =
    scores.reduce((a, b) => a + b, 0) / scores.length;

  return Number(avg.toFixed(2));
}
