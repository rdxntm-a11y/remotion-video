import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {MoustacheSequence} from './sequences/MoustacheSequence';
import {HERO_PROOF_TIMING} from './timing/heroProofTiming';
import {AnimoReel} from './AnimoReel';

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="MoustacheProof"
      component={MoustacheSequence}
      durationInFrames={HERO_PROOF_TIMING.durationInFrames}
      fps={HERO_PROOF_TIMING.fps}
      width={1080}
      height={1920}
      defaultProps={{audioSrc: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'}}
    />
    <Composition
      id="AnimoReel"
      component={AnimoReel}
      durationInFrames={900}
      fps={30}
      width={1080}
      height={1920}
    />
  </>
);

registerRoot(RemotionRoot);
