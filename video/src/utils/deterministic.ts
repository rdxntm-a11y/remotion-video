export function seeded(seed: number) {
  let state = seed >>> 0;
  return () => {
    state = (1664525 * state + 1013904223) >>> 0;
    return state / 4294967296;
  };
}

export function seededPoints(
  seed: number,
  count: number,
  width: number,
  height: number,
) {
  const random = seeded(seed);
  return Array.from({length: count}, (_, index) => ({
    id: index,
    x: random() * width,
    y: random() * height,
    alpha: 0.08 + random() * 0.22,
    radius: 0.5 + random() * 2.3,
  }));
}
