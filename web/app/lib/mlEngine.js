// Simple ML-like model (logistic regression style)

const trainedWeights = {
  bias: -1.2,
  slope: 2.5,
  rainfall: 2.0,
  vegetation: -1.8, // negative impact
  soil: 1.5,
  history: 1.2,
};

function sigmoid(x) {
  return 1 / (1 + Math.exp(-x));
}

export function mlRiskPrediction(features) {
  const z =
    trainedWeights.bias +
    trainedWeights.slope * features.slope +
    trainedWeights.rainfall * features.rainfall +
    trainedWeights.vegetation * features.vegetation +
    trainedWeights.soil * features.soil +
    trainedWeights.history * features.history;

  const probability = sigmoid(z);

  return Number(probability.toFixed(2));
}
