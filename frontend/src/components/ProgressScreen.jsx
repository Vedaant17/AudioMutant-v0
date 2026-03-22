import { useEffect, useState } from "react";

export default function ProgressScreen({ file, onComplete }) {
  const [progress, setProgress] = useState(0);
  const [step, setStep] = useState("");

  useEffect(() => {
    if (!file) return;

    const startAnalysis = async () => {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch("http://127.0.0.1:8000/analyze/start", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      const jobId = data.job_id;

      pollProgress(jobId);
    };

    const pollProgress = (jobId) => {
      const interval = setInterval(async () => {
        const res = await fetch(
          `http://127.0.0.1:8000/analyze/status/${jobId}`
        );
        const data = await res.json();

        setProgress(data.progress || 0);
        setStep(data.step || "");

        if (data.status === "completed") {
          clearInterval(interval);

          const resultRes = await fetch(
            `http://127.0.0.1:8000/analyze/result/${jobId}`
          );
          const result = await resultRes.json();

          onComplete(result); // 🔥 THIS replaces navigation
        }
      }, 500);
    };

    startAnalysis();
  }, [file]);

  return (
    <div className="overlay">
      <div className="glass-card">
        <h2>Analyzing your mix...</h2>
        <p>{step}</p>

        <div className="meter-bar">
          <div
            className="meter-fill"
            style={{ width: `${progress}%` }}
          />
        </div>

        <p>{progress}%</p>
      </div>
    </div>
  );
}