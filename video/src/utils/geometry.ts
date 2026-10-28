export type Point = {x: number; y: number};

export const lerp = (a: number, b: number, t: number) => a + (b - a) * t;

export const cubic = (
  p0: Point,
  p1: Point,
  p2: Point,
  p3: Point,
  t: number,
): Point => {
  const u = 1 - t;
  return {
    x: u ** 3 * p0.x + 3 * u ** 2 * t * p1.x + 3 * u * t ** 2 * p2.x + t ** 3 * p3.x,
    y: u ** 3 * p0.y + 3 * u ** 2 * t * p1.y + 3 * u * t ** 2 * p2.y + t ** 3 * p3.y,
  };
};

export const moustachePath = (centerX: number, y: number, width: number) => {
  const half = width / 2;
  return {
    left: [
      {x: centerX, y},
      {x: centerX - half * 0.16, y: y - 26},
      {x: centerX - half * 0.7, y: y - 4},
      {x: centerX - half, y: y + 92},
    ],
    right: [
      {x: centerX, y},
      {x: centerX + half * 0.16, y: y - 26},
      {x: centerX + half * 0.7, y: y - 4},
      {x: centerX + half, y: y + 92},
    ],
  };
};
