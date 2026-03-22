import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer
} from "recharts";

export default function EQCurve({ original, target }) {
  if (!original || !target) return null;

  const data = original.map((val, i) => ({
    band: i,
    original: val || 0,
    target: target[i] || 0,
    diff: (target[i] || 0) - (val || 0)
  }));

  return (
    <div style={{ marginTop: "40px" }}>
      <h2>🎚 EQ Curve Suggestion</h2>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <XAxis dataKey="band" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="original" stroke="#ffffff" />
          <Line type="monotone" dataKey="target" stroke="#22c55e" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}