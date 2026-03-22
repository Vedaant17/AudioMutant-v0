import {
  Radar, RadarChart, PolarGrid,
  PolarAngleAxis, PolarRadiusAxis,
  ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, Tooltip, Legend
} from "recharts";

import WaveformPlayer from "./WaveformPlayer";
import EQCurve from "./EQCurve";
import FrequencyBars from "./FrequencyBars";

export default function ResultsPanel({ result, file, audioUrl }) {
  if (!result) return null;

  const radarData = result.simulation_results
    ? Object.entries(result.simulation_results).map(([key, value]) => ({
        feature: key.replace("_", " ").toUpperCase(),
        value: Math.round((value || 0) * 100)
      }))
    : [];

  const comparisonData = (result.original_features && result.target_features)
    ? result.original_features.map((val, i) => ({
        feature: `F${i + 1}`,
        original: Math.round((val || 0) * 100),
        target: Math.round((result.target_features[i] || 0) * 100)
      }))
    : [];

  return (
    <div>
      <WaveformPlayer file ={file} />

      <h1>🎧 Analysis Complete</h1>

      <div style={{
        display: "grid",
        gridTemplateColumns: "repeat(auto-fit, minmax(200px, 1fr))",
        gap: "20px",
        marginTop: "20px"
      }}>
        <Card title="Genre" value={result.predicted_genre} />
        <Card title="Confidence" value={`${(result.confidence || 0).toFixed(2)}%`} />
        <MixScore score={result.mix_score || 0} />
        <Card title="Mix Quality" value={result.mix_label} />
      </div>

      <h2 style={{ marginTop: "40px" }}>📊 Feature Analysis</h2>
      <ResponsiveContainer width="100%" height={350}>
        <RadarChart data={radarData}>
          <PolarGrid />
          <PolarAngleAxis dataKey="feature" />
          <PolarRadiusAxis domain={[0, 100]} />
          <Radar dataKey="value" fill="#22c55e" fillOpacity={0.6} />
        </RadarChart>
      </ResponsiveContainer>

      <EQCurve
        original={result.original_features}
        target={result.target_features}
      />

      <FrequencyBars features={result.original_features} />

      <h2 style={{ marginTop: "40px" }}>🎛 Mix Comparison</h2>
      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={comparisonData}>
          <XAxis dataKey="feature" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="original" fill="#ffffff" />
          <Bar dataKey="target" fill="#22c55e" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div style={cardStyle}>
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}

function MixScore({ score }) {
  return (
    <div style={cardStyle}>
      <h3>Mix Score</h3>
      <div style={{ background: "#333", height: "10px", borderRadius: "5px" }}>
        <div
          style={{
            width: `${score}%`,
            height: "100%",
            background: "lime",
            borderRadius: "5px"
          }}
        />
      </div>
      <p>{score} / 100</p>
    </div>
  );
}

const cardStyle = {
  background: "#1e1e1e",
  padding: "15px",
  borderRadius: "10px",
  boxShadow: "0 0 10px rgba(0,0,0,0.5)"
};