"""Normalised keys for matching text that people type or speak.

A teacher's correction must be reused for the same sentence even if it is typed
slightly differently next time, and a child's answer must be graded the same
whether they say "7", "७" or "᱗". The key is for matching only; the original
text is always what gets stored and shown.
"""

import re
import unicodedata

_DIGITS = {**{chr(0x0966 + i): str(i) for i in range(10)},      # Devanagari
           **{chr(0x1C50 + i): str(i) for i in range(10)}}      # Ol Chiki
_INVISIBLE = "​‌‍﻿"          # zero-width space/non-joiner/joiner, BOM

# Bump when normalize_key changes, so stored keys are recomputed (database.py).
KEY_VERSION = 2


def normalize_key(text: str) -> str:
    """Matching key for a sentence or an answer.

    - Unicode NFC (so precomposed and decomposed letters compare equal)
    - nukta removed (ज़ = ज) and chandrabindu folded into anusvara (पाँच = पांच):
      both are routinely typed either way
    - zero-width characters removed
    - Devanagari and Ol Chiki digits become ASCII digits
    - all punctuation removed (dandas, Ol Chiki sentence marks, ?, commas...):
      speech recognition writes none, so a spoken line must match a typed one
    - whitespace collapsed, Latin lower-cased
    """
    if not text:
        return ""
    s = unicodedata.normalize("NFC", text)
    s = s.replace("़", "")                   # nukta (NFC decomposes क़ -> क + ़)
    s = s.replace("ँ", "ं")             # chandrabindu -> anusvara
    for ch in _INVISIBLE:
        s = s.replace(ch, "")
    s = "".join(_DIGITS.get(c, c) for c in s)
    s = "".join(" " if unicodedata.category(c).startswith("P") else c for c in s)
    return re.sub(r"\s+", " ", s).strip().lower()


def digits_of(text: str) -> str:
    """The ASCII digit string in a short answer ("᱗" -> "7"), or "" if none."""
    s = normalize_key(text)
    return s if s.isdigit() else ""


# Annotation tags in IndicVoices transcripts ("<unintelligible>"): no recogniser writes them.
_TAG = re.compile(r"<[^<>\s]*>")


def strip_reference_tags(text: str):
    """(reference without dataset annotation tags, number of tags removed).
    For REFERENCES only: a tag in a hypothesis stays and counts as an error."""
    if not text:
        return "", 0
    found = _TAG.findall(text)
    return _TAG.sub(" ", text), len(found)


# indic-nlp-library-itt (installed by the pinned IndicTransToolkit) defines
# DevanagariNormalizer.NUKTA = "\\u093C": decomposing a precomposed nukta letter
# (ड़ U+095C, क़ ... य़, ऩ ऱ ऴ) writes the base letter plus the six characters ़.
# A model fine-tuned on text that went through it learns to write them.
_NUKTA_ESCAPE = re.compile(r"\\u093[cC]")


# The precomposed nukta letters, written as base letter + nukta (U+093C) before a teacher's
# Hindi reaches the model, so the normaliser above never sees them. The tablet's IndicProc.kt
# does the same, so the hub and the tablet now read such input alike.
_NUKTA_LETTERS = {"\u0929": "\u0928", "\u0931": "\u0930", "\u0934": "\u0933",
                  "\u0958": "\u0915", "\u0959": "\u0916", "\u095a": "\u0917", "\u095b": "\u091c",
                  "\u095c": "\u0921", "\u095d": "\u0922", "\u095e": "\u092b", "\u095f": "\u092f"}
_NUKTA_LETTER_RE = re.compile("[" + "".join(_NUKTA_LETTERS) + "]")


def decompose_nukta(text: str) -> str:
    """ड़ (U+095C) -> ड + ़ (U+093C), and the same for the other precomposed nukta letters."""
    return _NUKTA_LETTER_RE.sub(lambda m: _NUKTA_LETTERS[m.group()] + "\u093c", text or "")


def fix_nukta_escape(text: str) -> str:
    """Model output with the literal escape \\u093C replaced by the nukta (U+093C), then NFC.
    Used for the Mundari preview's output and for both sides of its scoring."""
    if not text:
        return text or ""
    return unicodedata.normalize("NFC", _NUKTA_ESCAPE.sub("़", text))


def normalize_for_wer(text: str) -> str:
    """Text for the *normalised* WER/CER in bench/ (rules in bench/README.md).

    Only formatting is removed, the same way for Hindi and Santali: Unicode NFC;
    every punctuation mark (Unicode category P: , . ? । ॥ ᱾ ᱿ - ...) replaced by
    a space; Devanagari and Ol Chiki digits written as ASCII digits; whitespace
    collapsed. Spelling is left alone (no nukta or chandrabindu folding, unlike
    normalize_key). Dataset tags are removed from references before this, by
    strip_reference_tags, never from hypotheses.
    """
    if not text:
        return ""
    s = unicodedata.normalize("NFC", text)
    s = "".join(_DIGITS.get(c, c) for c in s)
    s = "".join(" " if unicodedata.category(c).startswith("P") else c for c in s)
    return re.sub(r"\s+", " ", s).strip()
