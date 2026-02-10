"use client";

import {
  MapContainer,
  TileLayer,
  ScaleControl,
  GeoJSON,
  ZoomControl
} from "react-leaflet";

import { useState, useEffect } from "react";
import "leaflet/dist/leaflet.css";
import { useRouter } from "next/navigation";


// ================= SENSOR DEPLOYED GRID =================
// ⭐ CHANGE THIS if you want a different grid later
const SENSOR_DEPLOYED_GRID = "+3467+934";


// ================= MAP BOUNDS =================

const MANIPUR_BOUNDS = [
  [23.0, 91.5],
  [27.5, 96.5],
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

  // ---------- load hill grid ----------

  useEffect(() => {
    fetch("/data/hill_grid_geojson.geojson")
      .then(r => r.json())
      .then(setHillGrid)
      .catch(e => console.error("Hill grid load failed:", e));
  }, []);

  // ---------- load ML risk grid ----------

  useEffect(() => {
    fetch("/data/grid_risk_collab.geojson")
      .then(r => r.json())
      .then(setRiskGrid)
      .catch(e => console.error("Risk grid load error", e));
  }, []);


  // ================= GRID STYLE LOGIC =================

  function getGridStyle(feature) {
    const r = feature.properties.risk;
    const id = feature.properties.grid_uid;

    // 🔵 SENSOR DEPLOYED GRID
    if (id === SENSOR_DEPLOYED_GRID) {
      return {
        color: "#2563eb",
        fillColor: "#2563eb",
        weight: 1.4,
        fillOpacity: 0.85,
        interactive: true
      };
    }

    // 🔴 HIGH RISK
    if (r > 0.7) {
      return {
        color: "#dc2626",
        fillColor: "#dc2626",
        weight: 0.8,
        fillOpacity: 0.6,
        interactive: true
      };
    }

    // 🟠 MODERATE
    if (r > 0.65) {
      return {
        color: "orange",
        fillColor: "orange",
        weight: 0.6,
        fillOpacity: 0.5,
        interactive: true
      };
    }

    return {
      color: "transparent",
      fillColor: "transparent",
      weight: 0,
      fillOpacity: 0,
      interactive: false
    };
  }


  // ================= RENDER =================

  return (
    <main className="relative h-screen w-screen overflow-hidden bg-black">

      {/* TITLE */}
      <div className="absolute top-6 left-6 z-[1000] rounded-2xl p-5 max-w-sm bg-white/30 backdrop-blur-xl border border-white/40">
        <h1 className="text-2xl font-bold">LEWS: Landslide Early Warning System</h1>
        <p className="mt-2 text-sm">
          Satellite-Based Landslide Susceptibility
        </p>
      </div>


      {/* LEGEND */}
      <div className="absolute bottom-6 right-6 z-[1000] rounded-xl p-4 bg-white/30 backdrop-blur border border-white/40 text-sm space-y-2">

        <div className="flex gap-2 items-center">
          <div className="w-3 h-3 bg-blue-600"></div>
          Ground Sensor Deployed
        </div>

        <div className="flex gap-2 items-center">
          <div className="w-3 h-3 bg-red-600"></div>
          High Risk
        </div>

        <div className="flex gap-2 items-center">
          <div className="w-3 h-3 bg-orange-400"></div>
          Moderate Risk
        </div>

      </div>


      {/* BASEMAP TOGGLE */}
      <div className="absolute top-1/2 -translate-y-1/2 left-6 z-[1000] rounded-xl p-4 bg-white/30 backdrop-blur border border-white/40">
        {Object.entries(BASEMAPS).map(([key, map]) => (
          <label key={key} className="block cursor-pointer">
            <input
              type="radio"
              checked={basemap === key}
              onChange={() => setBasemap(key)}
            /> {map.name}
          </label>
        ))}

        <label className="block mt-2">
          <input
            type="checkbox"
            checked={showHillGrid}
            onChange={() => setShowHillGrid(v => !v)}
          /> Show Hill Grid
        </label>
      </div>


      {/* MAP */}
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
        />

        <ScaleControl position="topright" imperial={false} />
        <ZoomControl position="topright" />


        {/* ===== ML GRID ===== */}

        {riskGrid && (
          <GeoJSON
            data={riskGrid}
            style={getGridStyle}
            onEachFeature={(feature, layer) => {

  const r = feature.properties.risk;
  const gridId = feature.properties.grid_uid;

  const hasSensor = gridId === SENSOR_DEPLOYED_GRID;

  layer.bindPopup(`
    <div style="min-width:160px">
      <b>Grid:</b> ${gridId}<br/>
      <b>Risk:</b> ${(r * 100).toFixed(1)}%<br/>
      <b>Sensor:</b> ${hasSensor ? "Deployed" : "Not deployed"}<br/><br/>

      <button 
        onclick="window.location.href='/dashboard?grid_uid=${encodeURIComponent(gridId)}'"
        style="
          background:#2563eb;
          color:white;
          padding:6px 10px;
          border-radius:6px;
          border:none;
          cursor:pointer;
        ">
        Open Satellite Dashboard
      </button>
    </div>
  `);
}}

          />
        )}


        {/* HILL GRID */}
        {hillGrid && showHillGrid && (
          <GeoJSON
            data={hillGrid}
            style={{
              color: "#3BC1A8",
              weight: 0.5,
              fillOpacity: 0.04
            }}
          />
        )}

      </MapContainer>
    </main>
  );
}
