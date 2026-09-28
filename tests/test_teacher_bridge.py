"""The teacher-bridge features (no models needed): the Devanagari reading guide,
the lesson plan PDF with tiers, and the community voice corpus rules."""

import io
import json
import re
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import corpus  # noqa: E402
import lesson_plan  # noqa: E402
from reading_guide import reading_guide  # noqa: E402
from textnorm import normalize_key  # noqa: E402

PACK = ROOT / "android/app/src/test/resources/pack"


# ── reading guide ────────────────────────────────────────────────────────────
def test_reading_guide_is_devanagari_for_santali_and_none_otherwise():
    g = reading_guide("ᱛᱮᱦᱮᱸᱡ ᱟᱞᱮ")
    assert g == "तेहेँच् आले"                     # the README's own example
    assert not any(0x1C50 <= ord(c) <= 0x1C7F for c in g)
    assert reading_guide("दो और तीन") is None     # Hindi output has no guide
    assert reading_guide("") is None and reading_guide(None) is None


def test_reading_guide_speaks_numbers_as_santali_words():
    assert reading_guide("᱓") and not any(c.isdigit() for c in reading_guide("᱓"))


def test_every_pack_line_gets_a_guide_without_ol_chiki_left_over():
    tr = json.loads((PACK / "translations.json").read_text(encoding="utf-8"))["hi-to-sat"]
    for e in tr.values():
        g = reading_guide(e["text"])
        assert g, e["text"]
        assert not any(0x1C50 <= ord(c) <= 0x1C7F for c in g), (e["text"], g)


# ── lesson plan ──────────────────────────────────────────────────────────────
def _pack():
    tr = json.loads((PACK / "translations.json").read_text(encoding="utf-8"))["hi-to-sat"]
    lessons = json.loads((PACK / "lessons.json").read_text(encoding="utf-8"))
    return tr, lessons


@pytest.mark.parametrize("grade,topic", [("2", "addition"), ("1", "counting_1_10"), ("3", "subtraction")])
def test_lesson_plan_has_every_line_with_santali_guide_and_tier(grade, topic):
    tr, lessons = _pack()
    lesson = next(x["lesson"] for x in lessons if x["grade"] == grade and x["topic"] == topic)
    buf = io.BytesIO()
    rows = lesson_plan.build(lesson, grade, topic, lambda hi: tr.get(normalize_key(hi)), buf)
    assert buf.getvalue()[:5] == b"%PDF-" and len(buf.getvalue()) > 5000
    assert [r["hindi"] for r in rows] == [s["hindi"] for s in lesson["steps"]]
    for r in rows:
        assert r["santali"] and r["guide"] and r["tier"] in ("A", "B", "C")


def test_lesson_plan_tiers():
    assert lesson_plan.tier("glossary", False) == "A"
    assert lesson_plan.tier("teacher", False) == "A"
    assert lesson_plan.tier("model", False) == "B"
    assert lesson_plan.tier("model", True) == "C"
    assert lesson_plan.tier("glossary", True) == "C"


def test_lesson_plan_marks_a_line_without_santali():
    lesson = {"title": "t", "lakshya_ids": ["NIPUN-G1-NUM-2"], "steps": [{"type": "lesson_script", "hindi": "नमस्ते"}]}
    rows = lesson_plan.build(lesson, "1", "x", lambda hi: None, io.BytesIO())
    assert rows == [{"hindi": "नमस्ते", "santali": "", "guide": None, "tier": None}]


def test_page_and_lesson_plan_use_the_same_tiers():
    html = (ROOT / "frontend.html").read_text(encoding="utf-8")
    m = re.search(r"const TIER = \{([^}]*)\}", html)
    page = dict(re.findall(r"(\w+):\"([ABC])\"", m.group(1)))
    assert {k: v for k, v in page.items() if k != "review"} == lesson_plan.TIER
    assert page["review"] == "C"


# ── community voice corpus ───────────────────────────────────────────────────
def test_corpus_refuses_without_adult_consent(tmp_path):
    with pytest.raises(corpus.CorpusError):
        corpus.add(b"x" * 100, "webm", "ᱡᱚᱦᱟᱨ", "sat", adult=False, share=True, root=tmp_path)
    assert not (tmp_path / "manifest.jsonl").exists()


@pytest.mark.parametrize("kw", [dict(lang="en"), dict(text=""), dict(text="x" * 301), dict(ext="exe"),
                                dict(audio=b""), dict(audio=b"x" * (corpus.MAX_BYTES + 1))])
def test_corpus_rejects_bad_input(tmp_path, kw):
    args = dict(audio=b"x" * 100, ext="webm", text="ᱡᱚᱦᱟᱨ", lang="sat", adult=True, share=False, root=tmp_path)
    args.update(kw)
    with pytest.raises(corpus.CorpusError):
        corpus.add(**args)


def test_corpus_keeps_no_names_and_exports_only_shareable(tmp_path):
    a = corpus.add(b"A" * 200, "webm", "ᱡᱚᱦᱟᱨ", "sat", adult=True, share=True, root=tmp_path)
    b = corpus.add(b"B" * 200, "wav", "जोहार", "unr", adult=True, share=False, root=tmp_path)
    assert set(a) == {"id", "file", "lang", "text", "date", "consent"}      # nothing that names a person
    s = corpus.summary(root=tmp_path)
    assert s == {"total": 2, "by_lang": {"sat": 1, "unr": 1, "hoc": 0}, "shareable": 1}
    z = zipfile.ZipFile(io.BytesIO(corpus.export_zip(root=tmp_path)))
    names = set(z.namelist())
    assert a["file"] in names and b["file"] not in names
    manifest = [json.loads(x) for x in z.read("manifest.jsonl").decode().splitlines()]
    assert [r["id"] for r in manifest] == [a["id"]]


def test_corpus_folder_is_git_ignored():
    assert "corpus/" in (ROOT / ".gitignore").read_text(encoding="utf-8").split()
