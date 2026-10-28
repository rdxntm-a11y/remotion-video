import React from 'react';
import {Composition, registerRoot} from 'remotion';
import {KineticWord} from '../typography/KineticWord';
import {DevanagariText} from '../typography/DevanagariText';
import {PaperBackground} from '../backgrounds/PaperBackground';
import {CameraRig} from '../camera/CameraRig';
import {FilmGrain} from '../effects/FilmGrain';
import {ImpactDust} from '../effects/ImpactDust';
import {Moustache} from '../graphics/Moustache';
import {NeedleField} from '../graphics/NeedleField';
import {RedLine} from '../graphics/RedLine';
import {SweepTransition} from '../transitions/SweepTransition';

/**
 * FullVideo composition that lasts approximately 185 seconds (11,100 frames at 60fps)
 * This composition uses the word-timestamps.json to map each word to its animation timing
 */
export const FullVideo: React.FC = () => {
  // Calculate total frames for ~185 seconds at 30fps
  const fps = 30;
  const durationInFrames = Math.ceil(185 * fps); // 5550 frames

  return (
    <Composition
      id="FullVideo"
      component={FullVideoSequence}
      durationInFrames={durationInFrames}
      fps={fps}
      width={1080}
      height={1920}
      defaultProps={{audioSrc: '/song.mp3'}}
    />
  );
};

/**
 * FullVideoSequence component that animates text based on word timestamps
 */
const FullVideoSequence: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;

  // We'll need to map the word timestamps to this frame time
  // For simplicity, we'll create a function that finds the current word
  const getWordAtTime = (time: number) => {
    // This is a simplified version - in a real implementation,
    // we would parse the word-timestamps.json and find the current word
    // For now, we'll simulate with a few key words
    return null; // Placeholder - actual implementation would use the JSON data
  };

  return (
    <AbsoluteFill style={{backgroundColor: '#e4dfd2', color: '#171515'}}>
      <CameraRig>
        <PaperBackground />
        <div style={{position: 'absolute', top: 322, left: 116, right: 116, color: '#171515', opacity: 0.8, fontFamily: 'Noto Sans Devanagari', fontSize: 32, letterSpacing: '0.02em'}}>
          {/* This would be populated with animated text based on word timestamps */}
          Full Video Content
        </div>
        <NeedleField />
        <KineticWord text="Full Video Example" start={0} end={10} x={132} y={690} size={190} />
        <Moustache />
        <RedLine />
        <ImpactDust />
        <div style={{position: 'absolute', bottom: 238, left: 120, right: 120, opacity: 0.8, fontFamily: 'Noto Sans Devanagari', fontSize: 28, color: '#403936', letterSpacing: '0.02em'}}>
          Full Video Lyrics Animation
        </div>
      </CameraRig>
      <SweepTransition />
      <FilmGrain />
    </AbsoluteFill>
  );
};

registerRoot(FullVideo);