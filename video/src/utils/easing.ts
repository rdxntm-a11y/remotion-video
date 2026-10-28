import {Easing} from 'remotion';

export const easeOutQuint = (t: number) => 1 - Math.pow(1 - t, 5);
export const easeInCubic = (t: number) => t * t * t;
export const easeInOutCubic = (t: number) =>
  t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

export const paperEase = Easing.bezier(0.21, 0.72, 0.32, 1);
export const inkEase = Easing.bezier(0.12, 0.76, 0.18, 1);
export const metalEase = Easing.bezier(0.65, 0, 0.15, 1);

export const clamp01 = (value: number) => Math.min(1, Math.max(0, value));
export const remap = (value: number, start: number, end: number) =>
  clamp01((value - start) / Math.max(0.0001, end - start));
