"""Render the deterministic five-second moustache hero proof.

This is the local render path for the checked-in Remotion scene. It keeps the
same scene clock and visual primitives, but uses Pillow + HarfBuzz/libraqm and
FFmpeg because this workspace does not currently contain a browser/Remotion
install. The frozen timing JSON and audio are read-only inputs.
"""

from __future__ import annotations

import math
import subprocess
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter


ROOT = Path(__file__).resolve().parents[2]
WIDTH, HEIGHT, FPS, FRAMES = 1080, 1920, 30, 150
OUT = ROOT / "hero-proof.mp4"
FRAME_DIR = ROOT / "hero-frames"
AUDIO = ROOT / "song.mp3"

PAPER = (229, 224, 211)
INK = (23, 21, 21)
SECONDARY = (64, 57, 54)
RED = (181, 38, 36)
AMBER = (166, 99, 43)

FONT_SANS = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/noto/NotoSerifDevanagari-Bold.ttf"
FONT_MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def remap(value: float, start: float, end: float) -> float:
    return clamp((value - start) / max(0.0001, end - start))


def ease_out_quint(value: float) -> float:
    t = clamp(value)
    return 1.0 - (1.0 - t) ** 5


def ease_in_out(value: float) -> float:
    t = clamp(value)
    return 4 * t * t * t if t < 0.5 else 1 - ((-2 * t + 2) ** 3) / 2


def cubic(p0: tuple[float, float], p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float], t: float) -> tuple[float, float]:
    u = 1.0 - t
    return (
        u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0],
        u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1],
    )


def sample_cubic(points: list[tuple[float, float]], progress: float, count: int = 42) -> list[tuple[int, int]]:
    if progress <= 0:
        return [tuple(map(round, points[0]))]
    samples = max(2, round(count * clamp(progress)))
    return [tuple(map(round, cubic(*points, index / (samples - 1)))) for index in range(samples)]


def transform_point(point: tuple[float, float], origin: tuple[float, float], dx: float, dy: float, angle: float) -> tuple[float, float]:
    ox, oy = origin
    x, y = point[0] - ox, point[1] - oy
    c, s = math.cos(angle), math.sin(angle)
    return (ox + x * c - y * s + dx, oy + x * s + y * c + dy)


def paper_plate() -> Image.Image:
    """Generate a quiet, deterministic paper plate once for all frames."""
    rng = np.random.default_rng(4207)
    small = rng.normal(0, 3.6, (240, 135)).astype(np.float32)
    noise = np.asarray(Image.fromarray(small, mode="F").resize((WIDTH, HEIGHT), Image.Resampling.BICUBIC))
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    distance = np.sqrt(((xx - WIDTH * 0.5) / WIDTH) ** 2 + ((yy - HEIGHT * 0.44) / HEIGHT) ** 2)
    vignette = -np.clip(distance - 0.25, 0, 0.8) * 22
    base = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    for channel, amount in enumerate((1.0, 0.7, 0.4)):
        base[:, :, channel] = PAPER[channel] + noise * amount + vignette
    return Image.fromarray(np.uint8(np.clip(base, 0, 255)), mode="RGB")


def draw_editorial_marks(draw: ImageDraw.ImageDraw, t: float) -> None:
    drift = math.sin(t * 0.7) * 9
    draw.line((86 + drift, 264, 994 + drift, 264), fill=(*INK, 78), width=2)
    draw.line((110 - drift * 0.3, 1654, 970 - drift * 0.3, 1654), fill=(*INK, 62), width=1)
    draw.line((106, 336, 106, 1600), fill=(*INK, 52), width=1)
    draw.line((72, 208, 156, 208), fill=(*RED, 150), width=2)
    draw.line((72, 208, 72, 292), fill=(*RED, 150), width=2)
    draw.line((1008, 1628, 924, 1628), fill=(*RED, 130), width=2)
    draw.line((1008, 1628, 1008, 1544), fill=(*RED, 130), width=2)


def draw_fibers(draw: ImageDraw.ImageDraw, t: float) -> None:
    rng = np.random.default_rng(810)
    for index in range(36):
        x = int(rng.uniform(40, WIDTH - 40))
        y = int(rng.uniform(360, HEIGHT - 250))
        length = int(rng.uniform(18, 96))
        alpha = int(rng.uniform(18, 52))
        sway = math.sin(t * 0.55 + index) * 4
        draw.line((x, y, x + length, y + sway), fill=(*INK, alpha), width=1)


def draw_text(draw: ImageDraw.ImageDraw, xy: tuple[float, float], text: str, font_obj: ImageFont.FreeTypeFont, fill: tuple[int, ...], anchor: str = "la", spacing: int = 8) -> tuple[int, int, int, int]:
    draw.text(xy, text, font=font_obj, fill=fill, anchor=anchor, spacing=spacing, stroke_width=0)
    return draw.textbbox(xy, text, font=font_obj, anchor=anchor, spacing=spacing)


def draw_needles(layer: Image.Image, t: float) -> None:
    progress = ease_out_quint(remap(t, 0.42, 1.35))
    opacity = int(clamp(progress * 1.6) * 180)
    draw = ImageDraw.Draw(layer, "RGBA")
    needles = [
        (186, 672, -18, 260), (272, 774, -10, 188), (820, 706, 16, 230),
        (908, 820, 23, 190), (358, 910, 6, 160), (724, 938, -8, 170),
    ]
    for x, y, degrees, length in needles:
        radians = math.radians(degrees)
        actual = length * progress
        draw.line((x, y, x + math.cos(radians) * actual, y + math.sin(radians) * actual), fill=(*RED, opacity), width=3)
        if progress > 0.25:
            draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(*RED, opacity))


def draw_word_with_breath(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], size: int, color: tuple[int, int, int], start: float, end: float, t: float, anchor: str = "la") -> tuple[int, int, int, int]:
    before = remap(t, start - 0.18, start)
    settle = remap(t, end, end + 0.24)
    y_nudge = 18 * (1 - ease_out_quint(before))
    font_obj = font(FONT_SERIF, size)
    reveal = int(255 * ease_out_quint(before) * (1 - ease_in_out(remap(t, end + 0.12, end + 0.52))))
    return draw_text(draw, (xy[0], xy[1] + y_nudge), text, font_obj, (*color, reveal), anchor=anchor)


def draw_moustache(layer: Image.Image, t: float, anchor_y: int) -> None:
    grow = ease_out_quint(remap(t, 2.15, 3.25))
    sweep = remap(t, 3.42, 4.75)
    # The first point is deliberately attached to the headline's shirorekha.
    base_y = anchor_y - sweep * 270
    width = 520 + sweep * 520
    half = width / 2
    left = [(540, base_y), (540 - half * 0.16, base_y - 28), (540 - half * 0.70, base_y - 4), (540 - half, base_y + 94)]
    right = [(540, base_y), (540 + half * 0.16, base_y - 28), (540 + half * 0.70, base_y - 4), (540 + half, base_y + 94)]
    dx = -sweep * 625
    dy = -sweep * 100
    angle = math.radians(-sweep * 10)
    draw = ImageDraw.Draw(layer, "RGBA")
    for points in (left, right):
        raw = sample_cubic(points, grow)
        transformed = [transform_point(point, (540, anchor_y), dx, dy, angle) for point in raw]
        if len(transformed) > 1:
            draw.line(transformed, fill=(*INK, 255), width=40, joint="curve")
            draw.line(transformed, fill=(*RED, 225), width=5, joint="curve")
    if grow > 0.02:
        center = transform_point((540, anchor_y), (540, anchor_y), dx, dy, angle)
        draw.ellipse((center[0] - 16, center[1] - 16, center[0] + 16, center[1] + 16), fill=(*RED, 220))


def draw_red_line(draw: ImageDraw.ImageDraw, t: float) -> None:
    draw_progress = remap(t, 0.18, 1.0)
    dash_start = int(84 + 920 * draw_progress)
    baseline = [(86, 1332), (280, 1288), (370, 1378), (520, 1328), (686, 1272), (768, 1336), (1002, 1280)]
    draw.line(baseline[: max(2, min(len(baseline), 2 + int(draw_progress * 5)))], fill=(*RED, 220), width=5, joint="curve")
    if t > 4.1:
        sweep = remap(t, 4.1, 5.0)
        path = [(x, y) for x, y in [(0, 870), (220, 800), (510, 920), (800, 740), (1160, 610)]]
        transformed = [(round(x - sweep * 360), round(y - sweep * 240)) for x, y in path]
        draw.line(transformed, fill=(*RED, int(180 * sweep)), width=10, joint="curve")


def draw_impact_dust(layer: Image.Image, t: float) -> None:
    impact = remap(t, 3.95, 4.35) * (1 - remap(t, 4.35, 5.0))
    if impact <= 0:
        return
    draw = ImageDraw.Draw(layer, "RGBA")
    rng = np.random.default_rng(201)
    for _ in range(42):
        angle = float(rng.uniform(0, math.tau))
        radius = float(rng.uniform(90, 350)) * impact
        x = 540 + math.cos(angle) * radius
        y = 930 + math.sin(angle) * radius
        size = int(rng.uniform(2, 8))
        draw.ellipse((x - size, y - size, x + size, y + size), fill=(*RED, int(rng.uniform(35, 150) * impact)))


def render_frame(base: Image.Image, frame_index: int) -> Image.Image:
    t = frame_index / FPS
    image = base.copy().convert("RGBA")
    draw = ImageDraw.Draw(image, "RGBA")
    draw_editorial_marks(draw, t)
    draw_fibers(draw, t)

    # The camera is a physical push, not a linear slide: it stays quiet until
    # the moustache takes over, then follows the stroke off the page.
    camera_scale = 1.0 + 0.035 * ease_in_out(remap(t, 2.0, 3.3)) + 0.12 * remap(t, 3.55, 5.0)
    camera_dx = -88 * remap(t, 3.55, 5.0)
    camera_dy = -122 * remap(t, 3.55, 5.0)
    scene = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    scene_draw = ImageDraw.Draw(scene, "RGBA")

    label_font = font(FONT_MONO, 18)
    small_font = font(FONT_SANS, 31)
    draw_text(scene_draw, (116, 316), "जो चुभती है तुझ को, हाँ जैसे मेरा काम और ये मूँछ", small_font, (*INK, int(215 * (1 - remap(t, 4.25, 4.85)))), anchor="la")
    draw_text(scene_draw, (118, 377), "CASE FILE / 04 — THE BODY LEAVES EVIDENCE", label_font, (*RED, int(215 * (1 - remap(t, 4.18, 4.85)))), anchor="la")

    # Supporting words hold the composition while the hero word earns the camera.
    draw_word_with_breath(scene_draw, "चुभती", (132, 690), 190, INK, 0.45, 1.28, t)
    draw_word_with_breath(scene_draw, "तुझ को", (164, 918), 110, SECONDARY, 1.16, 1.85, t)
    draw_word_with_breath(scene_draw, "काम", (676, 1052), 148, RED if 1.72 <= t <= 2.35 else SECONDARY, 1.72, 2.35, t)

    moustache_font = font(FONT_SERIF, 344)
    word_x, word_y = 186, 710
    word_reveal = ease_out_quint(remap(t, 2.0, 2.35))
    word_fade = word_reveal * (1 - ease_in_out(remap(t, 3.52, 4.35)))
    draw_text(scene_draw, (word_x, word_y), "मूँछ", moustache_font, (*INK, int(255 * word_fade)), anchor="la")
    word_bbox = scene_draw.textbbox((word_x, word_y), "मूँछ", font=moustache_font, anchor="la")
    # Use the visible upper headline area as the actual birth point.
    headline_y = word_bbox[1] + 70

    draw_needles(scene, t)
    draw_moustache(scene, t, headline_y)
    draw_red_line(scene_draw, t)
    draw_impact_dust(scene, t)

    footer_alpha = int(215 * (1 - remap(t, 4.18, 4.82)))
    draw_text(scene_draw, (120, 1642), "जो चुभती है तुझ को, हाँ जैसे मेरा काम और ये मूँछ", font(FONT_SANS, 28), (*SECONDARY, footer_alpha), anchor="la")

    if camera_scale != 1.0 or camera_dx or camera_dy:
        scaled = scene.resize((round(WIDTH * camera_scale), round(HEIGHT * camera_scale)), Image.Resampling.BICUBIC)
        scene = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        scene.alpha_composite(scaled, (round((WIDTH - scaled.width) / 2 + camera_dx), round((HEIGHT - scaled.height) / 2 + camera_dy)))
    image.alpha_composite(scene)

    # The line sweeps the lens into the next scene; the red band is a motivated
    # transition, not a reset.
    sweep = remap(t, 4.08, 4.92)
    if sweep > 0:
        overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay, "RGBA")
        left = int(WIDTH * (sweep * 1.22 - 0.20))
        od.polygon([(left, -100), (left + 170, -100), (left - 230, HEIGHT + 100), (left - 400, HEIGHT + 100)], fill=(*RED, 235))
        image.alpha_composite(overlay)

    grain = Image.effect_noise((WIDTH // 3, HEIGHT // 3), 52 + (frame_index % 7)).resize((WIDTH, HEIGHT), Image.Resampling.BILINEAR).convert("L")
    grain_rgba = Image.new("RGBA", (WIDTH, HEIGHT), (65, 44, 32, 0))
    grain_rgba.putalpha(grain.point(lambda value: int(value * 0.055)))
    image.alpha_composite(grain_rgba)
    return image.convert("RGB")


def render() -> None:
    FRAME_DIR.mkdir(parents=True, exist_ok=True)
    base = paper_plate()
    keyframes = {0, 18, 42, 60, 75, 96, 120, 145}
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-",
        "-ss", "0", "-t", "5", "-i", str(AUDIO),
        "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", "-preset", "medium", "-crf", "17",
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "320k", "-shortest", "-movflags", "+faststart", str(OUT),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    assert process.stdin is not None
    try:
        for frame_index in range(FRAMES):
            frame = render_frame(base, frame_index)
            if frame_index in keyframes:
                frame.save(FRAME_DIR / f"frame-{frame_index:04d}.png", optimize=True)
            process.stdin.write(frame.tobytes())
    finally:
        process.stdin.close()
    return_code = process.wait()
    if return_code != 0:
        raise SystemExit(f"ffmpeg failed with exit code {return_code}")
    print(f"wrote {OUT}")
    print(f"wrote {len(keyframes)} representative frames to {FRAME_DIR}")


if __name__ == "__main__":
    render()
