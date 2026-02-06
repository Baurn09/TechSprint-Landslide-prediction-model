import Sparkline from "../sparkline/page";

export default function Metric({ label, value, trend, direction, color }) {
  return (
    <div className="bg-gray-200 p-4 rounded shadow">
      <h4 className="text-sm text-gray-600">{label}</h4>
      <p className="text-xl font-semibold mt-1 flex items-center gap-2">
        {(value * 100).toFixed(0)}%

        {direction === "up" && (
          <span className="text-red-600 text-lg">▲</span>
        )}

        {direction === "down" && (
          <span className="text-green-600 text-lg">▼</span>
        )}

        {direction === "stable" && (
          <span className="text-gray-500 text-lg">▬</span>
        )}
      </p>


      {trend && (
        <Sparkline data={trend} color={color} />
      )}
    </div>
  );
}
