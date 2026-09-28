# F1 M1 on realme RMP2106 (realme-pad-mini-4gb-android11)

- Date: 2026-09-27. Read from the device: realme RMP2106 (RE87CCL1), Android 11 (SDK 30), RMP2106PU_11.A.24, SoC ums9230 (board ums9230), arm64-v8a, 8 cores, RAM 3.5 GB (MemTotal 3653068 kB); WebView: com.google.android.webview 149.0.7827.91, in use com.google.android.webview 149.0.7827.91.
- APK tested: `app-release.apk` (72.2 MB). Pack: `content-pack-20260927-0057.zip` (37.8 MB): {"lessons": 18, "flashcard_decks": 18, "translations_hi_to_sat": 203, "translations_sat_to_hi": 18, "audio_clips": 427}.
- This check imports the content pack only (no model pack), so the app has no speech or translation engine loaded: the contract cases that need one must answer 503 engine_not_on_device, and they did unless listed as failures. On-device speech and translation are measured separately (tools/android/voice_bench.py, nmt_bench.py).
- Manual steps asked for during the run: none.

| Check | Result |
|---|---|
| Pack import (push + SHA-256 check of every file + install, release build) | 7.0 s |
| REST contract, network on | 24 of 24 cases pass |
| Page in the WebView, airplane mode on (airplane_mode_on=1) | lesson lines listed: yes; line chosen: yes; Translate gave Santali: yes |
| REST contract, airplane mode | 24 of 24 cases pass |
| Typed lesson line from the pack, round trip over adb forward (20 runs) | median 14 ms, max 28 ms |
| Native mic, build under test, through the page (Hindi mic pressed for about 3 s) | 115909 bytes uploaded, about 3.6 s of 16 kHz audio |
| Native mic (MicBridge, 3 s, 16 kHz; debug build of the same code) | 2.92 s of audio, RMS 0.0247, peak 0.708 |
| Peak PSS over all stages (dumpsys meminfo every 1 s, 14 samples): app / WebView renderer / sum | 122 / 179 / **294 MB** |

Santali shown after Translate: ᱵᱟᱨ ᱩᱞ ᱟᱨ ᱯᱮ ᱩᱞ ᱢᱮᱥᱟᱣ ᱢᱮ। ᱡᱚᱛᱚ ᱛᱤᱱᱟᱜ ᱦᱩᱭᱮᱱᱟ? ᱩᱝᱜᱽᱞᱤ ᱨᱮ ᱜᱤᱱᱛᱤ ᱢᱮ।

Notes (added by hand, 27 Sep 2026):

- The tablet was already in airplane mode when this run started (airplane_mode_on=1 throughout), so the "network on" pass also ran with no network: both passes are offline runs.
- Before this run the tablet was in Android Safe mode (all downloaded apps disabled: the launcher could not start the app); a normal restart fixed it. The first run also found that on Android 11 the app could not list an import folder created by adb; `device_check.py` now starts the app first so the app creates the folder, then pushes the pack.
- No screen recording (no filming in this session).
