"""FLN translation sample: real hub output for lesson lines, with automatic checks.

    python tools/fln_sample_report.py        # writes docs/fln_translation_sample.md

Reads the content pack in the Android test resources (built by the laptop hub on
26 Sep 2026: IndicTrans2 indic-indic 320M, ONNX fp32, greedy; glossary and teacher
layers first). Nothing is translated here and no model is needed.

For every Hindi -> Santali lesson line it checks what can be checked without a
native speaker:
  script      every letter of the Santali is Ol Chiki (U+1C50-U+1C7F); spaces,
              punctuation and digits allowed. A Devanagari or Latin letter left in the
              output is an untranslated fallback.
  numbers     a Hindi number word (एक ... दस) or digit in the line -> is there a number
              in the Santali (Ol Chiki digit or a Santali number word)?
  flag        the round-trip caution flag (A3) the pack carries.
It then lists a sample of 24 lines across the four FLN kinds (lesson script,
activity instruction, assessment prompt, and counting / numbers), with the source
layer, the tier and the Devanagari reading guide. It does NOT measure accuracy:
that needs a native speaker (docs/native_review.md).
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from reading_guide import reading_guide  # noqa: E402
from textnorm import normalize_key  # noqa: E402
from translit.olchiki import _number_words  # noqa: E402

PACK = ROOT / "android/app/src/test/resources/pack"
HI_NUM = ["एक", "दो", "तीन", "चार", "पाँच", "पांच", "छह", "छः", "सात", "आठ", "नौ", "दस", "बीस", "सौ", "हज़ार", "हजार"]
TIER = {"teacher": "A", "glossary": "A", "model": "B", "cached": "B"}


def letters_ok(sat):
    bad = [c for c in sat if c.isalpha() and not (0x1C50 <= ord(c) <= 0x1C7F)]
    return not bad, "".join(dict.fromkeys(bad))


def has_number_hi(hi):
    return bool(re.search(r"\d|[०-९]", hi)) or any(re.search(rf"(^|\s){w}(\s|[।?,.!]|$)", hi) for w in HI_NUM)


def has_number_sat(sat):
    if re.search(r"[᱐-᱙]|\d", sat):
        return True
    words = set(_number_words().values()) if isinstance(_number_words(), dict) else set(_number_words())
    return any(w and w in sat for w in words)


def main():
    tr = json.loads((PACK / "translations.json").read_text(encoding="utf-8"))["hi-to-sat"]
    lessons = json.loads((PACK / "lessons.json").read_text(encoding="utf-8"))
    rows = []
    for x in lessons:
        for st in x["lesson"]["steps"]:
            e = tr.get(normalize_key(st["hindi"]))
            if e:
                rows.append({"grade": x["grade"], "lesson": x["lesson"]["title"], "type": st.get("type", ""),
                             "hi": st["hindi"], "sat": e["text"], "source": e["source"],
                             "flag": bool(e.get("needs_review"))})
    seen, uniq = set(), []
    for r in rows:
        if r["hi"] not in seen:
            seen.add(r["hi"]); uniq.append(r)
    rows = uniq
    script_bad = [(r, letters_ok(r["sat"])[1]) for r in rows if not letters_ok(r["sat"])[0]]
    num_rows = [r for r in rows if has_number_hi(r["hi"])]
    num_missing = [r for r in num_rows if not has_number_sat(r["sat"])]
    by_src = {}
    for r in rows:
        by_src[r["source"]] = by_src.get(r["source"], 0) + 1
    flagged = [r for r in rows if r["flag"]]

    def pick(pred, n):
        return [r for r in rows if pred(r)][:n]
    sample = (pick(lambda r: r["type"] == "lesson_script" and not has_number_hi(r["hi"]), 6)
              + pick(lambda r: r["type"] == "activity_instruction" and not has_number_hi(r["hi"]), 6)
              + pick(lambda r: r["type"] == "assessment_prompt", 6)
              + pick(lambda r: has_number_hi(r["hi"]) and r["type"] != "assessment_prompt", 6))
    for r in flagged[:3]:
        if r not in sample:
            sample.append(r)

    L = ["# FLN translation sample: real hub output, automatic checks", "",
         "Made by `tools/fln_sample_report.py` from the content pack the laptop hub built on 26 Sep 2026 "
         "(IndicTrans2 indic-indic 320M, ONNX fp32, greedy; teacher corrections and the glossary answer first). "
         "Nothing re-translated here. **Accuracy is not measured: no native speaker has reviewed these lines.**", "",
         "## Checks over every lesson line in the pack", "",
         f"- Lesson lines with a Santali translation: **{len(rows)}** (distinct Hindi lines, 18 lessons).",
         f"- Source layer: " + ", ".join(f"{k} {v}" for k, v in sorted(by_src.items())) + ".",
         f"- Script: **{len(rows) - len(script_bad)} of {len(rows)}** are Ol Chiki letters only "
         f"(no letter from another script)" + (": exceptions below." if script_bad else "."),
         f"- Numbers: {len(num_rows)} lines have a Hindi number; the Santali has a number (Ol Chiki digit or a "
         f"Santali number word) in **{len(num_rows) - len(num_missing)}** of them.",
         f"- Round-trip caution flag (A3): **{len(flagged)}** of {len(rows)} lines (shown with ⚠️ and not auto-played).",
         f"- Script guard (added 28 Sep, `nmt_guard.foreign_letters`): flags every line with a non-Ol Chiki letter; "
         f"of the {len(script_bad)} such lesson lines, **{sum(not r['flag'] for r, _ in script_bad)}** had passed the "
         "round-trip check unflagged. The tablet applies the guard to pack lines at once; the hub applies it to "
         "new model output (rebuild the content pack to carry the flags).", ""]
    if script_bad:
        L += ["### Lines with a non-Ol Chiki letter", "", "| Hindi | Santali | Letters |", "|---|---|---|"]
        L += [f"| {r['hi']} | {r['sat']} | {bad} |" for r, bad in script_bad]
        L.append("")
    if num_missing:
        L += ["### Number in the Hindi, none found in the Santali (to check: it may be written as a word the "
              "check does not know)", "", "| Hindi | Santali |", "|---|---|"]
        L += [f"| {r['hi']} | {r['sat']} |" for r in num_missing]
        L.append("")
    L += [f"## Sample of {len(sample)} lines", "",
          "Tier: A written by people (the team's glossary or a teacher's correction; native review pending), "
          "B model output with no warning, C model output flagged by the round-trip check.", "",
          "| # | Kind | Hindi (teacher) | Santali (Ol Chiki) | Reading guide (Devanagari) | Source | Tier |",
          "|---|---|---|---|---|---|---|"]
    for i, r in enumerate(sample, 1):
        kind = "numbers" if has_number_hi(r["hi"]) and r["type"] != "assessment_prompt" else r["type"].replace("_", " ")
        tier = "C" if r["flag"] else TIER.get(r["source"], "?")
        L.append(f"| {i} | {kind} | {r['hi']} | {r['sat']} | {reading_guide(r['sat']) or ''} | {r['source']} | {tier} |")
    L += ["", "Public benchmarks for the model alone (not these lines): chrF++ Hindi → Santali 31.3 (IN22-Gen), "
          "32.2 (IN22-Conv), 27.4 (FLORES-200), `eval/results/benchmarks.md`.", ""]
    out = ROOT / "docs" / "fln_translation_sample.md"
    out.write_text("\n".join(L), encoding="utf-8", newline="\n")
    print("\n".join(L[:14]))


if __name__ == "__main__":
    main()
