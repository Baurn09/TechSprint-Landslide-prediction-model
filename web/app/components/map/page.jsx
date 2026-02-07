"use client";
import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Rectangle,
  Polyline,
  Popup,
  ScaleControl
} from "react-leaflet";
import { useState } from "react";
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

const BASEMAPS = {
  street: {
    name: "Street",
    url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    attribution: "© OpenStreetMap",
  },
  terrain: {
    name: "Terrain",
    url: "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    attribution: "© OpenTopoMap",
  },
  satellite: {
    name: "Satellite",
    url: "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attribution: "© Esri",
  },
};



export default function RiskMap() {
  const router = useRouter();
  const [basemap, setBasemap] = useState("satellite");
  return (
    <main className="relative h-screen w-screen overflow-hidden bg-black">

      {/* ───────── Floating Title Box ───────── */}
      <div className="absolute top-6 left-6 z-[1000] 
                      bg-[#F2EFEA] backdrop-blur-md 
                      rounded-xl shadow-lg p-4 max-w-sm">
        <h1 className="text-2xl font-bold text-gray-900">
          LEWS: Landslide Early Warning System
        </h1>
        <h1 className="text-md pt-3 font-bold text-gray-900">
          Satellite-Based Landslide Susceptibility
        </h1>
        <p className="text-md text-gray-600 mt-1">
          Macro-level analysis to identify zones requiring ground sensor monitoring
        </p>
      </div>

      {/* ───────── Floating Legend ───────── */}
      <div className="absolute bottom-6 right-6 z-[1000] 
                      bg-[#F2EFEA] backdrop-blur-md 
                      rounded-xl shadow-lg p-3 text-sm space-y-2">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 bg-[#dc2626] rounded-sm"></span>
          <span className="text-black font-bold text-md">Satellite monitoring only</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 bg-[#2563eb] rounded-sm"></span>
          <span className="text-black font-bold text-md">Ground sensors deployed</span>
        </div>
      </div>

      {/*toggle */}
      <div className="absolute top-1/2 -translate-y-1/2 left-6 z-[1000] 
                bg-[#F2EFEA] backdrop-blur-md 
                rounded-xl shadow-lg p-3 text-sm space-y-2">
        <div className="font-bold text-xl text-gray-800">
          Terrain View
        </div>
        {Object.entries(BASEMAPS).map(([key, map]) => (
          <label key={key} className="flex items-center text-lg gap-2 cursor-pointer">
            <input
              type="radio"
              name="basemap"
              checked={basemap === key}
              onChange={() => setBasemap(key)}
            />
            <span className="text-black">{map.name}</span>
          </label>
        ))}
      </div>
      
      {/*North Arrow */}
      <div
        className="absolute top-24 right-6 z-[1000]
                  bg-[#F2EFEA] backdrop-blur-md
                  rounded-full shadow-lg
                  w-12 h-12
                  flex flex-col items-center justify-center"
      >
        <span className="text-xs font-bold text-red-500 leading-none">N</span>
        <svg
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
        >
          <path
            d="M12 2 L17 22 L12 17 L7 22 Z"
            fill="red"
          />
        </svg>
      </div>

      {/* ───────── Full Screen Map ───────── */}
      <MapContainer
        center={[24.8, 94.2]}
        zoom={10}
        zoomControl={false}
        minZoom={7}
        maxZoom={20}
        maxBounds={MANIPUR_BOUNDS}
        maxBoundsViscosity={0.4}
        className="h-full w-full z-0"
      >
        <TileLayer
          key={basemap}   // forces clean reload
          attribution={BASEMAPS[basemap].attribution}
          url={BASEMAPS[basemap].url}
          className={basemap === "terrain" ? "bw-tiles" : ""}
        />
        
        {/* Map scale */}
        <ScaleControl
          position="topright"
          imperial={false}   // no miles
          metric={true}      // meters / km
          maxWidth={120}
        />
        

        {/* Reference Grid */}
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

        {/* Hotspot Rectangles */}
        {hotspots.map((spot) => {
          const deployed = deployedSensors[spot.id];


          return (
            <Rectangle
              key={spot.id}
              bounds={[
                [spot.coords[0] - 0.015, spot.coords[1] - 0.015],
                [spot.coords[0] + 0.015, spot.coords[1] + 0.015],
              ]}
              pathOptions={{
                color: deployed ? "#2563eb" : "#dc2626",
                fillColor: deployed ? "#2563eb" : "#dc2626",
                fillOpacity: deployed ? 0.8 : 0.8,
              }}
            >
              <Popup>
                <strong className="uppercase">{spot.name}</strong>
                <br />
                <b>Soil type:</b>{" "}
                {areaMetadata[spot.id]?.soil ?? "Data not available"}
                <br />
                <b>Terrain:</b> {areaMetadata[spot.id]?.terrain}
                <br />
                <b>Nature:</b> {areaMetadata[spot.id]?.nature}
                <br />
                {deployed ? (
                  <span className="text-green-700 text-sm">
                    Ground sensors deployed
                  </span>
                ) : (
                  <span className="text-yellow-700 text-sm">
                    Satellite monitoring only
                  </span>
                )}
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