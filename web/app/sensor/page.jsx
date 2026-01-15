"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import LineChart from "../components/chart/LineChart";
import "../lib/chartConfig";
import { deployedSensors } from "../lib/deployedSensors";


export default function SensorPage() {
  const searchParams = useSearchParams();
  const area = searchParams.get("area") || "default";
  const sensorId = searchParams.get("sensor_id");


  // block access if no sensors
  

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

    setMoistureHistory((prev) =>
      [...prev.slice(-19), json.soilMoisture]
    );

    if (json.motion && typeof json.motion.magnitude === "number") {
  setMotionHistory((prev) => [
    ...prev.slice(-19),
    json.motion.magnitude,
  ]);
}

  };

  if (!data) {
    return <p className="p-8">Loading sensor data…</p>;
  }

const isCritical =
  data?.soilMoisture > 80 &&
  data?.motion?.magnitude > 0.25;


  return (
    <main className="p-8 bg-white text-black">
      {isCritical && (
        <div className="mb-6 bg-red-600 text-white p-4 rounded shadow animate-pulse">
          <h2 className="text-lg font-bold">
            🚨 GROUND INSTABILITY DETECTED
          </h2>
          <p className="text-sm">
            Immediate attention required in{" "}
            <strong>{area.toUpperCase()}</strong>
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
      <div className="">
        <div className="grid grid-cols-3 gap-6 mt-6">
          <Metric
            label="Soil Moisture (%)"
            value={
              data?.soilMoisture !== undefined
                ? data.soilMoisture.toFixed(1)
                : "—"
            }
          />

          <Metric
            label="Tilt (deg)"
            value={
              data?.motion?.tilt !== undefined
                ? data.motion.tilt.toFixed(3)
                : "—"
            }
          />

          <Metric
            label="Vibration Index"
            value={
              data?.motion?.vibration !== undefined
                ? data.motion.vibration.toFixed(3)
                : "—"
            }
          />
        </div>


      </div>

      {/* 3-axis motion */}
      <div className="mt-8">
        <h3 className="font-semibold mb-3">
          3-Axis Motion Sensor
        </h3>

        <div className="grid grid-cols-3 gap-4">
          <Metric
            label="X-Axis (E–W)"
            value={data.motion.x.toFixed(3)}
          />
          <Metric
            label="Y-Axis (N–S)"
            value={data.motion.y.toFixed(3)}
          />
          <Metric
            label="Z-Axis (Vertical)"
            value={data.motion.z.toFixed(3)}
          />
        </div>
      </div>

      {/* trends */}
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
        </ul>
      </div>
    </main>
  );
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
