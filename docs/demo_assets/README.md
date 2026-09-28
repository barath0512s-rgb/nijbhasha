# Demo video assets

Recorded with `adb screenrecord` (`tools/android/device_check.py --record ...`) or the tablet's own
screen recorder. Each clip is shown with its caption exactly as written here; the numbers are in
`STATUS.md` with their evidence files. v2 of this file: `_archive/demo_assets_README_v2.md`.

| File | Caption (exact) | Evidence |
|---|---|---|
| `android_realme.mp4` (to be recorded by the team, without USB) | Realme Pad Mini, 4 GB RAM, Android 11, airplane mode: 24 of 24 app checks pass offline; lessons and typed translation on the tablet. | `bench/results/realme-pad-mini-4gb-android11_2026-09-27_m1.md` |
| `android_emulator.mp4` (backup only) | Android 9 emulator, 2 GB RAM, airplane mode: the same app; 24 of 24 app checks pass offline. | `bench/results/emulator-2gb-android9_2026-09-26_m1.md` |

Lines that may be shown under a tablet clip (never mix the two devices in one line):
- "On a 2 GB RAM, Android 9 emulator: spoken lesson lines p50 0.50 s, p90 0.82 s." (`bench/results/emulator-2gb-android9_2026-09-26_voice.md`)
- "On the Realme Pad Mini: typed translation 1.5 s per sentence (median, 200 test sentences)." (`bench/results/realme-pad-mini-4gb-android11_2026-09-27_nmt.md`)
