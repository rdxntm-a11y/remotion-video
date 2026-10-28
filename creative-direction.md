# Prompt D — Creative Direction & Screenplay

## Status and source of truth

The synchronization test is approved. The alignment is frozen. This stage is
design-only: no final video is rendered here.

- Audio: `song.mp3` — unchanged.
- Timing: `word-timestamps.json` and `phrases.json` — unchanged start/end
  values from the approved sync test; only the displayed word strings are now
  Hinglish.
- Display lyric source: `lyrics_hinglish.txt`.
- Screenplay: `visual-screenplay.json`.
- Existing Devanagari `lyrics.txt` remains available as the archival source
  used to prove the transliteration mapping.

The project has 26 lyric lines, so the screenplay groups them into nine
continuous visual sequences rather than forcing a separate animation template
onto every line.

## Core concept — **The River That Refuses to Move**

The song is a portrait of longing that cannot resolve. The central visual
metaphor is a hand-drawn current trying to travel through a dark editorial
world. It becomes an underline, a pulse, a contour map, a tear-like ink trail,
and finally a river that stops just before release. The same line should
survive scene changes so the film feels authored as one continuous piece.

The emotional movement is:

1. **Longing ignites** — a tiny mark becomes a current.
2. **The current stalls** — silence, distance, and an absent person turn flow
   into a held line.
3. **Memory measures what cannot be measured** — rulers, grids, and notes fail
   to contain love.
4. **The loop tightens** — repeated questions form a compass with no direction.
5. **The image fades** — the self becomes a portrait with its ink washed out.
6. **The river returns** — the motif tries to move again, but the ending keeps
   its restraint instead of giving a generic cathartic release.

This is an original motion-graphics world. The album cover, its artwork, and
any blurred thumbnail treatment are excluded from the final design.

## Format and composition

- Master composition: 1080 × 1920, 9:16, 30 fps.
- Keep lyric-critical content inside a central safe column approximately
  x=110–970 and y=230–1600. Let only decorative lines, stars, and texture
  bleed into the Reels UI zones.
- Stop defaulting to a centered subtitle block. Use left editorial edges,
  low baselines, vertical stacks, cropped oversized words, circular paths, and
  generous negative space.
- The full phrase remains readable; only the active word receives the cyan
  highlight driven by the frozen word timestamp.

## Hinglish typography system

The visible lyric language is Latin-script Hinglish throughout. No Devanagari
word is used in the designed lyric layer.

| Job | Typeface direction | Treatment |
| --- | --- | --- |
| Hero lyrics | `Noto Sans` SemiBold, with `Noto Sans Display` as the bundled test candidate | Open counters, compact width, clean reading at rap speed; use sentence case from `lyrics_hinglish.txt`. |
| Quiet/melodic lyrics | `Noto Serif` Regular | Longer stems and softer contrast for lines about eyes, grief, and memory. |
| Timing/diagram labels | `Noto Sans Mono` | Small uppercase labels, ruler ticks, coordinates, and sequence metadata. |
| Impact words | Hero face at 2–5× scale | One word dominates; tracking tightens on emotional compression and opens on distance. |

The current ASS preparation uses the locally available `Noto Sans` Latin face.
Before any engine implementation, render a font sheet with `Mile`, `khamoshi`,
`khoobsurati`, `ulfaton`, `aankhon`, `dariya`, and `rehna` at hero sizes. The
Latin letterforms must have enough width for the transliterated words without
crushing line breaks. Treat each word as a safe text unit and each phrase as a
layout unit; do not split a word into uncontrolled character effects.

Typography behavior is physical rather than subtitle-like:

- **Ivory `#E6E6E6`** is the lyric body and paper mark.
- **Cyan `#00FFD7`** is the sung-word highlight and the moving river line.
- **Near-black `#101010`** is the night, ink, and negative-space field.
- Use opacity, blur, and texture density as variations of this palette; do not
  introduce album-art colors or a decorative rainbow system.
- Punctuation stays attached to its Hinglish word in the phrase layout.
- Hinglish vowel clusters such as `aa`, `ee`, `ai`, and `oo` are intentional
  visual rhythm. Do not silently respell them to shorten a line.

## Background and texture system

Every background is generated from original SVG/CSS/canvas primitives with a
seeded random source. There are no downloaded images, stock plates, album-art
layers, or static blurred thumbnails.

### 1. Charcoal paper / ink field

A near-black paper plane uses slowly drifting fiber lines, sparse graphite
flecks, pressure variation, and a soft vignette. Ivory strokes behave like
dry ink; cyan behaves like wet ink that can pool, wick, or pull the next scene
into existence. The texture remains subordinate to the lyric’s counters.

### 2. Night current

A deep `#101010` radial field contains a sparse, original star map and a
low-frequency cyan haze. Stars parallax at different depths; they do not
become a generic galaxy. The river line reflects the haze and briefly turns
the night into a navigational surface during the directionless section.

### 3. Measured geometry

Concentric arcs, ruler marks, contour lines, compass geometry, and a distorted
editorial grid are drawn procedurally. They appear when the lyric questions
measurement or direction and break apart when the lyric says that love cannot
be measured. Geometry is always motivated by the current composition.

### 4. Faded portrait / dry river

An original line-art portrait is assembled from contour strokes and then loses
ink from the inside out. Its face is never a literal photo or album-art cutout.
The portrait shares the river’s cyan baseline; when the river dries, the
portrait loses its last readable contour.

## Motion principles

- Word timing is primary. Beat/onset response is secondary and never changes
  lyric timing.
- Paper has slow drag and slight depth; ink spreads and feathers; the current
  has elastic pull; compass geometry has precise mechanical motion.
- Build anticipation before major words, allow overshoot and follow-through,
  and use stillness on held syllables and gaps.
- Repetition is meaningful: each repeated `kyun`, `sahte`, `rehte`, and refrain
  should evolve the same world instead of replaying the same effect.
- Use line-weight, position, scale, tracking, and negative space to create
  hierarchy. Avoid default scale-from-zero, constant fades, random glitches,
  and a new entrance for every word.
- Use deterministic seeds for fibers, stars, flecks, and particles so frame
  reviews are reproducible.

## Motivated transitions and recurring motif

The cyan river line is the protagonist. It should:

- ignite beneath `hasrat`,
- become a stalled underline at `behta na`,
- fold into a measuring line for `paimana`,
- wrap the compass during `disha`,
- become a portrait contour during `chehra`,
- dry into broken arcs at `bahna na chahe`, and
- continue as one last thread into the held outro.

Transitions are object-led: a line extends into the next baseline, a compass
ring becomes a night halo, a paper fold reveals the portrait, and a portrait
contour becomes the river. No random wipe, unrelated zoom, or unexplained
background reset is permitted.

## Intensity curve

| Time | Lines | Intensity | Direction |
| --- | --- | ---: | --- |
| 0.14–37.08 | 1–2 | 4 → 6 | Sparse paper, ignition, then a widening empty field. |
| 37.08–62.04 | 3–5 | 6 → 3 | The current stalls; the frame gets quieter as silence becomes the subject. |
| 62.13–75.86 | 6–9 | 5 → 7 | Rulers, marginal notes, and an ink-eye build toward the repeated `rehna tha`. |
| 75.88–111.14 | 10–13 | 8 → 6 | The strongest kinetic loop: pressure, compass, orbit, then a deliberate hold. |
| 111.25–138.40 | 14–17 | 7 → 8 | Portrait and dry-river sequence; mirrored repetitions accumulate visual wear. |
| 138.54–153.60 | 18–20 | 6 → 4 | The river tries to return, then mutes and settles. |
| 153.60–164.00 | 21–23 | 5 → 7 | The measuring system breaks open into a wide-eyed, floating refrain. |
| 164.00–179.76 | 24–26 | 5 → 2 | Repetition folds inward; the final river refuses a big release. |
| 179.76–185.26 | outro | 1 | Near-still night field; the last cyan thread remains visible, then dims. |

The audio is 185.256 seconds long. The lyric timing ends at 179.76 seconds;
the planned outro honors the remaining space. An audio inspection reported
integrated loudness around -10.2 LUFS, LRA around 8.3 LU, and a final quiet
region beginning around 183.47 seconds. These values support restrained
quiet sections and a controlled final fade; the frozen lyric times remain the
only source for word synchronization.

For secondary motion only, a coarse RMS/onset pass found the strongest body of
energy around 51.8–75.88 seconds and 111.25–164 seconds, with a quieter pocket
around 75.88–88.38 seconds. That supports the visual contrast between the
measurement/eye lift and the held compass loop. Detected onset candidates are
not lyric boundaries and must never move a word; implementation may use them
only for paper pressure, camera impulse, or background-scale changes.

## Sequence map

1. **Spark / absent meeting** — lines 1–2, 0.14–37.08.
2. **The stalled current** — lines 3–5, 37.08–62.04.
3. **No measure for love** — lines 6–9, 62.13–75.86.
4. **The directionless loop** — lines 10–13, 75.88–111.14.
5. **Faded portrait / dry river** — lines 14–17, 111.25–138.40.
6. **Return to the heart** — lines 18–20, 138.54–153.60.
7. **Re-measure / eyes** — lines 21–23, 153.60–164.00.
8. **Folded memory** — lines 24–25, 164.00–174.08.
9. **Withheld release** — line 26, 174.08–179.76, followed by the outro.

## Original assets to create during implementation

- Procedural paper/fiber and ink-wick shaders or SVG filters.
- Seeded night-star field and cyan haze layers.
- Contour-map and compass/ruler SVG primitives.
- Hinglish-safe typographic layout helpers and a font-test sheet.
- One continuous river-line SVG path that can morph between underline, orbit,
  portrait contour, and dry crack.
- Abstract editorial portrait built from original line art.
- A small set of paper folds, graphite flecks, and ink pools made in code.

## Creative self-review gates

Before implementation is approved, review representative frames for:

1. Hinglish spelling and punctuation match the three prepared assets.
2. No Devanagari or album-art pixels appear in the lyric layer or background.
3. Every fast word remains legible at 1080 × 1920.
4. The current line remains traceable through transitions.
5. Repeated lines evolve instead of replaying a template.
6. Background texture supports contrast and does not compete with letters.
7. Critical text remains inside the vertical-video safe area.
8. The quiet ending stays quiet and does not manufacture a generic climax.

## Strongest ten planned moments

1. `Mile` strikes a single paper fiber; the stroke becomes the current beneath
   the first phrase.
2. `hasrat` pulls the current into a wet cyan flare, then `bhadka` leaves a
   small ember-like mark without introducing a new color.
3. `behta na` catches the river at the edge of the frame and holds it against
   its own momentum.
4. `ulfaton mein nahi koi paimana` draws a ruler that physically bends around
   the phrase and breaks at `nahi`.
5. `surmai teri aankhon` turns the wet ink pool into a two-lobed abstract eye;
   `beh jaana` is the camera drifting into its contour.
6. The first `sahte sahte` winds the river around a translucent heart-shaped
   negative space; the second winds it tighter rather than replaying the move.
7. `disha` creates a compass whose needle is the lyric baseline; `kyun` pulls
   the needle off-axis and leaves the ring spinning without an answer.
8. `chehra` assembles a portrait from the surviving Latin letter strokes, then
   `khoobsurati` visibly loses ink from the inside out.
9. The repeated `rehna tha` folds the whole paper world into two stacked panels,
   with the second repetition refusing to unfold.
10. `bahna na chahe` ends as a cyan river line that stops one stroke short of
    the edge; the remaining outro is a dark, breathing field rather than a
    stock end card.
