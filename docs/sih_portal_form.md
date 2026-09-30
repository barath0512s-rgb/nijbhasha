# SIH portal: idea submission form (copy each box into its field)

Every number below is in `STATUS.md` or `bench/`/`eval/` results, with the same wording as the
decks. Plain text only (the portal fields do not render formatting).

## Idea Title (max 100 characters; this one is 89)

```text
Nijbhasha: Offline AI Bridge for Hindi-Medium Teachers to Teach Santali-Speaking Children
```

## Idea Description (max 50,000 characters)

```text
Problem statement SIH26042 (Ministry of Education): AI-Powered Vernacular Pedagogy and Real-Time Translation Tool for Mother Tongue-Based Primary Education. Team 8-bitPool (VITV), Team ID 168531.

1. The gap we are working on

In Jharkhand, most primary teachers teach in Hindi, but many of their Grade 1 children speak Ho, Santali or Mundari at home. The JEPC language mapping survey (Phase 1, 2024, 8,244 schools in 7 districts) found that about 98% of surveyed schools teach in Hindi, while Grade 1 home languages include Ho (17.03%), Santali (13.07%) and Mundari (7.32%). PALASH, the state's mother tongue programme, shows that teaching in the home language works, but it cannot find enough teachers who speak these languages. A child who cannot answer "दो और तीन कितने होते हैं?" may not be failing at addition. They may be failing at Hindi.

Nijbhasha (निजभाषा, "one's own language") lets a Hindi-speaking teacher run a lesson in Santali without learning Santali first. The teacher speaks or types Hindi. The child hears Santali and sees it in Ol Chiki, the script Santali children learn. When the child answers in Santali, the teacher hears it back in Hindi. Everything runs offline, on a low-cost 2 GB Android tablet or on a school laptop, after one initial content sync.

2. What we built (working today, all in the public repository)

Android tablet app (Android 9 and above):
- Lessons, worksheets and flashcards from a signed content pack.
- Spoken lesson lines: the teacher says a line from the lesson, the tablet recognises it on the device and plays the Santali. Lines that are not in the lesson are refused, never guessed.
- Typed translation of new Hindi sentences into Santali, on the tablet itself.
- Teacher corrections, exported as signed files and merged on the laptop hub, so every tablet gets them.
- Deployed and running on the target device class: we have installed the full tablet app, with its models, on a real 2 GB RAM Android tablet and run it offline. It is also tested on a Realme Pad Mini (4 GB RAM, Android 11) and a 2 GB Android 9 emulator, where 24 of 24 app checks pass in airplane mode on both.

Laptop hub (optional, for a cluster of classrooms):
- Free speech in both directions (Hindi to Santali and Santali to Hindi), with the larger models.
- Makes the printable material and the content packs for tablets.
- Tablets on the same Wi-Fi can use it through their browser.

For the teacher and the class:
- 18 ready lessons from Balvatika to Grade 3 covering every NIPUN Bharat Lakshya, each tagged with the Ministry's Lakshya IDs.
- For each lesson: a bilingual worksheet (count and write, match, fill in the blank, circle the answer, trace the numeral, with an answer key), cut-out picture flashcards, and a printable teacher's lesson plan.
- A Devanagari reading guide under every Santali line, so the teacher can say the Santali aloud.
- Teachers can add their own lessons from Hindi text; the app suggests the NIPUN goals and the teacher confirms them.
- Comprehension check: the child's spoken answer is marked green, yellow or red.
- Reading-fluency check: a child reads a passage aloud and the app counts words correct per minute against the NIPUN goals. The teacher can override any word, a consent box comes first, and the recording is deleted after scoring.
- Class progress by NIPUN Lakshya and week, as CSV and PDF, with no child names and no audio.
- Interface in Hindi, Santali and English.

3. The AI pipeline

Speech recognition: AI4Bharat IndicConformer (600M parameters on the laptop hub; the 120M model in int8 on the tablet, run with sherpa-onnx). Hindi uses the CTC decoder and Santali the RNN-T decoder.

Translation: AI4Bharat IndicTrans2 indic-indic 320M, translating directly between Hindi and Santali with no English in between. The hub runs it in ONNX Runtime; the tablet runs an int8 version through ONNX Runtime for Android, with our Kotlin port of the IndicTrans2 pre- and post-processing and SentencePiece.

Speech output: Piper (offline). There is no offline Santali voice, so we wrote an Ol Chiki to Devanagari transliterator and a Piper Hindi voice reads the result. We compared two alternatives (Indic Parler-TTS and our own fine-tuned Santali voice) against a rule we wrote down before scoring them. Both lost, so the current voice stays.

Every translation is answered by the most trustworthy source available, in this order: a teacher's correction, a verified sentence from our glossary, an earlier result from the cache, and only then the model.

4. What is new in our approach

Human first, model last. A teacher's correction always wins and is reused for the same sentence on every tablet after sync.

Trust tiers. Every Santali line carries a badge: A (written by a person), B (model output) or C (flagged). A tier C line is never played automatically, and the app offers the nearest verified sentence instead.

Three guards on model output:
- a loop guard that cuts repeating output;
- a round-trip check that translates the Santali back to Hindi and flags a large mismatch. It is a caution, not a quality score: test precision 0.464, recall 0.449;
- a script guard that flags Santali containing letters from another script. On our 119 lesson-line sample, 13 lines had such letters (6 had not been flagged before) and all are now tier C.

Lesson-line matching on the tablet. Spoken lines are matched against the lesson on the device (precision 0.980, recall 0.833 on the Realme) instead of being translated from scratch, which is fast and never invents a line.

Signed packs. Content packs, model packs and tablet correction files are signed with Ed25519 and checked on the tablet; a changed or unsigned pack is refused. We ported Ed25519 to Kotlin because Android 9 has none.

Low-resource languages. We trained our own Mundari LoRA adapters on IndicTrans2 (18,978 training pairs from the MMLoSo 2025 data). This is a preview on the laptop hub: held-out chrF++ 30.92 (Hindi to Mundari) and 35.97 (Mundari to Hindi), n = 1,021, not reviewed by a native speaker. Mundari and Ho voices are available as a preview. A community voice corpus records consenting adults on the laptop, to build Santali, Mundari and Ho speech data over time.

5. Measured results (all offline)

- Spoken lesson line to Santali speech on the tablet: median 0.70 s, p90 1.20 s, p95 1.27 s (Realme Pad Mini, n = 50); 0.50 / 0.82 / 0.93 s on the 2 GB emulator. The limit in the problem statement is 3 s.
- Laptop hub, free Hindi speech of up to 17 words (public FLEURS adult speech, 3 runs): median 2.04 s, p95 3.29 s; 8 of 96 sentences took more than 3 s. We report this tail openly. Santali to Hindi on the hub: p90 about 2.6 s.
- Typed new sentence translated on the tablet: median 1.50 s (Realme), 0.60 s (2 GB emulator).
- Translation quality, Hindi to Santali, chrF++: 31.3 (IN22-Gen), 32.2 (IN22-Conv, n = 1,503), 27.4 (FLORES-200). Benchmark sentences are blocked from any training by a leakage guard.
- Speech recognition on the hub (normalised WER): Hindi 12.5%, Santali 31.0%.
- Size: release APK 72 MB; model pack 361 MB (int8, signed); content pack 38 MB (signed).
- Peak memory: 0.30 GB for lessons, 0.75 GB for spoken lesson lines, 1.30 GB while translating typed sentences (loaded only when needed).
- 336 automated tests pass in CI on every push, plus 40 that need the models. A test fails if the README quotes a number that has no evidence file.

6. How it meets the five requirements

R1, accurate text and speech in the mother tongue: every lesson line has Santali in Ol Chiki and offline speech; human-written sentences come first; doubtful model output is flagged; the reading guide lets the teacher speak it too.
R2, real time within 3 seconds: 0.70 s median and 1.27 s at p95 for lesson lines on the tablet; free speech on the laptop hub at 2.04 s median, with the tail over 3 s disclosed.
R3, bilingual worksheets and flashcards aligned to NIPUN Bharat: generated for all 18 lessons, every Lakshya covered, plus lesson plans and the reading-fluency check.
R4, offline on low-cost tablets after the first sync: the app is deployed and running offline on a real 2 GB RAM Android tablet, and passes 24 of 24 checks in airplane mode on the Realme Pad Mini and on a 2 GB Android 9 emulator. Speech, translation and voice models all run on the device; memory peaks at 1.30 GB, while translating typed sentences, and the models load one at a time so they fit in 2 GB.
R5, working application, demo video and repository: the app, the demo video (laptop hub and tablet, recorded 30 September) and the public repository at github.com/barath0512s-rgb/nijbhasha.

7. Privacy and safety

No cloud at any point: speech stays on the tablet or the school laptop. Progress reports contain no names and no audio. The reading check asks for consent and deletes the recording after scoring. The voice corpus is adults only, with consent, and stays on the laptop.

8. What we have not done yet (stated plainly)

- No native Santali, Mundari or Ho speaker has reviewed the output or the voice yet. Every line is on a native-review list, and the app says so on screen.
- The Santali voice is a Hindi voice reading our transliteration.
- The timing figures above come from the Realme Pad Mini and the 2 GB emulator; the full benchmark run on our 2 GB tablet is next. There is no 32-bit ARM build yet.
- Free-form speech (any sentence, not only lesson lines) runs on the laptop hub; on 2 GB devices it took 13.5 s on the emulator, so on 2 GB tablets the app keeps it off and uses lesson-line matching and typed translation instead.
- Children's speech and classroom noise have not been measured; our speech benchmarks use adult speech.
- The lesson-to-NIPUN mapping has not been reviewed by a teacher.

9. Impact and scale

PALASH runs in 1,041 schools across 8 of Jharkhand's 24 districts (JEPC, January 2026), and the problem statement names more than 5,000 tribal-area schools. A classroom needs one Android tablet; the laptop hub is optional. The models are MIT-licensed and the app runs offline, so there are no licence or per-use cloud fees. Content is a signed pack that a district can build and send. The same pipeline extends to Mundari (preview done) and to Ho once written content exists. This supports NEP 2020 section 4.11 (teaching in the mother tongue), NIPUN Bharat and SDG 4.

10. Next steps

In 30 days: native review of the 18 lessons, a 32-bit build, the full benchmark run on our 2 GB tablet, and the APK as a public release. With a pilot (proposed, not yet agreed): five PALASH classrooms, a children's speech benchmark and Mundari on the tablet. Later: Ho content with native writers, and a voice built from the community corpus.

Our ask: one native Santali reviewer and one PALASH classroom to test in.
```

## Idea Template (PDF, up to 10 MB)

Upload `docs/deck/Nijbhasha_SIH26042_8-bitPool.pdf` (6 slides on the SIH template, 1.6 MB).
Export it from PowerPoint first (File → Export → PDF) so the Ol Chiki text renders correctly.

## Abstract / Summary (max 10,000 characters)

```text
Nijbhasha (निजभाषा, "one's own language") helps a Hindi-speaking primary teacher in Jharkhand teach children who speak Santali at home, without the teacher learning Santali first. The teacher speaks or types Hindi; the child hears Santali and sees it in Ol Chiki script; the child's Santali answer comes back to the teacher in Hindi. It is deployed and runs offline on a low-cost 2 GB RAM Android tablet (the app supports Android 9 and above), or on a school laptop, after one initial content sync. It is built for PALASH schools and for problem statement SIH26042.

The AI pipeline uses AI4Bharat IndicConformer for speech recognition (600M on the laptop, 120M int8 on the tablet), AI4Bharat IndicTrans2 for direct Hindi to Santali translation with no English pivot, and Piper for offline speech, reading Santali through our own Ol Chiki transliterator. A teacher's correction is always used first, then verified sentences, then the model.

Because no native Santali speaker has reviewed the output yet, the app never presents a doubtful line as correct. Every line carries a trust tier (A human-written, B model, C flagged); three guards (loop, round trip, script) flag suspect output, and a tier C line is never played automatically. On the tablet, spoken lesson lines are matched against the lesson and anything else is refused rather than guessed. Content, models and teacher corrections move between devices as Ed25519-signed packs.

Each of the 18 NIPUN-aligned lessons (Balvatika to Grade 3, every NIPUN Lakshya) produces a bilingual worksheet with an answer key, cut-out flashcards, a teacher's lesson plan with a Devanagari reading guide, a comprehension check and a reading-fluency check in words correct per minute. Class progress is reported by NIPUN Lakshya with no child names or audio. The interface is in Hindi, Santali and English. We also trained a Mundari translation preview (our LoRA on IndicTrans2) and added Mundari and Ho voice previews.

Measured offline: a spoken lesson line becomes Santali speech in 0.70 s median (p95 1.27 s) on a Realme Pad Mini tablet and 0.50 s on a 2 GB Android 9 emulator, under the 3-second limit. Typed sentences translate on the tablet in 1.50 s median. Hindi to Santali chrF++ is 32.2 on the public IN22-Conv test set. The app runs offline on a real 2 GB Android tablet, and passes 24 of 24 checks in airplane mode on the Realme and the 2 GB emulator. On the laptop, free speech of up to 17 words takes 2.04 s median; 8 of 96 test sentences took over 3 s, and we say so.

Not done yet: native-speaker review, a 32-bit build, the full timing benchmark on our 2 GB tablet, and tests with children's voices. Code, results and the test suite (336 tests in CI) are public at github.com/barath0512s-rgb/nijbhasha.
```

## YouTube Link (optional)

Paste the unlisted YouTube link of the demo video. Then, on the laptop:
`python tools\set_video_link.py <the same link>` so the README and both decks carry it too.

## Technology Bucket

Choose the Artificial Intelligence / Machine Learning option (the exact label depends on the
portal's list). If the list has no AI option, choose the education option.
