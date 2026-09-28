"""p50 / p90 / p95 from the saved latency runs (no models, no re-run).

    python tools/latency_percentiles.py        # writes bench/results/latency_percentiles.md

The published figures are p50 and p90; this adds p95 and the per-stage medians,
computed from the same saved rows with the same selections and the same
percentile method each benchmark already uses:
  laptop hub, from the end of speech   bench/latency_steps.py runs hp1-hp3 (public FLEURS
                                       Hindi -> Santali, distinct sentences, <= 17 words),
                                       nearest-rank percentiles (tools/latency_runs.pct)
  laptop hub, upload to reply audio    bench/bench_latency.py runs hp1-hp3 (warm, distinct)
  tablet, spoken lesson lines          tools/android/voice_bench.py JSON (matched lines with
                                       audio), interpolated percentiles (voice_bench.pctl)
The hub rows pool the three runs (each sentence once per run), so they are not the
"median of the three runs' p90s" headline; both are shown.
"""

import csv
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
RESULTS = ROOT / "bench" / "results"
RUNS = ("hp1", "hp2", "hp3")


def pct(v, p):
    """Nearest rank, as tools/latency_runs.pct."""
    v = sorted(v)
    return v[max(0, min(len(v) - 1, -(-len(v) * p // 100) - 1))]


def pctl(xs, q):
    """Linear interpolation, as tools/android/voice_bench.pctl."""
    xs = sorted(xs)
    k = (len(xs) - 1) * q
    f = int(k)
    return xs[f] + (xs[min(f + 1, len(xs) - 1)] - xs[f]) * (k - f)


def hub_end_of_speech():
    from bench.latency_steps import distinct_first, read_rows
    per_run, pooled = {}, []
    for tag in RUNS:
        d = [r for r in distinct_first(read_rows(f"app_{tag}")) if r["set"] == "public" and r["words"] <= 17]
        per_run[tag] = d
        pooled += d
    return per_run, pooled


def hub_upload():
    from textnorm import normalize_key
    per_run = {}
    for tag in RUNS:
        f = sorted(RESULTS.glob(f"*_public_{tag}.csv"))[-1]
        rows = [r for r in csv.DictReader(f.open(encoding="utf-8")) if r["cold"] == "False"]
        seen, dist = set(), []
        for r in rows:
            k = (r["direction"], normalize_key(r["reference"]))
            if k not in seen:
                seen.add(k); dist.append(r)
        per_run[tag] = dist
    return per_run


def tablet(name):
    d = json.loads((RESULTS / name).read_text(encoding="utf-8"))
    return [r["ms"] for r in d["rows"] if r["lang"] == "hi" and r["correct"] and r["audio"]]


def s(ms):
    return f"{ms / 1000:.2f}"


def main():
    L = ["# Latency percentiles (p50 / p90 / p95) from the saved runs", "",
         "Made by `tools/latency_percentiles.py` from saved rows only; nothing re-run. "
         "Sources and methods are in the script's docstring. Offline in every case.", ""]

    per_run, pooled = hub_end_of_speech()
    L += ["## Laptop hub, Hindi → Santali, from the end of speech, sentences of ≤ 17 words (FLEURS, public adult speech)", "",
          "| Run | n (distinct) | p50 full | p90 full | p95 full | p95 first audio |", "|---|---|---|---|---|---|"]
    for tag, d in per_run.items():
        full = [r["full_ms"] for r in d]; first = [r["first_audio_ms"] for r in d]
        L.append(f"| {tag} | {len(d)} | {s(pct(full, 50))} s | {s(pct(full, 90))} s | {s(pct(full, 95))} s | {s(pct(first, 95))} s |")
    full = [r["full_ms"] for r in pooled]
    L += [f"| pooled | {len(pooled)} | {s(pct(full, 50))} s | {s(pct(full, 90))} s | {s(pct(full, 95))} s | "
          f"{s(pct([r['first_audio_ms'] for r in pooled], 95))} s |", "",
          f"Over 3 s (pooled): {sum(x > 3000 for x in full)} of {len(full)}. "
          "Headline in README and STATUS: median of the three runs' p90s = 2.85 s.", "",
          "Per stage, pooled median (ms): speech recognition "
          f"{statistics.median(r['asr_ms'] for r in pooled):.0f}, translation {statistics.median(r['nmt_ms'] for r in pooled):.0f}, "
          f"speech {statistics.median(r['tts_ms'] for r in pooled):.0f}; full {statistics.median(full):.0f}.", ""]

    up = hub_upload()
    L += ["## Laptop hub, upload to reply audio (whole request, warm, distinct sentences)", "",
          "| Direction | Run | n | p50 | p90 | p95 | over 3 s |", "|---|---|---|---|---|---|---|"]
    for d in ("hi-to-sat", "sat-to-hi"):
        for tag, rows in up.items():
            v = [float(r["pipeline_ms"]) for r in rows if r["direction"] == d]
            L.append(f"| {d} | {tag} | {len(v)} | {s(pct(v, 50))} s | {s(pct(v, 90))} s | {s(pct(v, 95))} s | "
                     f"{sum(x > 3000 for x in v)} |")
    L.append("")

    L += ["## Tablet, spoken lesson lines, on the device (WAV handed to the app → reply audio ready)", "",
          "| Device | n | p50 | p90 | p95 | max |", "|---|---|---|---|---|---|"]
    for label, f in (("Realme Pad Mini (4 GB, Android 11), airplane mode", "realme-pad-mini-4gb-android11_2026-09-28_voice.json"),
                     ("2 GB RAM Android 9 emulator, airplane mode", "emulator-2gb-android9_2026-09-26_voice.json")):
        v = tablet(f)
        L.append(f"| {label} | {len(v)} | {s(pctl(v, .5))} s | {s(pctl(v, .9))} s | {s(pctl(v, .95))} s | {s(max(v))} s |")
    L += ["", "The tablet maximum includes the first line of the run, which loads the models.", ""]
    out = RESULTS / "latency_percentiles.md"
    out.write_text("\n".join(L), encoding="utf-8", newline="\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
