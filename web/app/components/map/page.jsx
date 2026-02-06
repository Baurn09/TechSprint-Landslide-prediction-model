"use client";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Rectangle,
  Polyline,
  Popup,
} from "react-leaflet";
import "leaflet/dist/leaflet.css";
import { useRouter } from "next/navigation";
import { deployedSensors } from "../../lib/deployedSensors";
import { generateGridLines } from "../../lib/gridUtils";
import { areaMetadata } from "../../lib/areaMetaData";

const hotspots = [
  // critical
  { id: "noney", name: "Tupul", coords: [24.8900, 93.6300] },
  { id: "senapati", name: "Senapati Hill Slopes", coords: [25.0900, 94.1100] },
  { id: "noney", name: "Noney General Hills", coords: [24.7500, 93.6300] },
  { id: "senapati", name: "NH 39 stretch : Mao–Karong", coords: [25.5200, 94.1500] },
  { id: "ukhrul", name: "Ukhrul Lower Slopes", coords: [25.0800, 94.3100] },
  // moderate
  { id: "churachandpur", name: "Churachandpur", coords: [24.3300, 94.3150] },
  { id: "pherzawl", name: "Pherzawl Hills", coords: [24.3000, 93.1500] },
  { id: "churachandpur", name: "Churachandpur Hill Outskirts", coords: [24.3325, 93.6850] },
  { id: "kangpokpi", name: "Kangpokpi Hill Areas", coords: [25.0300, 93.9500] },
  { id: "bishnupur", name: "Bishnupur Hill Fringes", coords: [24.6300, 93.7700] },
];

const MANIPUR_BOUNDS = [
  [23.8, 93.0],
  [26.0, 95.2],
];
const gridLines = generateGridLines(
  MANIPUR_BOUNDS,
  0.0025,   // smaller cells
  0.005
);
export default function RiskMap() {
  const router = useRouter();
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
        style={{ height: "80vh", width: "100%" }}
      >
        <TileLayer
          attribution="© OpenStreetMap"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {/* Reference grid (satellite scan resolution) */}
        {gridLines.map((line, i) => (
          <Polyline
            key={i}
            positions={line}
            pathOptions={{
              color: "black",
              weight: 0.5,
              opacity: 0.3,
            }}
            interactive={false}
          />
        ))}
        {/* Hotspots */}
        {hotspots.map((spot) => {
          const deployed = deployedSensors[spot.id];
          return deployed ? (
            <Rectangle
              key={spot.id}
              bounds={[
                [spot.coords[0] - 0.015, spot.coords[1] - 0.015],
                [spot.coords[0] + 0.015, spot.coords[1] + 0.015],
              ]}
              pathOptions={{
                color: "#111",
                fillColor: "#2563eb",
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
                <span className="text-green-700 text-sm">
                  Ground sensors deployed
                </span>
                <br />
                <button
                  className="mt-2 px-3 py-1 bg-blue-600 text-white rounded text-sm"
                  onClick={() =>
                    router.push(`/dashboard?area=${spot.id}`)
                  }
                >
                  View details
                </button>
              </Popup>
            </Rectangle>
          ) : (
            <Rectangle
              key={spot.id}
              bounds={[
                [spot.coords[0] - 0.015, spot.coords[1] - 0.015],
                [spot.coords[0] + 0.015, spot.coords[1] + 0.015],
              ]}
              pathOptions={{
                color: "#dc2626",
                fillOpacity: 0.7,
              }}
            >
              <Popup>
                <strong className="uppercase">{spot.name}</strong>
                <br />
                <b>Soil type:</b>{" "}{areaMetadata[spot.id]?.soil ?? "Data not available"}
                <br />
                <b>Terrain:</b> {areaMetadata[spot.id]?.terrain}
                <br />
                <b>Nature:</b> {areaMetadata[spot.id]?.nature}
                <br />
                <span className="text-yellow-700 text-sm">
                  Satellite monitoring only
                </span>
                <br />
                <button
                  className="mt-2 px-3 py-1 bg-blue-600 text-white rounded text-sm"
                  onClick={() =>
                    router.push(`/dashboard?area=${spot.id}`)
                  }
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