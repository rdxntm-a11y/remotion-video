import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {seededPoints} from '../utils/deterministic';

export const NightBackground: React.FC<{opacity?: number}> = ({opacity = 1}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const stars = React.useMemo(() => seededPoints(91, 70, width, height), [width, height]);
  const amber = interpolate(frame, [0, 149], [0.05, 0.19]);

  return (
    <AbsoluteFill style={{opacity, background: '#101014'}}>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        <defs>
          <radialGradient id="nightGlow" cx="50%" cy="38%" r="72%">
            <stop offset="0%" stopColor="#aa6c2f" stopOpacity={amber} />
            <stop offset="58%" stopColor="#1b1620" stopOpacity="0.2" />
            <stop offset="100%" stopColor="#050506" stopOpacity="0.85" />
          </radialGradient>
        </defs>
        <rect width={width} height={height} fill="url(#nightGlow)" />
        <g fill="#e4dfd2">
          {stars.map((star) => (
            <circle key={star.id} cx={star.x} cy={star.y} r={star.radius} opacity={star.alpha} />
          ))}
        </g>
        <path d="M -40 1320 C 280 1180 440 1450 1120 1190" fill="none" stroke="#b52624" strokeOpacity=".28" strokeWidth="3" />
      </svg>
    </AbsoluteFill>
  );
};
