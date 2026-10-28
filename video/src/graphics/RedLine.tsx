import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {remap} from '../utils/easing';

export const RedLine: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const draw = remap(t, 0.18, 1.0);
  const sweep = remap(t, 4.18, 5.0);
  const dash = interpolate(draw, [0, 1], [420, 0]);
  return (
    <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, pointerEvents: 'none'}}>
      <path
        d="M 86 1332 C 284 1288 370 1378 520 1328 C 686 1272 768 1336 1002 1280"
        fill="none"
        stroke="#b52624"
        strokeWidth="5"
        strokeLinecap="round"
        strokeDasharray="420 420"
        strokeDashoffset={dash}
        opacity={0.86}
      />
      <path
        d="M -180 870 C 210 760 520 1002 1220 632"
        fill="none"
        stroke="#b52624"
        strokeWidth="11"
        strokeLinecap="round"
        strokeDasharray="1500 1500"
        strokeDashoffset={interpolate(sweep, [0, 1], [1500, 0])}
        opacity={sweep * 0.72}
      />
    </svg>
  );
};
