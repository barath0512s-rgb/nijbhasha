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


# ---- Input side (decision of 30 Sep): a teacher's precomposed nukta letter reaches the model
# as base letter + real nukta, as on the tablet (IndicProc.kt), never as the escape.

from textnorm import decompose_nukta  # noqa: E402

PRECOMPOSED = "ऩऱऴक़ख़ग़ज़ड़ढ़फ़य़"


def test_decompose_nukta_writes_the_real_nukta():
    assert decompose_nukta(DA_PRE) == DA_DEC
    for ch in PRECOMPOSED:
        out = decompose_nukta(ch)
        assert len(out) == 2 and out[1] == NUKTA
        assert out == unicodedata.normalize("NFD", ch)     # the same as Unicode's decomposition
    assert decompose_nukta("बच्चे पढ़ रहे हैं। ᱵᱟᱨ") == "बच्चे पढ़ रहे हैं। ᱵᱟᱨ"
    assert decompose_nukta("") == "" and decompose_nukta(None) == ""


def test_translate_gives_the_model_the_real_nukta(monkeypatch):
    for m in ("torch", "transformers", "IndicTransToolkit"):
        pytest.importorskip(m)
    import pipeline
    pl = pipeline.VaaniSetuPipeline.__new__(pipeline.VaaniSetuPipeline)
    seen = []
    monkeypatch.setattr(pipeline.database, "get_correction", lambda text, d: None)
    monkeypatch.setattr(pipeline, "lookup_hi_to_sat", lambda text: None)
    monkeypatch.setattr(pl, "_nmt_review", lambda t, s, g: (seen.append(t), ("ᱵᱟᱨ", None, False))[1], raising=False)
    monkeypatch.setattr(pl, "_apply_domain_glossary", lambda o, l: o, raising=False)
    pipeline.TRANSLATION_CACHE.clear()
    try:
        pl.translate("पे" + DA_PRE + " पर चढ़ो।", "hi-to-sat")
    finally:
        pipeline.TRANSLATION_CACHE.clear()
    assert seen == ["पे" + DA_DEC + " पर चढ़ो।"]


def test_pinned_toolkit_gets_no_escape_after_decomposing():
    pytest.importorskip("IndicTransToolkit")
    from IndicTransToolkit.processor import IndicProcessor
    s = "बच्चे पे" + DA_PRE + " पर चढ़े।"
    ip = IndicProcessor(inference=True)
    assert LITERAL in ip.preprocess_batch([s], src_lang="hin_Deva", tgt_lang="sat_Olck")[0]
    assert LITERAL not in ip.preprocess_batch([decompose_nukta(s)], src_lang="hin_Deva", tgt_lang="sat_Olck")[0]
