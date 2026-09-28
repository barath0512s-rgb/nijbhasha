"""The teacher's lesson plan: a printable daily script with a pronunciation guide.

    python lesson_plan.py --grade 2 --topic addition      # writes docs/samples/lesson_plan_2_addition.pdf

One A4 PDF per lesson, for the teacher, not the class:
  header    lesson title, grade, the NIPUN Lakshya IDs with the Ministry's text, date
  steps     for every line of the lesson, in order:
              the step type (teach / do / ask) and the teaching note,
              the Hindi line the teacher says,
              the Santali in Ol Chiki (what the child hears),
              a reading guide: that Santali in Devanagari, so a Hindi-medium teacher
                can read it aloud (reading_guide.py),
              a tier letter: A written by people (glossary or a teacher's correction),
                B model output with no warning, C model output in doubt,
              for questions, the accepted answers (Hindi, Santali, digits).
  footer    what is and is not reviewed.
Pure layout, like worksheet_v2.py: the Santali comes from the caller (the hub's
translations or a content pack's), never from a model here.
"""

import argparse
import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import config
from nipun import lakshya
from reading_guide import reading_guide
from worksheet import P, ps, ps_sat

ROOT = Path(__file__).resolve().parent

STEP = {"lesson_script": "सिखाना (teach)", "activity_instruction": "करना (do)",
        "assessment_prompt": "पूछना (ask)"}
TIER = {"teacher": "A", "glossary": "A", "model": "B", "cached": "B"}


def tier(source, needs_review):
    """A / B / C as on the page (frontend.html TIER); None when there is no Santali."""
    if needs_review:
        return "C"
    return TIER.get(source)


def build(lesson, grade, topic, santali_of, out, date=None):
    """lesson: a lesson_engine lesson dict. santali_of(hindi) -> {"text", "source",
    "needs_review"} or None. Returns the steps as written, for tests:
    [{"hindi", "santali", "guide", "tier"}]."""
    date = date or datetime.date.today()
    doc = SimpleDocTemplate(out if hasattr(out, "write") else str(out), pagesize=A4,
                            leftMargin=1.5 * cm, rightMargin=1.5 * cm, topMargin=1.3 * cm, bottomMargin=1.4 * cm,
                            title=f"{config.APP_NAME} lesson plan {grade} {topic}", author=config.APP_NAME)
    HD = ps("LP_HD", 15, True, "#0D2137", TA_CENTER)
    SUB = ps("LP_SUB", 9.5, False, "#1A5276", TA_CENTER)
    GOAL = ps("LP_GOAL", 8.5, False, "#333333")
    TAG = ps("LP_TAG", 8.5, True, "#6B3FA0")
    HI = ps("LP_HI", 12.5, True)
    SAT = ps_sat("LP_SAT", 12.5)
    GD = ps("LP_GD", 11, False, "#1E6B3A")
    NOTE = ps("LP_NOTE", 9, False, "#555555")
    FT = ps("LP_FT", 7.5, False, "#777777", TA_CENTER)

    lids = lesson.get("lakshya_ids") or []
    grade_txt = "बालवाटिका (Balvatika)" if str(grade) == "0" else f"कक्षा {grade} (Grade {grade})"
    s = [P(f"{config.APP_NAME_LOCAL.get('hi') or config.APP_NAME} — पाठ योजना (lesson plan)", HD),
         P(f"{lesson.get('title', topic)}  |  {grade_txt}  |  {date.strftime('%d.%m.%Y')}", SUB),
         Spacer(1, 0.2 * cm)]
    for lid in lids:
        g = lakshya.get(lid)
        s.append(P(f"{lid}: {g['text'] if g else ''}", GOAL))
    s.append(Spacer(1, 0.3 * cm))

    written = []
    for i, st in enumerate(lesson.get("steps", []), 1):
        hi = st.get("hindi", "")
        r = santali_of(hi) or {}
        sat = r.get("text") or ""
        g = reading_guide(sat)
        tr = tier(r.get("source"), r.get("needs_review")) if sat else None
        written.append({"hindi": hi, "santali": sat, "guide": g, "tier": tr})
        body = [P(f"{i}. {STEP.get(st.get('type'), st.get('type', ''))}"
                  + (f"   ·   tier {tr}" if tr else ""), TAG),
                P(hi, HI)]
        if sat:
            body.append(P(sat, SAT))
        if g:
            body.append(P(f"पढ़ें: {g}", GD))
        if not sat:
            body.append(P("संताली अभी नहीं बनी (hub पर अनुवाद करें)", NOTE))
        acc = st.get("accept_answers") or {}
        answers = [a for k in ("hi", "sat", "digits") for a in acc.get(k, [])]
        if answers:
            body.append(P("सही उत्तर: " + ", ".join(dict.fromkeys(answers)), NOTE))
        if st.get("note"):
            body.append(P(st["note"], NOTE))
        t = Table([[body]], colWidths=[18 * cm])
        t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#C9C2B8")),
                               ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#FBF8F3")),
                               ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 5),
                               ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
        s += [KeepTogether([t]), Spacer(1, 0.25 * cm)]

    s += [Spacer(1, 0.3 * cm),
          P("Tier A: written by people (glossary or a teacher's correction). Tier B: machine translation, no warning. "
            "Tier C: machine translation in doubt, check with a native speaker. The reading guide is the same "
            "transliteration the offline voice speaks; its phonetic choices, and all Santali here, await native review. "
            f"Made by {config.APP_NAME}, offline.", FT)]
    doc.build(s)
    return written


def main():
    """A sample from the Android test content pack (real hub output), no models needed."""
    import json
    from textnorm import normalize_key
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--grade", default="2")
    ap.add_argument("--topic", default="addition")
    ap.add_argument("--pack", default=str(ROOT / "android/app/src/test/resources/pack"))
    ap.add_argument("--out", default=str(ROOT / "docs" / "samples"))
    a = ap.parse_args()
    pack = Path(a.pack)
    tr = json.loads((pack / "translations.json").read_text(encoding="utf-8"))["hi-to-sat"]
    lesson = next(x["lesson"] for x in json.loads((pack / "lessons.json").read_text(encoding="utf-8"))
                  if x["grade"] == a.grade and x["topic"] == a.topic)
    out = Path(a.out) / f"lesson_plan_{a.grade}_{a.topic}.pdf"
    out.parent.mkdir(parents=True, exist_ok=True)
    build(lesson, a.grade, a.topic, lambda hi: tr.get(normalize_key(hi)), out)
    print("wrote", out)


if __name__ == "__main__":
    main()
