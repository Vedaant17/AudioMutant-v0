import { useState } from "react";

export default function AIAdvicePanel({ result }) {
  const [mode, setMode] = useState("detailed");
  const [advice, setAdvice] = useState("");

  const fetchAdvice = async () => {
    const res = await fetch("http://localhost:8000/ai-feedback", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        engine_result: result,
        mode: mode,
      }),
    });

    const data = await res.json();
    setAdvice(data.ai_advice);
  };

  return (
    <div>
      <select value={mode} onChange={(e) => setMode(e.target.value)}>
        <option value="quick">Quick</option>
        <option value="detailed">Detailed</option>
        <option value="pro">Pro</option>
      </select>

      <button onClick={fetchAdvice}>Get AI Advice</button>

      <pre style={{ whiteSpace: "pre-wrap", marginTop: "20px" }}>
        {advice}
      </pre>
    </div>
  );
}