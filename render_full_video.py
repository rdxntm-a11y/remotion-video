"""Render the complete 9:16 Hinglish lyric video.

This renderer is intentionally independent of the five-second proof scene.  It
reads the frozen Hinglish phrase and word timing exports, draws the Prompt D/E
paper, night-current, geometry, portrait, and river systems procedurally, and
encodes the result with the supplied song audio.  The only readable text it
ever draws comes from ``lyrics_hinglish.txt`` / ``phrases.json``.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parent
WIDTH, HEIGHT, FPS = 1080, 1920, 30
OUT = ROOT / "final-9x16.mp4"
AUDIO = ROOT / "song.mp3"
PHRASES = ROOT / "phrases.json"
SCREENPLAY = ROOT / "visual-screenplay.json"
LYRICS = ROOT / "lyrics_hinglish.txt"
QA_DIR = ROOT / "full-render-frames"

INK = (16, 16, 16)
IVORY = (230, 230, 230)
CYAN = (0, 255, 215)
MUTED = (145, 156, 153)
GRAPHITE = (61, 67, 66)

FONT_SANS = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
FONT_SANS_REGULAR = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf"
FONT_MONO = "/usr/share/fonts/truetype/noto/NotoSansMono-Regular.ttf"
DEVANAGARI = re.compile(r"[\u0900-\u097F]")

SEQUENCE_EDGES = (0.14, 37.08, 62.04, 75.86, 111.14, 138.40, 153.60, 164.0, 174.08, 179.76)


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def smooth(value: float) -> float:
    value = clamp(value)
    return value * value * (3.0 - 2.0 * value)


def remap(value: float, start: float, end: float) -> float:
    return smooth((value - start) / max(0.0001, end - start))


def ease_out(value: float) -> float:
    value = clamp(value)
    return 1.0 - (1.0 - value) ** 4


def lerp(a: float, b: float, amount: float) -> float:
    return a + (b - a) * amount


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def alpha_color(color: tuple[int, int, int], alpha: float) -> tuple[int, int, int, int]:
    return (*color, int(clamp(alpha / 255.0) * 255) if alpha <= 255 else 255)


def validate_assets() -> tuple[list[dict], list[dict]]:
    """Load the prepared text/timing data and fail before rendering if it drifts."""
    phrases = json.loads(PHRASES.read_text(encoding="utf-8"))
    screenplay = json.loads(SCREENPLAY.read_text(encoding="utf-8"))
    source = LYRICS.read_text(encoding="utf-8").splitlines()
    if len(source) != 26 or source != [item["text"] for item in phrases]:
        raise ValueError("lyrics_hinglish.txt and phrases.json are not the same exact 26-line source")
    if source != [item["lyrics"] for item in screenplay]:
        raise ValueError("visual-screenplay.json is not aligned to the prepared Hinglish lyrics")
    for item in phrases:
        if DEVANAGARI.search(item["text"]):
            raise ValueError("Devanagari found in the final lyric source")
        tokens = item["text"].split(" ")
        if len(tokens) != len(item["words"]):
            raise ValueError(f"line {item['line']} token/word timing count mismatch")
        for word in item["words"]:
            if DEVANAGARI.search(word["word"]):
                raise ValueError("Devanagari found in word timing data")
    return phrases, screenplay


def paper_plate() -> Image.Image:
    """Create a deterministic near-black paper field once for the render."""
    rng = np.random.default_rng(1307)
    small = rng.normal(0.0, 2.8, (240, 135)).astype(np.float32)
    noise = np.asarray(
        Image.fromarray(small, mode="F").resize((WIDTH, HEIGHT), Image.Resampling.BICUBIC)
    )
    yy, xx = np.mgrid[0:HEIGHT, 0:WIDTH]
    radial = np.sqrt(((xx - WIDTH * 0.50) / WIDTH) ** 2 + ((yy - HEIGHT * 0.46) / HEIGHT) ** 2)
    vignette = -np.clip(radial - 0.18, 0, 0.85) * 22
    vertical = ((yy / HEIGHT) - 0.5) * 3.0
    result = np.zeros((HEIGHT, WIDTH, 3), dtype=np.float32)
    for channel, base, amount in ((0, 16.0, 1.0), (1, 17.0, 0.86), (2, 17.0, 0.72)):
        result[:, :, channel] = base + noise * amount + vignette + vertical
    return Image.fromarray(np.uint8(np.clip(result, 0, 255)), mode="RGB").convert("RGBA")


def seeded_marks() -> tuple[list[tuple[float, float, float, float, float]], list[tuple[float, float, float]]]:
    rng = np.random.default_rng(811)
    fibers: list[tuple[float, float, float, float, float]] = []
    for _ in range(72):
        x = float(rng.uniform(28, WIDTH - 28))
        y = float(rng.uniform(220, HEIGHT - 190))
        length = float(rng.uniform(22, 160))
        angle = float(rng.uniform(-0.14, 0.14))
        alpha = float(rng.uniform(12, 42))
        fibers.append((x, y, length, angle, alpha))
    stars: list[tuple[float, float, float]] = []
    for _ in range(58):
        stars.append((float(rng.uniform(58, WIDTH - 58)), float(rng.uniform(280, 1590)), float(rng.uniform(1.0, 3.4))))
    return fibers, stars


def sequence_at(t: float) -> int:
    for index in range(len(SEQUENCE_EDGES) - 1):
        if SEQUENCE_EDGES[index] <= t < SEQUENCE_EDGES[index + 1]:
            return index
    return 8 if t >= SEQUENCE_EDGES[-2] else 0


def active_phrase(phrases: list[dict], t: float) -> tuple[dict | None, int]:
    for phrase in phrases:
        if phrase["start"] <= t <= phrase["end"]:
            active = -1
            for index, word in enumerate(phrase["words"]):
                if word["start"] <= t <= word["end"]:
                    active = index
                    break
            return phrase, active
    return None, -1


def draw_line(draw: ImageDraw.ImageDraw, points: Sequence[tuple[float, float]], fill: tuple[int, ...], width: int = 2) -> None:
    if len(points) > 1:
        draw.line([(round(x), round(y)) for x, y in points], fill=fill, width=width, joint="curve")


def glow_path(image: Image.Image, points: Sequence[tuple[float, float]], color: tuple[int, int, int], width: int, alpha: int) -> None:
    # A broad translucent wet-ink pass supplies the bloom at a fraction of the
    # cost of a full-frame Gaussian blur on every video frame.
    draw = ImageDraw.Draw(image, "RGBA")
    draw_line(draw, points, (*color, max(1, alpha // 8)), width=max(8, width * 2))


def river_points(t: float, final_stop: bool = False) -> list[tuple[float, float]]:
    anchors = [(32, 1322), (160, 1286), (286, 1324), (410, 1242), (548, 1284), (682, 1218), (826, 1262), (948, 1198), (1040, 1215)]
    points: list[tuple[float, float]] = []
    wave = math.sin(t * 0.72) * 8.0
    for index, (x, y) in enumerate(anchors):
        progress = index / max(1, len(anchors) - 1)
        if final_stop:
            x = min(x, 32 + progress * 920)
        points.append((x, y + math.sin(t * 0.54 + index * 0.9) * 5.0 + wave * (0.2 + progress)))
    return points


def draw_river(image: Image.Image, t: float, final_stop: bool = False, alpha: int = 185) -> None:
    points = river_points(t, final_stop=final_stop)
    glow_path(image, points, CYAN, 5, alpha)
    draw = ImageDraw.Draw(image, "RGBA")
    draw_line(draw, points, (*CYAN, alpha), 4)
    pulse = (math.sin(t * 2.2) + 1.0) * 0.5
    index = int(pulse * (len(points) - 1))
    x, y = points[index]
    radius = 5 + int(5 * pulse)
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*CYAN, min(220, alpha + 25)))


def draw_background(image: Image.Image, t: float, sequence: int, marks: tuple[list, list]) -> None:
    fibers, stars = marks
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")
    paper_amount = 1.0 - remap(t, 38.0, 75.0) * 0.55
    star_amount = 0.24 + (0.66 if sequence in (2, 3, 6, 8) else 0.0)
    drift = math.sin(t * 0.31) * 10.0
    for index, (x, y, length, angle, alpha) in enumerate(fibers):
        dx = math.cos(angle) * length
        dy = math.sin(angle) * length + math.sin(t * 0.38 + index) * 3.0
        draw.line((x + drift * (index % 3) / 3, y, x + dx + drift * (index % 3) / 3, y + dy), fill=(145, 153, 150, int(alpha * paper_amount)), width=1)
    for index, (x, y, radius) in enumerate(stars):
        twinkle = (math.sin(t * 0.7 + index * 1.73) + 1.0) * 0.5
        a = int(80 * star_amount * (0.35 + twinkle * 0.65))
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*IVORY, a))
    # A slow radial cyan haze keeps the night-current sections related to the line.
    haze = int(28 + 24 * (math.sin(t * 0.22) + 1.0) * 0.5) if sequence in (2, 3, 6, 8) else 12
    draw.ellipse((120, 420, 960, 1490), outline=(*CYAN, haze), width=3)
    image.alpha_composite(overlay)
    draw = ImageDraw.Draw(image, "RGBA")
    # Editorial frame marks remain quiet and do not introduce any extra text.
    drift = math.sin(t * 0.28) * 8
    draw.line((92 + drift, 232, 988 + drift, 232), fill=(*GRAPHITE, 88), width=2)
    draw.line((110 - drift, 1652, 970 - drift, 1652), fill=(*GRAPHITE, 66), width=1)
    draw.line((105, 286, 105, 1590), fill=(*GRAPHITE, 58), width=1)
    draw.line((75, 198, 160, 198), fill=(*CYAN, 160), width=3)
    draw.line((75, 198, 75, 282), fill=(*CYAN, 160), width=3)
    draw.line((1006, 1620, 921, 1620), fill=(*CYAN, 115), width=2)
    draw.line((1006, 1620, 1006, 1535), fill=(*CYAN, 115), width=2)


def path_points(center: tuple[float, float], radii: tuple[float, float], start: float, end: float, count: int = 96) -> list[tuple[float, float]]:
    cx, cy = center
    rx, ry = radii
    return [(cx + math.cos(start + (end - start) * index / (count - 1)) * rx,
             cy + math.sin(start + (end - start) * index / (count - 1)) * ry) for index in range(count)]


def draw_heart_basin(draw: ImageDraw.ImageDraw, t: float, alpha: int = 120) -> None:
    points = []
    for index in range(120):
        theta = math.tau * index / 119
        x = 540 + 300 * math.sin(theta) ** 3
        y = 770 - 230 * (0.82 * math.cos(theta) - 0.30 * math.cos(2 * theta) - 0.16 * math.cos(3 * theta) - 0.07 * math.cos(4 * theta))
        points.append((x, y + math.sin(t * 0.6 + index * 0.05) * 3))
    draw_line(draw, points, (*CYAN, alpha), 3)
    draw_line(draw, [(220, 1075), (360, 1010), (540, 1040), (730, 980), (880, 1030)], (*GRAPHITE, 105), 2)


def draw_waveform(draw: ImageDraw.ImageDraw, t: float, y: float, alpha: int, scar: bool = False) -> None:
    points = []
    for index in range(100):
        x = 120 + index * 8.5
        amplitude = 50 * (0.35 + 0.65 * math.sin(index * 0.17 + 1.3) ** 2)
        if scar:
            amplitude *= 0.48 + 0.12 * math.sin(index * 0.4 + t)
        signal = math.sin(index * 0.61 + t * 3.2) * amplitude
        points.append((x, y + signal))
    draw_line(draw, points, (*CYAN, alpha), 3)
    if scar:
        draw.line((505, y - 54, 505, y + 54), fill=(*IVORY, 90), width=5)


def draw_ruler(draw: ImageDraw.ImageDraw, t: float, alpha: int = 120, orbital: bool = False) -> None:
    if orbital:
        center = (540, 890)
        draw.ellipse((190, 540, 890, 1240), outline=(*GRAPHITE, alpha), width=2)
        for index in range(24):
            angle = t * 0.3 + math.tau * index / 24
            x1 = center[0] + math.cos(angle) * 326
            y1 = center[1] + math.sin(angle) * 326
            x2 = center[0] + math.cos(angle) * 350
            y2 = center[1] + math.sin(angle) * 350
            draw.line((x1, y1, x2, y2), fill=(*IVORY, alpha), width=2)
        return
    y = 470 + math.sin(t * 0.45) * 12
    draw.line((132, y, 948, y), fill=(*GRAPHITE, alpha), width=3)
    for index in range(17):
        x = 132 + index * 51
        length = 32 if index % 4 == 0 else 18
        bend = math.sin(t * 0.6 + index) * (6 + 22 * remap(t, 63, 65.5))
        draw.line((x, y, x + bend, y + length), fill=(*IVORY, alpha), width=2)


def draw_compass(draw: ImageDraw.ImageDraw, t: float, alpha: int = 120, needle: bool = True) -> None:
    cx, cy = 540, 850
    radius = 315 + math.sin(t * 0.34) * 7
    draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=(*GRAPHITE, alpha), width=3)
    draw.ellipse((cx - radius + 24, cy - radius + 24, cx + radius - 24, cy + radius - 24), outline=(*GRAPHITE, alpha // 2), width=2)
    for index in range(16):
        angle = t * 0.25 + math.tau * index / 16
        inner = radius - (42 if index % 4 == 0 else 24)
        draw.line((cx + math.cos(angle) * inner, cy + math.sin(angle) * inner,
                   cx + math.cos(angle) * radius, cy + math.sin(angle) * radius), fill=(*IVORY, alpha), width=2)
    if needle:
        angle = -0.8 + math.sin(t * 0.2) * 1.1
        tip = (cx + math.cos(angle) * (radius - 16), cy + math.sin(angle) * (radius - 16))
        draw.line((cx, cy, tip[0], tip[1]), fill=(*CYAN, min(220, alpha + 60)), width=5)
        draw.ellipse((cx - 8, cy - 8, cx + 8, cy + 8), fill=(*CYAN, min(220, alpha + 50)))


def draw_eye(draw: ImageDraw.ImageDraw, t: float, center: tuple[float, float], scale: float, alpha: int) -> None:
    cx, cy = center
    points = []
    for index in range(100):
        u = math.pi * 2 * index / 99
        points.append((cx + math.cos(u) * 300 * scale, cy + math.sin(u) * 118 * scale))
    draw_line(draw, points, (*CYAN, alpha), 3)
    iris_alpha = max(18, alpha // 2)
    draw.ellipse((cx - 52 * scale, cy - 52 * scale, cx + 52 * scale, cy + 52 * scale), outline=(*IVORY, iris_alpha), width=3)
    draw.ellipse((cx - 13 * scale, cy - 13 * scale, cx + 13 * scale, cy + 13 * scale), fill=(*CYAN, max(22, alpha // 2)))


def draw_portrait(draw: ImageDraw.ImageDraw, t: float, alpha: int) -> None:
    cx, cy = 540, 890
    erosion = 0.72 * remap(t, 115.7, 118.9) + 0.48 * remap(t, 129.5, 132.8)
    face = [(cx - 188, cy - 330), (cx - 242, cy - 182), (cx - 216, cy + 80), (cx - 132, cy + 276),
            (cx, cy + 344), (cx + 132, cy + 276), (cx + 216, cy + 80), (cx + 242, cy - 182), (cx + 188, cy - 330)]
    draw_line(draw, face, (*IVORY, int(alpha * (1 - erosion * 0.38))), 4)
    brow_left = [(cx - 148, cy - 115), (cx - 70, cy - 145), (cx - 22, cy - 118)]
    brow_right = [(cx + 22, cy - 118), (cx + 70, cy - 145), (cx + 148, cy - 115)]
    for points in (brow_left, brow_right):
        draw_line(draw, points, (*CYAN, int(alpha * (1 - erosion))), 3)
    draw.line((cx, cy - 86, cx - 23, cy + 72, cx + 18, cy + 91), fill=(*IVORY, int(alpha * (1 - erosion * 0.7))), width=3)
    draw.arc((cx - 110, cy + 82, cx + 110, cy + 206), 16, 164, fill=(*IVORY, int(alpha * (1 - erosion))), width=3)
    # Dry ink falls in a controlled direction; the marks are deterministic, not noise.
    for index in range(18):
        x = cx - 210 + index * 24
        y = cy + 220 + math.sin(index * 2.7 + t) * 35
        length = 15 + (index % 5) * 9
        draw.line((x, y, x - 8, y + length * (0.5 + erosion)), fill=(*MUTED, int(100 * erosion)), width=2)


def draw_sequence_graphics(image: Image.Image, t: float, sequence: int) -> None:
    layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer, "RGBA")
    if sequence == 0:
        # The missing rectangle represents the absent meeting without a literal image.
        if t > 23.0:
            alpha = int(100 * remap(t, 23.0, 26.0))
            draw.rectangle((690, 500, 930, 1430), outline=(*IVORY, alpha), width=2)
            draw.line((690, 500, 690, 1430), fill=(*CYAN, alpha + 20), width=3)
    elif sequence == 1:
        draw_heart_basin(draw, t, 145)
        draw_waveform(draw, t, 1190, 90)
    elif sequence == 2:
        draw_ruler(draw, t, 135, orbital=False)
        if t > 68.5:
            draw_eye(draw, t, (540, 920), 1.0, 125)
    elif sequence == 3:
        draw_compass(draw, t, 142, needle=t < 110.8)
        orbit = path_points((540, 850), (360, 250), t * 0.15, t * 0.15 + math.tau * 0.88, 100)
        draw_line(draw, orbit, (*CYAN, 115), 3)
    elif sequence == 4:
        draw_portrait(draw, t, 135)
    elif sequence == 5:
        draw_heart_basin(draw, t, 105)
        draw_waveform(draw, t, 1210, 75, scar=True)
        draw.rectangle((410, 1010, 670, 1270), outline=(*GRAPHITE, 105), width=5)
    elif sequence == 6:
        draw_ruler(draw, t, 105, orbital=True)
        draw_eye(draw, t, (540, 890), 0.92, 115)
        for index in range(6):
            angle = t * 0.12 + index * 0.9
            draw.line((540 + math.cos(angle) * 300, 890 + math.sin(angle) * 210,
                       540 + math.cos(angle + 0.22) * 380, 890 + math.sin(angle + 0.22) * 280), fill=(*MUTED, 60), width=2)
    elif sequence == 7:
        draw.polygon([(95, 470), (540, 390), (985, 470), (985, 1530), (540, 1610), (95, 1530)], outline=(*GRAPHITE, 120))
        draw.line((540, 390, 540, 1610), fill=(*CYAN, 150), width=3)
        draw.line((495, 420, 585, 1600), fill=(*IVORY, 60), width=2)
    else:
        draw.line((110, 1430, 930, 1200), fill=(*GRAPHITE, 105), width=2)
        draw.ellipse((910, 1180, 944, 1214), outline=(*CYAN, 145), width=3)
    image.alpha_composite(layer)


def wrap_tokens(tokens: list[str], text_font: ImageFont.FreeTypeFont, max_width: int, spacing: int) -> list[list[str]]:
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    space_width = measure.textlength(" ", font=text_font)
    lines: list[list[str]] = []
    current: list[str] = []
    current_width = 0.0
    for token in tokens:
        width = measure.textlength(token, font=text_font)
        proposed = width if not current else current_width + space_width + width
        if current and proposed > max_width:
            lines.append(current)
            current = [token]
            current_width = width
        else:
            current.append(token)
            current_width = proposed
    if current:
        lines.append(current)
    return lines


def choose_lyric_layout(text: str) -> tuple[ImageFont.FreeTypeFont, list[list[str]], int]:
    tokens = text.split(" ")
    # Use the display face for the sung layer. Long lines step down only as far
    # as necessary to keep every word in the safe column.
    for size in (66, 60, 54, 50, 46, 42, 38, 34):
        text_font = font(FONT_SANS, size)
        lines = wrap_tokens(tokens, text_font, 870, 0)
        if len(lines) <= 2:
            return text_font, lines, size
    text_font = font(FONT_SANS, 32)
    return text_font, wrap_tokens(tokens, text_font, 870, 0), 32


def prepare_lyric_layouts(phrases: list[dict]) -> dict[int, dict]:
    layouts: dict[int, dict] = {}
    measure = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for phrase in phrases:
        text_font, lines, size = choose_lyric_layout(phrase["text"])
        line_metrics = []
        for line in lines:
            line_text = " ".join(line)
            line_width = measure.textlength(line_text, font=text_font)
            bbox = measure.textbbox((0, 0), line_text, font=text_font)
            line_metrics.append((line, line_width, bbox[3] - bbox[1]))
        layouts[phrase["line"]] = {
            "font": text_font,
            "lines": line_metrics,
            "total_height": sum(height for _, _, height in line_metrics) + max(0, len(line_metrics) - 1) * 18,
            "widest": max(width for _, width, _ in line_metrics),
            "size": size,
        }
    return layouts


def draw_lyric(image: Image.Image, phrase: dict | None, active_index: int, t: float, sequence: int, layouts: dict[int, dict]) -> None:
    if phrase is None:
        return
    layout = layouts[phrase["line"]]
    text_font = layout["font"]
    line_metrics = layout["lines"]
    token_cursor = 0
    total_height = layout["total_height"]
    base_y = {0: 710, 1: 720, 2: 650, 3: 610, 4: 690, 5: 720, 6: 600, 7: 680, 8: 780}.get(sequence, 700)
    base_y += int(math.sin(t * 0.23 + sequence) * 8)
    start_y = base_y - total_height // 2
    enter = remap(t, phrase["start"] - 0.14, phrase["start"] + 0.16)
    exit_amount = 1.0 - remap(t, phrase["end"] - 0.16, phrase["end"] + 0.18)
    overall_alpha = int(235 * min(1.0, enter) * min(1.0, exit_amount))
    if overall_alpha <= 0:
        return
    draw = ImageDraw.Draw(image, "RGBA")
    # A soft translucent plate makes fast long Hinglish lines readable without
    # turning the composition into a subtitle box.
    widest = layout["widest"]
    plate_left = int((WIDTH - widest) / 2 - 28)
    plate_right = int((WIDTH + widest) / 2 + 28)
    draw.rounded_rectangle((plate_left, start_y - 22, plate_right, start_y + total_height + 24), radius=18, fill=(8, 10, 10, min(34, overall_alpha // 7)))
    y = start_y
    for line, line_width, line_height in line_metrics:
        x = (WIDTH - line_width) / 2
        line_text = " ".join(line)
        shadow = (*INK, min(220, overall_alpha))
        draw.text((x + 2, y + 3), line_text, font=text_font, fill=shadow, stroke_width=2, stroke_fill=shadow)
        draw.text((x, y), line_text, font=text_font, fill=(*IVORY, overall_alpha), stroke_width=1, stroke_fill=(*INK, min(175, overall_alpha)))
        for token in line:
            token_width = draw.textlength(token, font=text_font)
            if token_cursor == active_index:
                draw.text((x, y), token, font=text_font, fill=(*CYAN, overall_alpha), stroke_width=1, stroke_fill=(*INK, min(175, overall_alpha)))
            x += token_width + draw.textlength(" ", font=text_font)
            token_cursor += 1
        y += line_height + 18


def draw_secondary_lyric_echo(image: Image.Image, phrase: dict | None, active_index: int, t: float, sequence: int) -> None:
    """Place an understated echo only in the later portrait/fold compositions."""
    if phrase is None or sequence not in (4, 7, 8):
        return
    # The echo is the same supplied phrase, rendered as a faint physical print
    # rather than new copy. It keeps the portrait and booklet scenes connected.
    tokens = phrase["text"].split(" ")
    text_font = font(FONT_SERIF, 30 if sequence != 8 else 26)
    draw = ImageDraw.Draw(image, "RGBA")
    text = " ".join(tokens)
    width = draw.textlength(text, font=text_font)
    x = (WIDTH - width) / 2
    y = 1540 if sequence != 8 else 1490
    alpha = int(60 * (0.6 + 0.4 * math.sin(t * 0.5)))
    draw.text((x, y), text, font=text_font, fill=(*MUTED, alpha), stroke_width=0)


def render_frame(base: Image.Image, frame_index: int, phrases: list[dict], layouts: dict[int, dict], marks: tuple[list, list]) -> Image.Image:
    t = frame_index / FPS
    sequence = sequence_at(t)
    phrase, active_index = active_phrase(phrases, t)
    image = base.copy()
    draw_background(image, t, sequence, marks)
    draw_sequence_graphics(image, t, sequence)
    final_stop = sequence == 8
    river_alpha = 105 if t < 37.0 else 150
    if sequence in (3, 4, 5, 6, 7, 8):
        river_alpha += 24
    draw_river(image, t, final_stop=final_stop, alpha=min(210, river_alpha))
    draw_lyric(image, phrase, active_index, t, sequence, layouts)
    draw_secondary_lyric_echo(image, phrase, active_index, t, sequence)

    return image.convert("RGB")


def audio_duration() -> float:
    command = [
        "ffprobe", "-v", "error", "-select_streams", "a:0",
        "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(AUDIO),
    ]
    output = subprocess.check_output(command, text=True).strip()
    return float(output)


def render(output: Path, preview_seconds: float | None = None) -> None:
    phrases, _ = validate_assets()
    duration = audio_duration()
    if preview_seconds is not None:
        duration = min(duration, preview_seconds)
    frames = math.ceil(duration * FPS)
    base = paper_plate()
    marks = seeded_marks()
    layouts = prepare_lyric_layouts(phrases)
    if preview_seconds is None:
        QA_DIR.mkdir(parents=True, exist_ok=True)
        keyframes = {0, int(23.6 * FPS), int(70 * FPS), int(94 * FPS), int(116 * FPS), int(145 * FPS), int(166 * FPS), int(180 * FPS)}
    else:
        keyframes = set()
    command = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{WIDTH}x{HEIGHT}", "-r", str(FPS), "-i", "-",
        "-i", str(AUDIO),
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "320k", "-t", f"{duration:.6f}", "-shortest", "-movflags", "+faststart", str(output),
    ]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    if process.stdin is None:
        raise RuntimeError("could not open FFmpeg video pipe")
    try:
        for frame_index in range(frames):
            frame = render_frame(base, frame_index, phrases, layouts, marks)
            if frame_index in keyframes:
                frame.save(QA_DIR / f"frame-{frame_index:04d}.png", optimize=True)
            process.stdin.write(frame.tobytes())
            if frame_index % (FPS * 10) == 0:
                print(f"rendered {frame_index / FPS:6.1f}s / {duration:6.1f}s", file=sys.stderr, flush=True)
    finally:
        process.stdin.close()
    return_code = process.wait()
    if return_code != 0:
        raise SystemExit(f"ffmpeg failed with exit code {return_code}")
    print(f"wrote {output}")
    if preview_seconds is None:
        print(f"wrote {len(keyframes)} QA frames to {QA_DIR}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render the complete 9:16 Hinglish lyric video")
    parser.add_argument("--output", type=Path, default=OUT)
    parser.add_argument("--preview-seconds", type=float, default=None)
    args = parser.parse_args()
    render(args.output, args.preview_seconds)


if __name__ == "__main__":
    main()
