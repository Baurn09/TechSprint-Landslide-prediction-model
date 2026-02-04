"use client";

import "../lib/chartConfig";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { deployedSensors } from "../lib/deployedSensors.js";
import Metric from "../components/metric/page";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const searchParams = useSearchParams();
  const area = searchParams.get("area") || "default";
  const router = useRouter();

  const hasSensors = deployedSensors[area] === true;

  useEffect(() => {
    fetch(`/api/satellite?area=${area}`)
      .then((res) => res.json())
      .then(setData)
      .catch(console.error);
  }, [area]);

  if (!data) {
    return <p className="p-8">Loading satellite assessment...</p>;
  }

  const { features, riskScore, decision } = data;

  return (
    <main className="p-8 w-full min-h-screen text-black bg-white">
      <h1 className="text-2xl font-bold">Live Dashboard</h1>

      <p className="text-sm text-gray-500 mt-1">
        Last updated: {new Date().toLocaleString()}
      </p>

      <p className="text-sm text-gray-600 mt-1">
        Monitoring Area: <strong>{area.toUpperCase()}</strong>
      </p>

      {/* Satellite Metrics */}
      <div className="grid grid-cols-3 gap-4 mt-6">
        <Metric
          label="Slope Factor"
          value={features.S}
          color="#ef4444"
        />

        <Metric
          label="Rainfall Index"
          value={features.R}
          color="#3b82f6"
        />

        <Metric
          label="Vegetation Index (NDVI)"
          value={features.V}
          color="#22c55e"
        />

        <Metric
          label="Soil Stability Proxy"
          value={features.P}
        />

        <Metric
          label="Historical Susceptibility"
          value={features.H}
        />
      </div>

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
