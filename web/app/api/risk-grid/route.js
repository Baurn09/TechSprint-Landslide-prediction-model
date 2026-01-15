import { generateGrid } from "../../lib/gridUtils";
import { computeRisk } from "../../lib/riskUtils";

const MANIPUR = [
  [23.8, 93.0],
  [26.0, 95.2],
];

export async function GET() {
  const grids = generateGrid(MANIPUR, 0.005);

  const enriched = grids.map((g) => {
    const satellite = {
      slope: Math.random(),
      rainfall: Math.random(),
      vegetation: Math.random(),
      soil: Math.random(),
    };

    return {
      ...g,
      risk: computeRisk(satellite),
    };
  });

  return Response.json(enriched);
}
