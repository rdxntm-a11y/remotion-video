import React from 'react';
import { AbsoluteFill, Sequence, useVideoConfig, useCurrentFrame, spring, interpolate, random } from 'remotion';
import { evolvePath } from '@remotion/paths';
import { loadFont } from '@remotion/google-fonts/NotoSansDevanagari';
import {PaperBackground} from './backgrounds/PaperBackground';
import {Moustache} from './graphics/Moustache';
import timestamps from '../../word-timestamps.json'; 

const { fontFamily } = loadFont();

export const FullVideo: React.FC = () => {
  const {fps} = useVideoConfig();
  const wordTimings = Array.isArray(timestamps) ? timestamps : [];

  return (
    <AbsoluteFill style={{backgroundColor: '#e4dfd2'}}>
      <PaperBackground />
      <Moustache />
      
      {wordTimings.map((item: any, index: number) => {
        const startFrame = Math.floor(item.start * fps);
        const endFrame = Math.floor(item.end * fps);
        const duration = endFrame - startFrame;
        if (duration <= 0) return null;

        return (
          <Sequence key={index} from={startFrame} durationInFrames={duration}>
            <CinematicScene word={item.word} duration={duration} index={index} fontFamily={fontFamily} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};

const CinematicScene: React.FC<{word: string, duration: number, index: number, fontFamily: string}> = ({word, duration, index, fontFamily}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  
  // स्प्रिंग (टेक्स्ट का ज़ूम होकर आना)
  const scale = spring({ frame, fps, config: { damping: 14, stiffness: 100 } });
  
  // लाल रेखा का एनिमेशन (Red Line Drawing)
  // हम एक सिंपल सीधी लाइन बनाते हैं जो टेक्स्ट के नीचे आती है
  const lineProgress = spring({ frame: frame - 5, fps, config: { damping: 200 } });
  const linePath = "M 0 0 L 800 0";
  const { strokeDasharray, strokeDashoffset } = evolvePath(lineProgress, linePath);

  // सेफ फेड इन/आउट
  const fadeDuration = Math.min(4, Math.max(1, duration / 2));
  const opacity = Math.min(
    interpolate(frame, [0, fadeDuration], [0, 1], { extrapolateRight: 'clamp' }),
    interpolate(frame, [duration - fadeDuration, duration], [1, 0], { extrapolateLeft: 'clamp' })
  );

  // टेक्स्ट का पोज़िशन (हर बार थोड़ा अलग)
  const yPos = 30 + random(`y-${index}`) * 40; 

  return (
    <AbsoluteFill style={{ opacity }}>
      {/* बैकग्राउंड में एक बड़ा सा हल्का सा सर्कल (PDF जैसा लुक देने के लिए) */}
      <div style={{
        position: 'absolute',
        top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
        width: 800, height: 800, borderRadius: '50%',
        background: 'radial-gradient(circle, rgba(255,255,255,0.4) 0%, rgba(255,255,255,0) 70%)',
        zIndex: 0
      }} />

      {/* टेक्स्ट */}
      <div style={{
        position: 'absolute',
        top: `${yPos}%`, left: '50%',
        transform: `translate(-50%, -50%) scale(${scale})`,
        color: '#171515',
        fontFamily: fontFamily, // Google Font
        fontSize: 180, 
        fontWeight: 900,
        textAlign: 'center',
        zIndex: 10,
        textShadow: '4px 4px 0px rgba(0,0,0,0.1)'
      }}>
        {word}
      </div>

      {/* लाल रेखा (Red Line) जो टेक्स्ट के नीचे ड्रॉ होती है */}
      <svg
        style={{
          position: 'absolute',
          top: `calc(${yPos}% + 100px)`, 
          left: '50%',
          transform: 'translateX(-50%)',
          width: 800,
          height: 20,
          zIndex: 5,
        }}
        viewBox="0 0 800 20"
      >
        <path
          d={linePath}
          fill="none"
          stroke="#e13f28" // PDF वाला लाल रंग
          strokeWidth="6"
          strokeDasharray={strokeDasharray}
          strokeDashoffset={strokeDashoffset}
          strokeLinecap="round"
        />
      </svg>
    </AbsoluteFill>
  );
};
