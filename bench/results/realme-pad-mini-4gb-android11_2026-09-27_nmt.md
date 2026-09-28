# A5 on-device translation: Realme Pad Mini, 4 GB, Android 11

- Device (read from it): RMP2106, Android 11, arm64-v8a, RAM 3.5 GB (MemTotal 3653068 kB). Airplane mode: on. Debug build (benchmark hook). Model pack `model-pack-20260926-2106.zip`.
- Engine: IndicTrans2 indic-indic-dist-320M int8 on ONNX Runtime (Android 1.28), greedy, no-repeat 3-gram, the int8 length cap and stem-loop guard; IndicTransToolkit pre/post-processing and SentencePiece ported to Kotlin (unit tests: identical pre-processing and token ids on 300 of 300 sentences).
- The recogniser is released before translation loads (one large model at a time).

## Same output as the laptop

- The 80 golden sentences (40 Hindi lesson lines, 40 IN22-Conv Santali): tablet output identical to the laptop's int8 output on **65 of 80**.
- IN22-Conv Hindi → Santali, 200 sentences: identical to the laptop's int8 output on 141 of 200.

## Quality (IN22-Conv, Hindi → Santali, CC BY 4.0)

| Engine | n | chrF++ |
|---|---|---|
| Laptop, int8 ONNX (Python) | 200 | 28.75 |
| Tablet, int8 ONNX (Kotlin port) | 200 | **29.00** |

- Difference: +0.25 (the bar: within 0.5).

## Time

- Translation on the tablet, per sentence (IN22-Conv, 200): p50 1.50 s, p90 2.86 s. First sentence (includes loading the model): 7.14 s.
- Peak PSS, phase 1 (translation): app 1172 MB + WebView 148 MB.

| Golden sentence | Laptop | Tablet |
|---|---|---|
| यह चौकोर है। इसके चार कोने हैं। | ᱱᱚᱶᱟ ᱫᱚ ᱢᱤᱫᱴᱟᱝ ᱵᱚᱨᱜᱚ ᱾ ᱱᱚᱶᱟ ᱨᱮᱭᱟᱜ ᱯᱳᱱ ᱠᱳᱱᱟ ᱢᱮᱱᱟᱜᱼᱟ ᱾ | ᱱᱚᱶᱟ ᱫᱚ ᱢᱤᱫᱴᱟᱝ ᱵᱚᱨᱜᱚ ᱴᱚᱴᱷᱟ ᱾ ᱱᱚᱶᱟ ᱨᱮᱭᱟᱜ ᱯᱳᱱ ᱠᱳᱱᱟ ᱢᱮᱱᱟᱜᱼᱟ ᱾ |
| दो आम और तीन आम मिलाओ। कुल कितने हुए? उंगलियों पर गिनो। | ᱵᱟᱨᱭᱟ ᱟᱨ ᱯᱮᱭᱟ ᱟᱢᱚᱞ ᱢᱮ ᱾ ᱜᱩᱴ ᱛᱤᱱᱟᱹᱜ? ᱛᱤ ᱨᱮ ᱜᱤᱭᱩᱱ ᱢᱮ ᱾ | ᱵᱟᱨᱭᱟ ᱟᱨ ᱯᱮᱭᱟ ᱟᱢᱚᱞ ᱢᱮ ᱾ ᱜᱩᱴ ᱛᱤᱱᱟᱹᱜ? ᱛᱤ ᱨᱮ ᱜᱩᱱ ᱢᱮ ᱾ |
| इस शब्द को तीन बार पढ़ो — पानी। | ᱱᱚᱶᱟ ᱥᱟᱵᱟᱫ ᱫᱚ ᱯᱮᱭᱟ ᱚᱠᱛᱮ ᱯᱟᱲᱦᱟᱣ ᱢᱮᱼ ᱫᱟᱜ ᱾ | ᱱᱚᱶᱟ ᱥᱟᱵᱟᱫ ᱫᱚ ᱯᱮᱭᱟ ᱚᱠᱛᱮ ᱧᱮᱞ ᱢᱮᱼ ᱫᱟᱜ ᱾ |
| हवा में उंगली से म लिखो। | ᱦᱚᱭ ᱨᱮ ᱢᱤᱫᱴᱟᱝ ᱯᱷᱤᱝᱜᱟᱨ ᱛᱮ ᱚᱞ ᱢᱮ ᱾ | ᱦᱚᱭ ᱨᱮ ᱢᱤᱫᱴᱟᱝ ᱯᱷᱤᱝᱜᱟᱨ ᱛᱮ ᱤᱧ ᱚᱞ ᱢᱮ ᱾ |
| ᱜᱚ, ᱜᱟᱯᱟ ᱢᱚᱵᱷᱤ ᱧᱮᱞᱵᱚᱱ ᱪᱚᱞᱚᱜᱼᱟ ᱾ | हां, भगवान की प्यारी प्यारी लग रही है। | हाँ, मेरी प्यारी प्यारी लग रही है। |
| ᱟᱵᱩ ᱫᱚ ᱥᱤᱱᱟᱹᱢᱟ ᱧᱮᱞ ᱪᱟᱞᱟᱜᱽ ᱨᱮᱭᱟᱜ ᱵᱩᱱ ᱯᱞᱟᱱ ᱫᱟᱲᱤᱭᱟᱜᱽᱼᱟ ! | अबू को सिनेमा देखने के लिए एक विस्तृत परियोजना की आवश्यकता है! | अबू को सिनेमा देखने के लिए एक योजना बनाने की अनुमति है! |
| ᱱᱤᱭᱟᱹ ᱢᱟᱸᱦᱟ ᱫᱚ ᱡᱟᱣᱥᱮᱨᱢᱟ ᱰᱚᱠᱴᱚᱨ ᱵᱤᱹ ᱟᱨ ᱟᱢᱵᱮᱫᱠᱟᱨᱟᱜᱽ ᱡᱟᱱᱟᱢ ᱢᱟᱸᱦᱟ ᱞᱮᱠᱟᱛᱮ ᱢᱟᱱᱟᱜᱽᱠᱟᱱᱟ ᱾ | यह रक्त प्रतिवर्ष डॉ. बी. आर. अम्बेडकर के जन्म के रक्त के रूप में बड़ा होता है। | यह रक्त प्रतिवर्ष डॉ. बी. आर. अम्बेडकर के जन्म के रक्त के रूप में महत्वपूर्ण है। |
| ᱱᱤᱛᱚᱜᱽᱤᱧ ᱫᱤᱥᱟᱹᱭᱮᱫᱟ ! | आज आप मुझे सलाह देंगे! | आज आप मुझे सलाह देते हैं! |

## Note: not identical to the laptop on this device (added by hand, 27 Sep 2026)

On the x86_64 emulator the tablet's output equalled the laptop's int8 output on 80 of 80 golden and 1502 of 1503 IN22-Conv sentences. On this ARM64 tablet it is 65 of 80 and 141 of 200: the bar "identical to the laptop" is **not met** on this device. Quality on the same 200 sentences is not lower (chrF++ 29.00 vs 28.75). The cause is **not verified**; the likely one is that ONNX Runtime's ARM64 int8 kernels round differently from the x86 ones, so greedy decoding sometimes picks a different token. The Kotlin pre-processing and token ids are covered by unit tests (300 of 300), which run on the laptop JVM, not on ARM.
