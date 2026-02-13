"use client";

import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler,
  Tooltip
} from "chart.js";

import { Line } from "react-chartjs-2";

ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler,
  Tooltip
);

export default function Sparkline({ data = [], color = "#2563eb" }) {

  if (!data || data.length < 2) return null;

  const chartData = {
    labels: data.map((_, i) => i),
    datasets: [
      {
        data,
        borderColor: color,
        backgroundColor: color + "22",
        borderWidth: 2,
        tension: 0.4,
        pointRadius: 0,
        fill: true,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: { enabled: false }
    },
    scales: {
      x: { display: false },
      y: {
        display: false,
        min: Math.min(...data) - 0.01,
        max: Math.max(...data) + 0.01,
      },
    },
  };

  return (
    <div style={{ height: 50, width: "100%" }}>
      <Line data={chartData} options={options} />
    </div>
  );
}
