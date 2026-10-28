import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';

export const FilmGrain: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{pointerEvents: 'none', mixBlendMode: 'multiply', opacity: 0.16}}>
      <svg width="100%" height="100%" viewBox="0 0 1080 1920" preserveAspectRatio="none">
        <filter id="grain" x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.84" numOctaves="2" seed={frame + 300} />
          <feColorMatrix values="0 0 0 0 0.18 0 0 0 0 0.13 0 0 0 0 0.1 0 0 0 .55 0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  );
};
