import Sparkline from "../sparkline/page";

export default function Metric({ label, value, trend, color }) {
  return (
    <div className="bg-gray-200 p-4 rounded shadow">
      <h4 className="text-sm text-gray-600">{label}</h4>
      <p className="text-xl font-semibold mt-1">
        {(value * 100).toFixed(0)}%
      </p>

      {trend && (
        <Sparkline data={trend} color={color} />
      )}
    </div>
  );
}
