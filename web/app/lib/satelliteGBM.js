// Satellite-Based Gradient Boosted Trees (GBDT-style)
// Uses satellite-derived feature vector: R, V, S, E, P, H

const learningRate = 0.25;

// Weak learners (trees) focusing on different physical factors
const trees = [
  // Tree 1: Rainfall + Slope (primary trigger)
  (f) => 0.6 * f.R + 0.4 * f.S,

  // Tree 2: Vegetation + Soil cohesion (stability)
  (f) => 0.7 * (1 - f.V) + 0.3 * f.P,

  // Tree 3: Elevation-driven drainage patterns
  (f) => f.E,

  // Tree 4: Rainfall–Soil interaction (failure likelihood)
  (f) => f.R * f.P,

  // Tree 5: Historical landslide influence
  (f) => f.H,
];

// Sigmoid → probability of landslide risk
function sigmoid(x) {
  return 1 / (1 + Math.exp(-x));
}

export function satelliteRiskGBM(featureVector) {
  let score = -1.1; // bias (learned during training)

  for (const tree of trees) {
    score += learningRate * tree(featureVector);
  }

  return Number(sigmoid(score).toFixed(2));
}
