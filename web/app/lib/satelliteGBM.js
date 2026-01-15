
const learningRate = 0.25;

const trees = [
  // Rainfall + slope trigger
  (f) => 0.6 * f.R + 0.4 * f.S,

  // Vegetation + soil stability
  (f) => 0.7 * (1 - f.V) + 0.3 * f.P,

  // Elevation / drainage influence
  (f) => f.E,

  // Rainfall–soil interaction
  (f) => f.R * f.P,

  // Historical susceptibility
  (f) => f.H,
];

function sigmoid(x) {
  return 1 / (1 + Math.exp(-x));
}

/**
 * @param {Object} f
 * @param {number} f.R Rainfall
 * @param {number} f.V Vegetation index (NDVI)
 * @param {number} f.S Slope
 * @param {number} f.E Elevation
 * @param {number} f.P Soil proxy
 * @param {number} f.H Historical risk
 */
export function satelliteRiskGBM(f) {
  let score = -1.1; // bias term (learned offline)

  for (const tree of trees) {
    score += learningRate * tree(f);
  }

  return Number(sigmoid(score).toFixed(2));
}
