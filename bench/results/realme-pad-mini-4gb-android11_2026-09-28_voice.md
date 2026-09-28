# A1 on-device voice for lesson lines: Realme Pad Mini, 4 GB, Android 11, 2 threads

- Device (read from it): realme RMP2106, Android 11 (SDK 30), arm64-v8a, RAM 3.5 GB (MemTotal 3653068 kB), 8 cores. Airplane mode: on.
- Build: **debug APK** (the benchmark hook exists only in debug builds; same native libraries and models as release). sherpa-onnx 1.13.8, int8 IndicConformer 120M (Hindi CTC, Santali transducer), 2 threads, one recogniser loaded at a time; Piper hi voice for synthesis.
- Thresholds: {'hi': 0.9, 'sat': 0.95} (bench/results/lesson_match.md). Clips: the test half of the laptop tuning set (synthetic lesson lines in the pack's own audio; non-lesson: public real clips and near-miss sentences).
- Runs on the tablet; the laptop only sent the clips and was idle. Release candidate 0.95-rc2's debug build.
- **How this run went (28 Sep):** the first run completed all 130 clips and the synthesis lines but crashed writing result.json (Android 11 refused the app a file in a folder made by adb; `voice_bench.py` now lets the app make its own). The second run's tool stopped on a single empty `pidof` answer while the app kept running (`device_check.app_alive` now needs three); its result was pulled after the tablet logged "voice_bench done". The recognisers were loaded fresh in this run (a new app process).

## Hindi lesson line → Santali

- **Parity with the laptop:** device transcript identical to the laptop's on **87 of 90** clips.
- Matching on the device: precision **0.980** (50 of 51 accepted), recall **0.833** (50 of 60 lesson lines); non-lesson clips accepted: 1 of 30.

- **Voice to voice, matched lesson lines (n = 50): p50 0.70 s, p90 1.20 s** (WAV handed to the app → reply with its audio file ready; playback start not included). Audio from: ['pack'].

| Clip | Laptop | Device |
|---|---|---|
| hi_f8019d8b37e8_pack | दो आम और तीन आम मिलाओ कुल कितने हुए ऊंगलियों पर गिनो | दो आम और तीन आम मिलाओ कुल कितने हुए ंगलियों पर गिनो |
| hi_neg_c00a258292f1 | फ़ोटोग्राफ़रों ने बाद में एक वृद्ध महिला की जगह ले ली क्योंकि उसे शौचालय जाना ज़रूरी था मेंडोज़ा को गोली मार दी गई थी | फ़ोटोग्राफ़रों ने बाद में एक वृद्ध महिला की जगह ले ली क्योंकि उसे शौचालय जाना ज़रूरी था मडोज़ा को गोली मार दी गई थी |
| hi_neg_34a955d4591d | लखा सिंह ने छप्पन बोग भजन भी प्रस्तुत किए गायक राजू खंडेलवाल उनके साथ थे | लक्खा सिंह ने छप्पन भोग भजन भी प्रस्तुत किए गायक राजू खंडेलवाल उनके साथ थे |

## Santali line → Hindi

- **Parity with the laptop:** device transcript identical to the laptop's on **34 of 40** clips.
- Matching on the device: precision **1.000** (4 of 4 accepted), recall **0.160** (4 of 25 lesson lines); non-lesson clips accepted: 0 of 15.

- **Voice to voice, matched lesson lines (n = 4): p50 0.48 s, p90 0.70 s** (WAV handed to the app → reply with its audio file ready; playback start not included). Audio from: ['pack'].

| Clip | Laptop | Device |
|---|---|---|
| sat_47e4e6bc2425_pack | ᱢᱤᱥᱟᱵᱟᱫᱽ ᱠᱷᱚᱱ ᱮᱛᱚᱠᱟ | ᱢᱤᱥ ᱥᱟᱵᱟᱫ ᱠᱷᱚᱱ ᱮᱛᱚ ᱠᱟᱜ ᱾ |
| sat_7c047f62c5f7_pack | ᱮᱠᱥᱮᱨᱟᱱ ᱨᱤᱭᱟᱜ ᱥᱮᱨᱮᱧ ᱟᱢ ᱪᱮᱫ ᱵᱟᱰᱟᱭᱟᱢᱟ | ᱮᱠᱥᱮᱨᱚ ᱨᱤᱭᱟᱜ ᱥᱮᱨᱮᱧ ᱟᱢ ᱪᱮᱫ ᱵᱟᱰᱟᱭᱟᱢᱟ |
| sat_d07595e37fdf_pack | ᱛᱮ ᱵᱚᱥᱞᱟ ᱨᱮ ᱵᱟᱲᱦᱟᱣ ᱠᱟᱛᱮ ᱪᱮᱫ ᱞᱮᱠᱟᱛᱮ ᱪᱟᱥ ᱠᱚᱨᱡᱟᱵᱟ | ᱛᱮ ᱟᱵᱚ ᱥᱞᱟ ᱨᱮ ᱵᱟ ᱯᱟᱲᱦᱟᱣ ᱠᱚ ᱪᱮᱫ ᱞᱮᱠᱟᱛᱮ ᱪᱟᱥ ᱠᱚᱨᱡᱟᱵᱟ |
| sat_conv_f6b89b3ca166 | ᱦᱮᱸ ᱤᱧ ᱚᱸᱰᱮᱧ ᱯᱟᱲᱦᱟᱣ ᱟᱠᱟᱱᱟ | ᱦᱮᱸ ᱤᱧ ᱚᱱᱰᱮ ᱯᱟᱲᱦᱟᱣ ᱟᱠᱟᱱᱟ |
| sat_conv_e77b4bf9815d | ᱤᱱᱟᱹ ᱠᱮᱫ ᱦᱚᱢᱫᱮᱥ ᱦᱤᱡᱩᱜ ᱠᱟᱱᱟ ᱢᱚᱪᱟ ᱫᱷᱟᱣ ᱪᱮᱫ ᱞᱮᱠᱟᱛᱮ ᱯᱚᱪᱷᱤᱢ ᱵᱟᱝᱞᱟ ᱫᱚ ᱴᱮᱯᱞᱟᱹᱣ ᱠᱚ ᱩᱫᱩᱜ ᱥᱚᱫᱚᱨ ᱞᱮᱫᱟ | ᱤᱱᱟᱹ ᱠᱱᱮᱛ ᱦᱚᱢᱫᱮᱥ ᱦᱤᱡᱩᱜ ᱠᱟᱱᱟ ᱢᱚᱪᱟ ᱫᱷᱟᱣ ᱪᱮᱫ ᱞᱮᱠᱟᱛᱮ ᱯᱚᱪᱷᱤᱢ ᱵᱟᱝᱞᱟ ᱫᱚ ᱴᱮᱯᱞᱟᱹᱣ ᱠᱚ ᱩᱫᱩᱜ ᱥᱚᱫᱚᱨ ᱞᱮᱫᱟ |

## Spoken Santali answers (child → grade → Hindi feedback)

- Graded as expected: **9 of 16** (right answers green, wrong answers not green). Hindi feedback audio returned: 16 of 16. Time per answer (recognition + grading + feedback audio): p50 0.20 s, p90 0.47 s (n = 16; the first includes loading the Santali model; the Hindi feedback audio may have come from the cache the first run filled).

| Answer | Said | Heard | Grade | Expected |
|---|---|---|---|---|
| ans_0_imp_67cb986ab3_6_right | ᱯᱮ | ᱴᱷᱤᱠ | yellow | green |
| ans_0_imp_67cb986ab3_6_wrong | ᱵᱤᱨᱫᱟᱹᱜᱟᱲ | ᱵᱤᱨᱫᱟᱹᱜᱟᱲ | yellow | not green |
| ans_3_imp_e065e91dbc_5_right | ᱵᱤᱨᱫᱟᱹᱜᱟᱲ | ᱵᱤᱨᱫᱟᱹᱜᱟᱲ | green | green |
| ans_3_imp_e065e91dbc_5_wrong | ᱯᱮ | ᱯᱮ | yellow | not green |
| ans_3_imp_46b74c74d2_10_right | ᱢᱤᱥ | ᱢᱮᱥ | yellow | green |
| ans_3_imp_46b74c74d2_10_wrong | ᱯᱮ | ᱴᱷᱤᱠ | yellow | not green |
| ans_2_imp_8835da564c_7_right | ᱫᱟᱜ | ᱰᱟᱠ | yellow | green |
| ans_2_imp_8835da564c_7_wrong | ᱯᱮ | ᱴᱷᱤᱠ | yellow | not green |
| ans_0_imp_223bee4bcc_6_right | ᱯᱮ | ᱯᱤᱪ | yellow | green |
| ans_2_imp_8835da564c_6_right | ᱫᱷᱤᱨᱤ | ᱫᱷᱤᱨᱤ | green | green |
| ans_2_imp_a96a02bca0_10_right | ᱵᱟᱨ | ᱵᱟᱨ | green | green |
| ans_3_imp_5c91c0c1bb_7_right | ᱱᱟᱶᱟ ᱜᱮᱞ ᱜᱮᱞ ᱜᱮᱞ ᱥᱮᱨᱢᱟ | ᱱᱟᱣᱟ ᱜᱮᱞ ᱜᱮᱞ ᱜᱮᱞ ᱥᱮᱨᱢᱟ | yellow | green |
| ans_0_imp_223bee4bcc_5_right | ᱢᱤᱫ | ᱢᱮᱛᱷᱟᱹᱲ | yellow | green |
| ans_3_imp_e065e91dbc_6_right | ᱵᱟᱨ | ᱵᱟᱨ | green | green |
| ans_2_imp_acb593a491_5_right | ᱢᱤᱫ ᱥᱟᱭ ᱵᱟᱨ ᱥᱟᱭ ᱥᱟᱭ ᱥᱟᱭ ᱜᱮᱞ ᱜᱮᱞ ᱜᱮᱞ ᱥᱟᱭ ᱥᱟᱭ ᱢᱤᱫ ᱥᱟᱭ ᱥᱟᱭ ᱵᱟᱨ ᱜᱮᱞ ᱜᱮᱞ ᱢᱤᱫ ᱥᱟᱭ ᱜᱮᱞ ᱥᱟᱭ ᱜᱮᱞ ᱢᱤᱫ ᱜᱮᱞ ᱜᱮᱞ ᱵᱟᱨ ᱜᱮᱞ ᱥᱟᱭ | ᱢᱤᱫ ᱥᱟᱭ ᱵᱟᱨ ᱥᱟᱭ ᱥᱟᱭ ᱥᱟᱭ ᱜᱮᱞ ᱜᱮᱞ ᱜᱮᱞ ᱥᱟᱭ ᱥᱟᱭ ᱢᱮᱥᱟᱭ ᱥᱟᱭ ᱵᱟᱨ ᱜᱮᱞ ᱜᱮᱞ ᱢᱤᱫ ᱥᱟᱭ ᱜᱮᱞ ᱥᱟᱭ ᱜᱮᱞ ᱢᱤᱫ ᱜᱮᱞ ᱜᱮᱞ ᱵᱟᱨ ᱜᱮᱞ ᱥᱟᱭ | yellow | green |
| ans_3_imp_2a190b718f_5_right | ᱤᱨᱟᱹᱞ | ᱤᱨᱟᱹᱞ | green | green |

- On-device synthesis, sat lines with no pack audio: **NOT MEASURED in this run** (the lines were synthesised and cached by the first, crashed run, so this run's 0.00 s is the cache).
- On-device synthesis, hi lines with no pack audio: **NOT MEASURED in this run** (cached by the first run, as above).

## Memory

- **Peak PSS: app 481 MB** (in-app, Debug.getPss after each call). The dumpsys sampler (app + WebView renderer) stopped with the tool, so the renderer and the sum are **NOT MEASURED** in this run. During the run the recogniser for one language and the synthesis voice are loaded.
