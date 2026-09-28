# Why Nijbhasha: the case for the judges

Every claim here points to a file in this repository. Where something is not measured,
it says so. Use this for the finale talk and the Q&A.

## One sentence

A Hindi-medium teacher runs a NIPUN lesson in Santali, on a tablet with no internet: the
child hears Santali in about 0.7 s, the teacher can read it aloud from a Devanagari guide,
and every doubtful line is flagged instead of guessed.

## Five differentiators we can defend

1. **Offline on the tablet itself, measured.** Spoken lesson lines are recognised, matched
   and voiced on the device in airplane mode: p50 0.70 s, p95 1.27 s on a Realme Pad Mini
   (4 GB, Android 11); p50 0.50 s, p95 0.93 s on a 2 GB Android 9 emulator; 24 of 24 app
   checks offline on both. *Evidence:* `bench/results/latency_percentiles.md`,
   `…realme…rc2_2026-09-28_m1.md`, `…emulator-2gb-android9_2026-09-26_m1.md`.
2. **It never guesses in front of a child.** A spoken line that matches no lesson line is
   refused on the tablet; model output with a loop, a failed round trip or a word in another
   script is tier C: not auto-played, "check with a native speaker", nearest verified sentence
   offered. We found 13 lesson lines with Meetei Mayek or Urdu words in the model's output and
   built the guard that catches them. *Evidence:* `nmt_guard.py`, `docs/fln_translation_sample.md`.
3. **A bridge for the teacher, not only a translator.** Every Santali reply comes with a
   Devanagari reading guide; every lesson prints a teacher's plan with the guide, the tier and
   the accepted answers. *Evidence:* `reading_guide.py`, `lesson_plan.py`, `docs/samples/`.
4. **The whole lesson, aligned to NIPUN.** 18 lessons from Balvatika to Grade 3, every Lakshya
   covered, worksheets and cut-out flashcards, answer checking in any digit script, a
   reading-fluency check against the NIPUN words-per-minute goals, progress per Lakshya.
   *Evidence:* `nipun/lakshya.py`, `worksheet_v2.py`, `orf.py`, `progress.py`.
5. **Gets better with the community, safely.** Teacher corrections are reused first and synced
   between tablets as signed files; adults can record lines for a local voice corpus with
   consent; conflicts go to a native-review list. *Evidence:* `sync.py`, `corpus.py`,
   `docs/native_review.md`.

Underneath all five: numbers produced by scripts, decisions fixed before the results, a
leakage guard, and a test that fails if the README quotes a number without evidence.

## What strong rivals will show, and our answer

| Rival strength | Our answer |
|---|---|
| A polished UI, maybe a cloud LLM | A cloud tool stops without internet, which is most of the target schools, and sends children's voices away. Ours runs in airplane mode with nothing leaving the device. |
| Bigger models, higher BLEU on a slide | Our model's public scores are stated with the test set (chrF++ 32.2, IN22-Conv); we do not claim to beat anyone. What we add is what a classroom needs: flags, lessons, worksheets, speed on a tablet. |
| "Supports Ho, Mundari and Santali" | Ask which stage. Ours: Santali end to end; Mundari translation in preview from our own LoRA adapters (held-out chrF++ 30.92); Ho and Mundari voices in preview; each stage's maturity in `languages.json`. |
| Google Translate or Bhashini wrappers | They translate text; they do not run a NIPUN lesson, check answers, print worksheets, or work offline on a 2 GB-class tablet. |
| A live demo that looks fast | Our speed is measured on real devices over 50 lines, with p95 and the cases over 3 s reported. |

## The 15 hardest questions, with honest answers

1. **How do you know the Santali is correct without a native speaker?** We don't, and we say
   so. We measure the model on public test sets (chrF++ 31.3 / 32.2 / 27.4), put
   human-written sentences first, flag doubtful output (loops, round trip, script), and route
   every line to a native-review list. The first thing we want from a pilot is a native reviewer.
2. **Your Santali voice is a Hindi voice?** Yes. No offline Santali voice exists. A Hindi Piper
   voice reads our Ol Chiki transliteration. We trained our own Santali voice and tested Indic
   Parler-TTS; both lost to it on a rule we fixed before the test. Children's comprehension of
   the voice is not measured yet.
3. **Does it really run on a 2 GB tablet?** Measured on a 2 GB Android 9 emulator and a real
   4 GB tablet, not on a real 2 GB device. Lessons, lesson-line voice and sync fit (up to about
   0.75 GB); typing new sentences needs about 1.2 GB, so translation loads on demand.
   Free-form speech stays on the laptop hub.
4. **What about 32-bit tablets?** Not built yet: the APK has arm64 and x86_64. Adding
   armeabi-v7a is a build change on our list; the engines support it.
5. **Is it really under 3 s?** On the tablet for lesson lines: p95 1.27 s. On the laptop for free
   Hindi speech of up to 17 words: p90 2.85 s, but p95 3.29 s: 8 of 96 sentences went over,
   mostly long ones. We say so.
6. **What about children's speech and classroom noise?** Not measured. All speech figures are
   adult public speech or synthetic clips. It is the first benchmark we would run in a pilot.
7. **Where does your data come from, and may you use it?** Published models (IndicConformer,
   IndicTrans2: MIT), public test sets (CC BY / CC BY-SA), MMLoSo 2025 for Mundari (CC BY-SA),
   the Piper voice (CC BY-NC-SA). All in `THIRD_PARTY_LICENSES.md`. Our code is MIT; the APK is
   GPL-3.0 because of espeak-ng.
8. **Ho?** A Ho voice (Meta MMS) in preview; no Ho translation, because we found no licensed Ho
   parallel text. The same LoRA path as Mundari applies once a community provides data.
9. **How does it scale to more schools and languages?** A school needs a tablet and one content
   sync; a hub laptop is optional. Lessons, corrections and packs are signed files. A new
   language is a row in `languages.json` plus models; Mundari translation came from LoRA training on a single Kaggle GPU.
10. **What does it cost?** No licence or per-use fees; runs on the school's own tablet or
    laptop. Hardware and training costs are not estimated here.
11. **Children's privacy?** No cloud. Progress reports have no names and no audio. The
    reading-check recording is deleted after scoring. The voice corpus takes adults only, with
    consent, stays on the laptop, and exports only with consent to share.
12. **Why not an LLM?** It would need the internet or far more memory than a 2 GB tablet, and it
    can invent. IndicTrans2 is a 320M translation model that runs on the tablet.
13. **What if the teacher's correction is wrong?** Corrections are labelled as teacher-written
    (tier A, native review pending); two tablets that disagree are not merged but listed for a
    native speaker.
14. **Who maintains it?** Open code and models; content is lessons in JSON the state can edit;
    corrections and the corpus grow with use. We propose a PALASH pilot (not agreed with anyone).
15. **What is not done?** A real 2 GB device, a 32-bit build, native review, children's speech,
    the demo video. All in `docs/audit_2026-09-28.md`.
