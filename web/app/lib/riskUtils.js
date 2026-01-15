export function computeRisk({ slope, rainfall, vegetation, soil }) {
  const score =
    0.3 * slope +
    0.3 * rainfall +
    0.2 * (1 - vegetation) +
    0.2 * soil;

  if (score > 0.7) return "HIGH";
  if (score > 0.4) return "MODERATE";
  return "LOW";
}
