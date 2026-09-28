# Nijbhasha (निजभाषा)

*Formerly VaaniSetu (renamed on 26 Sep 2026 to avoid confusion with another team's project).*

[![tests](https://github.com/barath0512s-rgb/nijbhasha/actions/workflows/tests.yml/badge.svg)](https://github.com/barath0512s-rgb/nijbhasha/actions/workflows/tests.yml)

**An offline Hindi ↔ Santali teaching assistant for Grade 1–3 classrooms in Jharkhand.**
The teacher speaks or types Hindi. The child hears Santali and can answer in
Santali. The teacher hears Hindi.

| | |
|---|---|
| Event | Smart India Hackathon 2026 |
| Problem statement | SIH26042, *AI-Powered Vernacular Pedagogy and Real-Time Translation Tool for Mother Tongue-Based Primary Education* (Government of Jharkhand) |
| Theme / category | Smart Education / Software |
| Languages | Hindi (Devanagari) ↔ Santali (Ol Chiki) |
| Runs today on | (1) A laptop (the "laptop hub"), CPU only, no internet; a tablet or phone on the same Wi-Fi can use it through its browser. (2) **The Android app** (`android/`, build 0.95, tag `v0.95-submission`), in airplane mode, from signed content and model packs: measured on a **Realme Pad Mini (4 GB, Android 11)** and a **2 GB RAM, Android 9 emulator** |
| Interface languages | हिंदी, ᱥᱟᱱᱛᱟᱲᱤ (Santali) and English, one button each, on the hub and the tablet |
| Current state | `STATUS.md`, the two tables at its top (submission freeze, 28 Sep 2026). Where this README and those tables differ, the tables win |

### At a glance (for evaluators)

| | Measured, offline |
|---|---|
| Voice to voice on the tablet, spoken lesson lines | Realme Pad Mini (4 GB, Android 11): **p50 0.70 s, p90 1.20 s** (n = 50); 2 GB Android 9 emulator: p50 0.50 s, p90 0.82 s |
| Voice to voice on the laptop hub, free speech | Hindi → Santali, ≤ 17 words, from the end of speech: **p90 2.85 s**; Santali → Hindi: p90 2.58 s |
| Typed new sentences translated on the tablet | Realme Pad Mini p50 1.50 s; 2 GB emulator p50 0.60 s |
| Airplane mode on the tablet | **24 of 24** contract cases (Realme Pad Mini and the 2 GB emulator) |
| Translation quality, Hindi → Santali (public test sets) | chrF++ 31.3 (IN22-Gen), **32.2 (IN22-Conv)**, 27.4 (FLORES-200) |
| Mundari (our LoRA adapters, preview) | held-out chrF++ hi→unr 30.92, unr→hi 35.97 (MMLoSo 2025 data; not comparable with the Santali test sets) |

What sets it apart:
- **Offline end to end, on the tablet itself**: speech recognition, translation and speech in airplane mode, from signed content and model packs (Ed25519; a changed pack is refused).
- **The whole lesson, not just translation**: 18 NIPUN-tagged lessons, answer checking, bilingual worksheets and flashcards, a reading-fluency check against the NIPUN words-per-minute goals, class progress by Lakshya, and lessons a teacher adds from Hindi text.
- **Never guesses**: a spoken line that matches no lesson line is refused; a doubtful model translation is flagged "⚠️ मूल वक्ता से जाँचें" and not played automatically; teacher corrections are reused first and sync between tablets.
- **Every number is checkable**: each figure has a script and a results file (`python tools/deck_numbers.py`), choices were made by rules fixed before the results, and a leakage guard keeps test sentences out of training. What is not measured says **NOT MEASURED**.

Full audit against the problem statement (R1–R5, bugs, novelty, scorecard): `docs/audit_2026-09-28.md`. Every feature and where it is shown: `docs/feature_traceability.md`.

Verify in five minutes: `pip install -r requirements-ci.txt && pytest -q` (no models needed), then read `STATUS.md` (two tables at the top) and `docs/deck/SOURCES.md`.

The product name is set in one place, `APP_NAME` in `config.py`.

**Every number in this README comes from a script in this repository.** Run
`python tools/deck_numbers.py` to print them with their source files. Anything
without a script behind it is marked **NOT MEASURED**.

---

## 1. The problem

The JEPC Language Mapping Survey, Phase 1, was carried out by the Jharkhand
Education Project Council with JCERT. Its data was collected in January and
February 2024
([report](https://languageandlearningfoundation.org/wp-content/uploads/2025/04/LM-Report-Jharkhand-Phase-1.pdf);
page numbers below are the report's printed page numbers).

- Coverage: 7 districts, 72 blocks, **8,244 schools**, **1,06,930 Grade 1 students** (p. 13).
- *"In the surveyed districts, Hindi serves as the Medium of Instruction (MoI) in approximately 98% of schools."* (p. 18)
- Home languages of Grade 1 students include **Ho 17.03%, Santali 13.07%, Mundari 7.32%** (Table 1, p. 17).
- *"Approximately 80% of schools in the surveyed districts of Jharkhand, falling under Type II, III, and IV categories, pose moderate to severe learning disadvantages for students"* (p. 6).
- On children's Hindi, the report gives two figures. The executive summary says: *"The survey found that 36.1% of students have minimal proficiency, 41.2% have functional proficiency, and only 22.7% have good proficiency in Hindi."* (p. 6). The findings section says the minimal-proficiency segment is *"around 51.2% of students, indicating that a sizeable portion of the student population possesses a very less or no understanding of Hindi."* (p. 18). We quote both, because the report does.

So a child who cannot answer "दो और तीन कितने होते हैं?" may not be failing at
addition. They may not understand the Hindi question.

---

## 2. What the ministry asks for, and what runs today

The problem statement's clauses, one row each. "Runs today" means on the
laptop, offline, and checked by the named test or script.

| # | Requirement | Runs today (laptop, offline) | Not done yet | How to check |
|---|---|---|---|---|
| 1 | Hindi-speaking teachers teach in the mother tongue (Ho, Mundari, Santali) with no language training | **Santali:** Hindi ↔ Santali, typed or spoken, with Santali speech (hub); on the tablet for lesson lines and typed sentences. **Mundari: translation preview** on the laptop hub (IndicTrans2 + our Hindi–Mundari LoRA adapters, trained on the MMLoSo 2025 data; held-out 5% of the MMLoSo 2025 training file, n=1,021 pairs: hi→unr chrF++ 30.92, unr→hi 35.97; not comparable with the Santali test sets), labelled Preview | Ho and Mundari: no speech recognition. Mundari and Ho **voices are Preview**, laptop hub only (Meta MMS, CC BY-NC 4.0; pronunciation not reviewed). Ho: no translation (no licensed Ho text found). Mundari output: not reviewed by a native speaker; not on the tablet | `python test_pipeline.py`, `pytest tests/test_mundari_preview.py` |
| 2 | Translate Hindi FLN content (lesson scripts, activity instructions, assessment prompts) into accurate text and synthesised audio | Every lesson line is translated to Ol Chiki text and spoken offline. 18 lesson sentences come from a hand-written glossary; other lines come from the model. A model translation whose back-translation drifts is marked "⚠️ मूल वक्ता से जाँचें" and not played automatically (typed lines and content packs; a weak signal: `eval/results/roundtrip_flag.md`) | Translation quality on public test sets (the model alone): chrF++ Hindi → Santali 31.3 (IN22-Gen), 32.2 (IN22-Conv), 27.4 (FLORES-200); see §6. Lesson lines themselves: **NOT MEASURED** (no reference translations). No native speaker has reviewed the output or the Santali voice. Content modes organise the lesson but **do not change the translation** (see §5) | `pytest tests/test_api.py`, `tests/test_offline.py` |
| 3 | Real-time voice-to-voice dialogue, no more than 3 s | Laptop, offline, public adult speech, three runs (AC, Best performance mode, apps closed; median of the runs' p90s, distinct sentences, definitions in §6). **Headline, sentences of ≤ 17 words, from the end of speech: full time p90 2.85 s** (32 sentences), first audio p90 2.41 s; upload to reply audio, Hindi → Santali, p90 2.14 s (34 sentences). Santali → Hindi, all 80 answers: **p90 2.58 s**; answers of ≤ 10 words 2.27 s (IndicVoices validation split; may overlap model-development data). Neither figure includes the 500 ms silence endpoint, which is off by default | Longer sentences: 18-23 words take p90 2.47 s (upload) to 4.76 s (end of speech; why the two differ is explained, not yet measured in class, §6) to finish; over all sentences, first audio p90 was 2.54, 2.75 and **3.40 s** in the three runs. Bins under 10 sentences are small samples. **On the tablet, no laptop, spoken lesson lines:** Realme Pad Mini (4 GB, Android 11) p50 0.70 s, p90 1.20 s (n = 50); 2 GB emulator p50 0.50 s, p90 0.82 s. Free-form speech on a 2 GB tablet: p50 13.48 s, so it stays on the laptop hub. Child speech, classroom Wi-Fi, a real 2 GB tablet: **NOT MEASURED** | `python bench/latency_steps.py --backend app --tag hp1` and `python bench/bench_latency.py --clips bench/clips/public/manifest.json --label public_hp1` (three times), then `python tools/latency_runs.py` |
| 4 | Auto-generated bilingual worksheets and visual flashcard sets, aligned to NIPUN Bharat learning outcomes | Worksheet v2 for every lesson: student exercises with pictures (count and write, match picture to word, fill in the blank, circle the answer, trace the numeral), Ol Chiki / Devanagari / Western numerals, the Lakshya IDs and a teacher answer key; cut-out flashcard PDFs with a review-pending mark (samples: `docs/samples/`). Flashcard decks (`GET /flashcards`). A reading-fluency check (words correct per minute against the NIPUN goals, teacher override). A teacher can add a lesson from Hindi text (§3). The tablet serves the pre-rendered PDFs from its content pack | 18 lessons (Balvatika to Grade 3, literacy and numeracy): 5 built in, 13 written by the team; every Lakshya has a lesson. Reading fluency on adult read speech: 5.9 % of correct words marked wrongly (`bench/results/orf_validation.md`); **children: NOT MEASURED**. The lesson-to-goal mapping has not been checked by a teacher. The tablet does not draw PDFs itself | `pytest tests/test_lakshya.py tests/test_curriculum.py` |
| 5 | Whole application offline on low-cost tablets (**2 GB RAM, Android 9+**) after initial content synchronisation | Fully offline **on the laptop hub** (tablets use its browser page over local Wi-Fi). **Android app** (Android 9 emulator, 2 GB RAM, airplane mode): lessons, flashcards, worksheets from a signed content pack (24 of 24 contract cases); **on-device voice for lesson lines**: speech recognition and speech on the tablet, a spoken lesson line matched to its pre-translated Santali (voice to voice p50 0.50 s, p90 0.82 s, to the reply audio file); **typed new sentences translated on the tablet** (same output as the laptop on 1502 of 1503 test sentences, p50 0.60 s); corrections synced to the hub by signed files | Free-form speech → speech on 2 GB: works but p50 13.48 s (models swapped), so it is **off**; translating needs about 1.2 GB (peak app PSS 1197 MB), above the 900 MB guideline. Lesson-line matching and spoken answers with real teachers' and children's voices: **NOT MEASURED**. A real 2 GB tablet: **NOT MEASURED**. **Realme Pad Mini (4 GB, Android 11), airplane mode:** 24 of 24 contract cases, peak PSS 294 MB; spoken lesson lines p50 0.70 s, p90 1.20 s (n = 50); typed translation p50 1.50 s, chrF++ 29.00 (laptop 28.75), not identical to the laptop's output on this ARM64 device (65 of 80 golden sentences) (`bench/results/realme-pad-mini-4gb-android11_2026-09-28_voice.md`, `…_2026-09-27_nmt.md`) | `bench/results/emulator-2gb-android9_2026-09-26_voice.md`, `…_nmt.md`, `…_nmt_memfix.md`; `pytest tests/test_offline.py` |
| 6 | A working application, a demo video and a GitHub repository | The laptop hub, the Android app (`android/`) and this repository | Demo video: script and captions ready (`docs/demo_video_script.md`); link added here once recorded | |

### Languages and how far each stage is (from `languages.json`)

Maturity: **production** = in the app and measured; **preview** = works, labelled Preview in the app, quality not measured; **phrasebook** = verified fixed sentences only; not available.

<!-- languages:start -->
| Language | Speech recognition | Translation | Speech |
|---|---|---|---|
| Hindi (हिंदी) | **production**: IndicConformer 600M multilingual (hub); 120M CTC int8 via sherpa-onnx (tablet) (MIT) | **production**: IndicTrans2 indic-indic-dist-320M (hub); on the tablet: pack lines, and int8 for typed new sentences (MIT) | **production**: Piper hi_IN-pratham-medium (CC BY-NC-SA 4.0) |
| Santali (ᱥᱟᱱᱛᱟᱲᱤ) | **production**: IndicConformer 600M multilingual (hub); 120M transducer int8 via sherpa-onnx (tablet) (MIT) | **production**: IndicTrans2 indic-indic-dist-320M (hub); on the tablet: pack lines, and int8 for typed new sentences (MIT) | **production**: Piper hi_IN-pratham-medium reading an Ol Chiki transliteration (pending native review) (CC BY-NC-SA 4.0) |
| Mundari (मुंडारी) | not available | **preview**: IndicTrans2 + Hindi–Mundari LoRA (notebooks/mundari_lora.ipynb, Kaggle v6), int8 ONNX, laptop hub only (MUNDARI_NMT_PREVIEW) (MIT (model); data CC BY-SA 4.0) | **preview**: facebook/mms-tts-unr (reads Odia script; Devanagari converted); samples from the MMLoSo test split only (CC BY-NC 4.0) |
| Ho (हो) | not available | not available | **preview**: facebook/mms-tts-hoc (reads Odia script; Devanagari converted; Warang Citi not supported yet). Ho voice model available; content pending a native speaker (CC BY-NC 4.0) |
<!-- languages:end -->

---

## 3. What it does

1. **Two-way classroom dialogue.** Hindi → Santali and Santali → Hindi, typed or spoken, with speech in both directions.
2. **NIPUN Bharat lessons.** 18 lessons from Balvatika to Grade 3, in literacy and numeracy. Five are built in (counting, shapes, addition, reading words, subtraction). Thirteen were written by the team in simple Hindi (`content/team_lessons.json`). The server adds them on its first start, through the same import path a teacher uses (below). Each lesson is a sequence of steps: the line to say, a teaching note, and for questions, the accepted answers.
2a. **Add a lesson (curriculum import).** The teacher pastes Hindi lesson text, or uploads a `.txt`, `.csv` or `.json` file (`grade, topic, line`). The app:
    - splits it into sentences;
    - labels each line as a lesson script, activity or question (the teacher taps a label to change it);
    - suggests NIPUN goals from the grade and keywords, which the teacher must confirm.

    It then makes the Santali and the audio for every line, a flashcard deck and a worksheet, and stores the lesson. Every Santali line is marked as awaiting native review.
3. **NIPUN Lakshya tags.** Every lesson names the NIPUN goals it works towards, e.g. `NIPUN-G1-NUM-2`: *"Perform simple addition and subtraction"*. See `docs/lakshya_mapping.md`.
4. **Answer checking.** After a question, the child's answer (Hindi or Santali, typed or spoken, any digit script: 7, ७, ᱗) is marked green, yellow or red.
5. **Session summary.** Steps done, lines translated, green/yellow/red counts.
6. **Bilingual worksheet (PDF)** of the lesson just taught, with its Lakshya tags.
7. **Flashcards** made from the numbers and nouns in each lesson. Each card says where its Santali came from: the word list, a teacher's correction, or the model. Anything no native speaker has checked carries a "review pending" badge. So does every answer check whose accepted answers are unreviewed.
8. **Teacher corrections are reused.** A 👎 opens a correction box. The correction is stored and used, before the model, every time that line comes up again, in either direction.
9. **Where each translation came from.** A badge on each translation shows its source: verified glossary, teacher correction, cached, or model. No confidence number is shown, because the model's score does not tell good output from bad (`eval/model_score_sanity.py`).
10. **Voice-to-voice timer.** The browser measures from the end of the teacher's input to the reply starting to play, and shows it.
11. **Offline.** No internet at any point after setup.
12. **Reading guide for the teacher.** Under every Santali reply, the same Santali in Devanagari (the transliteration the voice speaks), so a Hindi-medium teacher can read it aloud (`reading_guide.py`; hub, and the tablet from the next build).
13. **Trust tiers.** The source badge carries a tier: **A** written by people (the glossary or a teacher's correction; native review still pending), **B** model output with no warning, **C** model output in doubt. Tier C comes from three guards: a loop guard, the round-trip check, and a **script guard** that flags Santali containing letters of another script (it found 13 of 119 lesson lines in the content pack with Urdu, Meetei Mayek, Odia or Latin letters, 6 of them not flagged before; `docs/fln_translation_sample.md`). Tier C is not played automatically.
14. **Teacher's lesson plan (PDF).** Every line in Hindi, Ol Chiki and the reading guide, with the tier, the accepted answers and the Lakshya text (`lesson_plan.py`, `GET /lesson_plan`, the 🗒️ button in Flashcards; samples in `docs/samples/`). Laptop hub.
15. **Community voice corpus.** An adult community member reads a line in Santali, Mundari or Ho; refused without the adult's consent; no names; stays on the laptop (`corpus/`); exported only from the laptop and only with consent to share (`corpus.py`, Settings → आवाज़ संग्रह).
16. **Local-context lessons.** `content/samples/local_context_lesson.csv`: a Grade 1 counting lesson with village examples (sal leaves, mahua, goats, the haat) for a teacher to import; the app makes the Santali, marked for native review.

---

## 4. How it works

```
 Browser (frontend.html, one file, no build step)        Tablet browser on the same Wi-Fi
 Classroom · Lessons · Flashcards · Progress · Settings   (optional; https, see §9)
                 │   HTTP / JSON                                  │
                 ▼                                                ▼
 ┌─────────────────────────── laptop hub: app.py (Flask) ──────────────────────────┐
 │ pipeline.py                                                                     │
 │   voice ─ ffmpeg 16 kHz ─► ASR  IndicConformer 600M (ONNX, CTC)                  │
 │                             │                                                   │
 │   text ────────────────────►├─► 1. teacher correction   (SQLite)                │
 │                             ├─► 2. sentence glossary    (education_glossary.py) │
 │                             ├─► 3. earlier translation  (memory cache)          │
 │                             └─► 4. NMT  IndicTrans2 indic-indic 320M, greedy    │
 │                                          │  direct Hindi ↔ Santali, no English  │
 │                                          ▼                                      │
 │                             TTS  Piper, offline                                 │
 │                               Santali: Ol Chiki → Devanagari → Hindi voice      │
 │                               Hindi:   read directly                            │
 └─────────────────────────────────────────────────────────────────────────────────┘
   SQLite: corrections, sessions, latency log   ·   lesson_engine.py   ·   worksheet.py (PDF)
```

A translation is answered by the first layer that can answer it, in the order
shown. The model runs only when the other three cannot answer.

### Laptop hub and tablet: two set-ups

- **Laptop hub = higher accuracy.** The laptop runs the larger models: IndicConformer
  600M for speech and IndicTrans2 in full precision (fp32), identical to the
  published model.
- **Tablet = portable.** The Android app (`android/`: Kotlin, WebView on the
  same `frontend.html`, a local server on 127.0.0.1) runs smaller engines:
  IndicConformer **120M** int8 per language (Hindi and Santali) through
  sherpa-onnx, IndicTrans2 **int8** on ONNX Runtime with a length cap and a
  repetition guard (`nmt_guard.py`), and the Piper voice. Measured on the
  laptop: 120M Hindi WER 10.9% (600M: 12.5%), 120M Santali 34.5% (600M: 31.0%);
  int8 IN22-Conv chrF++ 32.0 / 35.0 vs fp32 32.2 / 35.1. Content and models
  arrive as **signed packs** (Ed25519; a changed or unsigned pack is refused).
  Spoken **lesson lines** are recognised and matched to their pre-translated
  Santali on the tablet; typed new sentences are translated on the tablet;
  free-form speech stays on the laptop hub (on 2 GB it swaps models: p50 13.48 s).

### Speech recognition: IndicConformer 600M
- `ai4bharat/indic-conformer-600m-multilingual`, ONNX Runtime on the CPU. It reads Santali (`sat`) in Ol Chiki natively.
- Decoding per language, from public speech (§6): Hindi **CTC**, Santali **RNN-T**. Silence trimming: Hindi off, Santali on.
- There is no fallback. If the model files are missing, the server stops and says how to get them.

### Translation: IndicTrans2 indic-indic 320M
- `ai4bharat/indictrans2-indic-indic-dist-320M`, **direct** Hindi ↔ Santali. Going through English would lose distinctions English does not make, such as respectful आप versus familiar तुम.
- Greedy decoding (`NMT_NUM_BEAMS = 1`), `no_repeat_ngram_size = 3`, and an output-length cap sized to the input.
- Runs on **ONNX Runtime** (fp32, 6 threads) when the exported model is on disk (`tools/export/export_indictrans2_onnx.py`); otherwise on PyTorch. The ONNX output is token-for-token identical to PyTorch on every sentence tested (`bench/results/golden_nmt_fp32.md`).
- The model sometimes starts its output with a label such as `ᱥᱮᱪᱮᱫ:` ("Teaching:"); that prefix is removed.
- At start-up, a background thread translates every lesson line and flashcard word once, so the lesson answers from the cache.

### Speech synthesis: Piper
- No offline voice reads Ol Chiki. `translit/olchiki.py` rewrites Santali in Devanagari, so the offline Hindi voice `hi_IN-pratham-medium` can speak it. For example, `ᱛᱮᱦᱮᱸᱡ ᱟᱞᱮ` becomes `तेहेँच् आले`.
- The transliterator is a parser, not a lookup table. It covers the whole Ol Chiki block, including digits (spoken as Santali number words), punctuation and every diacritic. Its core is cross-checked against the independent Aksharamukha transliterator, and 125 reference cases are tested. Its phonetic choices still need native review.
- If a clip cannot be made offline, the translation is still shown. The reply carries `audio_url: null` and a `tts_error`. The screen says so in Hindi, and the failure is logged. Silence is never played.
- gTTS (online) is off: it is used only if `config.ALLOW_ONLINE_TTS = True`.

---

## 5. Content modes

Every lesson step is typed as **lesson script**, **activity instruction** or
**assessment prompt**, as the problem statement names them. The modes organise
the lesson: they set the step's label, its teaching note, and whether an answer
is expected. **They do not change the translation.** The same Hindi line gets
the same Santali in every mode. Only the cache key includes the mode.

---

## 6. Measured performance (laptop, offline)

Laptop: Dell G15 5520, Intel Core i7-12700H, 15.7 GB RAM, Windows, CPU only.
Every figure is from `bench/`. See `bench/README.md` to re-run.

### Voice to voice, synthetic clips

60 clips of Piper reading classroom lines. **This is not real speech.** Each
clip is sent to `/translate/audio` exactly as the browser sends it. The time
runs from upload start to the reply audio being received. The app runs
in-process, so Wi-Fi is not included. Warm requests, empty caches.
Source: `bench/results/Dell-Inc-Dell-G15-5520_2026-09-24_synthetic-after.csv`.

| Direction | n | Median | p90 | Max |
|---|---|---|---|---|
| Hindi → Santali | 29 | 1.51 s | 1.68 s | 2.08 s |
| Santali → Hindi | 30 | 1.57 s | 1.85 s | 2.25 s |

- Requests over 3 s: **0 of 59**.
- Server start with all models loaded: **20.4 s**.
- The same benchmark before the latency work: median 2.19 s and 2.20 s, 1 request over 3 s (`…_synthetic-baseline.md`). Single runs vary; the next table isolates each change.

### What each change did

| Change | Measured effect | Decision | Source |
|---|---|---|---|
| CTC instead of RNN-T decoding | ASR about 2× faster (Hindi 693 vs 1521 ms), CER no worse | CTC for both languages | `asr_decoding_synthetic.md` |
| Trim silence at both ends | With CTC, 115 ms (Hindi) and 156 ms (Santali) less median ASR time; CER better for Hindi, slightly worse for Santali | On for Hindi only | `asr_decoding_synthetic.md` |
| Warm the ASR up at start | The first request costs nothing extra (−105 ms, within noise) | Not added | `cold_start.md` |
| Size the NMT output limit to the input | No time saved, no output changed | Kept as a safety cap | `nmt_limits.md` |
| Play the first sentence early | At most 86 ms (median), on 22 of 60 replies | Not built | `tts_first_sentence.md` |
| Match glossary sentences ignoring punctuation | Spoken lesson lines answered by the glossary: 0 → 11 of 59 | Done | the two benchmark files |

### What the teacher sees

The timer's big number is measured **in the browser**: from releasing the
microphone (or pressing Translate) to the reply starting to play. The bars
under it are the server's ASR, NMT and TTS times. Every request is logged, and
`GET /metrics/latency` returns count, median, p90 and max per path.

### Public speech (adult), both directions

80 Hindi clips from `google/fleurs` (**test** split, CC BY 4.0, 3-10 s) and 80
Santali clips from `ai4bharat/IndicVoices` (**IndicVoices validation split (no
public Santali test split)**; CC BY 4.0, 62 speakers, Ol Chiki transcripts),
both seeded. The model cards do not say how that split was used, so the Santali
numbers **may overlap model-development data** (`docs/sources.md#indicvoices`).
None of these clips, sentences or speakers can be used for fine-tuning
(`eval/leakage.py`). **Public dataset, adult speech; child speech NOT MEASURED.**
Laptop, offline. `bench/fetch_public_clips.py` fetches the same clips for
anyone with access.

**n** = clips, **n_distinct** = distinct sentences. FLEURS has several readers
per sentence (80 clips, 69 sentences): WER uses all 80 clips (different
speakers); translation and latency use the first clip of each sentence.

Speech recognition (`bench/results/asr_decoding_public.md`; corpus-level).
**Raw** WER compares the texts exactly as written; **normalised** WER and CER
remove punctuation (including ᱾ and ।) and digit-script differences, the same
way for both languages, after removing dataset tags (`<unintelligible>`: 2 in
the Santali references) from the **references only** (rules: `bench/README.md`).

| Language | Decoding | Silence trimmed | n | n_distinct | WER raw | WER normalised | CER normalised | Median time |
|---|---|---|---|---|---|---|---|---|
| Hindi | **CTC (in use)** | **no (in use)** | 80 | 69 | 13.6% | 12.5% | 4.8% | 516 ms |
| Hindi | CTC | yes | 80 | 69 | 14.3% | 13.1% | 4.9% | 485 ms |
| Hindi | RNN-T | yes | 80 | 69 | 14.3% | 13.1% | 4.9% | 1314 ms |
| Santali | **RNN-T (in use)** | **yes (in use)** | 80 | 80 | 31.1% | 31.0% | 10.3% | 1144 ms |
| Santali | RNN-T | no | 80 | 80 | 31.3% | 31.2% | 10.4% | 1281 ms |
| Santali | CTC | yes | 80 | 80 | 34.7% | 34.7% | 11.6% | 386 ms |

Voice to voice, upload to reply audio, in-process (no Wi-Fi), warm requests:

| Direction | n | n_distinct | Median | p90 | Max | Over 3 s | Source |
|---|---|---|---|---|---|---|---|
| Hindi → Santali | 79 | 68 | 1.96 s | 2.25 s | 2.74 s | 0 | `…_2026-09-25_public.csv` |
| Santali → Hindi (RNN-T, trimmed: in use) | 79 | 79 | 2.22 s | 2.57 s | 3.15 s | 2 | `…_public_sat_rnnt_trim.csv` |
| Santali → Hindi (CTC, trimmed) | 79 | 79 | 1.69 s | 2.01 s | 3.85 s | 1 | `…_public_sat_ctc_trim.csv` |
| Hindi → Santali, before Phase L | 79 | 68 | 2.99 s | 3.72 s | 5.68 s | 34 | `…_public_before_phase_l.csv` |

Santali → Hindi by answer length (Santali words), median / p90 (IndicVoices
validation split; may overlap model-development data):

| Answer length | n | n_distinct | RNN-T (in use) | CTC |
|---|---|---|---|---|
| ≤ 10 words | 41 | 41 | 1.98 / **2.34 s** (1 over 3 s) | 1.58 / 1.77 s (0 over) |
| ≤ 5 words | 10 | 10 | 1.82 / 1.99 s | 1.34 / 1.54 s |
| 6-10 words | 31 | 31 | 2.04 / 2.34 s | 1.60 / 1.77 s |
| 11-17 words | 25 | 25 | 2.26 / 2.56 s | 1.73 / 2.01 s |
| 18+ words | 13 | 13 | 2.50 / 2.76 s | 1.90 / 2.21 s |

Santali uses RNN-T because the rule was: RNN-T if its p90 for answers of up to
10 words stays within 3 s (2.34 s). The trade-off: about 0.4-0.6 s more per
reply for 3.7 fewer word errors per 100 words. Silence trimming is on for
Santali too: normalised WER 31.0% vs 31.2% without, 137 ms faster.
Hindi stays on CTC, and Hindi silence trimming is **off**: on this data it was
0.6 WER points worse (13.1% vs 12.5%) for 31 ms.

### Translation quality (public test sets)

The model alone (no glossary, cache or teacher corrections), as the app runs it
(ONNX Runtime fp32, greedy). chrF++ and BLEU with sacrebleu
(`eval/eval_benchmarks.py`, `eval/results/benchmarks.md`). These sets are for
evaluation only; `eval/leakage.py` stops any training script that sees them.

| Test set | Licence | n | n_distinct (hi / sat sources) | Hindi → Santali chrF++ / BLEU | Santali → Hindi chrF++ / BLEU | Paper chrF++ (all-source avg, → sat / sat →) |
|---|---|---|---|---|---|---|
| IN22-Gen | CC BY 4.0 | 1024 | 1024 / 1024 | 31.3 / 4.2 | 37.6 / 15.8 | 30.0 / 35.8 |
| IN22-Conv | CC BY 4.0 | 1503 | 1497 / 1500 | 32.2 / 5.5 | 35.1 / 15.3 | 30.4 / 33.8 |
| FLORES-200 devtest | CC BY-SA 4.0 | 1012 | 1012 / 1012 | 27.4 / 3.3 | 34.1 / 12.6 | 26.1 / 31.5 |

Scores use every pair, as published results do. On distinct sources only
(IN22-Conv repeats a few short lines) every score is the same to one decimal
(`eval/results/benchmarks.md`).

For comparison only: the IndicTrans2 paper reports this model's chrF++
**averaged over all Indic languages** into / out of Santali (FLORES 26.1 / 31.5,
IN22-Gen 30.0 / 35.8, IN22-Conv 30.4 / 33.8). That is not the Hindi pair itself,
so it shows the scores are plausible, not better. Compare chrF++, not BLEU: the
paper tokenises Indic text differently.

### Speed on realistic speech (Phase L)

Two measures, both timed **from the end of speech**: from the moment the
recorded audio reaches the speech recogniser. Upload and audio decoding are not
included (laptop, in-process), and neither is endpointing (below).

- **Full time**: until the Santali audio for the **whole** utterance is ready.
  This is what a reply costs when the sentence is translated in one piece.
- **Time to first audio**: with **clause streaming** (`streaming.py`), a long
  utterance is cut at sentence ends and clause words (लेकिन, क्योंकि, और, कि…,
  never inside a phrase, at most 10 words per chunk). The first chunk is
  translated and spoken while the rest are still being prepared, and time to
  first audio runs until that first chunk's audio is ready. **Time to last
  audio** runs until the last chunk's audio is ready; the listener hears it
  after the chunks before it have played.

The app translates utterances of up to 17 words whole, and streams only longer
ones (`config.STREAM_MIN_WORDS`), because chunking changes the wording: the
chunked translation agrees with the whole-sentence one at chrF++ 69 (median).
Against human references it costs little: on the 814 FLORES-200 devtest
sentences of 18+ words, chunked chrF++ 27.3 vs whole 27.5 (BLEU 2.3 vs 3.4);
chunking scores higher on 387 of them (`eval/results/chunk_quality.md`).

**Current reference: three runs** (26 Sep 2026; laptop on AC power, Windows Best performance mode, other apps closed; Hindi silence trimming off). Every run is shown; the bold column is the median of the three runs' p90s (`bench/results/latency_hp_runs.md`). Headline: the **≤ 17-word** row.

**Definitions.** Neither measure includes the endpointing wait: the silence endpoint (500 ms, 1000 ms after 2.5 s of speech) is a setting, off by default; with it on, add at least that wait. Neither includes Wi-Fi or the browser starting playback.
- **From the end of speech** (`bench/latency_steps.py`, Hindi -> Santali): starts when the recorded audio, already a WAV file, is handed to speech recognition in the same process. **Full time** stops when the Santali audio for the whole utterance is written (not streamed). **Time to first audio** stops when the first clause chunk's audio is written (streamed; computed for every clip, although the app streams only utterances of 18+ words). **Time to last audio**: the last chunk's audio. For each clip the benchmark runs the whole path and then the streamed path, and goes straight on to the next clip.
- **Upload to reply audio** (`bench/bench_latency.py`, both directions): starts when the request with the audio file is sent to the app in the same process (Flask test client, no network); includes saving the upload, re-encoding it with ffmpeg, speech recognition, the translation layers (teacher, glossary, cache, model), synthesis and downloading the reply audio; stops when the reply audio is received. Whole utterance, not streamed. One request after another.
- **Why the end-of-speech full time has the longer tail (p90 3.67 vs 2.38 s, medians 2.11 vs 2.03 s in run 3): an explanation, partly supported, not a result.** The medians agree; the tail comes from speech recognition. In the end-of-speech runs the same six clips were slow every time (ASR median 2.02 s, full 4.17 s); each follows a clip with about twice the usual streaming work (3.5 vs 1.9 s), run just before with no pause. Re-run after a 1 s idle pause (`bench/results/pause_check.md`), the six clips took ASR 1.16 s, full 3.13 s (median): the preceding work explains about half the extra time, not all of it (alone, with only the ASR model loaded, ASR took 0.76 s). So the upload figure may be closer to a line spoken after a pause, but that is not measured in class.
- **Streaming threshold:** on the saved runs, streaming brings the first sound forward by a median 0.25-0.29 s for 12-17 words but delays the last audio by 0.65-0.70 s; for 18+ words it gains 0.48-0.60 s. The app streams only 18+ words (`config.STREAM_MIN_WORDS = 18`); the data support it.
- Rows with fewer than 10 distinct sentences are marked **small sample**. The headline is the **<= 17-word** row.

#### From the end of speech: FLEURS Hindi -> Santali (`bench/latency_steps.py --backend app`)

Time to first audio (clause streaming) and full time (whole utterance voiced), p90 in seconds.

| Words | n | n_distinct | hp1: first / full | hp2: first / full | hp3: first / full | Median of p90s: first / full |
|---|---|---|---|---|---|---|
| all | 80 | 69 | 3.40 / 4.08 | 2.75 / 3.62 | 2.54 / 3.67 | **2.75 / 3.67** |
| ≤ 17 | 37 | 32 | 2.41 / 2.96 | 2.42 / 2.85 | 2.14 / 2.75 | **2.41 / 2.85** |
| 0-11 (small sample) | 3 | 3 | 2.23 / 3.29 | 2.47 / 3.21 | 2.13 / 2.90 | **2.23 / 3.21** |
| 12-17 | 34 | 29 | 2.59 / 2.96 | 2.42 / 2.85 | 2.21 / 2.75 | **2.42 / 2.85** |
| 18-23 | 34 | 28 | 3.74 / 4.93 | 3.25 / 4.19 | 3.40 / 4.76 | **3.40 / 4.76** |
| 24+ (small sample) | 9 | 9 | 3.71 / 4.33 | 3.40 / 4.09 | 3.10 / 3.68 | **3.40 / 4.09** |

Source files: `latency_steps_app_hp1.csv`, `latency_steps_app_hp2.csv`, `latency_steps_app_hp3.csv`

#### Upload to reply audio, both directions (`bench/bench_latency.py`, public clips)

Full time (no streaming in this path), p90 in seconds. Santali clips: IndicVoices validation split (no public Santali test split); may overlap model-development data. Word bins count the reference words of the spoken sentence.

| Direction | Words | n | n_distinct | hp1 | hp2 | hp3 | Median of p90s |
|---|---|---|---|---|---|---|---|
| hi-to-sat | all | 79 | 68 | 2.93 | 2.38 | 2.37 | **2.38** |
| hi-to-sat | ≤ 17 | 40 | 34 | 2.60 | 2.14 | 2.09 | **2.14** |
| hi-to-sat | 0-11 (small sample) | 4 | 4 | 2.22 | 1.87 | 1.87 | **1.87** |
| hi-to-sat | 12-17 | 36 | 30 | 2.60 | 2.14 | 2.09 | **2.14** |
| hi-to-sat | 18-23 | 32 | 27 | 3.17 | 2.47 | 2.37 | **2.47** |
| hi-to-sat | 24+ (small sample) | 7 | 7 | 3.32 | 3.22 | 2.61 | **3.22** |
| sat-to-hi | all | 80 | 80 | 2.60 | 2.52 | 2.58 | **2.58** |
| sat-to-hi | 0-10 | 42 | 42 | 2.27 | 2.23 | 2.29 | **2.27** |
| sat-to-hi | 11-17 | 25 | 25 | 2.62 | 2.55 | 2.69 | **2.62** |
| sat-to-hi | 18+ | 13 | 13 | 2.94 | 2.80 | 2.75 | **2.80** |

Source files: `Dell-Inc-Dell-G15-5520_2026-09-26_public_hp1.csv`, `Dell-Inc-Dell-G15-5520_2026-09-26_public_hp2.csv`, `Dell-Inc-Dell-G15-5520_2026-09-26_public_hp3.csv`

The two earlier runs below (Balanced plan, Hindi trimming on) are kept for the record.

FLEURS Hindi (public dataset, adult speech; n = 80 clips, n_distinct = 69
sentences, the first clip of each counted) and the 30 lesson lines; laptop,
offline; `bench/latency_steps.py`. Run twice with the same settings (run 1:
`latency_steps_app_run1.*`; run 2: `latency_steps_app.*`).

| Measure (distinct sentences) | n / n_distinct | Before Phase L | Now, run 1 | Now, run 2 | Target |
|---|---|---|---|---|---|
| Full time, sentences of ≤ 17 words, p90 | 38 / 32 | 3.46 s | **2.48 s** | **3.02 s** | ≤ 3 s: met in run 1, missed by 20 ms in run 2 |
| Time to first audio, all sentences, median / p90 | 80 / 69 | 1.80 / 2.43 s | 1.80 / **2.46 s** | 1.66 / **2.68 s** | p90 ≤ 3 s: **met** |
| Full time, all sentences, median / p90 | 80 / 69 | 3.16 / 4.13 s | 2.26 / 3.29 s | 2.01 / 3.57 s | — |
| Full time over 3 s | 80 / 69 | 47 of 69 | 12 of 69 | 11 of 69 | — |
| Time to last audio, median / p90 | 80 / 69 | 3.42 / 5.35 s | 3.41 / 4.54 s | 3.15 / 4.52 s | — |
| Lesson lines, full time, p90 | 30 / 30 | 1.63 s | 1.24 s | 1.21 s | — |

By sentence length (words recognised), full time median / p90, and time to
first audio p90:

| Words | n / n_distinct | Before Phase L: full | first p90 | Run 1: full | first p90 | Run 2: full | first p90 |
|---|---|---|---|---|---|---|---|
| 0-11 | 3 / 3 | 2.70 / 2.86 s | 1.80 s | 2.09 / 2.30 s | 1.85 s | 1.69 / 3.02 s | 2.30 s |
| 12-17 | 35 / 29 | 2.99 / 3.74 s | 2.27 s | 1.97 / 2.84 s | 2.25 s | 1.84 / 3.02 s | 2.11 s |
| 18-23 | 33 / 28 | 3.41 / 4.15 s | 2.80 s | 2.35 / 3.39 s | 2.55 s | 2.10 / 4.97 s | 3.21 s |
| 24+ | 9 / 9 | 3.40 / 4.80 s | 2.26 s | 2.87 / 3.29 s | 2.71 s | 2.14 / 4.32 s | 3.48 s |

The slowest clips in run 2 were slow in all three steps at once (speech
recognition 1.7-2.4 s against a 0.7 s median), so the tail is the laptop, not a
step of the pipeline. The ≤ 17-word target is therefore borderline on this
laptop, not reliably met.

What changed (each measured):

| Step | Result | Decision |
|---|---|---|
| Translation on ONNX Runtime fp32 instead of PyTorch | median 504 vs 1455 ms on the FLEURS sentences; identical outputs on 99 of 99 distinct sentences (69 FLEURS + 30 lesson lines) | **Adopted** |
| Threads | More threads were slower: translation best at 6 (of 14 cores), speech recognition at 8 | NMT 6, ASR 8 |
| ONNX Runtime dynamic int8 | 244 ms; IN22-Conv chrF++ 32.0 / 35.0 vs fp32 32.2 / 35.1 (n = 1503; `eval/results/benchmarks_onnx-int8.md`). But only 42 of 99 outputs identical, some long outputs run on (24+ words: full p90 7.04 s), and time to first audio p90 is 3.07 s | Passes the quality rule; **kept for the tablet** (F1). The laptop stays on fp32, which already meets the targets |
| PyTorch dynamic int8 (Linear layers) | 1111 ms, only 15 of 99 identical | Rejected |
| CTranslate2 | Its converters do not support this model (`docs/sources.md#ctranslate2`) | Not possible |
| Endpointing: stop after 500 ms of silence | Cuts 27 of 78 read FLEURS clips early (n = 80 clips, 78 evaluated, n_distinct = 67 sentences; each recording's pauses count); 0 of 30 lesson lines. Adaptive 500/1000 ms: 16 of 78 | A **setting, off by default** (`bench/results/endpoint_sim_*.md`) |
| Word counter | Live count while typing; an estimate (≈) while speaking, from FLEURS' 2.2 words per second; past 15 words a Hindi hint to speak shorter sentences | Built |

Sources: `bench/results/latency_steps_app.md`, `latency_steps_torch-t14.md`,
`latency_steps_onnx-int8-t6.md`, `nmt_engines.md`, `golden_nmt_fp32.md`,
`golden_nmt_int8.md`, `endpoint_sim_public.md`, `endpoint_sim_synthetic.md`.

### Not measured yet

| What | Status |
|---|---|
| Real teacher and child recordings | **NOT MEASURED** (`bench/clips/real/` is empty) |
| ASR error rate on child speech and with classroom noise | **NOT MEASURED** (adult speech, both languages: see above) |
| Latency tail on the laptop hub | Free Hindi speech of up to 17 words, from the end of speech: p95 3.29 s over three runs, 8 of 96 over 3 s (`bench/results/latency_percentiles.md`). Tablet lesson lines: p95 1.27 s (Realme), 0.93 s (2 GB emulator) |
| Voice to voice from a tablet over classroom Wi-Fi | **NOT MEASURED** in a classroom. Realme Pad Mini's browser via the laptop hub over the laptop's hotspot, a spoken lesson line: 1.71, 0.97, 0.87 s (3 of 3; one speaker) |
| A real 2 GB RAM, Android 9+ tablet | **NOT MEASURED**. Measured instead on a 2 GB Android 9 emulator and a Realme Pad Mini (4 GB, Android 11): see §2 row 5 |
| Peak RAM of the laptop server | **NOT MEASURED** |

---

## 7. NIPUN Bharat alignment

Lakshya text is quoted from *NIPUN Bharat — Guidelines for Implementation*,
Ministry of Education, 2021, p. 11. The IDs are ours.

| Grade | Lesson | Lakshya IDs | Fit |
|---|---|---|---|
| 1 | Counting 1 to 10 | NIPUN-BV-NUM-1, NIPUN-G1-NUM-1 | full, partial |
| 1 | Basic Shapes | NIPUN-BV-NUM-2 | partial |
| 2 | Simple Addition | NIPUN-G1-NUM-2 | full |
| 2 | Reading Simple Words | NIPUN-BV-LIT-2, NIPUN-G2-LIT-1 | full, partial |
| 3 | Simple Subtraction | NIPUN-G1-NUM-2, NIPUN-G2-NUM-2 | full, partial |
| Balvatika | पाँच तक गिनती (counting to 5) | NIPUN-BV-NUM-1 | imported |
| Balvatika | छोटे से बड़े तक (small to big) | NIPUN-BV-NUM-2 | imported |
| Balvatika | अक्षर म (the letter म) | NIPUN-BV-LIT-1 | imported |
| Balvatika | दो अक्षर वाले शब्द (two-letter words) | NIPUN-BV-LIT-2 | imported |
| 1 | दस से बीस तक (10 to 20) | NIPUN-G1-NUM-1 | imported |
| 1 | छोटे वाक्य पढ़ना (short sentences) | NIPUN-G1-LIT-1 | imported |
| 2 | सौ से बड़ी संख्याएँ (numbers above 100) | NIPUN-G2-NUM-1 | imported |
| 2 | कहानी सुनो और समझो (listen to a story) | NIPUN-G2-LIT-1 | imported |
| 3 | गुणा: बराबर समूह (multiplication) | NIPUN-G3-NUM-2 | imported |
| 3 | पढ़कर समझना (reading for meaning) | NIPUN-G3-LIT-1 | imported |
| 3 | हज़ार तक की संख्याएँ (numbers to 9999, place value) | NIPUN-G3-NUM-1 | imported |
| 3 | ज़ोर से पढ़ना: रीना और तालाब (read-aloud fluency) | NIPUN-G3-LIT-2, NIPUN-G3-LIT-1 | imported |

Every stage from Balvatika to Grade 3 now has at least one literacy and one numeracy lesson, and every Lakshya has a lesson (G2-LIT-2, 45–60 words per minute, since 27 Sep 2026). For reading fluency (G2-LIT-2, G3-LIT-2) the app has a reading check: the child reads a passage aloud, the laptop hub recognises it (not on the tablet yet), aligns it to the passage and counts words correct per minute; the teacher can override any word. Validated on adult read speech only; children: NOT MEASURED. For the imported lessons, the goals were suggested by keyword rules and confirmed by the team. Every mapping awaits teacher review.
Details: `docs/lakshya_mapping.md`.

---

## 8. The interface

- **Three interface languages: हिंदी (default), ᱥᱟᱱᱛᱟᱲᱤ and English**, one button each in the header, on the laptop hub and in the Android app (`config.UI_ENGLISH`; a test checks every interface string has all three). In English, numbers use Western digits and the 13 team lessons show English titles; lesson lines and translations stay Hindi and Santali.
- The Santali interface text was written without a native speaker, so treat it as a first draft.
- Five views: Classroom (कक्षा), Lessons (पाठ), Flashcards (चित्र पत्ते), Progress (प्रगति), Settings (सेटिंग).
- Settings are kept in the browser: interface language, autoplay, large type, spoken confirmations, and the **server address**, which points a tablet's browser at the laptop hub.
- Keyboard: Ctrl/Cmd + Enter translates, Enter submits an answer, Escape closes dialogs.

---

## 9. Setup

You need Python 3.10 or 3.11, `ffmpeg` on PATH, and room for the model files
(`model_manifest.json` pins 423 files, 3.98 GB).

```bash
python -m venv vaanisetu_env
vaanisetu_env\Scripts\activate            # Windows
source vaanisetu_env/bin/activate         # Mac/Linux
pip install -r requirements.txt
python download_models.py                  # models and voices, pinned revisions, checked against model_manifest.json
pip install -r tools/export/requirements-export.txt
python tools/export/export_indictrans2_onnx.py   # optional: faster translation (ONNX Runtime), same output
python verify_models.py                    # loads everything, checks speech is audible
python app.py                              # the first start also adds the team's lessons, so it takes longer
```

Already have the models on another checkout? Copy (or link) its `models/`
folder into the new one and run `python download_models.py --verify-only`
instead of downloading again.

Open **http://127.0.0.1:5000**. On Windows, double-click `run_nijbhasha.bat`,
or use `run_nijbhasha.bat verify` to check everything first.

### Laptop hub for tablets on the same Wi-Fi

A browser allows the microphone only on `https://` pages or on localhost. To
let a tablet's browser use the laptop:

```bash
run_nijbhasha.bat https          # or: python app.py --https
```

This makes a certificate for the laptop's current Wi-Fi addresses
(`tools/make_cert.py`, files in `certs/`, never committed). It then serves on
port 5443 and prints the address to open on the tablet, e.g.
`https://172.18.222.252:5443`. The tablet either accepts the browser's
warning once, or installs the laptop's CA certificate (`/hub-ca.crt`, served by
the plain server on port 5000). That CA can vouch only for this laptop and for
private-network addresses.

Everything still runs on the laptop; the tablet is only a screen and a
microphone. Checked on the laptop: a client that trusts only the hub's CA
connects over the Wi-Fi address (`tests/test_https.py`). Checked on a real
tablet: the Realme Pad Mini's Chrome over the laptop's hotspot, a spoken lesson
line, 3 of 3 end to end (`bench/results/realme-pad-mini-4gb-android11_2026-09-27_hub_mic.md`).

---

## 10. Tests

```bash
pip install -r requirements-dev.txt
pytest -q                  # tests that need the models are skipped without them
                           # (GitHub Actions runs this without models: .github/workflows/tests.yml)
python test_pipeline.py    # 7 end-to-end component checks
python verify_models.py    # the pre-flight check; writes verify_report.txt
```

The pytest suite covers:
- transliteration (125 cases);
- text normalisation and correction reuse;
- separate audio for concurrent requests;
- offline operation (network sockets blocked before the models load);
- the frontend loading nothing from the internet;
- the API's routes and responses;
- sessions surviving a restart;
- latency logging;
- speech-failure handling;
- Lakshya tags;
- worksheets and flashcards;
- the HTTPS certificate;
- curriculum import (splitting, labels, goal suggestions, uploads, and the addendum's acceptance test: a 10-line lesson with typed steps, Lakshya IDs, audio, a worksheet and at least 5 flashcards);
- overlapping translations finishing (a hang, fixed).

---

## 11. API

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | The UI (`frontend.html`) |
| GET | `/config` | Product name, for the UI |
| GET | `/health` | Liveness and device |
| GET | `/health/models` | Per language: which ASR, NMT and TTS engine loaded, its files and size, and `online_dependencies` |
| GET | `/lessons` | All lessons with their steps and Lakshya tags |
| GET | `/flashcards?grade=&topic=` | Flashcard decks from the lessons, each card with its source and review status |
| POST | `/translate/text` | Translate typed text (`direction`: `hi-to-sat` or `sat-to-hi`) |
| POST | `/translate/audio` | Translate a recorded clip (multipart) |
| POST | `/translate/reverse` | Santali → Hindi shortcut |
| POST | `/speak` | Speak a given line as it is (`text`, `lang`: `sat` or `hi`) |
| GET | `/audio/<id>` | The clip for one reply |
| GET | `/audio/output`, `/audio/hindi` | Deprecated: the newest Santali / Hindi clip |
| POST | `/session/start`, `/session/next`, `/session/goto` | Run a lesson |
| POST | `/session/response` | Mark an answer to a given `step` (JSON, or multipart with `audio`) |
| POST | `/session/summary` | Session summary |
| POST | `/worksheet` | The bilingual PDF |
| POST | `/feedback` | 👍 / 👎 or a correction, with `direction` |
| POST | `/metrics/client` | The browser's own timing for a request |
| GET | `/metrics/latency` | Count, median, p90 and max per path |
| POST | `/curriculum/import` | Hindi text or a `.txt` / `.csv` / `.json` file → draft lessons: lines with suggested labels and suggested NIPUN goals. Nothing is stored |
| POST | `/curriculum/save` | The teacher's corrected draft with `lakshya_confirmed: true` → Santali, audio, flashcards, stored lesson |
| GET | `/curriculum` | The imported lessons |
| GET | `/curriculum/<topic>/worksheet` | An imported lesson's worksheet (PDF) |
| GET | `/lesson_audio/<topic>/<n>` | The audio for line n of an imported lesson |
| GET | `/hub-ca.crt` | The laptop hub's CA certificate, for tablets |
| GET | `/lesson_plan?grade=&topic=` | The teacher's lesson plan PDF (Hindi, Ol Chiki, reading guide, tiers, answers) |
| POST | `/corpus/record` | Community voice corpus: an adult's recording of a line (`audio`, `text`, `lang`, `adult=1`, `share`) |
| GET | `/corpus/summary`, `/corpus/export` | Recording counts; the shareable recordings as a zip (from the laptop itself only) |

A reply from `/translate/text`:

```json
{
  "translated_text": "ᱜᱤᱫᱽᱨᱟᱹ ᱠᱚ ᱵᱤᱨᱫᱟᱹᱜᱟᱲ ᱨᱮ ᱪᱟᱞᱟᱣᱚᱜ ᱠᱟᱱᱟ ᱾",
  "source": "model",
  "model_score": 0.7,
  "audio_url": "/audio/110bfe8dd4fa448a95e12c280dfffeaa",
  "tts_error": null,
  "tts_engine": "piper",
  "request_id": "…",
  "latency": { "asr": 0.0, "nmt": 0.41, "tts": 0.12, "total": 0.53 },
  "english_pivot": "",
  "confidence": null
}
```

- `source` is `teacher`, `glossary`, `cached` or `model`.
- `model_score` is set only for `model` output. It is not a quality estimate, and the UI does not show it.
- `english_pivot` and `confidence` are always empty. They are kept so older clients do not break.
- `reading_guide` is the Santali in Devanagari for the teacher (null for Hindi output); `needs_review` marks tier C.
- The latency values are one example; yours will differ.

---

## 12. Project layout

| Path | What it is |
|---|---|
| `app.py` | Flask server |
| `pipeline.py` | ASR, translation layers, transliteration, Piper TTS, caches |
| `indicconformer_asr.py` | ONNX wrapper for IndicConformer |
| `translit/olchiki.py` | Ol Chiki → Devanagari / Latin transliteration |
| `textnorm.py` | Text normalisation for matching corrections and glossary lines |
| `education_glossary.py` | Verified sentences, word lists, and the log of glossary changes |
| `lesson_engine.py` | Lessons, flashcard words, answer checking, sessions |
| `nipun/lakshya.py` | NIPUN Lakshya goals, verbatim, with our IDs |
| `worksheet.py` | Bilingual PDF |
| `database.py` | SQLite: `feedback`, `sessions`, `session_events`, `latency_log` |
| `config.py` | Product name, paths, model revisions, settings |
| `frontend.html` | The whole UI |
| `download_models.py`, `model_manifest.json` | Fetch and verify the pinned model files |
| `verify_models.py`, `test_pipeline.py`, `tests/` | Checks and tests |
| `bench/`, `eval/` | Benchmarks and evaluations, with results |
| `tools/deck_numbers.py` | Prints every number the deck may use, with its source |
| `tools/make_cert.py` | Certificate for the HTTPS laptop hub |
| `curriculum.py` | Curriculum import: reading uploads, splitting, labels, goal suggestions, flashcard words |
| `content/team_lessons.json`, `tools/import_lessons.py` | The team's 13 lessons (added on first start), and a script to import other lesson files through the import endpoints |
| `tools/demo_reset.py`, `docs/demo_video_script.md`, `docs/RECORDING_GUIDE.md` | Getting ready to record the demo, the shot list, and how to record the laptop and the tablet |
| `tools/set_video_link.py`, `docs/SUBMISSION_CHECKLIST.md` | Putting the video link into the README and both decks; the steps left before submission |
| `docs/` | Lakshya mapping, glossary changes, the native-review list |
| `THIRD_PARTY_LICENSES.md` | Model, voice, package and font licences |
| `training_data/`, `train_nmt.py`, `generate_dataset.py` | A 33-pair corpus and a LoRA script. Not used for any accuracy figure |
| `_archive/` | Old scripts and drafts, not used by the app. Do not run `patch.py` or `extract.py` |

Git ignores `models/`, audio files, caches, the database, `certs/` and the
virtual environment. A fresh clone must download the models (§9).

---

## 13. Known limitations

| Item | Impact |
|---|---|
| The APK has no 32-bit ARM (armeabi-v7a) build | A 32-bit-only low-cost tablet cannot install it; adding the ABI needs a rebuild (and the ONNX Runtime JNI patch for that ABI) on the team laptop |
| No real 2 GB tablet measured | On-device results are from a 2 GB Android 9 emulator and a Realme Pad Mini (4 GB, Android 11). Translating on the tablet needs about 1.2 GB, above the 900 MB guideline, so it loads on demand |
| Free-form speech → speech is not on the tablet | On 2 GB it works but takes p50 13.48 s (models swapped), so it stays on the laptop hub; the tablet handles spoken lesson lines and typed sentences |
| Ho and Mundari are previews | No speech recognition for either; Mundari translation and both voices on the laptop hub only, labelled Preview, not reviewed by a native speaker; Ho has no translation |
| No native speaker has reviewed the Santali | This covers translations, the glossary, the transliteration, the Santali interface text and the voice. See `docs/native_review.md` |
| Santali is spoken by a Hindi voice reading a transliteration | How well children understand it: **NOT MEASURED** |
| Speed figures use synthetic clips and public adult speech | Real classroom speech, children's voices and classroom noise may be slower or less accurate: **NOT MEASURED** |
| Word lists in `education_glossary.py` are used only for flashcards | Translation uses whole verified sentences only |
| Imported lessons are stored in the local database, not in git | The team's lessons are added again on any laptop's first start. A teacher's own imports reach tablets through the next signed content pack (`tools/build_content_pack.py`) |
| Line labels and goal suggestions come from simple keyword rules | The teacher checks every label and must confirm the goals. The rules were tuned on the team's own lessons: they matched 7 of 10 goal suggestions before tuning and 9 of 10 after. That is not an independent accuracy figure |
| The NIPUN goal text on the import screen is in English | It is quoted from the Ministry's English guidelines |
| Flask development server | Fine for a classroom hub, not a public deployment |
| Default voice licence is non-commercial (CC BY-NC-SA 4.0); Mundari/Ho voices CC BY-NC 4.0 | Fine for a free government programme; a commercial deployment would need other voices |
| The APK includes espeak-ng (GPL-3.0-or-later) through sherpa-onnx's Piper path | The APK as a whole is distributed under GPL-3.0 terms (text and source notice in the APK and `android/`); our own code is MIT (`LICENSE`). On the laptop, `piper-tts` (GPL-3.0-or-later) is installed separately and not redistributed. See `THIRD_PARTY_LICENSES.md` |

---

## 14. Roadmap

1. **A real 2 GB tablet:** repeat the emulator and Realme checks on real 2 GB, Android 9 hardware; bring free-form speech to the tablet within the memory budget.
2. **Real recordings:** re-run every benchmark on teacher and child speech. Report adult and child, quiet and noisy, separately.
3. **Native review** of the glossary, the number words, the transliteration, the voice and the Mundari output; native listener ratings for the voice comparison (`docs/samples/mos_lite_sheet.md`).
4. **Mundari and Ho:** Mundari on the tablet; Ho content once a native speaker writes it.
5. A character-based Santali voice without espeak-ng, chosen by the rule fixed in advance (`docs/voice_rule_finale.md`).

---

## 15. Deck outline (for the slides)

Use only numbers printed by `python tools/deck_numbers.py` or quoted in the two
tables at the top of `STATUS.md`, each with its device label ("laptop hub,
offline", "Realme Pad Mini, 4 GB, Android 11, airplane mode", "2 GB Android 9
emulator") and "synthetic clips" or "public adult speech" wherever that applies.
The do-not-say list in `docs/demo_video_script.md` applies to the deck too.

---

## 16. Credits

Models from **AI4Bharat** (IIT Madras): IndicConformer and IndicTrans2.
Offline speech by **Piper**. Fonts: Noto Sans Devanagari, Noto Sans Ol Chiki,
Baloo 2, Kalam. Learning goals from **NIPUN Bharat**, Ministry of Education,
Government of India. Our code: MIT (`LICENSE`). Everything else: `THIRD_PARTY_LICENSES.md`.
