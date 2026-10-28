import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {moustachePath, cubic} from '../utils/geometry';
import {easeOutQuint, remap} from '../utils/easing';

const toPath = (points: ReturnType<typeof moustachePath>['left'], progress: number) => {
  const [p0, p1, p2, p3] = points;
  const sampleCount = Math.max(2, Math.round(32 * progress));
  const samples = Array.from({length: sampleCount}, (_, index) => cubic(p0, p1, p2, p3, index / (sampleCount - 1)));
  return samples.map((point, index) => `${index === 0 ? 'M' : 'L'} ${point.x.toFixed(1)} ${point.y.toFixed(1)}`).join(' ');
};

export const Moustache: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const seconds = frame / fps;
  const grow = easeOutQuint(remap(seconds, 2.15, 3.25));
  const sweep = remap(seconds, 3.42, 4.75);
  const path = moustachePath(540, 846 - sweep * 320, 780 + sweep * 480);
  const y = 846 - sweep * 320;
  const transform = `translate(${sweep * -740}px, ${sweep * -150}px) rotate(${sweep * -11}deg)`;

  return (
    <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{position: 'absolute', inset: 0, overflow: 'visible'}}>
      <g transform={transform}>
        <path d={toPath(path.left, grow)} fill="none" stroke="#171515" strokeWidth={34} strokeLinecap="round" />
        <path d={toPath(path.right, grow)} fill="none" stroke="#171515" strokeWidth={34} strokeLinecap="round" />
        <path d={toPath(path.left, grow)} fill="none" stroke="#b52624" strokeOpacity={0.74} strokeWidth={5} strokeLinecap="round" />
        <path d={toPath(path.right, grow)} fill="none" stroke="#b52624" strokeOpacity={0.74} strokeWidth={5} strokeLinecap="round" />
      </g>
      <path d={`M 405 ${y} C 460 ${y - 10} 500 ${y - 20} 540 ${y - 4}`} fill="none" stroke="#b52624" strokeWidth="5" opacity={grow} />
    </svg>
  );
};
