import { useMemo } from "react";
import ResultsPanel from "../components/ResultsPanel";
import { useNavigate } from "react-router-dom";

function Dashboard({ result, file }) {
  const navigate = useNavigate();
  const audioUrl = useMemo(() => {
    if (!file) return null;
    return URL.createObjectURL(file);
  }, [file]);

  // ✅ HANDLE REFRESH CASE
  if (!result) {
    return (
      <div style={{ padding: "20px", color: "white" }}>
        <h2>No analysis data found</h2>
        <p>Please upload a file again.</p>
      </div>
    );
  }

  return (
    <div>
      <div><button onClick={() => navigate("/")}>Back to Home</button></div>
      <ResultsPanel
        result={result}
        file={file}
        audioUrl={audioUrl}
      />
    </div>
  );
}

export default Dashboard;