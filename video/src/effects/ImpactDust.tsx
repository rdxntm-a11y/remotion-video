import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {seededPoints} from '../utils/deterministic';

export const ImpactDust: React.FC = () => {
  const frame = useCurrentFrame();
  const {width, height, fps} = useVideoConfig();
  const points = React.useMemo(() => seededPoints(201, 42, width, height), [width, height]);
  const t = frame / fps;
  const impact = interpolate(t, [3.95, 4.35, 5], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{pointerEvents: 'none', opacity: impact * 0.58}}>
      <svg width={width} height={height}>
        {points.map((point) => (
          <circle key={point.id} cx={540 + (point.x - width / 2) * impact} cy={980 + (point.y - height / 2) * impact} r={point.radius * 2} fill="#b52624" opacity={point.alpha} />
        ))}
      </svg>
    </AbsoluteFill>
  );
};
