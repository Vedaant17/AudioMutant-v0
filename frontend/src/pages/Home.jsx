import { useEffect, useState } from "react";
import "../App.css";

import img1 from "../assets/img1.jpg";
import img2 from "../assets/img2.jpg";
import img4 from "../assets/img4.jpg";
import img6 from "../assets/img6.jpg";
import img7 from "../assets/img7.jpg";

const images = [img1, img2, img4, img6, img7];

export default function Home({ onUpload }) {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % images.length);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="container">
      {images.map((img, i) => (
        <div
          key={i}
          className={`bg-slide ${i === index ? "active" : ""}`}
          style={{ backgroundImage: `url(${img})` }}
        />
      ))}

      <div className="overlay">
        <div className="glass-card">
          <h1>AudioMutant</h1>
          <p>Your AI-powered Mix Assistant</p>

          <input
            type="file"
            accept="audio/*"
            id="fileInput"
            style={{ display: "none" }}
            onChange={(e) => {
              const file = e.target.files[0];
              if (file) onUpload(file);
            }}
          />

          <button
            className="cta"
            onClick={() => document.getElementById("fileInput").click()}
          >
            Upload Your Mix
          </button>
        </div>
      </div>
    </div>
  );
}