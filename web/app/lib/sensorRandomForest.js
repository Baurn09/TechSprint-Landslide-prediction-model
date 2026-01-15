// lib/sensorRandomForest.js
// Random Forest style inference for real-time ground sensor data

/**
 * Each function represents a decision tree
 * Trees focus on different physical instability indicators
 */
const trees = [
  // Tree 1: Soil saturation
  (f) =>
    f.soilMoisture > 85 ? 0.9 :
    f.soilMoisture > 70 ? 0.6 :
    0.2,

  // Tree 2: Tilt-based instability
  (f) =>
    f.tilt > 0.25 ? 0.85 :
    f.tilt > 0.15 ? 0.55 :
    0.2,

  // Tree 3: Vibration (micro-slips)
  (f) =>
    f.vibration > 0.03 ? 0.8 :
    f.vibration > 0.015 ? 0.5 :
    0.2,

  // Tree 4: Acceleration magnitude
  (f) =>
    f.magnitude > 0.35 ? 0.75 :
    f.magnitude > 0.2 ? 0.45 :
    0.2,

  // Tree 5: Combined failure signature
  (f) =>
    f.soilMoisture > 75 &&
    f.tilt > 0.18 &&
    f.vibration > 0.02
      ? 0.95
      : 0.3,
];

/**
 * @param {Object} f
 * @param {number} f.soilMoisture
 * @param {number} f.tilt
 * @param {number} f.vibration
 * @param {number} f.magnitude
 */
export function sensorRiskRandomForest(f) {
  const scores = trees.map((tree) => tree(f));
  const avg =
    scores.reduce((sum, s) => sum + s, 0) / scores.length;

  return Number(avg.toFixed(2));
}
