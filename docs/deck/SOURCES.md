# Deck sources (`Nijbhasha_SIH26042_8-bitPool.pptx`, 28 Sep 2026)

The idea-submission deck (6 slides, the SIH template), updated to the submission freeze.
Every number on it, and where it comes from. The PDF is a LibreOffice export for
preview; export the PDF for upload from PowerPoint.

| Slide | On the slide | Source |
|---|---|---|
| 4 | **0.70 s** median voice to voice on the tablet, spoken lesson lines, p90 1.20 s (n = 50), Realme Pad Mini (4 GB, Android 11), airplane mode | `bench/results/realme-pad-mini-4gb-android11_2026-09-28_voice.md`; STATUS clause 3 |
| 4 | **2.85 s** p90, free Hindi speech of ≤ 17 words → Santali audio, laptop hub, from the end of speech (median of three runs' p90s) | `bench/results/latency_hp_runs.md`; README §6 |
| 4 | 2 GB Android 9 emulator: spoken lesson lines p50 0.50 s (p90 0.82 s); typed new sentences p50 0.60 s; 24 / 24 in airplane mode | `bench/results/emulator-2gb-android9_2026-09-26_voice.md`, `…_nmt.md`, `bench/results/emulator-2gb-android9_2026-09-26_m1.md`; STATUS clauses 3, 5 |
| 4 | Realme Pad Mini: typed new sentences p50 1.50 s | `bench/results/realme-pad-mini-4gb-android11_2026-09-27_nmt.md` |
| 4 | Santali → Hindi p90 2.58 s, laptop hub, all 80 answers (upload to reply audio; IndicVoices validation split) | `bench/results/latency_hp_runs.md`; README §2 row 3 |
| 4 | 300+ automated tests in CI (311 pass without model weights) | `.github/workflows/tests.yml`; `pytest -q` |
| 2, 3 | Reading-fluency check (words correct per minute vs NIPUN goals, laptop hub); teacher lesson import; class progress by Lakshya; clause streaming for 18+ word sentences | STATUS C1, A8; README §3, §6 |
| 4 | **32.2 chrF++** Hindi → Santali, IN22-Conv, n = 1,503 | `eval/results/benchmarks.md` |
| 4 | **24 / 24** app checks in airplane mode, Realme and 2 GB emulator | `bench/results/realme-pad-mini-4gb-android11-rc2_2026-09-28_m1.md`, `bench/results/emulator-2gb-android9_2026-09-26_m1.md` |
| 4 | chrF++ 31.3 / 32.2 / 27.4 (IN22-Gen, IN22-Conv, FLORES-200) | `eval/results/benchmarks.md` |
| 4 | Mundari preview, held-out chrF++ 30.92 (hi→unr; held-out 5 % of the MMLoSo 2025 training file, n = 1,021, not reviewed by a native speaker) | `eval/results/mundari_hub_int8.json`; STATUS C3 |
| 4 | Singh, Ekbal & Pakray, MMLoSo 2025: fine-tuned IndicTrans2 beats ByT5 for English↔Santali (Ol Chiki) | https://aclanthology.org/2025.mmloso-1.9/ (English↔Santali, not Hindi↔Santali) |
| 3, 4, 5 | 18 lessons (5 built in, 13 by the team), every NIPUN Lakshya has a lesson | README §2 row 4, §7 |
| 3 | 600M ASR on the hub, 120M int8 on the tablet; IndicTrans2 int8 on the tablet; Piper voice | README §4, `languages.json` |
| 5 | 1,041 PALASH schools in 8 of Jharkhand's 24 districts | JEPC State Project Director to PTI, Jan 2026 (reported by Careers360 and Awaz The Voice). PALASH's figures, not ours |
| 5 | 5,000+ tribal-area primary schools | the SIH26042 problem statement |
| 2, 6 | Adi Vaani (Ministry of Tribal Affairs, launched 1 Sep 2025; Santali, Mundari, Bhili, Gondi) | https://adivaani.tribal.gov.in/ ; PIB |
| 6 | Screenshots: the current `frontend.html` (English view) with lessons, translations and flashcards from the Android test content pack; the classroom shot shows a model translation ("Model" badge) | `android/app/src/test/resources/pack/` |

What the deck does **not** claim: a real 2 GB tablet, free-form speech on the tablet, native
review of any Santali or Mundari output, children's speech, or tablet output identical to the
laptop's (see the do-not-say list in `docs/demo_video_script.md`).

| 2 | "Never guesses": unmatched spoken lines refused on the tablet; doubtful model output flagged | STATUS A1 (matcher), A3 (round-trip flag) |
| 3, 4 | Our training: Mundari LoRA adapters; Santali voice fine-tuned on one IndicVoices-R speaker and scored by the rule fixed on 27 Sep (Piper stays) | STATUS C3, C4; `docs/voice_rule_finale.md` |

Still to fill: the demo video link on slide 6 (placeholder "[add link after recording]").
