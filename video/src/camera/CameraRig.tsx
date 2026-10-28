import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';

export const CameraRig: React.FC<{children: React.ReactNode}> = ({children}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const push = interpolate(t, [0, 2.2, 3.4, 5], [1.035, 1.0, 1.04, 1.16], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const x = interpolate(t, [0, 3.4, 5], [0, 0, -96], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const y = interpolate(t, [0, 3.4, 5], [0, 0, -132], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const rotation = interpolate(t, [0, 3.4, 5], [0, 0, -2.5], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
      <div style={{position: 'absolute', inset: 0, transform: `translate(${x}px, ${y}px) scale(${push}) rotate(${rotation}deg)`, transformOrigin: '50% 46%'}}>
        {children}
      </div>
    </AbsoluteFill>
  );
};
