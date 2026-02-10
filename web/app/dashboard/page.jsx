"use client";

import "../lib/chartConfig";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { deployedSensors } from "../lib/deployedSensors.js";
import Metric from "../components/metric/page";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const searchParams = useSearchParams();
  const rawId = searchParams.get("grid_uid");
  const grid_uid = rawId?.trim();
  const area = searchParams.get("area");
  const router = useRouter();

  const hasSensors = area ? deployedSensors[area] === true : false;


  useEffect(() => {
    const url = grid_uid
      ? `/api/satellite?grid_uid=${encodeURIComponent(grid_uid)}`
      : `/api/satellite?area=${area}`;

    fetch(url)
      .then(async res => {
        if (!res.ok) {
          const err = await res.json();
          throw new Error(err.error || "API error");
        }
        return res.json();
      })
      .then(setData)
      .catch(e => {
        console.error(e);
        setData(null);
      });

  }, [area, grid_uid]);



 if (!data) {
  return (
    <p className="p-8 text-red-600">
      Satellite data unavailable for this grid.
    </p>
  );
}


  const { features, rawFeatures, riskScore, decision, drivers, contributions } = data;



  const directions = {
  S: (features?.S ?? 0) > 0.7 ? "up" : "stable",
  R: (features?.R ?? 0) > 0.6 ? "up" : "down",
  V: (features?.V ?? 0) < 0.4 ? "down" : "stable",
  P: "stable",
};

console.log("Dashboard data:", data);



  return (
    <main className="p-8 w-full min-h-screen text-black bg-[#F2EFEA]">
      <h1 className="text-2xl font-bold">Live Dashboard</h1>

      <p className="text-sm text-gray-500 mt-1">
        Last updated: {new Date().toLocaleString()}
      </p>

      <p className="text-sm text-gray-600 mt-1">
        Monitoring Target:  
        <strong>
          {grid_uid ? ` GRID ${grid_uid}` : (area || "UNKNOWN").toUpperCase()}
        </strong>
      </p>

      {/* Satellite Metrics */}
      <div className="grid grid-cols-3 gap-4 mt-6">
        <Metric
          label="Slope Factor"
          value={features.S}
          color="#ef4444"
          trend={[0.6, 0.65, features.S]}   // sparkline data
          direction={directions.S}
        />

        <Metric
          label="Rainfall Index"
          value={features.R}
          color="#3b82f6"
          trend={[0.6, 0.65, features.R]}   // sparkline data
          direction={directions.R}
        />

        <Metric
          label="Vegetation Index (NDVI)"
          value={features.V}
          color="#22c55e"
          trend={[0.6, 0.65, features.V]}   // sparkline data
          direction={directions.V}
        />

        <Metric
          label="Soil Stability Proxy"
          value={features.P}
          trend={[0.6, 0.65, features.P]}   // sparkline data
          direction={directions.P}
        />

        
      </div>

      {rawFeatures && (
        <div className="mt-6 p-4 rounded bg-white shadow">
          <h3 className="font-semibold mb-3">
            Grid Environmental Features
          </h3>

          <div className="grid grid-cols-2 gap-3 text-sm">

            <div>Elevation: <b>{rawFeatures.elevation?.toFixed(1)} m</b></div>
            <div>Slope: <b>{rawFeatures.slope?.toFixed(2)} °</b></div>

            <div>NDVI: <b>{rawFeatures.ndvi?.toFixed(3)}</b></div>

            <div>Rain 1d: <b>{rawFeatures.rain_1d?.toFixed(1)} mm</b></div>
            <div>Rain 7d: <b>{rawFeatures.rain_7d?.toFixed(1)} mm</b></div>
            <div>Rain 30d: <b>{rawFeatures.rain_30d?.toFixed(1)} mm</b></div>

            <div>Soil Moisture: <b>{rawFeatures.soil_moisture?.toFixed(3)}</b></div>
            <div>Soil Type: <b>{rawFeatures.soil_type}</b></div>

            <div>Population: <b>{rawFeatures.population?.toFixed(0)}</b></div>

          </div>
        </div>
      )}

      {/* ================= EXPLAINABILITY ================= */}

      {drivers && (
        <div className="mt-6 p-4 rounded bg-white shadow">
          <h3 className="font-semibold mb-2">
            Why this grid is risky
          </h3>

          <ul className="text-sm space-y-2">

            {drivers.includes("rainfall") && (
              <li>🌧️ High recent rainfall increased ground saturation</li>
            )}

            {drivers.includes("slope") && (
              <li>⛰️ Steep terrain raises landslide probability</li>
            )}

            {drivers.includes("vegetation") && (
              <li>🌱 Low vegetation cover reduces soil binding</li>
            )}

            {drivers.includes("soil") && (
              <li>💧 High soil moisture weakens slope stability</li>
            )}

          </ul>

          <div className="mt-3 text-xs text-gray-500">
            Model contribution weights:
            {Object.entries(contributions).map(([k,v]) => (
              <div key={k}>{k}: {(v*100).toFixed(1)}%</div>
            ))}
          </div>
        </div>
      )}  




      {/* Risk Assessment */}
      <div className="mt-6 p-4 rounded bg-gray-100">
        <h3 className="font-semibold">Sensor Deployment Assessment</h3>

        <p className="mt-1">
          Satellite Risk Score: <strong>{riskScore.toFixed(2)}</strong>
        </p>

        {decision === "DEPLOY_SENSORS" && (
          <p className="text-red-600 mt-2">
            🔴 High susceptibility detected. Ground sensors recommended.
          </p>
        )}

        {decision === "MONITOR" && (
          <p className="text-yellow-600 mt-2">
            🟠 Moderate susceptibility. Continue satellite monitoring.
          </p>
        )}

        {decision === "NO_DEPLOYMENT" && (
          <p className="text-green-600 mt-2">
            🟢 Low susceptibility. No sensor deployment needed.
          </p>
        )}
      </div>

      {/* Ground Sensor Status */}
      <div className="mt-6 bg-gray-100 p-4 rounded">
        <h3 className="font-semibold">Ground Sensor Status</h3>

        {hasSensors ? (
          <>
            <p className="text-green-700 mt-1">
              Ground sensors are deployed in this area.
            </p>

            <button
              className="mt-3 px-4 py-2 bg-blue-600 text-white rounded"
              onClick={() => router.push(`/sensor?area=${area}`)}
            >
              View Ground Sensor Data
            </button>
          </>
        ) : (
          <p className="text-yellow-700 mt-1">
            No ground sensors deployed yet.
            <br />
            Satellite assessment recommends monitoring.
          </p>
        )}
      </div>
    </main>
  );
}
