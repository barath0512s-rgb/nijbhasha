# Recording the demo video: step by step

**What to film, shot by shot, and the exact captions:** [`docs/demo_video_script.md`](demo_video_script.md)
(v4, the "Segments" table, segments 1–11, about 5 minutes). Keep it open on a second screen
or printed. This page covers only *how* to get the laptop and tablet ready and record.

Film segments in any order and cut them together afterwards. Laptop shots and tablet shots are
never mixed in one clip. Each clip carries its device caption, exactly as the script writes it.

---

## A. Laptop hub (segments 3c, 4, 5, 6, 7, 9 and the hub half of 8)

1. **Power and clean-up.** Plug the laptop into mains power and close other programs, especially
   anything using the microphone (Teams, Zoom, Discord).
2. **Start the server.** Open the project folder and double-click `run_nijbhasha.bat`,
   or from a terminal in that folder:
   ```bat
   run_nijbhasha.bat
   ```
   Wait for `Running on http://127.0.0.1:5000` (the first start loads the models, about a minute).
   Leave this window open.
3. **Reset and warm up.** In a **second** terminal in the same folder:
   ```bat
   vaanisetu_env\Scripts\activate
   python tools\demo_reset.py --forget-demo-correction
   ```
   It must end with **`Ready.`** It also prints:
   - `segment 4, tier C line to type: ...` — **write this line down**. Type it in segment 4 to show
     the "C · Check with a native speaker" badge (the model's output decides which line is flagged,
     so the tool finds one for you).
   - the lesson plan check (a byte count), so segment 5's 🗒️ button is warm.
   Nothing is lost: the database is copied to `data\backups\` first.
4. **Go offline.** Turn Wi-Fi off (and unplug any network cable). Keep the Wi-Fi icon visible in
   the taskbar for the offline proof.
5. **Browser.** Chrome → `http://127.0.0.1:5000` → zoom 125 % (Ctrl +). Pick the interface language
   with the button at the top: **English** for judges, or हिंदी as the script's button names show.
   Click once anywhere on the page (browsers block sound until the first click). Allow the microphone
   when Chrome asks.
6. **Record the screen.** Either:
   - **OBS Studio** (free): Sources → + → *Window Capture* (Chrome) and *Audio Input Capture*
     (your microphone) and *Audio Output Capture* (so the Santali voice is recorded) →
     Settings → Output → Recording format **mp4** → *Start Recording*; or
   - **Windows Game Bar**: focus Chrome, press **Win + Alt + R** to start and stop (it records the
     app's sound; turn on "Capture microphone" with Win + Alt + M).
7. **Between takes** of the same segment, run `python tools\demo_reset.py` again (without the flag
   when you want to keep a correction you just made) and reload the page (F5).

## B. Tablet app (segments 1, 2, 3 and the tablet half of 8)

1. **Build on the tablet.** The Realme Pad Mini with the Nijbhasha app **0.95** (tag
   `v0.95-submission`), the **model pack** and the **content pack** imported (Settings → import).
   Optional: install the new build first (the reading guide and the script guard on the tablet;
   see `docs/SUBMISSION_CHECKLIST.md`, step 1). Otherwise film 0.95 as it is; the script already
   says so.
2. **Airplane mode on:** swipe down → tap the airplane icon. **Film this** for segment 1 (the
   status bar icon is the offline proof).
3. **Screen recorder:** swipe down → **Screen Recorder** (Realme UI; add it with the pencil icon
   if it is missing) → settings (the gear) → *Record sound* → **System sound and microphone**.
   Start, then open the Nijbhasha app.
4. Film segments 1, 2, 3 and the tablet half of 8 exactly as the script's table says. Speak the lesson
   line exactly (for example *"दो आम और तीन आम मिलाओ।"*); a line that is not in the lesson is
   refused by design.
5. Optional but convincing: film the tablet with a phone camera too, so judges see a real device
   in a hand.
6. Copy the recordings to the laptop (USB cable → the phone's *Movies/Screen recordings* or
   *DCIM/Screen recordings* folder).

## C. Segment 3b: the tablet's microphone through the laptop hub (optional, 20 s)

1. On the laptop: Settings → Network → **Mobile hotspot** on. Connect the tablet to it
   (airplane mode off for this segment only; say so in the caption).
2. Then start the server over HTTPS (after the hotspot, so the certificate names its address):
   ```bat
   run_nijbhasha.bat https
   ```
3. One time only, install the certificate on the tablet: in its Chrome open
   `https://192.168.137.1:5443/hub-ca.crt`, or copy `certs\hub-ca.crt` (**never** `hub-ca.key`)
   → Settings → Security → *Install from storage* → **CA certificate** → Install anyway.
   Details: `docs/device_session.md`.
4. The tablet's Chrome → **`https://192.168.137.1:5443`** → allow the microphone → speak the lesson line.
5. Check that the hub heard it: `python tools\hub_mic_check.py --since-minutes 10`.
6. If it shows `ERR_CONNECTION_REFUSED`, the hub is still loading (about 25 s); reload.

## D. Segments 10 and 11 (cards)

Plain title cards. Use the result tables and the closing sentence written in the script.
Make them in the video editor or as a slide.

## E. Editing, captions and upload

1. Cut the clips in the script's order in any editor (Clipchamp is built into Windows;
   DaVinci Resolve and Shotcut are free). Add each **caption exactly as written** in the script's
   last column. Keep it at about 5 minutes.
2. **Do not** say or show anything from the script's "Do not say or show" list (for example
   "2 GB tablet", spoken translation on the tablet, or native-speaker review).
3. Export as **1080p mp4**. Upload to YouTube as **Unlisted** (or Google Drive with "Anyone with
   the link can view"). Open the link in a private window to check it plays without signing in.
4. Put the link everywhere in one step:
   ```bat
   python tools\set_video_link.py https://youtu.be/XXXXXXXXXXX
   ```
   This fills in the README, slide 6 of the submission deck, slide 14 of the finale deck (a clickable
   link) and `docs/deck/SOURCES.md`. Then open both `.pptx` files in PowerPoint →
   File → Export → PDF (replace the PDFs next to them), and commit:
   ```bat
   git add -A
   git commit -m "Demo video link"
   git push
   ```

## Troubleshooting

See the script's "If something goes wrong" table: no sound, a refused pack, the
"not a lesson line" message, a low reading score for an adult, a missing Mundari button.
