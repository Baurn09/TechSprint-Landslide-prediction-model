"use client";

import LineChart from "../components/chart/LineChart";
import "../lib/chartConfig";
import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { getAlertMessage } from "../lib/alertTemplates";

export default function SensorPage() {
  const searchParams = useSearchParams();
  const area = searchParams.get("area") || "default";

  const [data, setData] = useState(null);
  const [moistureHistory, setMoistureHistory] = useState([]);
  const [tiltHistory, setTiltHistory] = useState([]);
  const [alertActive, setAlertActive] = useState(false);
  const [alertHistory, setAlertHistory] = useState([]);

  // fetch ground sensor data   

  const fetchData = async () => {
    try {
      const res = await fetch(`/api/sensor?area=${area}`);
      const json = await res.json();

      setData(json);

      setMoistureHistory((prev) =>
        [...prev.slice(-19), json.soilMoisture]
      );

      setTiltHistory((prev) =>
        [...prev.slice(-19), json.tilt]
      );
    } catch (err) {
      console.error(err);
    }
  };
   useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 3000);
    return () => clearInterval(interval);
  }, [area]);

  // ALERT LOGIC — ONLY HERE
  useEffect(() => {
    if (!data) return;

    if (data.riskLevel === "CRITICAL" && !alertActive) {
      setAlertActive(true);

      const message = getAlertMessage("CRITICAL", area);

      setAlertHistory((prev) => [
        {
          time: new Date().toLocaleTimeString(),
          title: message.title,
          details: message.body,
        },
        ...prev,
      ]);
    }

    if (data.riskLevel !== "CRITICAL" && alertActive) {
      setAlertActive(false);
    }
  }, [data, alertActive, area]);

  if (!data) {
    return <p className="p-8">Loading ground sensor data…</p>;
  }

  return (
    <main className="p-8 bg-white text-black">
      {alertActive && (
        <div className="mb-6 bg-red-600 text-white p-4 rounded shadow animate-pulse">
          <h2 className="text-lg font-bold">
            🚨 GROUND SENSOR ALERT
          </h2>
          <p className="text-sm mt-1">
            Imminent landslide risk detected in{" "}
            <strong>{area.toUpperCase()}</strong>
          </p>
        </div>
      )}

      <h1 className="text-2xl font-bold">
        Ground Sensor Monitoring
      </h1>

      <p className="text-sm text-gray-600 mt-1">
        Area: <strong>{area.toUpperCase()}</strong>
      </p>

      {/* sensor values */}
      <div className="grid grid-cols-3 gap-6 mt-6">
        <div className="bg-gray-200 p-4 rounded">
          <h3>Soil Moisture</h3>
          <p className="text-2xl">{data.soilMoisture}%</p>
        </div>

        <div className="bg-gray-200 p-4 rounded">
          <h3>Rainfall</h3>
          <p className="text-2xl">{data.rainfall} mm/hr</p>
        </div>

        <div className="bg-gray-200 p-4 rounded">
          <h3>Tilt</h3>
          <p className="text-2xl">{data.tilt}°</p>
        </div>
      </div>

      {/* charts */}
      <div className="grid grid-cols-2 gap-6 mt-8">
        <LineChart
          label="Soil Moisture"
          dataPoints={moistureHistory}
          color="rgba(37,99,235,1)"
        />
        <LineChart
          label="Tilt"
          dataPoints={tiltHistory}
          color="rgba(220,38,38,1)"
        />
      </div>

      {/* alert timeline */}
      <div className="mt-8 bg-gray-100 p-4 rounded">
        <h3 className="font-semibold mb-2">
          Alert Timeline
        </h3>

        {alertHistory.length > 0 ? (
          alertHistory.map((a, i) => (
            <div key={i} className="mb-2">
              <strong>{a.time}</strong> — {a.title}
              <pre className="text-xs whitespace-pre-wrap text-gray-600">
                {a.details}
              </pre>
            </div>
          ))
        ) : (
          <p className="text-sm text-gray-500">
            No alerts issued yet.
          </p>
        )}
      </div>
    </main>
  );
}
