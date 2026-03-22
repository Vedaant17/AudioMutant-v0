export default function Meter({ label, value }) {
  const safeValue = isNaN(value) ? 0 : value;
  const width = Math.min(100, safeValue * 100);

  return (
    <div style={{ marginBottom: "20px" }}>
      <p>{label}</p>

      <div
        style={{
          width: "100%",
          height: "10px",
          background: "#444",
        }}
      >
        <div
          style={{
            width: `${width}%`,   // ✅ FIXED HERE
            height: "100%",
            background: "limegreen",
          }}
        />
      </div>

      <p>{safeValue}</p>
    </div>
  );
}