"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import LineChart from "../components/chart/LineChart";
import "../lib/chartConfig";
import { deployedSensors } from "../lib/deployedSensors";

export default function SensorPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const area = searchParams.get("area") || "default";
  const sensorId = searchParams.get("sensor_id");

  // 🔒 block access if no sensors deployed
  if (!deployedSensors[area]) {
    router.push(`/dashboard?area=${area}`);
    return null;
  }

  const [data, setData] = useState(null);
  const [moistureHistory, setMoistureHistory] = useState([]);
  const [motionHistory, setMotionHistory] = useState([]);

  useEffect(() => {
    fetchData();
    
    const id = setInterval(fetchData, 3000);
    return () => clearInterval(id);
  }, [area]);

  const fetchData = async () => {
    const res = await fetch(`/api/sensor?area=${area}`);
    const json = await res.json();

    setData(json);

    console.log("Fetched sensor data:", json);

    if (json?.features?.soilMoisture !== undefined) {
      setMoistureHistory((prev) => [
        ...prev.slice(-19),
        json.features.soilMoisture,
      ]);
    }

    if (json?.features?.magnitude !== undefined) {
      setMotionHistory((prev) => [
        ...prev.slice(-19),
        json.features.vibration,
      ]);
    }
  };

  if (!data) {
    return <p className="p-8">Loading ground sensor data…</p>;
  }

  const { features, riskScore } = data;

  // ==========================
  // 🔮 FORECAST LOGIC
  // ==========================
  const forecast = getForecast(riskScore);

  return (
    <main className="p-8 bg-white text-black min-h-screen">
      {/* NEAR-TERM ALERT */}
      {forecast.level === "NEAR_TERM" && (
        <div className="mb-6 bg-red-600 text-white p-4 rounded shadow animate-pulse">
          <h2 className="text-lg font-bold">
            🚨 NEAR-TERM LANDSLIDE WARNING
          </h2>
          <p className="text-sm">
            Expected within <strong>{forecast.duration}</strong>
          </p>
        </div>
      )}

      <h1 className="text-2xl font-bold mb-1">
        Ground Sensor Monitoring
      </h1>

      <p className="text-sm text-gray-600">
        Area: {area.toUpperCase()}
      </p>

      <p className="text-sm text-gray-600">
        Sensor ID: <strong>{sensorId ?? "—"}</strong>
      </p>

      {/* Sensor summary */}
      <div className="grid grid-cols-3 gap-6 mt-6">
        <Metric
          label="Soil Moisture (%)"
          value={features.soilMoisture}
        />

        <Metric
          label="Tilt Index"
          value={features.tilt}
        />

        <Metric
          label="Vibration Index"
          value={features.vibration}
        />
      </div>

      {/* ML Risk */}
      <div className="mt-6 p-4 bg-gray-100 rounded">
        <h3 className="font-semibold">
          Ground Sensor ML Risk Estimation
        </h3>
        <p className="mt-1">
          Risk Score: <strong>{riskScore}</strong>
        </p>
      </div>

      {/* 🔮 FORECAST PANEL */}
      <div className="mt-6 p-4 rounded bg-gray-100">
        <h3 className="font-semibold">Landslide Forecast</h3>

        <p className={`mt-2 font-medium ${forecast.textClass}`}>
          {forecast.message}
        </p>

        <p
          className={`text-md font-bold rounded-md px-2 w-fit text-white py-1 mt-2 ${forecast.windowClass}`}
        >
          Forecast Window: <strong>{forecast.duration}</strong>
        </p>

      </div>

      {/* Trends */}
      <div className="grid grid-cols-2 gap-6 mt-10">
        <div className="bg-gray-100 p-4 rounded">
          <h4 className="font-semibold mb-2">
            Soil Moisture Trend
          </h4>
          <LineChart
            label="Soil Moisture"
            dataPoints={moistureHistory}
            color="rgba(34,197,94,1)"
          />
        </div>

        <div className="bg-gray-100 p-4 rounded">
          <h4 className="font-semibold mb-2">
            Motion Magnitude Trend
          </h4>
          <LineChart
            label="Motion"
            dataPoints={motionHistory}
            color="rgba(220,38,38,1)"
          />
        </div>
      </div>

      {/* metadata */}
      <div className="mt-10 bg-gray-50 p-4 rounded text-sm text-gray-700">
        <strong>Sensor Configuration</strong>
        <ul className="list-disc list-inside mt-1">
          <li>Soil moisture probe (depth: 1 m)</li>
          <li>3-axis accelerometer</li>
          <li>Sampling interval: 3 seconds</li>
          <li>ML model: Random Forest</li>
        </ul>
      </div>
    </main>
  );
}

/* ==========================
   Helper Components & Logic
   ========================== */

function getForecast(riskScore) {
  if (riskScore >= 0.7) {
    return {
      level: "NEAR_TERM",
      duration: "24–72 hours",
      message:
        "🚨 Landslide likely in the near term. Immediate preparedness advised.",
      textClass: "text-red-700",
      windowClass: "bg-red-700 animate-pulse",
    };
  }

  if (riskScore >= 0.4) {
    return {
      level: "MODERATE",
      duration: "3–7 days",
      message:
        "🟠 Conditions indicate increasing instability. Monitor closely.",
      textClass: "text-orange-600",
      windowClass: "bg-orange-600",
    };
  }

  return {
    level: "STABLE",
    duration: "No immediate threat",
    message: "🟢 Ground conditions are currently stable.",
    textClass: "text-green-700",
    windowClass: "bg-green-700",
  };
}


function Metric({ label, value }) {
  return (
    <div className="bg-gray-200 p-4 rounded shadow">
      <p className="text-sm text-gray-600">{label}</p>
      <p className="text-2xl font-semibold mt-1">
        {value}
      </p>
    </div>
  );
}
