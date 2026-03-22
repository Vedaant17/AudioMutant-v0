import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar
} from "recharts";

export default function FeatureRadar({ data }) {
  return (
    <RadarChart width={400} height={300} data={data}>
      <PolarGrid />
      <PolarAngleAxis dataKey="feature" />
      <PolarRadiusAxis domain={[0, 100]} />
      <Radar dataKey="original" />
      <Radar dataKey="target" />
    </RadarChart>
  );
}