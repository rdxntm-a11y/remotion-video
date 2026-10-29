import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, spring, interpolate } from 'remotion';

export const AnimoReel: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  const captions = [
    "Once upon a time",
    "In a world of colors",
    "A new story begins",
    "Wait for the magic"
  ];
  const captionIndex = Math.min(
    Math.floor(frame / (fps * 3)),
    captions.length - 1
  );

  const mouthHeight = Math.abs(Math.sin(frame / 3)) * 20 + 5; 
  const bobbing = Math.sin(frame / 10) * 10; 

  const card1Opacity = spring({ frame: frame - 30, fps, config: { damping: 12 } });
  const card2Opacity = spring({ frame: frame - 90, fps, config: { damping: 12 } });
  const card3Opacity = spring({ frame: frame - 150, fps, config: { damping: 12 } });

  return (
    <AbsoluteFill style={{ background: 'linear-gradient(45deg, #6a11cb 0%, #2575fc 100%)' }}>
      <div style={{
        position: 'absolute',
        top: '50%', left: '50%',
        transform: `translate(-50%, -50%) translateY(${bobbing}px)`,
        display: 'flex', flexDirection: 'column', alignItems: 'center'
      }}>
        <svg width="200" height="250" viewBox="0 0 200 250">
          <rect x="50" y="120" width="100" height="120" rx="20" fill="#f1c27d" />
          <circle cx="100" cy="80" r="60" fill="#ffdfba" />
          <circle cx="75" cy="70" r="8" fill="#333" />
          <circle cx="125" cy="70" r="8" fill="#333" />
          <ellipse cx="100" cy="105" rx="20" ry={mouthHeight} fill="#333" />
        </svg>
      </div>

      <div style={{ position: 'absolute', top: '30%', left: '10%', opacity: card1Opacity, transform: `scale(${card1Opacity})`, background: 'white', padding: '20px', borderRadius: '15px', boxShadow: '0 10px 20px rgba(0,0,0,0.2)' }}>
        <h3 style={{ margin: 0, color: '#333' }}>Welcome!</h3>
      </div>
      <div style={{ position: 'absolute', top: '60%', right: '10%', opacity: card2Opacity, transform: `scale(${card2Opacity})`, background: 'white', padding: '20px', borderRadius: '15px', boxShadow: '0 10px 20px rgba(0,0,0,0.2)' }}>
        <h3 style={{ margin: 0, color: '#333' }}>Magic</h3>
      </div>
      <div style={{ position: 'absolute', top: '40%', left: '10%', opacity: card3Opacity, transform: `scale(${card3Opacity})`, background: 'white', padding: '20px', borderRadius: '15px', boxShadow: '0 10px 20px rgba(0,0,0,0.2)' }}>
        <h3 style={{ margin: 0, color: '#333' }}>Story</h3>
      </div>

      <div style={{
        position: 'absolute', bottom: '10%', width: '100%', textAlign: 'center',
        fontSize: 60, fontWeight: 'bold', color: 'white', fontFamily: 'sans-serif',
        textShadow: '2px 2px 10px rgba(0,0,0,0.5)'
      }}>
        {captions[captionIndex]}
      </div>
    </AbsoluteFill>
  );
};
