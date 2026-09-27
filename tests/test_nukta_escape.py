"""The literal "\\u093C" that the pinned IndicNLP normaliser writes instead of the nukta."""

import unicodedata

import pytest

from textnorm import fix_nukta_escape

NUKTA = "़"
DA_PRE = "ड़"                 # ड़ precomposed
DA_DEC = "ड" + NUKTA         # ड़ decomposed
LITERAL = "\\u093C"               # the six characters


def test_literal_escape_becomes_the_nukta():
    hyp = "यही प" + "ड" + LITERAL + "हा पत्थर"
    assert fix_nukta_escape(hyp) == "यही प" + DA_DEC + "हा पत्थर"
    assert "\\" not in fix_nukta_escape(hyp)


def test_lower_case_escape_too():
    assert fix_nukta_escape("ड\\u093c") == DA_DEC


def test_nfc_and_precomposed_agree():
    # U+095C is a composition exclusion: NFC writes it decomposed, so the fixed
    # hypothesis and a reference typed with the precomposed letter compare equal.
    assert fix_nukta_escape("ड" + LITERAL) == fix_nukta_escape(DA_PRE) == DA_DEC


def test_clean_text_unchanged_except_nfc():
    for s in ("बच्चे पढ़ रहे हैं।", "ᱵᱟᱨ ᱩᱞ", "", "a\\b"):
        assert fix_nukta_escape(s) == unicodedata.normalize("NFC", s)


def test_pinned_toolkit_still_writes_the_escape():
    """Documents the upstream behaviour the helper exists for; if a newer toolkit fixes it,
    this test fails and the note in textnorm.py can be updated."""
    pytest.importorskip("IndicTransToolkit")
    from IndicTransToolkit.processor import IndicProcessor
    out = IndicProcessor(inference=False).preprocess_batch(["प" + DA_PRE + "हा"], src_lang="hin_Deva",
                                                          tgt_lang=None, is_target=True)[0]
    assert LITERAL in out
    assert fix_nukta_escape(out) == "प" + DA_DEC + "हा"
