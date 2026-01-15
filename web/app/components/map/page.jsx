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
  //critical risk spots
  { id: "noney", name: "Tupul", coords: [24.8900, 93.6300] },//done                         1            2           3
  { id: "senapati", name: "Senapati Hill Slopes", coords: [25.0900, 94.1100] },//done       4
  { id: "noney", name: "Noney General Hills", coords: [24.7500, 93.6300]},//done            5
  { id: "senapati", name: "NH 39 strech : Mao-Karong", coords: [25.5200, 94.1500]},//done   6
  { id: "ukhrul", name: "Ukhrul Lower Slopes", coords: [25.0800, 94.3100]},//done           7
  //moderate risk spots
  { id: "chandel", name: "Chandel", coords: [24.3300, 94.3150] },//done                         1
  { id: "pherzwal", name: "Pherzwal Hills", coords: [24.3000, 93.1500]},//done                  2
  { id: "churchandpur", name: "Churchandpur Hill Outskrts", coords: [24.3325, 93.6850]},//done  3
  { id: "kangpokpi", name: "Kangpokpi Hill Areas", coords: [25.0300, 93.9500]},//done           4
  { id: "bishnupur", name: "Bishnupur HIll Fringes", coords: [24.6300, 93.7700]},//done but was supposed to be critical
  
  { id: "noney", name: "Tupul", coords: [24.8900, 93.6300] },//done                             01
  { id: "noney", name: "Tamenglong Hill", coords: [24.8100, 93.6300] },//done                   02
  { id: "ukhrul", name: "Ukhrul Hill Region", coords: [25.1300, 94.3500] },//done               03
  { id: "senapati", name: "Senapati Hill Slopes", coords: [25.0900, 94.1100] },//done           04
  { id: "noney", name: "Noney General Hills", coords: [24.7500, 93.6300]},//done                05
  { id: "senapati", name: "NH 39 strech : Mao-Karong", coords: [25.5200, 94.1500]},//done       06
  { id: "ukhrul", name: "Ukhrul Lower Slopes", coords: [25.0800, 94.3100]},//done               07
  { id: "chandel", name: "Chandel", coords: [24.3300, 94.3150] },//done                         08
  { id: "pherzwal", name: "Pherzwal Hills", coords: [24.3000, 93.1500]},//done                  09
  { id: "churchandpur", name: "Churchandpur Hill Outskrts", coords: [24.3325, 93.6850]},//done  10
  { id: "kangpokpi", name: "Kangpokpi Hill Areas", coords: [25.0300, 93.9500]},//done           11
  { id: "bishnupur", name: "Bishnupur HIll Fringes", coords: [24.6300, 93.7700]},//done         12
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
                fillColor: "#dc2626",
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
                color: "#f59e0b",
                fillOpacity: 0.7,
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