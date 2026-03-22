import { useEffect, useRef } from "react";
import WaveSurfer from "wavesurfer.js";
import RegionsPlugin from "wavesurfer.js/dist/plugins/regions.esm.js";

export default function WaveformPlayer({ file }) {
  const containerRef = useRef(null);
  const waveRef = useRef(null);

  useEffect(() => {
    if (!file || !containerRef.current) return;

    // destroy old instance
    if (waveRef.current) {
      waveRef.current.destroy();
      waveRef.current = null;
    }

    const regions = RegionsPlugin.create();

    const ws = WaveSurfer.create({
      container: containerRef.current,
      waveColor: "#888",
      progressColor: "#22c55e",
      height: 100,
      plugins: [regions],
    });

    waveRef.current = ws;

    console.log("Loading file:", file.name);

    // ✅ THIS IS THE FIX
    ws.loadBlob(file);

    ws.on("ready", () => {
      const duration = ws.getDuration();

      regions.addRegion({
        start: duration * 0.2,
        end: duration * 0.3,
        color: "rgba(255, 0, 0, 0.3)"
      });

      regions.addRegion({
        start: duration * 0.5,
        end: duration * 0.6,
        color: "rgba(255, 255, 0, 0.3)"
      });
    });

    ws.on("error", (e) => {
      console.error("WaveSurfer error:", e);
    });

    return () => {
      if (waveRef.current) {
        waveRef.current.destroy();
        waveRef.current = null;
      }
    };
  }, [file]);

  return (
    <div>
      <div ref={containerRef} />
      <button onClick={() => waveRef.current?.playPause()}>
        Play / Pause
      </button>
    </div>
  );
}