"""Create an ASS subtitle track with phrase display and word highlighting."""

import json
from pathlib import Path


ROOT = Path(__file__).parent
PHRASES = ROOT / "phrases.json"
ASS = ROOT / "lyrics.ass"


def ass_time(seconds: float) -> str:
    total_cs = max(0, round(seconds * 100))
    hours, remainder = divmod(total_cs, 360000)
    minutes, remainder = divmod(remainder, 6000)
    secs, centis = divmod(remainder, 100)
    return f"{hours}:{minutes:02d}:{secs:02d}.{centis:02d}"


def ass_text(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def main() -> None:
    phrases = json.loads(PHRASES.read_text(encoding="utf-8"))
    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1920",
        "PlayResY: 1080",
        "ScaledBorderAndShadow: yes",
        "WrapStyle: 2",
        "YCbCr Matrix: None",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: Base,Noto Sans,58,&H00E6E6E6,&H00E6E6E6,&H00101010,&HAA000000,0,0,0,0,100,100,0,0,1,3,2,5,80,80,0,1",
        "Style: Highlight,Noto Sans,58,&H00D7FF,&H00D7FF,&H00101010,&HAA000000,0,0,0,0,100,100,0,0,1,3,2,5,80,80,0,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    base_color = "&H00E6E6E6&"
    highlight_color = "&H00D7FF&"
    position = "{\\an5\\pos(960,830)}"

    for phrase in phrases:
        phrase_text = ass_text(phrase["text"])
        start = ass_time(phrase["start"])
        end = ass_time(phrase["end"])
        lines.append(f"Dialogue: 0,{start},{end},Base,,0,0,0,,{position}{phrase_text}")

        display_words = phrase["text"].split(" ")
        if len(display_words) != len(phrase["words"]):
            raise ValueError(f"Phrase {phrase['line']} word count mismatch")
        for active_index, word in enumerate(phrase["words"]):
            rendered = []
            for index, display_word in enumerate(display_words):
                escaped = ass_text(display_word)
                if index == active_index:
                    rendered.append(f"{{\\c{highlight_color}}}{escaped}{{\\c{base_color}}}")
                else:
                    rendered.append(escaped)
            text = " ".join(rendered)
            lines.append(
                f"Dialogue: 1,{ass_time(word['start'])},{ass_time(word['end'])},Highlight,,0,0,0,,{position}{text}"
            )

    ASS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {ASS} with {len(lines) - 12} timed dialogue events")


if __name__ == "__main__":
    main()
