import { useState, useEffect } from "react";
import { Routes, Route, useNavigate } from "react-router-dom";

import Home from "./pages/Home";
import ProgressScreen from "./components/ProgressScreen";
import Dashboard from "./pages/Dashboard";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);

  const navigate = useNavigate();

  // ✅ Load persisted data on refresh
  useEffect(() => {
    const savedResult = localStorage.getItem("result");
    if (savedResult) {
      setResult(JSON.parse(savedResult));
    }

    const savedAudioUrl = sessionStorage.getItem("audioUrl");
    if (savedAudioUrl) {
      setAudioUrl(savedAudioUrl);
    }
  }, []);

  // ✅ Save result persistently
  useEffect(() => {
    if (result) {
      localStorage.setItem("result", JSON.stringify(result));
    }
  }, [result]);

  return (
    <Routes>
      {/* 🏠 HOME */}
      <Route
        path="/"
        element={
          <Home
            onUpload={(file) => {
              const url = URL.createObjectURL(file);

              setFile(file);
              setAudioUrl(url);

              sessionStorage.setItem("audioUrl", url); // ✅ lightweight persistence

              navigate("/loading");
            }}
          />
        }
      />

      {/* ⏳ LOADING */}
      <Route
        path="/loading"
        element={
          <ProgressScreen
            file={file}
            onComplete={(data) => {
              setResult(data);
              navigate("/results"); // ✅ move after analysis
            }}
          />
        }
      />

      {/* 📊 RESULTS */}
      <Route
        path="/results"
        element={
          <Dashboard
            file={file}
            result={result}
            audioUrl={audioUrl}
          />
        }
      />
    </Routes>
  );
}

export default App;