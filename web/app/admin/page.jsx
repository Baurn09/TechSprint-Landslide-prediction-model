"use client";

import { deployedSensors } from "../lib/deployedSensors";

export default function AdminOverview() {
  const totalZones = Object.keys(deployedSensors).length;
  const deployedCount = Object.values(deployedSensors).filter(Boolean).length;

  // mock alert data (we’ll wire real alerts later)
  const alerts = [
    {
      area: "Noney",
      level: "CRITICAL",
      time: "14:32 IST",
    },
    {
      area: "Ukhrul",
      level: "WARNING",
      time: "13:10 IST",
    },
  ];

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-6">
        System Overview
      </h2>

      {/* KPI Cards */}
      <div className="grid grid-cols-4 gap-4 mb-8">
        <KPI label="Monitored Zones" value={totalZones} />
        <KPI label="Sensor-Deployed Zones" value={deployedCount} />
        <KPI
          label="Active Alerts"
          value={alerts.length}
          highlight
        />
        <KPI
          label="Last Update"
          value="2 min ago"
        />
      </div>

      {/* Active Alerts */}
      <div className="bg-slate-800 rounded p-4">
        <h3 className="text-lg font-semibold mb-3">
          Active Alerts
        </h3>

        {alerts.length === 0 ? (
          <p className="text-slate-400">
            No active alerts.
          </p>
        ) : (
          <table className="w-full text-sm">
            <thead className="text-slate-400">
              <tr>
                <th className="text-left py-1">Area</th>
                <th className="text-left py-1">Level</th>
                <th className="text-left py-1">Time</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map((alert, i) => (
                <tr key={i} className="border-t border-slate-700">
                  <td className="py-2">{alert.area}</td>
                  <td
                    className={`py-2 font-semibold ${
                      alert.level === "CRITICAL"
                        ? "text-red-400"
                        : "text-yellow-400"
                    }`}
                  >
                    {alert.level}
                  </td>
                  <td className="py-2">{alert.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

function KPI({ label, value, highlight }) {
  return (
    <div
      className={`rounded p-4 ${
        highlight
          ? "bg-red-900/40"
          : "bg-slate-800"
      }`}
    >
      <p className="text-sm text-slate-400">
        {label}
      </p>
      <p className="text-2xl font-bold mt-1">
        {value}
      </p>
    </div>
  );
}
