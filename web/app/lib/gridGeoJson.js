export function gridCellsToGeoJSON(gridCells) {
  return {
    type: "FeatureCollection",
    features: gridCells.map((cell) => ({
      type: "Feature",
      properties: {
        grid_id: cell.grid_id,
      },
      geometry: {
        type: "Polygon",
        coordinates: [[
          [cell.bounds[0][1], cell.bounds[0][0]], // SW
          [cell.bounds[1][1], cell.bounds[0][0]], // SE
          [cell.bounds[1][1], cell.bounds[1][0]], // NE
          [cell.bounds[0][1], cell.bounds[1][0]], // NW
          [cell.bounds[0][1], cell.bounds[0][0]], // close
        ]],
      },
    })),
  };
}
     