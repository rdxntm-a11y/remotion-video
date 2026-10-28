"""Transliterate the frozen lyric assets without touching their timing."""

from __future__ import annotations

import copy
import json
import re
from pathlib import Path


ROOT = Path(__file__).parent
DEVANAGARI_WORD = re.compile(r"[\u0900-\u097F]+")

# Deliberately explicit rather than an automatic phonetic transliterator: these
# spellings are the approved on-screen Hinglish style for this lyric video.
TRANSLITERATION = {
    "मिले": "Mile",
    "तो": "to",
    "तू": "tu",
    "कभी": "kabhi",
    "नहीं": "nahi",
    "मेरी": "meri",
    "हसरत": "hasrat",
    "क्यों": "kyun",
    "भड़का": "bhadka",
    "बेवजा": "bewaja",
    "के": "ke",
    "तुम": "tum",
    "बिना": "bina",
    "जिए": "jiye",
    "अगर": "agar",
    "हुआ": "hua",
    "कैसे": "kaise",
    "ना": "na",
    "ये": "ye",
    "जीना": "jeena",
    "रागा": "raaga",
    "दरिया": "dariya",
    "मेरे": "mere",
    "दिल": "dil",
    "का": "ka",
    "यह": "yeh",
    "बहता": "behta",
    "दुखी": "dukhi",
    "की": "ki",
    "सदा": "sada",
    "कुछ": "kuch",
    "कहता": "kehta",
    "इसकी": "iski",
    "खामोशी": "khamoshi",
    "वजह": "wajah",
    "है": "hai",
    "से": "se",
    "तंग": "tang",
    "आ": "aa",
    "गया": "gaya",
    "यही": "yahi",
    "सजा": "saza",
    "उल्फतों": "ulfaton",
    "में": "mein",
    "कोई": "koi",
    "पैमाना": "paimana",
    "अपनों": "apnon",
    "मुझसे": "mujhse",
    "कहना": "kehna",
    "था": "tha",
    "सुरमई": "surmai",
    "तेरी": "teri",
    "आंखों": "aankhon",
    "बह": "beh",
    "जाना": "jaana",
    "क्या": "kya",
    "पता": "pata",
    "तेरे": "tere",
    "गम": "gham",
    "ही": "hi",
    "रहना": "rehna",
    "यूं": "yun",
    "सहते": "sahte",
    "को": "ko",
    "खा": "kha",
    "चुका": "chuka",
    "जान": "jaan",
    "रहते": "rehte",
    "दिखे": "dikhe",
    "दिशा": "disha",
    "जो": "jo",
    "ऐसा": "aisa",
    "मैं": "main",
    "चेहरा": "chehra",
    "जिसकी": "jiski",
    "खूबसूरती": "khoobsurati",
    "मांद": "maand",
    "पड़ी": "padi",
    "हो": "ho",
    "बहना": "behna",
    "चाहे": "chahe",
}


def transliterate(text: str) -> str:
    def replace(match: re.Match[str]) -> str:
        word = match.group(0)
        try:
            return TRANSLITERATION[word]
        except KeyError as exc:
            raise ValueError(f"Missing transliteration for {word!r}") from exc

    return DEVANAGARI_WORD.sub(replace, text)


def timing_snapshot(items: list[dict]) -> list[tuple]:
    snapshot = []
    for item in items:
        snapshot.append(
            (
                item["start"],
                item["end"],
                [
                    (word["start"], word["end"])
                    for word in item.get("words", [])
                ],
            )
        )
    return snapshot


def main() -> None:
    source = (ROOT / "lyrics.txt").read_text(encoding="utf-8")
    lyrics_hinglish = transliterate(source)

    word_path = ROOT / "word-timestamps.json"
    phrase_path = ROOT / "phrases.json"
    words = json.loads(word_path.read_text(encoding="utf-8"))
    phrases = json.loads(phrase_path.read_text(encoding="utf-8"))

    original_word_timing = [(item["start"], item["end"]) for item in words]
    original_phrase_timing = timing_snapshot(phrases)

    for item in words:
        item["word"] = transliterate(item["word"])
    for phrase in phrases:
        phrase["text"] = transliterate(phrase["text"])
        for word in phrase["words"]:
            word["word"] = transliterate(word["word"])

    if original_word_timing != [(item["start"], item["end"]) for item in words]:
        raise AssertionError("word-timestamps.json timing changed")
    if original_phrase_timing != timing_snapshot(phrases):
        raise AssertionError("phrases.json timing changed")

    (ROOT / "lyrics_hinglish.txt").write_text(lyrics_hinglish, encoding="utf-8")
    word_path.write_text(
        json.dumps(words, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    phrase_path.write_text(
        json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # Keep this check in the generator so it fails loudly if a future source
    # lyric contains a word that was not deliberately approved above.
    source_words = DEVANAGARI_WORD.findall(source)
    if any(word not in TRANSLITERATION for word in source_words):
        raise AssertionError("source contains an unapproved Devanagari word")
    print(
        f"wrote lyrics_hinglish.txt, {len(words)} word entries, "
        f"and {len(phrases)} phrase entries; timing preserved"
    )


if __name__ == "__main__":
    main()
