export type TimedWord = {
  readonly id: string;
  readonly text: string;
  readonly start: number;
  readonly end: number;
};

export type HeroProofTiming = {
  readonly durationInFrames: number;
  readonly fps: number;
  readonly words: readonly TimedWord[];
};
