"use client";

import { MapContainer, TileLayer, Rectangle, Popup } from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useRouter } from "next/navigation";
import { useMemo } from "react";

import { deployedSensors } from "../../lib/deployedSensors";
import { areaMetadata } from "../../lib/areaMetaData";
import { generateGridCells } from "../../lib/gridCells";
import { gridCellsToGeoJSON } from "../../lib/gridGeoJson";
import { useMapEvents, GeoJSON } from "react-leaflet";
import { useState } from "react";

function GridLayer({ gridGeoJSON }) {
  const [showGrid, setShowGrid] = useState(false);

  useMapEvents({
    zoomend: (e) => {
      const z = e.target.getZoom();
      setShowGrid(z >= 11);
    },
  });

  if (!showGrid) return null;

  return (
    <GeoJSON
      data={gridGeoJSON}
      style={{
        color: "#000",
        weight: 0.3,
        fillOpacity: 0.05,
      }}
    />
  );
}


const MANIPUR_BOUNDS = [
  [23.8, 93.0],
  [26.0, 95.2],
];

const GRID_STYLE = {
  color: "#000",
  weight: 0.3,
  fillOpacity: 0.05,
};

const hotspots = [
  { id: "noney", name: "Tupul", coords: [24.89, 93.63] },
  { id: "senapati", name: "Senapati Hill Slopes", coords: [25.09, 94.11] },
  { id: "ukhrul", name: "Ukhrul Lower Slopes", coords: [25.08, 94.31] },
  { id: "chandel", name: "Chandel", coords: [24.33, 94.315] },
  { id: "kangpokpi", name: "Kangpokpi Hill Areas", coords: [25.03, 93.95] },
];

// -------------------- COMPONENT --------------------

export default function RiskMap() {
  const router = useRouter();

  // Generate grid ONCE
  const gridGeoJSON = useMemo(() => {
    const cells = generateGridCells(MANIPUR_BOUNDS, 0.0025, 0.005);
    return gridCellsToGeoJSON(cells);
  }, []);

  return (
    <main className="p-6 bg-[#F2EFEA] text-black">
      <h1 className="text-2xl font-bold">
        Satellite-Based Landslide Susceptibility Assessment
      </h1>
      <p className="text-sm text-gray-600 mb-4">
        Macro-level analysis to identify zones requiring ground sensor monitoring
      </p>

      <MapContainer
        center={[24.8, 94.2]}
        zoom={10}
        minZoom={7}
        maxZoom={20}
        maxBounds={MANIPUR_BOUNDS}
        maxBoundsViscosity={0.4}
        preferCanvas={true}   // 🔥 IMPORTANT
        style={{ height: "80vh", width: "100%" }}
      >

        {/* Base Map */}
        <TileLayer
          attribution="© OpenStreetMap"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* GRID OVERLAY (FAST) */}
        <GridLayer gridGeoJSON={gridGeoJSON} />

        {/* HOTSPOTS (TEMPORARY, LOW COUNT = OK) */}
        {hotspots.map((spot) => {
          const deployed = deployedSensors[spot.id];
          const color = deployed ? "#dc2626" : "#f59e0b";

          return (
            <Rectangle
              key={spot.id}
              bounds={[
                [spot.coords[0] - 0.015, spot.coords[1] - 0.015],
                [spot.coords[0] + 0.015, spot.coords[1] + 0.015],
              ]}
              pathOptions={{
                color: "#111",
                fillColor: color,
                fillOpacity: 0.6,
              }}
            >
              <Popup>
                <strong className="uppercase">{spot.name}</strong>
                <br />
                <b>Soil type:</b> {areaMetadata[spot.id]?.soil}
                <br />
                <b>Terrain:</b> {areaMetadata[spot.id]?.terrain}
                <br />
                <b>Nature:</b> {areaMetadata[spot.id]?.nature}
                <br />
                <span
                  className={`text-sm ${
                    deployed ? "text-green-700" : "text-yellow-700"
                  }`}
                >
                  {deployed
                    ? "Ground sensors deployed"
                    : "Satellite monitoring only"}
                </span>
                <br />
                <button
                  className="mt-2 px-3 py-1 bg-blue-600 text-white rounded text-sm"
                  onClick={() => router.push(`/dashboard?area=${spot.id}`)}
                >
                  View details
                </button>
              </Popup>
            </Rectangle>
          );
        })}
      </MapContainer>
    </main>
  );
}