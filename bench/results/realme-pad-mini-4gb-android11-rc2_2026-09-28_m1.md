# F1 M1 on realme RMP2106 (realme-pad-mini-4gb-android11-rc2)

- Date: 2026-09-28. Read from the device: realme RMP2106 (RE87CCL1), Android 11 (SDK 30), RMP2106PU_11.A.24, SoC ums9230 (board ums9230), arm64-v8a, 8 cores, RAM 3.5 GB (MemTotal 3653068 kB); WebView: com.google.android.webview 153.0.8010.36, in use com.google.android.webview 153.0.8010.36.
- APK tested: `app-release.apk` (72.2 MB). Pack: `content-pack-20260927-0057.zip` (37.8 MB): {"lessons": 18, "flashcard_decks": 18, "translations_hi_to_sat": 203, "translations_sat_to_hi": 18, "audio_clips": 427}.
- This check imports the content pack only (no model pack), so the app has no speech or translation engine loaded: the contract cases that need one must answer 503 engine_not_on_device, and they did unless listed as failures. On-device speech and translation are measured separately (tools/android/voice_bench.py, nmt_bench.py).
- Manual steps asked for during the run: none.

| Check | Result |
|---|---|
| Pack import (push + SHA-256 check of every file + install, release build) | 6.9 s |
| REST contract, network on | 24 of 24 cases pass |
| Page in the WebView, airplane mode on (airplane_mode_on=1) | lesson lines listed: yes; line chosen: yes; Translate gave Santali: yes |
| REST contract, airplane mode | 24 of 24 cases pass |
| Typed lesson line from the pack, round trip over adb forward (20 runs) | median 17 ms, max 30 ms |
| Native mic, build under test, through the page (Hindi mic pressed for about 3 s) | 117189 bytes uploaded, about 3.6 s of 16 kHz audio |
| Native mic (MicBridge, 3 s, 16 kHz; debug build of the same code) | 2.92 s of audio, RMS 0.0225, peak 0.708 |
| Peak PSS over all stages (dumpsys meminfo every 1 s, 15 samples): app / WebView renderer / sum | 131 / 183 / **304 MB** |

Santali shown after Translate: ᱵᱟᱨ ᱩᱞ ᱟᱨ ᱯᱮ ᱩᱞ ᱢᱮᱥᱟᱣ ᱢᱮ। ᱡᱚᱛᱚ ᱛᱤᱱᱟᱜ ᱦᱩᱭᱮᱱᱟ? ᱩᱝᱜᱽᱞᱤ ᱨᱮ ᱜᱤᱱᱛᱤ ᱢᱮ।
