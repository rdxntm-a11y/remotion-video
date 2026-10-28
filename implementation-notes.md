# Prompt E — Engine + Hero Proof

## Delivered

- `video/src/` — Remotion + React + TypeScript motion-design engine skeleton.
- `video/scripts/render_hero_proof.py` — deterministic local fallback renderer for
  the current environment, which has FFmpeg/Pillow but no browser or installed
  Remotion dependency tree.
- `hero-proof.mp4` — five-second vertical Moustache Sequence proof only.
- `hero-frames/` — eight representative PNG frames for visual QA.

The full song was **not** rendered. The proof is deliberately limited to 150
frames / 5 seconds at 30 FPS, 1080×1920, with the original audio included for
the first five seconds.

## Sequence intent

The lyric proof uses the requested Devanagari line:

`जो चुभती है तुझ को, हाँ जैसे मेरा काम और ये मूँछ`

The motion is staged as:

1. `चुभती` enters as a heavy editorial word while pointed red geometry creates
   physical pressure and sharpness.
2. The tension transfers to `तुझ को` and `काम` rather than treating every word
   as an unrelated animation.
3. `मूँछ` appears as the hero word. Its visible headline/shirorekha is used as
   the origin point for the dark/red moustache stroke.
4. The moustache curls outward with a drawn path, then sweeps across the camera.
5. The continuous red line follows the sweep into a motivated transition.

## Engine map

- `timing/` — explicit proof clock and typed timing contracts.
- `typography/` — intact Devanagari text units and kinetic word behavior.
- `backgrounds/` — generated paper and night primitives.
- `graphics/` — needle field, moustache path, and recurring red line.
- `camera/` — nonlinear push/follow camera rig.
- `effects/` — deterministic grain and impact dust.
- `transitions/` — red-line-led sweep transition.
- `sequences/` — composition assembly.

The source lyric/timing files in the workspace were not modified. The current
approved sync export does not contain the later PDF's Moustache lyric/timing,
so `video/src/timing/heroProofTiming.ts` records a local proof clock only; it
must not be treated as a replacement for the frozen song timestamps.

## Render paths

### Current local path

```bash
python3 video/scripts/render_hero_proof.py
```

### Remotion path once dependencies/browser are supplied

```bash
npm install
npm run render:hero
```

The Remotion composition is `MoustacheProof` in `video/src/index.tsx`.

## QA evidence

The local proof was rendered and inspected with:

```bash
python3 -m py_compile video/scripts/render_hero_proof.py
python3 video/scripts/render_hero_proof.py
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height,r_frame_rate,nb_frames,sample_rate,channels -of json hero-proof.mp4
```

Observed output: 5.000 seconds; H.264 video, 1080×1920, 30 FPS, 150 frames;
AAC stereo audio at 48 kHz. Key frames are 1080×1920 PNGs.

The visible checks cover Devanagari shaping, safe-area placement, red-line
continuity, deterministic grain/fibers/particles, readable supporting text,
the word-to-moustache birth, and the sweep transition. Full-song sync,
Hook-Seal continuity, and the remaining PDF pages are intentionally open for
the next implementation pass.
