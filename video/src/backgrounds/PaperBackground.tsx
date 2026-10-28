import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {seededPoints} from '../utils/deterministic';

const PAPER = '#e4dfd2';
const INK = '#171515';
const RED = '#b52624';

export const PaperBackground: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const points = React.useMemo(() => seededPoints(4207, 150, width, height), [width, height]);
  const drift = interpolate(frame, [0, 149], [0, 18]);

  return (
    <AbsoluteFill style={{backgroundColor: PAPER, overflow: 'hidden'}}>
      <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`}>
        <defs>
          <filter id="paperNoise">
            <feTurbulence baseFrequency="0.72" numOctaves="3" seed="17" />
            <feColorMatrix values="0 0 0 0 0.38 0 0 0 0 0.33 0 0 0 0 0.25 0 0 0 .16 0" />
          </filter>
          <radialGradient id="paperVignette" cx="50%" cy="43%" r="72%">
            <stop offset="0%" stopColor="#fffdf5" stopOpacity="0.36" />
            <stop offset="100%" stopColor="#5f5148" stopOpacity="0.14" />
          </radialGradient>
        </defs>
        <rect width={width} height={height} fill={PAPER} />
        <rect width={width} height={height} filter="url(#paperNoise)" opacity="0.24" />
        <rect width={width} height={height} fill="url(#paperVignette)" />
        <g opacity="0.34" stroke={INK} fill="none">
          <path d={`M ${86 + drift} 265 H 994`} strokeWidth="2" />
          <path d={`M ${112 - drift * 0.4} 1650 H 970`} strokeWidth="1" />
          <path d={`M 106 ${340 + drift * 0.15} V 1604`} strokeWidth="1" />
        </g>
        <g fill={INK}>
          {points.map((point) => (
            <circle
              key={point.id}
              cx={point.x + drift * ((point.id % 3) - 1) * 0.35}
              cy={point.y}
              r={point.radius}
              opacity={point.alpha}
            />
          ))}
        </g>
        <g stroke={RED} strokeWidth="2" opacity="0.52">
          <path d="M 72 208 H 156" />
          <path d="M 72 208 V 292" />
          <path d="M 1008 1628 H 924" />
          <path d="M 1008 1628 V 1544" />
        </g>
      </svg>
    </AbsoluteFill>
  );
};
