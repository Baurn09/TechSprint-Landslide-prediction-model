export function generateGridLines(bounds, latStep, lngStep) {
  const lines = [];
  const [[minLat, minLng], [maxLat, maxLng]] = bounds;

  // horizontal lines
  for (let lat = minLat; lat <= maxLat; lat += latStep) {
    lines.push([
      [lat, minLng],
      [lat, maxLng],
    ]);
  }

  // vertical lines
  for (let lng = minLng; lng <= maxLng; lng += lngStep) {
    lines.push([
      [minLat, lng],
      [maxLat, lng],
    ]);
  }

  return lines;
}

export async function GET() {
  const MANIPUR_BOUNDS = [
    [23.8, 93.0],
    [26.0, 95.2],
  ];

  const gridLines = generateGridLines(
    MANIPUR_BOUNDS,
    0.00225, // 250 m
    0.005
  );

  return Response.json(gridLines);
}
