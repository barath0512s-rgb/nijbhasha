"""The finale voice rule (docs/voice_rule_finale.md, fixed 27 Sep 2026) for the C4 Santali voice.

    python bench/voice_rule_finale_eval.py       # -> bench/results/voice_rule_finale.md / .json

Candidates: Piper (the live voice: the content pack's own audio, Piper hi_IN-pratham
reading the Ol Chiki transliteration) and Ours (the C4 fine-tuned MMS voice,
models/santali-voice-c4/, from notebooks/santali_voice.ipynb, run through onnxruntime).
Parler and the hybrid are not re-scored here.

Data, as the rule fixes it: the newest content pack's Santali lines; held-out = SHA-1 of
the line's text is odd; only the held-out half is scored, once. Nothing is chosen on the
selection half (no hybrid guard is evaluated).
Measures, as the rule fixes them: ASR round-trip CER with the hub's Santali recogniser
(IndicConformer 600M, the app's settings) after normalize_for_wer with spaces removed
(bench/voice_compare.py's cer), mean and median; failure rate = CER above 0.5.
MOS-lite: no native listener scores exist (NOT MEASURED), so that condition does not apply.
Decision: Ours replaces Piper only if mean CER is lower by at least 0.02, the median is
not higher and the failure rate is not higher.

Also reported (not part of the rule): the same measures on the 20 held-out recordings'
texts from the voice's training data (never used in training), with Piper synthesised
through the app's own Santali path. One synthesis per line; the VITS noise is seeded
(onnxruntime.set_seed) so the run can be repeated.
"""

import glob
import hashlib
import io
import json
import statistics
import sys
import tempfile
import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "bench"))

import config  # noqa: E402
from voice_compare import cer  # noqa: E402

OURS = config.MODELS_DIR / "santali-voice-c4"
HELD20 = ROOT / "dist" / "santali_voice" / "v1" / "santali_voice_onnx" / "samples" / "texts.json"
OUT = ROOT / "bench" / "results" / "voice_rule_finale"
SEED = 20260928


def held_out(text):
    return int(hashlib.sha1(text.encode("utf-8")).hexdigest(), 16) % 2 == 1


def summary(rows):
    c = [r["cer600"] for r in rows if r["cer600"] is not None]
    return {"n": len(c), "cer600_mean": round(statistics.mean(c), 4), "cer600_median": round(statistics.median(c), 4),
            "failure_rate": round(sum(x > 0.5 for x in c) / len(c), 4), "failures": sum(x > 0.5 for x in c),
            "audio_seconds": round(sum(r["seconds"] for r in rows), 1)}


def decide(piper, ours):
    checks = {"mean lower by >= 0.02": ours["cer600_mean"] <= piper["cer600_mean"] - 0.02,
              "median not higher": ours["cer600_median"] <= piper["cer600_median"],
              "failure rate not higher": ours["failure_rate"] <= piper["failure_rate"],
              "MOS-lite clear not lower": "n/a (no native listener scores)"}
    ship = all(v is True for v in checks.values() if not isinstance(v, str))
    return checks, ship


def main():
    import numpy as np
    import onnxruntime as ort
    import soundfile as sf
    import mms_tts
    import pipeline
    ort.set_seed(SEED)
    ours = mms_tts.MmsVoice("sat", threads=4, model_dir=OURS)
    pl = pipeline.VaaniSetuPipeline()
    tmp = Path(tempfile.mkdtemp())
    from translit.odia import olchiki_to_odia

    def ours_synth(text):
        """The C4 voice on a Santali line: Ol Chiki -> Odia with olchiki_to_odia, as in its training
        (mms_tts.to_model_script would send a line without Ol Chiki letters, e.g. "3425", down the
        Devanagari path). None if nothing is sayable: scored as a failure (CER 1.0)."""
        ids = ours.ids(olchiki_to_odia(text))
        if len(ids) <= 1:
            return None
        return ours.sess.run(None, {"input_ids": np.array([ids], dtype=np.int64)})[0][0].astype(np.float32),             ours.meta["sample_rate"]

    def score_ours(text):
        out = ours_synth(text)
        if out is None:
            return {"line": text, "voice": "ours", "seconds": 0.0, "asr600": "", "cer600": cer(text, "") or 1.0,
                    "unsayable": True}
        return score(text, "ours", *out)

    def score(text, voice, wav, sr):
        f = tmp / f"{voice}.wav"
        sf.write(str(f), wav, sr)
        heard = pl.transcribe_santali(str(f))
        return {"line": text, "voice": voice, "seconds": round(len(wav) / sr, 2), "asr600": heard, "cer600": cer(text, heard)}

    pack = sorted(glob.glob(str(ROOT / "dist" / "packs" / "content-pack-*.zip")))[-1]
    z = zipfile.ZipFile(pack)
    index = json.loads(z.read("audio/index.json"))["sat"]
    lines = sorted(index)
    held = [t for t in lines if held_out(t)]
    rows_pack, t0 = [], time.time()
    for i, text in enumerate(held):
        x, sr = sf.read(io.BytesIO(z.read(f"audio/{index[text]}")), dtype="float32")
        rows_pack.append(score(text, "piper", x.mean(axis=1) if x.ndim > 1 else x, sr))
        rows_pack.append(score_ours(text))
        if i % 20 == 0:
            print(f"pack {i}/{len(held)} {time.time() - t0:.0f} s", flush=True)

    rows_20 = []
    for item in json.loads(HELD20.read_text(encoding="utf-8")):
        text = item["olchiki"]
        p = tmp / "piper20.wav"
        info = {}
        pl.santali_tts(text, out_path=str(p), info=info)
        assert info.get("tts_engine") in ("piper", "cache"), info       # the offline Piper voice, never gTTS
        x, sr = sf.read(str(p), dtype="float32")
        rows_20.append(score(text, "piper", x, sr))
        rows_20.append(score_ours(text))

    S = {name: {v: summary([r for r in rows if r["voice"] == v]) for v in ("piper", "ours")}
         for name, rows in (("pack_heldout", rows_pack), ("heldout_clips_20", rows_20))}
    checks, ship = decide(S["pack_heldout"]["piper"], S["pack_heldout"]["ours"])
    checks20, ship20 = decide(S["heldout_clips_20"]["piper"], S["heldout_clips_20"]["ours"])
    res = {"rule": "docs/voice_rule_finale.md", "pack": Path(pack).name, "pack_lines": len(lines),
           "pack_heldout_lines": len(held), "seed": SEED, "run_time_s": round(time.time() - t0, 1),
           "summary": S, "decision_checks": checks, "decision": "ship Ours (replaces Piper)" if ship else "keep Piper",
           "heldout_clips_20_checks": {**checks20, "would_pass": ship20},
           "rows": {"pack_heldout": rows_pack, "heldout_clips_20": rows_20}}
    OUT.with_suffix(".json").write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    P, O = S["pack_heldout"]["piper"], S["pack_heldout"]["ours"]
    p20, o20 = S["heldout_clips_20"]["piper"], S["heldout_clips_20"]["ours"]
    L = ["# Finale voice rule: C4 Santali voice vs Piper (ASR round-trip CER)", "",
         f"- Rule: `docs/voice_rule_finale.md` (fixed 27 Sep 2026, before any finale data). Pack `{res['pack']}`: "
         f"{len(lines)} Santali lines; held-out half (SHA-1 of the text odd): **{len(held)} lines**, scored once.",
         "- Ours: the C4 voice (`notebooks/santali_voice.ipynb`, Kaggle; one IndicVoices-R Santali speaker, 0.6 h) as fp32 "
         "ONNX via onnxruntime, Ol Chiki -> Odia script; Piper: the pack's own audio. Recogniser: IndicConformer 600M (hub). "
         "CER after `normalize_for_wer`, spaces removed. **A proxy for intelligibility; native listener ratings: NOT MEASURED.**",
         f"- One synthesis per line, VITS noise seeded ({SEED}).", "",
         "| Held-out pack lines | Piper | Ours |", "|---|---|---|",
         f"| CER mean | {P['cer600_mean']:.3f} | {O['cer600_mean']:.3f} |",
         f"| CER median | {P['cer600_median']:.3f} | {O['cer600_median']:.3f} |",
         f"| Failure rate (CER > 0.5) | {P['failure_rate']:.3f} ({P['failures']} of {P['n']}) | {O['failure_rate']:.3f} ({O['failures']} of {O['n']}) |",
         f"| Audio | {P['audio_seconds']} s | {O['audio_seconds']} s |", "",
         "Conditions: " + "; ".join(f"{k}: {v}" for k, v in checks.items()), "",
         f"**Decision (by the rule): {res['decision']}.**", "",
         "Not part of the rule: the 20 held-out recordings' texts (never used in training), Piper synthesised by the app:",
         f"Piper CER mean {p20['cer600_mean']:.3f}, median {p20['cer600_median']:.3f}, failures {p20['failures']} of {p20['n']}; "
         f"Ours mean {o20['cer600_mean']:.3f}, median {o20['cer600_median']:.3f}, failures {o20['failures']} of {o20['n']} "
         f"(the rule's conditions on this set: {'all hold' if ship20 else 'not all hold'}).",
         f"- Run time {res['run_time_s']} s."]
    OUT.with_suffix(".md").write_text("\n".join(L) + "\n", encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
