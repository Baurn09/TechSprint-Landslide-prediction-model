"use client";

import { Line } from "react-chartjs-2";

export default function LineChart({ label, dataPoints, color }) {
  const data = {
    labels: dataPoints.map((_, i) => i + 1),
    datasets: [
      {
        label,
        data: dataPoints,
        borderColor: color,
        backgroundColor: color,
        tension: 0.4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      y: {
        beginAtZero: false,
      },
    },
  };

  return (
    <div className="h-64">
      <Line data={data} options={options} />
    </div>
  );
}
