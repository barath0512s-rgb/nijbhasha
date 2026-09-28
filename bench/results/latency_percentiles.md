# Latency percentiles (p50 / p90 / p95) from the saved runs

Made by `tools/latency_percentiles.py` from saved rows only; nothing re-run. Sources and methods are in the script's docstring. Offline in every case.

## Laptop hub, Hindi → Santali, from the end of speech, sentences of ≤ 17 words (FLEURS, public adult speech)

| Run | n (distinct) | p50 full | p90 full | p95 full | p95 first audio |
|---|---|---|---|---|---|
| hp1 | 32 | 2.28 s | 2.96 s | 4.08 s | 3.02 s |
| hp2 | 32 | 1.99 s | 2.85 s | 3.26 s | 2.53 s |
| hp3 | 32 | 1.88 s | 2.75 s | 3.13 s | 2.50 s |
| pooled | 96 | 2.04 s | 2.90 s | 3.29 s | 2.59 s |

Over 3 s (pooled): 8 of 96. Headline in README and STATUS: median of the three runs' p90s = 2.85 s.

Per stage, pooled median (ms): speech recognition 861, translation 846, speech 360; full 2042.

## Laptop hub, upload to reply audio (whole request, warm, distinct sentences)

| Direction | Run | n | p50 | p90 | p95 | over 3 s |
|---|---|---|---|---|---|---|
| hi-to-sat | hp1 | 68 | 2.27 s | 2.93 s | 3.24 s | 6 |
| hi-to-sat | hp2 | 68 | 2.03 s | 2.38 s | 2.47 s | 1 |
| hi-to-sat | hp3 | 68 | 2.02 s | 2.37 s | 2.56 s | 0 |
| sat-to-hi | hp1 | 80 | 2.21 s | 2.60 s | 2.70 s | 2 |
| sat-to-hi | hp2 | 80 | 2.16 s | 2.52 s | 2.67 s | 1 |
| sat-to-hi | hp3 | 80 | 2.16 s | 2.58 s | 2.70 s | 1 |

## Tablet, spoken lesson lines, on the device (WAV handed to the app → reply audio ready)

| Device | n | p50 | p90 | p95 | max |
|---|---|---|---|---|---|
| Realme Pad Mini (4 GB, Android 11), airplane mode | 50 | 0.70 s | 1.20 s | 1.27 s | 4.34 s |
| 2 GB RAM Android 9 emulator, airplane mode | 50 | 0.50 s | 0.82 s | 0.93 s | 3.24 s |

The tablet maximum includes the first line of the run, which loads the models.
