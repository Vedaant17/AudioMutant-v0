import { useEffect, useRef } from "react";
import WaveSurfer from "wavesurfer.js";
import RegionsPlugin from "wavesurfer.js/dist/plugins/regions.esm.js";

export default function WaveformPlayer({ file,audioUrl, onRegionClick }) {
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
    const problemRegions = [
  {
    startRatio: 0.2,
    endRatio: 0.3,
    color: "rgba(255,0,0,0.3)",
    data: {
      type: "mud",
      message: "Mud detected",
      fixes: [
        "Cut 250Hz by -3dB",
        "Reduce reverb",
        "High-pass guitars"
      ]
    }
  },
  {
    startRatio: 0.5,
    endRatio: 0.6,
    color: "rgba(255,255,0,0.3)",
    data: {
      type: "harshness",
      message: "Harshness detected",
      fixes: [
        "Cut 3kHz by -2dB",
        "De-ess vocals",
        "Reduce cymbal brightness"
      ]
    }
  }
];

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
    if(file){
    ws.loadBlob(file);
    }
    else if (audioUrl){
      ws.load(audioUrl);
    }

    ws.on("ready", () => {
      const duration = ws.getDuration();

problemRegions.forEach(r => {
  const region = regions.addRegion({
  start: duration * r.startRatio,
  end: duration * r.endRatio,
  color: r.color,
  drag: false,
  resize: false
});

// ✅ Attach custom data manually
region.customData = {
  ...r.data,
  start: duration * r.startRatio,
  end: duration * r.endRatio
};

  // 🔥 CLICK HANDLER
  region.on("click", (e) => {
    e.stopPropagation();
    console.log("Region Clicked:", region.data);
    if (onRegionClick){
      onRegionClick(region.customData);
    }
  });
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