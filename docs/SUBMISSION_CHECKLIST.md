# Submission checklist: what is left, and who does it

State on 28 Sep 2026: the code, tests, CI, README, both decks, the demo script and the samples are
in `main`. The steps below need **your laptop, the tablet or your accounts**. They cannot be done
from the cloud session: it has no Android SDK, no models and no camera. Do them in this order.
Each step says how you know it is done.

| # | Step | Needed for | Time |
|---|---|---|---|
| 1 | Pull `main` on the laptop | everything | 2 min |
| 2 | Check the laptop hub | video, finale | 5 min |
| 3 | Compile and test the Android changes, reinstall (optional) | tablet clips with the reading guide | 30 min |
| 4 | Record the video | clause 6 (demo video) | 2–3 h |
| 5 | Upload and insert the link | clause 6 | 10 min |
| 6 | Export the deck PDFs from PowerPoint | upload to the SIH portal | 5 min |
| 7 | GitHub Release with the APK | judges install the app | 10 min |
| 8 | Final check of the repository page | — | 5 min |
| — | Team decisions (no deadline) | — | — |

## 1. Pull the latest code

```bat
cd "C:\Users\Barath Srinivasan\Desktop\vaanisetu_1"
git checkout main
git pull origin main
vaanisetu_env\Scripts\activate
pip install -r requirements.txt
```
**Done when** `git log -1` shows the same commit as the top of
https://github.com/barath0512s-rgb/nijbhasha/commits/main.

## 2. Check the laptop hub (models present, tests pass)

```bat
run_nijbhasha.bat verify
python -m pytest -q
```
**Done when** verify reports every model OK and pytest shows **0 failed**. With the models
installed, the 38 tests skipped in CI also run.

## 3. Android: compile the 28 Sep evening changes (optional before the video)

`android/app/src/main/java/.../core/Api.kt` gained the reading guide and the script guard (a
Santali result with Latin or other foreign letters is marked "check with a native speaker"). This
was written **without an Android compiler** (the cloud session cannot download the SDK), so build and
test it before it goes on a tablet:

```bat
python tools\android\sync_config.py
python tools\android\fetch_sherpa_aar.py
python tools\android\patch_ort_jni.py
cd android
set JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=C:\gt
gradlew testDebugUnitTest assembleDebug assembleRelease
cd ..
python tools\build_content_pack.py
python tools\android\device_check.py --apk android\app\build\outputs\apk\release\app-release.apk --debug-apk android\app\build\outputs\apk\debug\app-debug.apk --pack dist\packs\content-pack-<newest>.zip --label realme-pad-mini-4gb-android11
```
(When `device_check.py` stops with "ACTION NEEDED", do what it says, then run the same command
again with `--resume`.)

**Done when** the Gradle build says `BUILD SUCCESSFUL` and device_check reports 24 of 24. If Gradle
reports a Kotlin error in `Api.kt`, the error is in `readingGuide()` or `foreignLetters()` (the only
new code); send the message and it will be fixed. If you skip this step, film the tablet with
0.95 as it is: the demo script already says the reading guide is shown on the hub.
If you ship the new build, raise `versionName` in `android/app/build.gradle.kts` (for example
`0.96`) so the video and the release name match.

## 4. Record the demo video

Follow **`docs/RECORDING_GUIDE.md`** (how to start the laptop and the tablet and record them). The
shots and exact captions are in **`docs/demo_video_script.md`**, section "Segments", 1–11.

**Done when** you have one mp4 of about 5 minutes with every caption as written.

## 5. Upload the video and insert the link

Upload the video to YouTube as **Unlisted**, or to Drive shared as "Anyone with the link". Then:
```bat
python tools\set_video_link.py https://youtu.be/XXXXXXXXXXX
```
The script fills in the README, submission deck slide 6, finale deck slide 14 and `docs/deck/SOURCES.md`.
**Done when** it prints four "Updated" files.

## 6. Export the PDFs (PowerPoint, not LibreOffice)

Open `docs/deck/Nijbhasha_SIH26042_8-bitPool.pptx` → File → Export → Create PDF → save over
`docs/deck/Nijbhasha_SIH26042_8-bitPool.pdf`. Do the same for `deck/final_deck.pptx` →
`deck/final_deck.pdf`. Check the pages: Ol Chiki must show as letters, not boxes (install
**Noto Sans Ol Chiki** from Google Fonts if it shows boxes). Then:
```bat
git add -A
git commit -m "Demo video link; decks exported from PowerPoint"
git push origin main
```
**Upload to the SIH portal:** the 6-slide `docs/deck/Nijbhasha_SIH26042_8-bitPool.pdf` (the
template, at most 6 slides). Keep the finale deck for the presentation round.

## 7. GitHub Release (so judges can install the app)

On https://github.com/barath0512s-rgb/nijbhasha → **Releases** → *Draft a new release* → tag
`v0.95-submission` (or `v0.96` if you did step 3) → attach:
- `app-release.apk` (72.2 MB);
- the content pack `content-pack-<time>.zip` from `dist\packs\` (37.8 MB);
- the model pack `model-pack-<time>.zip` (361 MB; GitHub allows up to 2 GB per file).

Release notes: copy the "Android app" section of the README, and add this licence line: *"The APK
as a whole is distributed under GPL-3.0 (it includes espeak-ng via sherpa-onnx); our source code
is MIT. The source is this repository at this tag."*
**Never attach** `certs/*.key`, `data/*.db` or anything from `corpus/`.

## 8. Final check of the repository page (private window, not signed in)

- The README opens with the name, team and ID, the "At a glance" table and the demo video link.
- The **Actions** tab shows a green tick on the last commit of `main`.
- `docs/demo_video_script.md`, `docs/feature_traceability.md` and `deck/final_deck.pdf` open.
- The video link plays without signing in.

## Team decisions (made 30 Sep 2026)

| Decision | Chosen | Why | What you do |
|---|---|---|---|
| A 32-bit (armeabi-v7a) build | **Not in this submission; finale roadmap item.** The APK stays arm64-v8a + x86_64 (the builds that were tested) | `tools/android/patch_ort_jni.py` rewrites 64-bit ELF files only (it reads 64-bit offsets). Adding the ABI would produce a 32-bit library that looks patched but does not load, on devices we cannot test. The README already lists "no 32-bit build" under limitations | Nothing now. For the finale: extend the patch to ELF32, add the ABI to `ABIS` and `abiFilters`, run `device_check.py` on a 32-bit tablet, and only then claim it |
| Nukta in typed Hindi input | **Fixed** (30 Sep) | Typed ड़ (U+095C) and the other precomposed nukta letters are now written as base letter + nukta before the model, exactly as the tablet does. Checked with the pinned IndicTransToolkit: before, `पेड़` reached the model as `पेड\u093C`; after, as `पेड़`. Applied only in `pipeline.translate` (teachers' text). The benchmark path (`pipeline._nmt`) is unchanged, so the published chrF++ numbers stay valid | Nothing; `tests/test_nukta_escape.py` covers it |
| Stale branch `fix/pipeline-import-tests-session-logging` | **Keep its history, take it out of the branch list** | Its 6 commits (VaaniSetu, before the rename) are not in `main` by hash, so deleting would lose them. The cloud session cannot rename or delete branches | GitHub → the repository → **Branches** → the branch → ✏️ **Rename** → `archive/pre-rename-history`. (Do the same for `android-wp4` if you like: it points at `v0.95-submission`, which the tag keeps anyway, so deleting it is safe too) |
| Native review | **Keep every "awaiting native review" label**; ask a Santali speaker before the finale | Claiming review without it would be false. It cannot be decided by us | Before the finale: 20–30 lesson lines through `docs/native_review.md`, then update the labels |
