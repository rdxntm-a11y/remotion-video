import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

export const SweepTransition: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const progress = interpolate(t, [4.06, 4.92], [-0.24, 1.22], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{pointerEvents: 'none', overflow: 'hidden', opacity: progress > 0 ? 1 : 0}}>
      <div style={{position: 'absolute', top: 0, bottom: 0, left: `${progress * 125 - 20}%`, width: '18%', background: '#b52624', transform: 'skewX(-16deg)', boxShadow: '0 0 34px rgba(181,38,36,.34)'}} />
    </AbsoluteFill>
  );
};
