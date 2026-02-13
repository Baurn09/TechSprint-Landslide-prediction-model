"use client";

import "../lib/chartConfig";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { deployedSensors } from "../lib/deployedSensors.js";
import Metric from "../components/metric/page";
import RiskCircle from "../components/riskCircle/RiskCircle";

export default function Dashboard() {

  const [data, setData] = useState(null);
  const searchParams = useSearchParams();
  const grid_uid = searchParams.get("grid_uid")?.trim();
  const area = searchParams.get("area");
  const router = useRouter();

  const SENSOR_DEPLOYED_GRID = "+3467+934";

  const hasSensors =
    (grid_uid && grid_uid === SENSOR_DEPLOYED_GRID) ||
    (area && deployedSensors[area]);

  useEffect(() => {
    const url = grid_uid
      ? `/api/satellite?grid_uid=${encodeURIComponent(grid_uid)}`
      : `/api/satellite?area=${area}`;

    fetch(url).then(r => r.json()).then(setData);
  }, [area, grid_uid]);

  if (!data) return <p className="p-8">Loading…</p>;

  const { features, rawFeatures, riskScore, decision, drivers } = data;

  const directions = {
    S: features.S > 0.7 ? "up" : "stable",
    R: features.R > 0.6 ? "up" : "down",
    V: features.V < 0.4 ? "down" : "stable",
    P: "stable",
  };

  // ================= UI =================

  return (
    <main className="p-8 bg-[#F2EFEA] min-h-screen text-black">

      {/* HEADER */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold">Live Dashboard</h1>
        <p className="text-sm text-gray-600">
          Target: {grid_uid ? `GRID ${grid_uid}` : area}
        </p>
      </div>

      {/* ================= ROW 1 ================= */}

      <div className="grid grid-cols-3 gap-6">

        {/* LEFT — BIG SUMMARY */}
        <div className="col-span-2 bg-white rounded-xl p-10 shadow border border-gray-100">

          <h3 className="font-semibold mb-4">
            Satellite Risk Overview
          </h3>

          <div className="flex items-center justify-between">

            <div>
              <div className="text-lg text-gray-600 font-bold">
                Risk Score
              </div>

              <div className="text-sm text-gray-500 mt-2">
                Last updated: {new Date().toLocaleString()}
              </div>
            </div>

            <RiskCircle score={riskScore} />

          </div>
        </div>


        {/* RIGHT COLUMN STACK */}
        <div className="flex flex-col gap-6">

          {/* Deployment Decision */}
          <div className="bg-white rounded-xl p-6 shadow border border-gray-100">

            <h3 className="font-semibold mb-4">
              Deployment Decision
            </h3>

            {decision === "DEPLOY_SENSORS" && (
              <div className="text-red-600 font-semibold text-lg">
                🔴 Deploy Ground Sensors
              </div>
            )}

            {decision === "MONITOR" && (
              <div className="text-orange-600 font-semibold text-lg">
                🟠 Monitor Closely
              </div>
            )}

            {decision === "NO_DEPLOYMENT" && (
              <div className="text-green-600 font-semibold text-lg">
                🟢 No Deployment Needed
              </div>
            )}

          </div>


          {/* ⭐ MOVED — Ground Sensor Status */}
          <div className="bg-white rounded-xl p-6 shadow border border-gray-100">

            <h3 className="font-semibold mb-3">
              Ground Sensor Status
            </h3>

            {hasSensors ? (
              <>
                <div className="text-green-700 font-medium">
                  Sensors deployed
                </div>

                <button
                  className="mt-3 px-4 py-2 bg-blue-600 text-white rounded-lg shadow hover:bg-blue-700"
                  onClick={() =>
                    router.push(`/sensor?area=noney&sensor_id=${grid_uid}`)
                  }
                >
                  Open Ground Sensor Dashboard
                </button>
              </>
            ) : (
              <div className="text-yellow-700">
                No sensors deployed yet
              </div>
            )}

          </div>

        </div>
      </div>



      {/* ================= METRICS ================= */}

      <div className="grid grid-cols-4 gap-5 mt-6">

        <Metric label="Slope" value={features.S} direction={directions.S}/>
        <Metric label="Rainfall" value={features.R} direction={directions.R}/>
        <Metric label="NDVI" value={features.V} direction={directions.V}/>
        <Metric label="Soil" value={features.P} direction={directions.P}/>

      </div>


      {/* ================= DETAILS ================= */}

      <div className="grid grid-cols-2 gap-6 mt-6">

        {/* FEATURES */}
        {rawFeatures && (
          <div className="bg-white rounded-xl p-6 shadow border border-gray-100">

            <h3 className="font-semibold mb-4">
              Environmental Features
            </h3>

            <div className="grid grid-cols-2 gap-3 text-sm">
              <Info label="Elevation" v={rawFeatures.elevation}/>
              <Info label="Slope" v={rawFeatures.slope}/>
              <Info label="NDVI" v={rawFeatures.ndvi}/>
              <Info label="Rain 7d" v={rawFeatures.rain_7d}/>
              <Info label="Rain 30d" v={rawFeatures.rain_30d}/>
              <Info label="Soil Moisture" v={rawFeatures.soil_moisture}/>
            </div>

          </div>
        )}

        {/* DRIVERS */}
        {drivers && (
          <div className="bg-white rounded-xl p-6 shadow border border-gray-100">

            <h3 className="font-semibold mb-4">
              Risk Drivers
            </h3>

            <ul className="space-y-2 text-sm font-medium">
              {drivers.includes("rainfall") && <li>🌧️ High rainfall</li>}
              {drivers.includes("slope") && <li>⛰️ Steep slope</li>}
              {drivers.includes("vegetation") && <li>🌱 Low vegetation</li>}
              {drivers.includes("soil") && <li>💧 Soil saturation</li>}
            </ul>

          </div>
        )}

      </div>

    </main>
  );
}


// helper
function Info({ label, v }) {
  return (
    <div>
      <div className="text-gray-500 text-xs">{label}</div>
      <div className="font-semibold">{v?.toFixed ? v.toFixed(2) : v}</div>
    </div>
  );
}
