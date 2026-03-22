export default function FrequencyBars({ features }) {
  if (!features) return null;

  const bands = [
    { name: "Low", range: [0, 5] },
    { name: "Low-Mid", range: [6, 10] },
    { name: "Mid", range: [11, 15] },
    { name: "High-Mid", range: [16, 20] },
    { name: "High", range: [21, 25] },
  ];

  const data = bands.map(b => {
    const values = features.slice(b.range[0], b.range[1] + 1);
    const avg = values.reduce((a, v) => a + v, 0) / values.length;

    return {
      name: b.name,
      value: Math.round(avg * 100)
    };
  });

  return (
    <div style={{ marginTop: "40px" }}>
      <h2>🎛 Frequency Balance</h2>

      {data.map((b) => (
        <div key={b.name} style={{ marginBottom: "10px" }}>
          <strong>{b.name}</strong>
          <div style={{ background: "#333", height: "10px" }}>
            <div
              style={{
                width: `${b.value}%`,
                height: "100%",
                background: "cyan"
              }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}