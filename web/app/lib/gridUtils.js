export function generateGridLines(bounds, latStep, lngStep) {
  const lines = [];
  const [[minLat, minLng], [maxLat, maxLng]] = bounds;

  for (let lat = minLat; lat <= maxLat; lat += latStep) {
    lines.push([
      [lat, minLng],
      [lat, maxLng],
    ]);
  }

  for (let lng = minLng; lng <= maxLng; lng += lngStep) {
    lines.push([
      [minLat, lng],
      [maxLat, lng],
    ]);
  }

  return lines;
}
