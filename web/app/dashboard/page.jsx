"use client";

import LineChart from "../components/chart/LineChart";
import "../lib/chartConfig";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { getAlertMessage } from "../lib/alertTemplates";
import { deployedSensors } from "../lib/deployedSensors.js";
import Metric from "../components/metric/page";




export default function Dashboard() {
  const [moistureHistory, setMoistureHistory] = useState([]);
  const [tiltHistory, setTiltHistory] = useState([]);
  const [data, setData] = useState(null);
  const searchParams = useSearchParams();
  const area = searchParams.get("area") || "default";
  const router = useRouter()
  
  const hasSensors = deployedSensors[area] == true;


  useEffect(() => {
  fetch(`/api/satellite?area=${area}`)
    .then(res => res.json())
    .then(setData);
  }, [area]);

  if (!data) {
    return <p className="p-8">Loading sensor data...</p>;
  }

  return (
    <main className="p-8 w-full min-h-screen text-black bg-white">
    


      <h1 className="text-2xl font-bold">Live Dashboard</h1>

      <p className="text-sm text-gray-500 mt-1">
        Last updated: {data.timestamp}
      </p>

      <p className="text-sm text-gray-600 mt-1">
        Monitoring Area: <strong>{area.toUpperCase()}</strong>
      </p>

      <div className="grid grid-cols-3 gap-4 mt-6">
        

        <Metric
          label="Slope Factor"
          value={data.slope}
          trend={data.trends.slope}
          color="#ef4444"
        />

        <Metric
          label="Rainfall Index"
          value={data.rainfall}
          trend={data.trends.rainfall}
          color="#3b82f6"
        />

        <Metric
          label="Vegetation Index"
          value={data.vegetation}
          trend={data.trends.vegetation}
          color="#22c55e"
        />
        <Metric label="Soil Proxy" value={data.soil} />
        <Metric label="Historical Susceptibility" value={data.history} />
      </div>



      {/*risk*/}
      <div className="mt-6 p-4 rounded bg-gray-100">
        <h3 className="font-semibold">Sensor Deployment Assessment</h3>

        <p className="mt-1">
          Satellite Risk Score: <strong>{data.riskScore}</strong>
        </p>

        {data.decision === "DEPLOY_SENSORS" && (
          <p className="text-red-600 mt-2">
            🔴 High susceptibility detected. Ground sensors recommended.
          </p>
        )}

        {data.decision === "MONITOR" && (
          <p className="text-yellow-600 mt-2">
            🟠 Moderate susceptibility. Continue satellite monitoring.
          </p>
        )}

        {data.decision === "NO_DEPLOYMENT" && (
          <p className="text-green-600 mt-2">
            🟢 Low susceptibility. No sensor deployment needed.
          </p>
        )}
      </div>


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
