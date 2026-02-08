"use client";

import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Rectangle,
  Popup,
  ScaleControl,
  GeoJSON,
  ZoomControl
} from "react-leaflet";

import { useState, useEffect } from "react";
import "leaflet/dist/leaflet.css";
import { useRouter } from "next/navigation";

import { deployedSensors } from "../../lib/deployedSensors";
import { areaMetadata } from "../../lib/areaMetaData";


// ================= HOTSPOTS =================

const hotspots = [
  { id: "noney", name: "Tupul", coords: [24.8900, 93.6300] },
  { id: "senapati", name: "Senapati Hill Slopes", coords: [25.0900, 94.1100] },
  { id: "noney", name: "Noney General Hills", coords: [24.7500, 93.6300] },
  { id: "senapati", name: "NH 39 stretch : Mao–Karong", coords: [25.5200, 94.1500] },
  { id: "ukhrul", name: "Ukhrul Lower Slopes", coords: [25.0800, 94.3100] },

  { id: "churachandpur", name: "Churachandpur", coords: [24.3300, 94.3150] },
  { id: "pherzawl", name: "Pherzawl Hills", coords: [24.3000, 93.1500] },
  { id: "churachandpur", name: "Churachandpur Hill Outskirts", coords: [24.3325, 93.6850] },
  { id: "kangpokpi", name: "Kangpokpi Hill Areas", coords: [25.0300, 93.9500] },
  { id: "bishnupur", name: "Bishnupur Hill Fringes", coords: [24.6300, 93.7700] },
];


// ================= MAP BOUNDS =================

const MANIPUR_BOUNDS = [
  [23.8, 93.0],
  [26.0, 95.2],
];


// ================= BASEMAPS =================

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


// ================= PAGE =================

export default function RiskMap() {

  const router = useRouter();

  const [basemap, setBasemap] = useState("satellite");
  const [hillGrid, setHillGrid] = useState(null);
  const [showHillGrid, setShowHillGrid] = useState(false);
  const [riskGrid, setRiskGrid] = useState(null);

  // ---------- load hill grid geojson ----------

  useEffect(() => {
    fetch("/data/hill_grid_geojson.geojson")
      .then(r => r.json())
      .then(setHillGrid)
      .catch(e => console.error("Hill grid load failed:", e));
  }, []);

  useEffect(() => {
    fetch("/data/grid_risk.geojson")
      .then(r => r.json())
      .then(setRiskGrid)
      .catch(e => console.error("Risk grid load error", e));
  }, []);

  function getRiskColor(r) {
    if (r > 0.95) return "#dc2626";     // red
    if (r > 0.86) return "orange";     // orange
    // if (r > 0.2) return "#22c55e";     // yellow
    return "transparent";                  // green
  }

  return (
    <main className="relative h-screen w-screen overflow-hidden bg-black">

      {/* ================= TITLE ================= */}

      <div className="absolute top-6 left-6 z-[1000] bg-[#F2EFEA] rounded-xl shadow-lg p-4 max-w-sm">
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


      {/* ================= LEGEND ================= */}

      <div className="absolute bottom-6 right-6 z-[1000] bg-[#F2EFEA] rounded-xl shadow-lg p-3 text-sm space-y-2">
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 bg-[#2563eb] rounded-sm"></span>
          <span className="text-black font-bold text-md">Ground sensors deployed</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 bg-[#dc2626] rounded-sm"></span>
          <span className="text-black font-bold text-md">High Risk: Satellite monitoring only</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="w-3 h-3 bg-orange-300 rounded-sm"></span>
          <span className="text-black font-bold text-md">Moderate Risk: Satellite monitoring only</span>
        </div>
      </div>


      {/* ================= BASEMAP TOGGLE ================= */}

      <div className="absolute text-black top-1/2 -translate-y-1/2 left-6 z-[1000] bg-[#F2EFEA] rounded-xl shadow-lg p-3 space-y-2">
        <div className="font-bold text-lg">Terrain View</div>

        {Object.entries(BASEMAPS).map(([key, map]) => (
          <label key={key} className="flex gap-2 cursor-pointer">
            <input
              type="radio"
              checked={basemap === key}
              onChange={() => setBasemap(key)}
            />
            {map.name}
          </label>
        ))}

        <hr />

        <label className="flex gap-2 cursor-pointer text-sm">
          <input
            type="checkbox"
            checked={showHillGrid}
            onChange={() => setShowHillGrid(v => !v)}
          />
          Show Hill Grid
        </label>
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

      {/* ================= MAP ================= */}

      <MapContainer
        center={[24.8, 94.2]}
        zoom={10}
        minZoom={7}
        maxZoom={20}
        maxBounds={MANIPUR_BOUNDS}
        zoomControl={false}
        className="h-full w-full"
      >

        <TileLayer
          key={basemap}
          url={BASEMAPS[basemap].url}
          attribution={BASEMAPS[basemap].attribution}
          className={basemap == "terrain" ? "bw-tiles" : ""}
        />

          <ScaleControl position="topright" imperial={false}  />
          <ZoomControl position="topright" />

          {/* ===== ML RISK GRID LAYER ===== */}

        {riskGrid && (
          <GeoJSON
            data={riskGrid}
            style={(feature) => ({
              color: getRiskColor(feature.properties.risk),
              fillColor: getRiskColor(feature.properties.risk),
              weight: 0.6,
              fillOpacity: 0.55,
              interactive: true
            })}
            onEachFeature={(feature, layer) => {
              const r = feature.properties.risk;
              layer.bindPopup(
                `Risk: ${(r * 100).toFixed(1)}%`
              );
            }}
          />
        )}



        {/* ================= HILL GRID LAYER ================= */}

        {hillGrid && showHillGrid && (
          <GeoJSON
            data={hillGrid}
            style={{
              color: basemap == "street" ? "black" : "yellow",
              weight: 0.5,
              fillOpacity: 0.04  
            }}

          />
        )}


        {/* ================= HOTSPOTS ================= */}

        {hotspots.map((spot) => {
          const deployed = deployedSensors[spot.id];

          return (
            <Rectangle
              key={spot.name}
              bounds={[
                [spot.coords[0] - 0.015, spot.coords[1] - 0.015],
                [spot.coords[0] + 0.015, spot.coords[1] + 0.015],
              ]}
              pathOptions={{
                color: deployed ? "#2563eb" : "#dc2626",
                fillOpacity: 0.6,
              }}
            >
              <Popup>
                <strong>{spot.name}</strong><br/>
                Soil: {areaMetadata[spot.id]?.soil}<br/>
                Terrain: {areaMetadata[spot.id]?.terrain}<br/>
                Nature: {areaMetadata[spot.id]?.nature}
                <br/>
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
