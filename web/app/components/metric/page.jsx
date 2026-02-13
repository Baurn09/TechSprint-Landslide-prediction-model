import Sparkline from "../sparkline/Sparkline";

export default function Metric({
  label,
  value = 0,
  trend,
  direction,
  color
}) {
  console.log(label, trend);

  return (
    <div className="bg-white p-4 rounded-xl shadow border border-gray-100 flex flex-col gap-2">

      <h4 className="text-sm text-gray-600">{label}</h4>

      <div className="flex items-center gap-2">
        <span className="text-2xl font-bold">
          {(value * 100).toFixed(0)}%
        </span>

        {direction === "up" && <span className="text-red-600 text-lg">▲</span>}
        {direction === "down" && <span className="text-green-600 text-lg">▼</span>}
        {direction === "stable" && <span className="text-gray-400 text-lg">▬</span>}
      </div>

      {trend && trend.length > 1 && (
        <Sparkline data={trend} color={color} />
      )}

    </div>
  );
}
