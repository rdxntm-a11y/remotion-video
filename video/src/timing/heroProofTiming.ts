import type {HeroProofTiming} from './types';

/**
 * The approved timing JSON is intentionally not edited for this proof. The
 * target moustache lyric is not present in the current 26-line sync export,
 * so this local scene clock is a visual blocking map, not a replacement for
 * the frozen song timestamps.
 */
export const HERO_PROOF_TIMING: HeroProofTiming = {
  fps: 30,
  durationInFrames: 150,
  words: [
    {id: 'sharp', text: 'चुभती', start: 0.45, end: 1.28},
    {id: 'tension', text: 'तुझ को', start: 1.16, end: 1.85},
    {id: 'work', text: 'काम', start: 1.72, end: 2.35},
    {id: 'moustache', text: 'मूँछ', start: 2.15, end: 4.45},
  ],
};

export const HERO_PROOF_LYRIC =
  'जो चुभती है तुझ को, हाँ जैसे मेरा काम और ये मूँछ';
