"use client";

import { useEffect, useState } from "react";
import { sensorRegistry } from "../../lib/sensorRegistry";
import { generateGatewayFeed } from "../../lib/gatewayFeed";
import { useRouter } from "next/navigation";


export default function GatewayDashboard() {
  const [feed, setFeed] = useState([]);
  const router = useRouter();

  useEffect(() => {
    updateFeed();
    const id = setInterval(updateFeed, 4000);
    return () => clearInterval(id);
  }, []);

  const updateFeed = () => {
    setFeed(generateGatewayFeed());
  };

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-6">
        Collection Booth (Grid`` Gateway)
      </h2>

      <p className="text-sm text-slate-400 mb-4">
        Aggregated sensor feed from hill-region ground sensors
      </p>

      <div className="bg-slate-800 rounded p-4">
        <table className="w-full text-sm">
          <thead className="text-slate-400 border-b border-slate-700">
            <tr>
              <th className="text-left py-2">Sensor ID</th>
              <th className="text-left py-2">Area</th>
              <th className="text-left py-2">Risk</th>
              <th className="text-left py-2">Soil (%)</th>
              <th className="text-left py-2">Motion</th>
              <th className="text-left py-2">Last Seen</th>
            </tr>
          </thead>

          <tbody>
            {feed.map((sensor) => (
              <tr
                key={sensor.sensorId}
                className="border-t border-slate-700"
              >
                <td className="py-2 font-mono">
                    <button
                        onClick={() =>
                        router.push(
                            `/sensor?area=${sensor.area}&sensor_id=${sensor.sensorId}`
                        )
                        }
                        className="text-blue-400 hover:underline"
                    >
                        {sensor.sensorId}
                    </button>
                </td>

                <td className="py-2 uppercase">
                  {sensor.area}
                </td>
                <td
                  className={`py-2 font-semibold ${
                    sensor.risk === "CRITICAL"
                      ? "text-red-400"
                      : sensor.risk === "WARNING"
                      ? "text-yellow-400"
                      : "text-green-400"
                  }`}
                >
                  {sensor.risk}
                </td>
                <td className="py-2">
                  {sensor.soilMoisture}
                </td>
                <td className="py-2">
                  {sensor.motion}
                </td>
                <td className="py-2 text-slate-400">
                  {sensor.lastSeen}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <p className="text-xs text-slate-400 mt-4">
        * Data represents LoRa uplink packets received at
        gateway.
      </p>
    </div>
  );
}
