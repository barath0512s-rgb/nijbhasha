# Deck audit (28 Sep 2026)

Decks found: two drafts supplied by the team (`VaaniSetu_SIH26042_8-bitPool_v3.pptx`,
`…_revised.pptx`, 6 slides each, the SIH idea template; not in git) and the updated
idea-submission deck `docs/deck/Nijbhasha_SIH26042_8-bitPool.pptx` (6 slides). No Google
Slides, Keynote or markdown outline in the repository. The finale deck
`deck/final_deck.pptx` was built from scratch on 28 Sep (14 core + 7 appendix slides).

SIH limit: the idea submission is **at most 6 slides including the title** and must use the
template, so the 6-slide deck is the submission and the 14-slide deck is for the
presentation round.

## Claims in the drafts, and what the evidence says

| Draft slide | Claim | Verdict | Now |
|---|---|---|---|
| 2, 3 | "VaaniSetu" | Renamed 26 Sep to Nijbhasha (another team's name) | Nijbhasha everywhere, infographics repainted |
| 2 | "offline, on-device AI pipeline (Android tablet)" | Partly: lesson lines and typed sentences on the tablet; free speech on the laptop hub | "offline AI on an Android tablet or a school laptop" |
| 2 infographic | "On-device on 2 GB-RAM Android 9+ tablets" | Not measured on a real 2 GB tablet | "Android 9+ tablet app, or a laptop hub" |
| 3 | "Android tablet app (Android 9+, ≤2 GB RAM): full pipeline on-device" | False (free speech 13.48 s on 2 GB, so off on the tablet; no real 2 GB device) | Rewritten with what runs, "tested on a 4 GB tablet and a 2 GB Android 9 emulator" |
| 3 | "ASR: IndicConformer 600M, ONNX/RNN-T" | Half: hub uses Hindi CTC + Santali RNN-T; tablet uses 120M int8 | "600M on the hub, 120M int8 on the tablet" |
| 3 | "TTS: 0.15 s per line (was 30 s)" | Never measured | Removed |
| 3 | "Santali (own script)" / "own voice" | The voice is a Hindi voice reading a transliteration | "Piper voice reads Santali via our Ol Chiki transliterator" |
| 4 | "All 3 core AI models … on-device … Nothing left to build" | False for free speech; overclaim | Replaced with measured on-device figures |
| 4 | "Real data already in use: curated NIPUN corpus, AI4Bharat BPCC" | False (33-pair corpus unused; BPCC is IndicTrans2's training data) | Replaced with the public benchmarks |
| 4 | "full ASR→NMT→TTS pipeline runs end-to-end offline on a ≤2 GB Android 9+ tablet" | False as stated | Removed |
| 4 (v3) | Metric tiles "[x.x] s", "[xxx] MB", "[xx.x] chrF++", "[n] lessons checked by native Santali-speaking teachers" | Placeholders; the last one would be false (no native review) | 0.70 s, 2.85 s, 32.2 chrF++, 24 / 24 |
| 4 | "100% on-device … designed around the DPDP Act 2023" | No compliance review | "No cloud; no child names; reading-check audio deleted" |
| 4 | "Hindi & Santali interface (English view for evaluators)" | Outdated: English is a normal third option | "Hindi, Santali and English interface" |
| 5 | "≤2 GB RAM, Android 9+ tablet — whole app runs offline" tile | Not measured on a real 2 GB tablet | Replaced by "18 lessons, every NIPUN Lakshya" |
| 5 | "1,041 PALASH schools", "8 of 24 districts" | True for PALASH (JEPC to PTI, Jan 2026); not our reach | Attributed "(JEPC, Jan 2026)" |
| 5 | "Rs. 0 recurring cost — MIT" | Voice is CC BY-NC-SA; APK GPL | "No licence or cloud fees" |
| 6 (revised) | Mozilla Common Voice, SOAS as references | Not used by the project | Dropped (v3's IndicConformer / Adi Vaani links kept) |
| 6 | Screenshots with "VaaniSetu" and "Model confidence 100%" | Outdated UI; the app shows no confidence number | Current screenshots (English view, "Model" badge) |
| 6 | Demo video and GitHub "[paste link]" | Placeholders | GitHub filled; video marked "[add link after recording]" |

Missing from the drafts (now in the decks): the 2 GB emulator results, typed translation on
the tablet, Santali → Hindi latency, curriculum import, reading-fluency check, progress by
Lakshya, signed packs and correction sync, the review flags, the Mundari preview, the
reading guide, lesson plans, the community corpus.

## Checks on the finished decks

| Check | Submission deck (6) | Finale deck (21) |
|---|---|---|
| Every requirement R1–R5 has a proof slide | S2–S5 | F5 (R1), F6 (R2), F7 (R3), F8 (R4), F14 + A3 (R5) |
| Every number sourced | `docs/deck/SOURCES.md` | a source line on every slide with a number |
| No placeholder except the demo video link | yes | yes |
| Limitations disclosed | S4 risks, SOURCES "does not claim" | F10, A5 |
| Text fits, validated | `validate.py` PASS, rendered | `validate.py` PASS, rendered |
| Screenshots current | 28 Sep | 28 Sep |

## Final checklist (28 Sep 2026)

| Check | Status |
|---|---|
| R1 has a proof slide | ✅ F5 (+ A6 real lines), S3 |
| R2 has a proof slide | ✅ F6 (p50/p90/p95 chart, stage medians, the tail over 3 s disclosed), S4 |
| R3 has a proof slide | ✅ F7 (real worksheet, flashcards, lesson plan; Lakshya shown), S2, S6 |
| R4 has a proof slide | ✅ F8 (airplane mode 24/24, sizes, memory vs 2 GB, gaps disclosed), S3, S4 |
| R5 has a proof slide | ✅ F14 (repo QR; video link placeholder), A3 (tests, CI) |
| Every feature in the deck | ✅ `docs/feature_traceability.md` maps every row to a slide (the unused 33-pair training scaffold deliberately not shown) |
| Every number sourced | ✅ source line on each finale slide; `docs/deck/SOURCES.md` for the submission deck |
| Every limitation disclosed | ✅ F8, F10, A5; submission S4 risks |
| No invented statistics, testimonials or native-speaker validation | ✅ none; PALASH figures attributed to JEPC; pilot marked "proposed, not agreed" |
| Branding and team name unchanged | ✅ Nijbhasha, Team 8-bitPool (VITV), ID 168531 |
| Still open | ⬜ demo video link (both decks); export the upload PDFs from PowerPoint |
