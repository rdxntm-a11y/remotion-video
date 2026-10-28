import React from 'react';
import {interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {DevanagariText} from './DevanagariText';
import {easeInOutCubic, easeOutQuint, remap} from '../utils/easing';

export const KineticWord: React.FC<{
  text: string;
  start: number;
  end: number;
  x: number;
  y: number;
  size: number;
  color?: string;
  activeColor?: string;
  rotate?: number;
}> = ({text, start, end, x, y, size, color = '#171515', activeColor = '#b52624', rotate = 0}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const seconds = frame / fps;
  const before = remap(seconds, start - 0.18, start);
  const active = remap(seconds, start, end);
  const settle = remap(seconds, end, end + 0.24);
  const reveal = easeOutQuint(before);
  const exit = 1 - easeInOutCubic(remap(seconds, end + 0.12, end + 0.52));
  const anticipation = interpolate(before, [0, 1], [18, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const yOffset = interpolate(easeOutQuint(before), [0, 1], [anticipation, 0]);
  const skew = interpolate(easeInOutCubic(settle), [0, 1], [0, -2], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const colorMix = active > 0 && active < 1 ? activeColor : color;

  return (
    <div
      style={{
        position: 'absolute',
        left: x,
        top: y + yOffset,
        transform: `translateY(${skew}px) rotate(${rotate}deg)`,
        transformOrigin: 'left bottom',
        opacity: reveal * exit,
        color: colorMix,
        fontSize: size,
        lineHeight: 0.92,
        letterSpacing: '-0.04em',
        whiteSpace: 'nowrap',
        textShadow: active > 0 && active < 1 ? '0 5px 0 rgba(181,38,36,.12)' : 'none',
      }}
    >
      <DevanagariText text={text} />
    </div>
  );
};
