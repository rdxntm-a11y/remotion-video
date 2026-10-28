import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {easeOutQuint, remap} from '../utils/easing';

const needles = [
  {x: 186, y: 672, angle: -18, length: 260},
  {x: 272, y: 774, angle: -10, length: 188},
  {x: 820, y: 706, angle: 16, length: 230},
  {x: 908, y: 820, angle: 23, length: 190},
  {x: 358, y: 910, angle: 6, length: 160},
  {x: 724, y: 938, angle: -8, length: 170},
];

export const NeedleField: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const progress = easeOutQuint(remap(frame / fps, 0.42, 1.35));
  const activeOpacity = interpolate(progress, [0, 0.22, 1], [0, 0.85, 0.42]);
  return (
    <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0}}>
      <g stroke="#b52624" strokeWidth="3" strokeLinecap="round" opacity={activeOpacity}>
        {needles.map((needle) => {
          const radians = (needle.angle * Math.PI) / 180;
          const length = needle.length * progress;
          return (
            <line
              key={`${needle.x}-${needle.y}`}
              x1={needle.x}
              y1={needle.y}
              x2={needle.x + Math.cos(radians) * length}
              y2={needle.y + Math.sin(radians) * length}
            />
          );
        })}
      </g>
    </svg>
  );
};
