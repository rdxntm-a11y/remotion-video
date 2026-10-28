import React from 'react';
import {AbsoluteFill, Audio, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {PaperBackground} from '../backgrounds/PaperBackground';
import {CameraRig} from '../camera/CameraRig';
import {FilmGrain} from '../effects/FilmGrain';
import {ImpactDust} from '../effects/ImpactDust';
import {Moustache} from '../graphics/Moustache';
import {NeedleField} from '../graphics/NeedleField';
import {RedLine} from '../graphics/RedLine';
import {KineticWord} from '../typography/KineticWord';
import {HERO_PROOF_LYRIC} from '../timing/heroProofTiming';
import {SweepTransition} from '../transitions/SweepTransition';

export const MoustacheSequence: React.FC<{audioSrc?: string}> = ({audioSrc = '/song.mp3'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const phraseOpacity = interpolate(t, [0, 0.42, 4.3, 4.8], [0, 0.86, 0.72, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const labelOpacity = interpolate(t, [0, 0.35, 4.2, 4.7], [0, 0.65, 0.65, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});

  return (
    <AbsoluteFill style={{backgroundColor: '#e4dfd2', color: '#171515'}}>
      <CameraRig>
        <PaperBackground />
        <div style={{position: 'absolute', top: 322, left: 116, right: 116, color: '#171515', opacity: labelOpacity, fontFamily: 'Noto Sans Devanagari', fontSize: 32, letterSpacing: '0.02em'}}>
          {HERO_PROOF_LYRIC}
        </div>
        <div style={{position: 'absolute', top: 382, left: 118, color: '#b52624', opacity: labelOpacity, fontFamily: 'Noto Sans Mono', fontSize: 18, letterSpacing: '0.26em'}}>CASE FILE / 04 — THE BODY LEAVES EVIDENCE</div>
        <NeedleField />
        <KineticWord text="चुभती" start={0.45} end={1.28} x={132} y={690} size={190} />
        <KineticWord text="तुझ को" start={1.16} end={1.85} x={164} y={920} size={110} color="#403936" />
        <KineticWord text="काम" start={1.72} end={2.35} x={674} y={1050} size={148} color="#403936" activeColor="#b52624" />
        <KineticWord text="मूँछ" start={2.15} end={4.45} x={186} y={710} size={344} color="#171515" activeColor="#171515" />
        <Moustache />
        <RedLine />
        <ImpactDust />
        <div style={{position: 'absolute', bottom: 238, left: 120, right: 120, opacity: phraseOpacity, fontFamily: 'Noto Sans Devanagari', fontSize: 28, color: '#403936', letterSpacing: '0.02em'}}>
          जो चुभती है तुझ को, हाँ जैसे मेरा काम और ये मूँछ
        </div>
      </CameraRig>
      <SweepTransition />
      <FilmGrain />
      {audioSrc ? <Audio src={audioSrc} startFrom={0} /> : null}
    </AbsoluteFill>
  );
};
