# Feature traceability matrix (28 Sep 2026)

Every feature, module, model, script, screen, offline mechanism, data pipeline, test and
benchmark in the repository, with the requirement it serves, its novelty tag and where it
appears in the decks.

- **Req**: R1 translation + audio, R2 voice to voice ≤ 3 s, R3 worksheets / flashcards / NIPUN,
  R4 offline on low-cost Android, R5 deliverables.
- **Novelty** (audit Phase 4): N1 teacher-in-the-loop, N2 Devanagari reading guide, N3 tiers and
  review flags, N4 cultural context, N5 lesson plans, N6 progress per competency, N7 community
  corpus, N8 low-resource strategy.
- **Status**: done, preview (works, labelled Preview), partial, planned.
- **Decks**: F = finale deck `deck/final_deck.pptx` (F1–F14 core, A1–A7 appendix);
  S = idea-submission deck `docs/deck/Nijbhasha_SIH26042_8-bitPool.pptx` (S1–S6, 6-slide SIH limit).

## Translation and speech (R1)

| Feature | Path | Req | Novelty | Status | Deck |
|---|---|---|---|---|---|
| Hindi ↔ Santali translation, IndicTrans2 320M direct (no English pivot) | `pipeline.py` (`translate`), `nmt_onnx.py` | R1 | N8 | done | F4, F5, S3 |
| Four translation layers: teacher correction → sentence glossary → cache → model | `pipeline.py`, `education_glossary.py`, `database.py` | R1 | N1, N8 | done | F5, S3 |
| FLN glossary: verified sentences, number words, word lists (flashcards only) | `education_glossary.py` | R1, R3 | N8 | done | F5, A6 |
| Ol Chiki ↔ Devanagari / Latin transliterator (125 reference cases) | `translit/olchiki.py`, `tests/test_olchiki.py` | R1 | N2 | done | F5 |
| Offline Santali speech: Hindi Piper voice reading the transliteration (proxy, disclosed) | `pipeline.py` (`santali_tts`) | R1 | — | done | F5, A5, S3 |
| Voice selection by pre-set rule (Parler, own fine-tuned voice both lost) | `docs/voice_rule_finale.md`, `bench/voice_rule_finale_eval.py`, `notebooks/santali_voice.ipynb` | R1 | N8 | done | F10, A3 |
| **Devanagari reading guide** on every Santali reply (hub and tablet) | `reading_guide.py`, `app.py`, `core/Api.kt`, `frontend.html` | R1 | N2 | done (tablet: build pending) | F5, F9, S3 |
| **A/B/C tiers** on the source badge | `frontend.html` (`TIER`, `badge`) | R1 | N3 | done | F5, F10 |
| Loop guard (int8), length cap | `nmt_guard.py`, `core/NmtGuard.kt` | R1 | N3 | done | F10 |
| Round-trip caution flag (weak signal: precision 0.464, recall 0.449) | `pipeline.py` (`_roundtrip`), `eval/roundtrip_flag.py` | R1 | N3 | done | F10, A2 |
| **Script guard** (non-Ol Chiki letters flagged) | `nmt_guard.py` (`foreign_letters`), `pipeline.py`, `core/Api.kt` | R1 | N3 | done (tablet: build pending) | F10 |
| Nearest verified sentence offered for a flagged line | `education_glossary.py` (`nearest_verified`) | R1 | N3 | done | F10 |
| Mundari translation (our LoRA adapters, int8 ONNX, hub) | `mundari_nmt.py`, `notebooks/mundari_lora.ipynb`, `/preview/translate` | R1 | N8 | preview | F9, F12, S4 |
| Mundari and Ho voices (MMS, Odia script) | `mms_tts.py`, `translit/odia.py`, `/preview/speak` | R1 | — | preview | F9, S3 |
| Language registry (engine, licence, maturity per stage) | `languages.json`, `languages.py`, `/languages` | R1, R5 | — | done | A1 |
| Nukta escape clean-up (output) | `textnorm.fix_nukta_escape` | R1 | — | done; input side open | A5 |
| FLN sample report over real hub output | `tools/fln_sample_report.py`, `docs/fln_translation_sample.md` | R1 | N3 | done | F5, A6 |
| Public translation benchmarks (IN22-Gen, IN22-Conv, FLORES) | `eval/eval_benchmarks.py`, `eval/results/benchmarks.md` | R1 | — | done | F5, A2, S4 |
| Leakage guard (no test sentence in training) | `eval/leakage.py`, `eval/test_set_hashes.json` | R1 | N8 | done | A3, S4 |

## Voice to voice (R2)

| Feature | Path | Req | Novelty | Status | Deck |
|---|---|---|---|---|---|
| Hub voice pipeline: ffmpeg → IndicConformer 600M (Hindi CTC, Santali RNN-T) → translation → Piper | `app.py` (`/translate/audio`), `pipeline.py`, `indicconformer_asr.py` | R2 | — | done | F6, S3 |
| Clause streaming for 18+ words (NDJSON) | `streaming.py`, `/translate/audio_stream` | R2 | — | done | F6, S3 |
| Silence endpoint (VAD) in the page, off by default | `frontend.html` (`startVad`), `bench/endpoint_sim.py` | R2 | — | done | A2 |
| Browser-measured latency timer and server stage bars | `frontend.html` (`timing`), `/metrics/*` | R2 | — | done | F6, F14 |
| On-device speech: IndicConformer 120M int8 via sherpa-onnx, one language at a time | `engine/SherpaSpeech.kt`, `tools/export/` | R2, R4 | — | done | F6, F8, S3 |
| Lesson-line matching on the tablet (never guesses) | `lesson_match.py`, `core/LessonMatch.kt` | R2 | N3 | done | F6, F10, S2 |
| Latency benchmarks (hub runs, tablet 50 lines) | `bench/bench_latency.py`, `bench/latency_steps.py`, `tools/android/voice_bench.py` | R2 | — | done | F6, A2, S4 |
| p50 / p90 / p95 from the saved runs | `tools/latency_percentiles.py`, `bench/results/latency_percentiles.md` | R2 | — | done | F6, A2 |
| Tablet browser through the hub over Wi-Fi (3 tries) | `tools/hub_mic_check.py`, `…_hub_mic.md` | R2 | — | done (small sample) | A2 |
| Free-form speech → speech on 2 GB (13.48 s, kept on the hub) | `…_nmt_memfix.md` | R2, R4 | — | measured; off on tablet | F8, A5 |

## Teaching content (R3)

| Feature | Path | Req | Novelty | Status | Deck |
|---|---|---|---|---|---|
| 18 NIPUN lessons (5 built in, 13 team-written), Balvatika–Grade 3 | `lesson_engine.py`, `content/team_lessons.json` | R3 | — | done | F7, S3, S5 |
| NIPUN Lakshya text (verbatim) and IDs | `nipun/lakshya.py`, `docs/lakshya_mapping.md` | R3 | — | done | F7, S3 |
| Worksheet v2 (5 exercise types, numerals, answer key) | `worksheet_v2.py`, `docs/samples/` | R3 | — | done | F7, S2 |
| Cut-out flashcards (mirrored backs, review mark) | `worksheet_v2.py` (`build_flashcards`), `/flashcards/pdf` | R3 | — | done | F7, S2, S6 |
| **Teacher's lesson plan PDF** with reading guide, tiers, answers | `lesson_plan.py`, `/lesson_plan` | R3 | N5, N2 | done (hub) | F7, F9 |
| Answer checking green / yellow / red, any digit script | `lesson_engine.py`, `/session/response` | R3 | — | done | F7, S3 |
| Curriculum import (paste or file → labels, Lakshya suggestion, Santali, audio) | `curriculum.py`, `/curriculum/*` | R3 | N4 | done | F9, S3 |
| **Village-context sample lesson** for import | `content/samples/` | R3 | N4 | done (sample) | F9 |
| Reading-fluency check (words correct per minute vs NIPUN goals) | `orf.py`, `/orf/*`, `content/orf_passages.json` | R3 | N6 | done (hub) | F7, F9, S2, S3 |
| Class progress per Lakshya and week (CSV / PDF, no names) | `progress.py`, `/progress/lakshya` | R3 | N6 | done | F9, S3 |
| Photo import (OCR) | `ocr.py`, `/curriculum/photo` | R3 | — | built, off, not claimed | A5 |

## Offline, tablet and sync (R4)

| Feature | Path | Req | Novelty | Status | Deck |
|---|---|---|---|---|---|
| Android app shell: WebView + NanoHTTPD on 127.0.0.1, minSdk 28 | `MainActivity.kt`, `server/LocalServer.kt` | R4 | — | done | F8, S3 |
| Shared REST contract (24 cases), hub and tablet | `contract/rest_contract.json`, `core/Api.kt`, `ContractTest.kt` | R4 | — | done | F8, A3 |
| Signed content pack (lessons, translations, audio, PDFs) | `tools/build_content_pack.py`, `pack_signing.py`, `core/Pack.kt` | R4 | — | done | F8, S3 |
| Signed model pack (361 MB int8) | `tools/android/build_model_pack.py` | R4 | — | done | F8 |
| On-device typed translation, IndicTrans2 int8 (Kotlin IndicTransToolkit + SentencePiece ports) | `core/OnnxNmt.kt`, `core/IndicProc.kt`, `core/Spm.kt` | R4, R1 | — | done | F8, S4 |
| Ed25519 verification (RFC 8032 port for Android 9) | `core/Ed25519.kt` | R4 | — | done | F8, A4 |
| Correction sync between tablets via the hub (signed exports, conflict list) | `sync.py`, `/sync/*`, `SyncTest.kt` | R4 | N1 | done | F9, S5 |
| Native 16 kHz microphone bridge with permission request | `bridge/MicBridge.kt`, `MainActivity.kt` | R4, R2 | — | done | A4 |
| Offline tests (sockets blocked), frontend loads nothing online | `tests/test_offline.py`, `tests/test_frontend_offline.py` | R4 | — | done | F8, A3, S3 |
| Old-WebView (Chrome 69) syntax guard | `tests/test_frontend_offline.py` | R4 | — | done | A3 |
| Device tools: one-pass device check, NMT bench, sync round trip | `tools/android/*.py` | R4 | — | done | A3 |
| 32-bit ARM (armeabi-v7a) build | `android/app/build.gradle.kts` | R4 | — | **planned** | F13, A5 |
| Resumable pack download | — | R4 | — | **planned** | F13, A5 |
| Real 2 GB tablet run | — | R4 | — | **planned** | F13, A5 |

## Interface, privacy, community (all)

| Feature | Path | Req | Novelty | Status | Deck |
|---|---|---|---|---|---|
| Hindi / Santali / English interface | `frontend.html` (`T`) | R1, R5 | — | done | F4, F14, S6 |
| HTTPS hub for tablet browsers (own CA) | `tools/make_cert.py`, `tests/test_https.py` | R2, R4 | — | done | A4 |
| **Community voice corpus** (adults, consent, local, export only with consent) | `corpus.py`, `/corpus/*` | R1 | N7 | done (hub) | F9, F10, A4 |
| Reading-check recording deleted after scoring; consent box | `orf.py`, `frontend.html` | R3 | — | done | F10, A4 |
| No child names in progress; no audio in reports | `progress.py` | R3 | N6 | done | F10, A4 |

## Evidence and delivery (R5)

| Feature | Path | Req | Novelty | Status | Deck |
|---|---|---|---|---|---|
| Fact-check test: every README number has an evidence file | `tests/test_claims.py`, `docs/claims.yaml` | R5 | — | done | A3 |
| Deck numbers printed from files | `tools/deck_numbers.py`, `docs/deck/SOURCES.md` | R5 | — | done | A3 |
| CI (GitHub Actions), public summary | `.github/workflows/tests.yml`, `.github/ci_summary.py` | R5 | — | done | A3, S4 |
| Test suite: 332 pass without models, 38 need models | `tests/` | R5 | — | done | A3 |
| Model download with pinned revisions and checks | `download_models.py`, `model_manifest.json`, `verify_models.py` | R5 | — | done | A1 |
| Licences (MIT code, GPL APK, model / voice / data licences) | `LICENSE`, `THIRD_PARTY_LICENSES.md` | R5 | — | done | A1 |
| Demo video script v3, reset tool | `docs/demo_video_script.md`, `tools/demo_reset.py` | R5 | — | done; video **planned** | F14 |
| Audit, deck audit, narrative | `docs/audit_2026-09-28.md`, `docs/deck_audit.md`, `docs/winning_narrative.md` | R5 | — | done | A7 |
| Unused training scaffold (33 pairs, no accuracy figure uses it) | `train_nmt.py`, `generate_dataset.py`, `training_data/` | — | — | not used | not shown |

Every row maps to a finale-deck slide, except the unused training scaffold (deliberately not shown).
