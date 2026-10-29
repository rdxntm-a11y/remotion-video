import React, {useState, useMemo} from 'react';
import {Composition, useFrame} from 'remotion';

const totalSeconds = 30;
const fps = 30;
const totalFrames = totalSeconds * fps; // 900

const captions = [
  "Once upon a time",
  "In a world of colors",
  "Dreams came alive",
  "And stories unfolded",
  "The end",
];

export const AnimoReel: React.FC = () => {
  const [captionIndex, setCaptionIndex] = useState(0);
  const [frame, setFrame] = useState(0);

  useFrame({
    durationInFrames: totalFrames,
    fps,
    onFrame: (frameNumber) => {
      setFrame(frameNumber);
      const newIndex = Math.floor(frameNumber / 90); // change every 90 frames (3 seconds)
      if (newIndex !== captionIndex) {
        setCaptionIndex(newIndex);
      }
    },
  });

  // Compute mouth open/close using sine wave
  const mouthOpen = (Math.sin(frame * 0.05) + 1) / 2; // 0..1

  return (
    <Composition
      id="AnimoReel"
      component={() => (
        <div style={{position: "relative", width: "100%", height: "100%"}}>
          {/* Gradient background */}
          <rect
            width="1080"
            height="1920"
            fill="linear-gradient(135deg, #8a2be2, #1e90ff)"
          />

          {/* Character SVG */}
          <svg
            width="200"
            height="300"
            style={{position: "absolute", left: "540", top: "860"}}
          >
            {/* Head */}
            <circle cx="100" cy="100" r="50" fill="#ffcc00" />

            {/* Body */}
            <rect x="80" y="150" width="40" height="100" fill="#ffcc00" />

            {/* Mouth */}
            <path
              d="M95,155 Q100,165 105,155"
              stroke="#ff0000"
              strokeWidth="4"
              fill="none"
              style={{
                transform: `scaleY(${mouthOpen})`,
                transformOrigin: "center",
              }}
            />
          </svg>

          {/* Pop‑up cards with spring animation */}
          {[30, 90, 150].map((showFrame) => (
            <rect
              key={showFrame}
              x={showFrame === 30 ? 20 : showFrame === 90 ? 800 : 20}
              y={showFrame === 30 ? 500 : showFrame === 90 ? 500 : 700}
              width={200}
              height={120}
              rx={15}
              ry={15}
              fill="white"
              stroke="black"
              strokeWidth={2}
              opacity={frame >= showFrame ? 1 : 0}
              style={{
                transition: "all 0.4s cubic-bezier(0.25, 0.8, 0.25, 1)",
                transform: frame >= showFrame ? "scale(1.1)" : "scale(0.9)",
              }}
            />
          ))}

          {/* Caption */}
          <div
            style={{
              position: "absolute",
              bottom: "40",
              left: "50%",
              transform: "translateX(-50%)",
              color: "#000",
              fontWeight: "bold",
              fontSize: "48px",
              textAlign: "center",
            }}
          >
            {captions[captionIndex] || "Story"}
          </div>
        </div>
      )}
      durationInFrames={totalFrames}
      fps={fps}
      width={1080}
      height={1920}
    />
  );
};

export default AnimoReel;