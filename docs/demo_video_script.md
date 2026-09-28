# Demo video script v3 (about 5 minutes)

v3 (28 Sep 2026): written from `STATUS.md` only (the two tables at its top); every number
below is in STATUS with its evidence file. v2 is in `_archive/demo_video_script_v2.md`.

Every segment carries its **device label** on screen, exactly as written here.
Two set-ups appear, never mixed in one shot:

- **Laptop hub**: caption **"Laptop hub: everything runs on this laptop, offline"**.
- **Tablet app**: recorded clips on the **Realme Pad Mini** (its session passed, 27 Sep), release
  candidate `0.95-rc1`, content pack and model pack imported, airplane mode on. Caption
  **"Realme Pad Mini, 4 GB RAM, Android 11, airplane mode"**.

**Do not say or show:**
- a speed other than the ones in the captions or on the page's timer;
- "on a 2 GB tablet" for anything (no real 2 GB tablet was measured; say "2 GB emulator" or
  "Realme Pad Mini, 4 GB");
- that the tablet's translation is identical to the laptop's (true on the emulator, **not** on the
  Realme: 65 of 80 test sentences);
- free-form *spoken* translation on the tablet (off; it stays on the laptop hub);
- photo import (off, a finale item);
- our own fine-tuned Santali voice as an improvement (it lost by the rule; not shipped);
- Mundari numbers next to Santali numbers (different test sets);
- any claim that Santali output, the voices or Mundari output are reviewed by a native speaker.

## Before recording

1. Laptop on mains power, other programs closed. `run_nijbhasha.bat`; then
   `python tools/demo_reset.py --forget-demo-correction` (must end with `Ready.`).
2. Wi-Fi off. Chrome at `http://127.0.0.1:5000`, zoom 125 %.
3. Tablet: release APK `0.95-rc1`, the newest signed **model pack** and **content pack** imported,
   airplane mode on. Segment 3b needs the hub over the laptop's hotspot instead
   (`run_nijbhasha.bat https`, the tablet's Chrome at `https://192.168.137.1:5443`).
4. A Santali speaker on the team writes the correction for segment 8 and, if possible, speaks the
   child's answer in segment 2. **Do not invent Santali.**

## Segments

| # | Time | Set-up | Shot | Caption (exact) |
|---|---|---|---|---|
| 1 | 0:00–0:20 | Tablet clip | Airplane mode on; open the app; lessons appear from the content pack | **"Realme Pad Mini, 4 GB RAM, Android 11, airplane mode: 24 of 24 app checks pass offline."** |
| 2 | 0:20–1:00 | Tablet clip (the Realme A1 check passed, 28 Sep) | **Lesson line by voice, on the tablet (A1):** the teacher says a lesson line (e.g. *"दो आम और तीन आम मिलाओ।"*); the Santali appears and plays. Then a child's Santali answer; it turns green and the Hindi praise plays | Device caption, plus: **"On-device speech for lesson lines; lines not in the lesson are refused, never guessed. On this tablet: 0.7 s (median) from the end of speech to the reply."** |
| 3 | 1:00–1:30 | Tablet clip | **New typed sentences (A5):** type a new Hindi sentence → Santali, translated on the tablet | Device caption, plus: **"Translated on the tablet: 1.5 s per sentence (median, 200 test sentences); quality on par with the laptop's compressed model (chrF++ 29.00 vs 28.75)."** |
| 3b | 1:30–1:50 | Tablet browser → hub | **Tablet's microphone through the laptop hub:** the tablet's Chrome, the lesson line spoken, the Santali plays | **"Tablet browser via laptop hub, Wi-Fi: 1.71 / 0.97 / 0.87 s from the end of speech to the reply playing (3 tries, one speaker)."** |
| 3c | 1:50–2:05 | Hub | Speak a *free* Hindi sentence on the laptop → Santali voice | **"Laptop hub: everything runs on this laptop, offline"** |
| 4 | 2:05–2:25 | Hub | **Check with a native speaker (A3):** type a line the model gets wrong (pick one flagged in the pack); the ⚠️ मूल वक्ता से जाँचें badge shows, no auto-play, the nearest verified sentence is offered | **"A warning, not a quality score."** |
| 5 | 2:25–3:00 | Hub | **Worksheet v2 and flashcards (A2):** कार्यपत्रक → the PDF: pictures, count and write, circle the answer, trace the numerals, the answer key page; चित्र पत्ते → 🖨️ → the cut-out cards with the review-pending mark | **"Pictures: OpenMoji (CC BY-SA 4.0). Santali lines await native review."** |
| 6 | 3:00–3:30 | Hub | **Reading fluency (C1):** प्रगति → पढ़ने की गति जाँचें; tick the consent box; a team member reads *बगीचे की सैर*; words correct per minute and the NIPUN goal; tap one word to override | **"Checked on adult read speech; children not measured yet. The recording is not saved."** |
| 7 | 3:30–3:45 | Hub | **Class progress by NIPUN Lakshya (A8):** the table by Lakshya and week; CSV and PDF | **"Class level only: no child names, no voices."** |
| 8 | 3:45–4:10 | Tablet clip + hub | **Corrections between tablets (A4):** a correction on the tablet → निर्यात → the signed file merged on the hub → the next pack shows it | Device caption; **"Packs and tablet files are signed (Ed25519); a changed pack is refused."** |
| 9 | 4:10–4:30 | Hub | **Mundari and Ho (A7, C3):** सेटिंग → मुंडारी / हो आवाज़; a teacher's Hindi line → हिंदी → मुंडारी → सुनें; then Ho: the voice only | **"Preview: Mundari translation and both voices are not reviewed by a native speaker. Ho: voice only, content pending a native speaker."** |
| 10 | 4:30–4:45 | Card | **Santali voice (A6, C4):** the two result tables (`bench/results/voice_compare.md`, `bench/results/voice_rule_finale.md`) | **"The current voice stays, by rules fixed in advance: Indic Parler-TTS and our own fine-tuned voice (one speaker, 0.6 h) both lost on the recognition test. Native listener ratings not collected yet."** |
| 11 | 4:45–5:00 | Card | Close: *"Offline on the laptop hub, and offline on Android tablets (a 4 GB tablet and a 2 GB emulator) for lessons, spoken lesson lines, typed translation, worksheets and sync. Next: a real 2 GB tablet, children's voices and native review."* | — |

## If something goes wrong

| Problem | Fix |
|---|---|
| No sound | Click once on the page, then 🔊. |
| A spoken line on the tablet says "not a lesson line" | That is the designed answer for lines not in the lesson; speak the lesson line exactly, or type it. |
| The tablet refuses a pack | It is unsigned or changed: rebuild it on the hub (`tools/build_content_pack.py`) and import again. |
| The tablet's Chrome shows ERR_CONNECTION_REFUSED on the hub | The hub is still loading its models (about 25 s); reload. The tablet must be on the laptop's hotspot. |
| The reading check gives a low score for an adult | Recognition errors count as misreadings (5.9 % of words on adult speech); tap the word to correct it. |
| The Mundari button is missing | The Mundari translation model is not installed on this laptop (`python tools/install_mundari_nmt.py`) or `MUNDARI_NMT_PREVIEW` is off. |
