"use client";

export default function RiskCircle({ score }) {
  const percent = Math.round(score * 100);

  let color = "#22c55e";
  let label = "LOW";

  if (score >= 0.7) {
    color = "#dc2626";
    label = "CRITICAL";
  } else if (score >= 0.4) {
    color = "#f59e0b";
    label = "MODERATE";
  }

  const ringStyle = {
    background: `conic-gradient(${color} ${percent * 3.6}deg, #e5e7eb 0deg)`
  };

  return (
    <div className="relative w-40 h-40">
      <div className="w-40 h-40 rounded-full p-3" style={ringStyle}>
        <div className="w-full h-full rounded-full bg-white flex flex-col items-center justify-center shadow-inner">

          <div className="text-3xl font-bold">
            {percent}%
          </div>

          <div
            className={`text-xs font-semibold mt-1 ${
              score >= 0.7 ? "animate-pulse" : ""
            }`}
            style={{ color }}
          >
            {label}
          </div>

        </div>
      </div>
    </div>
  );
}
