export function generateGridCells(bounds, latStep, lngStep) {
  const cells = [];
  const [[minLat, minLng], [maxLat, maxLng]] = bounds;

  let id = 0;

  for (let lat = minLat; lat < maxLat; lat += latStep) {
    for (let lng = minLng; lng < maxLng; lng += lngStep) {
      cells.push({
        grid_id: `G_${id.toString().padStart(4, "0")}`,
        bounds: [
          [lat, lng],
          [lat + latStep, lng + lngStep],
        ],
      });
      id++;
    }
  }

  return cells;
}
