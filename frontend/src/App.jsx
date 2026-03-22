import { useState } from "react";
import Home from "./pages/Home";
import ProgressScreen from "./components/ProgressScreen";
import Dashboard from "./pages/Dashboard";

function App() {
  const [stage, setStage] = useState("home");
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);

  return (
    <>
      {stage === "home" && (
        <Home
          onUpload={(file) => {
            setFile(file);
            setAudioUrl(URL.createObjectURL(file)); // ✅ FIXED HERE
            setStage("loading");
          }}
        />
      )}

      {stage === "loading" && (
        <ProgressScreen
          file={file}
          onComplete={(data) => {
            setResult(data);
            setStage("dashboard");
          }}
        />
      )}

      {stage === "dashboard" && (
        <Dashboard
          result={result}
          file={file}
          audioUrl={audioUrl}
        />
      )}
    </>
  );
}

export default App;