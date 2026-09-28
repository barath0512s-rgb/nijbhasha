# FLN translation sample: real hub output, automatic checks

Made by `tools/fln_sample_report.py` from the content pack the laptop hub built on 26 Sep 2026 (IndicTrans2 indic-indic 320M, ONNX fp32, greedy; teacher corrections and the glossary answer first). Nothing re-translated here. **Accuracy is not measured: no native speaker has reviewed these lines.**

## Checks over every lesson line in the pack

- Lesson lines with a Santali translation: **119** (distinct Hindi lines, 18 lessons).
- Source layer: cached 62, glossary 17, model 39, teacher 1.
- Script: **106 of 119** are Ol Chiki letters only (no letter from another script): exceptions below.
- Numbers: 57 lines have a Hindi number; the Santali has a number (Ol Chiki digit or a Santali number word) in **56** of them.
- Round-trip caution flag (A3): **32** of 119 lines (shown with ⚠️ and not auto-played).
- Script guard (added 28 Sep, `nmt_guard.foreign_letters`): flags every line with a non-Ol Chiki letter; of the 13 such lesson lines, **6** had passed the round-trip check unflagged. The tablet applies the guard to pack lines at once; the hub applies it to new model output (rebuild the content pack to carry the flags).

### Lines with a non-Ol Chiki letter

| Hindi | Santali | Letters |
|---|---|---|
| एक गाँव में एक प्यासी चिड़िया थी। | ᱢᱤᱫᱴᱟᱝ ᱟᱛᱳ ᱨᱮ ᱢᱤᱫᱴᱟᱝ ᱠᱷᱮᱹᱞᱚᱜ ᱠᱟᱱ ꯎꯆꯦꯛ ᱛᱟᱦᱮᱸ ᱠᱟᱱᱟ ᱾ | ꯎꯆꯛ |
| चिड़िया ने घड़े में छोटे पत्थर डाले। | ꯎꯆꯦꯛ ᱫᱚ ᱞᱚᱫᱚᱢ ᱨᱮ ᱦᱩᱰᱤᱧ ᱚᱛᱢᱚᱱ ᱠᱚ ᱫᱚᱦᱚ ᱞᱮᱫᱟ ᱾ | ꯎꯆꯛ |
| पानी ऊपर आ गया और चिड़िया ने पानी पिया। | ᱫᱟᱜ ᱪᱮᱛᱟᱱ ᱨᱮ ᱦᱮᱡ ᱮᱱᱟ ᱟᱨ ꯎꯆꯦꯛ ᱫᱚ ᱫᱟᱜ ᱮ ᱦᱟᱛᱟᱣ ᱞᱮᱫᱟ ᱾ | ꯎꯆꯛ |
| चिड़िया को क्या चाहिए था? | ꯎꯆꯦꯛ ᱫᱚ ᱪᱮᱫ ᱮ ᱠᱷᱚᱡ ᱞᱮᱫᱟ? | ꯎꯆꯛ |
| सोनू हर सुबह स्कूल जाता है। | ᱥᱳᱱᱩ ᱡᱚᱛᱚ صبح ᱜᱮ ᱵᱤᱨᱫᱟᱹᱜᱟᱲ ᱨᱮᱭ ᱥᱮᱱᱚᱜᱼᱟ ᱾ | صبح |
| सोनू हर सुबह कहाँ जाता है? | ᱥᱳᱱᱩ ᱡᱚᱛᱚ صبحᱮ ᱪᱮᱫ ᱥᱮᱫ ᱮ ᱥᱮᱱᱚᱜᱼᱟ? | صبح |
| हर अंक की एक जगह होती है: इकाई, दहाई, सैकड़ा और हज़ार। | ᱡᱚᱛᱚ پوائنٹس ᱨᱮᱭᱟᱜ ᱢᱤᱫᱴᱟᱝ ᱴᱷᱟᱶ ᱢᱮᱱᱟᱜᱼᱟ ᱤᱭᱩᱱᱤᱴ, ᱵᱟᱨ ᱥᱟᱭ ᱥᱟᱭ ᱥᱟᱭ ᱜᱮᱞ ᱥᱟᱭ ᱥᱟᱭ ᱟᱭ ᱾ | پوائنٹس |
| 4 सैकड़े की जगह पर है, 2 दहाई की जगह पर और 5 इकाई की जगह पर। | 4 ᱥᱟᱭ ᱥᱟᱭ ᱥᱟᱭ ᱰᱟᱣᱩᱱ ᱰᱟᱣᱚᱱ ᱰᱟᱣᱩ ᱰᱟᱣᱤᱱ ᱰᱟᱣᱮᱱ ᱰᱟᱣᱱ ᱰᱟᱣꯟ ᱰᱟᱣᱳᱱ ᱰᱟᱣون ᱰᱟᱣᱩᱱᱰ ᱰᱟᱣᱩᱱᱤᱴ ᱰᱟᱣୂନ ᱰᱟᱣᱩᱢ ᱰᱟᱣᱩᱴ ᱰᱟᱣᱟᱣᱩᱱᱰ ᱰᱟᱣᱚᱞ ᱰᱟᱣᱩᱱᱩ ᱰᱟᱣun ᱰᱟᱣᱟᱱ ᱰᱟᱣᱧ ᱰᱟᱣᱟᱹᱲ ᱰᱟᱣ ᱾ | ꯟونନun |
| हर सुबह वह अपनी दादी के साथ तालाब पर जाती है। | ᱡᱚᱛᱚ صبح ᱜᱮ ᱩᱱᱤ ᱫᱚ ᱟᱡ ᱟᱭᱳ ᱥᱟᱶᱛᱮ ᱞᱚᱫᱚᱢ ᱨᱮ ᱥᱮᱱᱚᱜᱼᱟ ᱾ | صبح |
| आज रविवार है। | ᱛᱮᱦᱮᱧ ᱫᱚ اتوار ᱾ | اتور |
| एक पेड़ पर दो चिड़ियाँ बैठी थीं। | ᱢᱤᱫᱴᱟᱝ ᱫᱟᱨᱮ ᱨᱮ ᱵᱟᱨᱭᱟ ꯎꯆꯦꯛ ᱠᱚ ᱛᱟᱦᱮᱸ ᱠᱟᱱᱟ ᱾ | ꯎꯆꯛ |
| मीना ने चिड़ियों को दाना दिया। | ᱢᱮᱱᱟ ꯎꯆꯦꯛ ᱠᱚ ᱞᱟᱹᱜᱤᱫ ᱡᱚᱢᱟᱜ ᱮ ᱮᱢ ᱞᱮᱫᱟ ᱾ | ꯎꯆꯛ |
| पेड़ पर कितनी चिड़ियाँ बैठी थीं? | ᱵᱤᱨ ᱨᱮ ᱛᱤᱱᱟᱹᱜ ᱜᱚᱴᱟᱝ ꯎꯆꯦꯛ ᱠᱚ ᱛᱟᱦᱮᱸ ᱠᱟᱱᱟ? | ꯎꯆꯛ |

### Number in the Hindi, none found in the Santali (to check: it may be written as a word the check does not know)

| Hindi | Santali |
|---|---|
| हर वाक्य में चार शब्द हैं। | ᱥᱟᱱᱟᱢ ᱵᱚᱨᱱᱚᱱ ᱨᱮ ᱯᱳᱱ ᱜᱚᱴᱟᱝ ᱵᱚᱨᱱᱚᱱ ᱢᱮᱱᱟᱜᱼᱟ ᱾ |

## Sample of 26 lines

Tier: A written by people (the team's glossary or a teacher's correction; native review pending), B model output with no warning, C model output flagged by the round-trip check.

| # | Kind | Hindi (teacher) | Santali (Ol Chiki) | Reading guide (Devanagari) | Source | Tier |
|---|---|---|---|---|---|---|
| 1 | lesson script | यह शब्द है — माँ। इसे पढ़ो। | ᱱᱚᱶᱟ ᱟᱲᱟᱝ ᱠᱟᱱᱟ — ᱟᱭᱳ। ᱱᱚᱶᱟ ᱯᱟᱲᱦᱟᱣ ᱢᱮ। | नॉवा आड़ां काना — आयो। नॉवा पाड़्हाव् मे। | glossary | A |
| 2 | lesson script | शाबाश, तुमने अच्छा गिना। | ᱥᱟᱵᱟᱥ, ᱟᱢ ᱟᱹᱰᱤ ᱱᱟᱯᱟᱭ ᱛᱮ ᱞᱮᱠᱷᱟ ᱟᱠᱟᱫᱟ ᱾ | साबास्, आम् अडि नापाय् ते लेखा आकादा। | cached | C |
| 3 | lesson script | आज हम चीज़ों को क्रम से रखना सीखेंगे। | ᱛᱮᱦᱮᱧ ᱟᱢ ᱡᱤᱱᱤᱥ ᱠᱚ ᱵᱚᱱᱚᱫᱚᱞ ᱨᱮ ᱫᱚᱦᱚ ᱥᱮᱪ ᱢᱮ ᱾ | तेहेञ् आम् जिनिस् कॉ बॉनॉदॉल् रे दॉहॉ सेच् मे। | cached | B |
| 4 | lesson script | यह छोटी गेंद है और यह बड़ी गेंद है। | ᱱᱚᱶᱟ ᱫᱚ ᱢᱤᱫᱴᱟᱝ ᱦᱩᱰᱤᱧ ᱵᱚᱞ ᱟᱨ ᱱᱚᱶᱟ ᱫᱚ ᱢᱟᱨᱟᱝ ᱵᱚᱞ ᱾ | नॉवा दॉ मित्टां हुडिञ् बॉल् आर् नॉवा दॉ मारां बॉल्। | cached | B |
| 5 | lesson script | आज हम अक्षर म सीखेंगे। | ᱛᱮᱦᱮᱧ ᱟᱢ ᱚᱞᱼᱵᱩᱴᱟᱹ ᱠᱚ ᱥᱮᱪ ᱢᱮ ᱾ | तेहेञ् आम् ऑल्बुट कॉ सेच् मे। | cached | B |
| 6 | lesson script | म की ध्वनि है म। | ᱤᱧᱟᱹᱜ ᱥᱮᱨᱮᱧ ᱫᱚ ᱦᱩᱭᱩᱜ ᱠᱟᱱᱟ ᱤᱧ ᱾ | इञक् सेरेञ् दॉ हुयुक् काना इञ्। | cached | C |
| 7 | activity instruction | अपनी उंगलियां दिखाओ और मेरे साथ गिनो। | ᱟᱢᱟᱜ ᱩᱝᱜᱽᱞᱤ ᱫᱮᱠᱷᱟᱣ ᱢᱮ ᱟᱨ ᱟᱢᱟᱜ ᱥᱟᱝ ᱜᱤᱱᱛᱤ ᱢᱮ। | आमाक् उंग्लि देखाव् मे आर् आमाक् सां गिन्ति मे। | glossary | A |
| 8 | activity instruction | अपने आसपास गोल चीज़ें ढूंढो। | ᱟᱢᱟᱜ ᱥᱩᱨ ᱨᱮ ᱜᱚᱞ ᱡᱤᱱᱤᱥ ᱯᱟᱱᱛᱮ ᱢᱮ। | आमाक् सुर् रे गॉल् जिनिस् पान्ते मे। | glossary | A |
| 9 | activity instruction | सबसे छोटी चीज़ पहले रखो। | ᱯᱳᱭᱞᱳ ᱨᱮ ᱦᱩᱰᱤᱧ ᱡᱤᱱᱤᱥ ᱠᱚ ᱫᱚᱦᱚ ᱢᱮ ᱾ | पोय्लो रे हुडिञ् जिनिस् कॉ दॉहॉ मे। | model | C |
| 10 | activity instruction | उसके बाद उससे बड़ी चीज़ रखो। | ᱚᱱᱟ ᱛᱟᱭᱚᱢ ᱚᱱᱟ ᱠᱷᱚᱱ ᱢᱟᱨᱟᱝ ᱠᱤᱪᱷᱩ ᱫᱚᱦᱚ ᱢᱮ ᱾ | ऑना तायॉम् ऑना खॉन् मारां किछु दॉहॉ मे। | model | C |
| 11 | activity instruction | सबसे बड़ी चीज़ आखिर में रखो। | ᱢᱩᱪᱟᱹᱫ ᱨᱮ ᱡᱚᱛᱚ ᱠᱷᱚᱱ ᱢᱟᱨᱟᱝ ᱫᱚ ᱫᱚᱦᱚ ᱢᱮ ᱾ | मुचत् रे जॉतॉ खॉन् मारां दॉ दॉहॉ मे। | model | C |
| 12 | activity instruction | हवा में उंगली से म लिखो। | ᱦᱚᱭ ᱨᱮ ᱢᱤᱫᱴᱟᱝ ᱯᱷᱤᱝᱜᱟᱨ ᱛᱮ ᱚᱞ ᱢᱮ ᱾ | हॉय् रे मित्टां फिंगार् ते ऑल् मे। | model | B |
| 13 | assessment prompt | यहाँ कितने पत्थर हैं? बताओ। | ᱱᱮᱞᱮ ᱡᱚᱛᱚ ᱫᱷᱤᱨᱤ ᱢᱮᱱᱟᱜᱼᱟ? ᱞᱟᱹᱭ ᱢᱮ। | नेले जॉतॉ धिरि मेनाक्आ? लय् मे। | glossary | A |
| 14 | assessment prompt | यह कौन सा आकार है? | ᱱᱚᱶᱟ ᱚᱠᱟ ᱪᱤᱛᱟᱹᱨ ᱠᱟᱱᱟ? | नॉवा ऑका चितर् काना? | glossary | A |
| 15 | assessment prompt | तीन और चार कितने होते हैं? | ᱯᱮ ᱟᱨ ᱯᱩᱱ ᱡᱚᱛᱚ ᱦᱩᱭᱩᱜᱼᱟ? | पे आर् पुन् जॉतॉ हुयुक्आ? | glossary | A |
| 16 | assessment prompt | यह शब्द क्या है? पढ़कर बताओ। | ᱱᱚᱶᱟ ᱟᱲᱟᱝ ᱪᱮᱫ ᱠᱟᱱᱟ? ᱯᱟᱲᱦᱟᱣ ᱠᱟᱛᱮ ᱞᱟᱹᱭ ᱢᱮ। | नॉवा आड़ां चेत् काना? पाड़्हाव् काते लय् मे। | glossary | A |
| 17 | assessment prompt | आठ में से पांच घटाओ। उत्तर क्या है? | ᱤᱨᱟᱹᱞ ᱠᱷᱚᱱ ᱢᱚᱬᱮ ᱠᱚᱢ ᱢᱮ। ᱛᱮᱞᱟ ᱪᱮᱫ ᱠᱟᱱᱟ? | इरल् खॉन् मॉणे कॉम् मे। तेला चेत् काना? | glossary | A |
| 18 | assessment prompt | मेज़ पर कितने पत्थर हैं? | ᱴᱮᱵᱤᱞ ᱨᱮ ᱛᱤᱱᱟᱹᱜ ᱜᱟᱱ ᱫᱷᱤᱨᱤ ᱢᱮᱱᱟᱜᱼᱟ? | टेबिल् रे तिनक् गान् धिरि मेनाक्आ? | model | B |
| 19 | numbers | आज हम एक से दस तक गिनना सीखेंगे। | ᱛᱮᱦᱮᱸᱡ ᱟᱞᱮ ᱢᱤᱫ ᱠᱷᱚᱱ ᱜᱮᱞ ᱛᱩᱨᱩᱭ ᱜᱤᱱᱛᱤ ᱥᱮᱪᱮᱫᱟ। | तेहेँच् आले मित् खॉन् गेल् तुरुय् गिन्ति सेचेदा। | glossary | A |
| 20 | numbers | अब तुम्हारे सामने पांच पत्थर हैं। उन्हें गिनो। | ᱱᱤᱛᱚᱜ ᱟᱢᱟᱜ ᱠᱷᱚᱱ ᱢᱚᱬᱮ ᱫᱷᱤᱨᱤ ᱢᱮᱱᱟᱜᱼᱟ। ᱱᱤᱭᱟᱹ ᱜᱤᱱᱛᱤ ᱢᱮ। | नितॉक् आमाक् खॉन् मॉणे धिरि मेनाक्आ। निय गिन्ति मे। | glossary | A |
| 21 | numbers | यह गोल है। यह एक वृत्त है। | ᱱᱚᱶᱟ ᱜᱚᱞ ᱠᱟᱱᱟ। ᱱᱚᱶᱟ ᱢᱤᱫ ᱜᱚᱞ ᱪᱤᱛᱟᱹᱨ ᱠᱟᱱᱟ। | नॉवा गॉल् काना। नॉवा मित् गॉल् चितर् काना। | glossary | A |
| 22 | numbers | यह चौकोर है। इसके चार कोने हैं। | ᱱᱚᱶᱟ ᱪᱟᱩᱠᱟ ᱠᱟᱱᱟ। ᱱᱚᱶᱟ ᱨᱮᱭᱟᱜ ᱯᱩᱱ ᱠᱩᱱᱟᱹ ᱢᱮᱱᱟᱜᱼᱟ। | नॉवा चाउका काना। नॉवा रेयाक् पुन् कुन मेनाक्आ। | glossary | A |
| 23 | numbers | आज हम जोड़ना सीखेंगे। एक और एक मिलाओ। | ᱛᱮᱦᱮᱸᱡ ᱟᱞᱮ ᱡᱚᱲᱟᱣ ᱥᱮᱪᱮᱫᱟ। ᱢᱤᱫ ᱟᱨ ᱢᱤᱫ ᱢᱮᱥᱟᱣ ᱢᱮ। | तेहेँच् आले जॉड़ाव् सेचेदा। मित् आर् मित् मेसाव् मे। | teacher | A |
| 24 | numbers | दो आम और तीन आम मिलाओ। कुल कितने हुए? उंगलियों पर गिनो। | ᱵᱟᱨ ᱩᱞ ᱟᱨ ᱯᱮ ᱩᱞ ᱢᱮᱥᱟᱣ ᱢᱮ। ᱡᱚᱛᱚ ᱛᱤᱱᱟᱜ ᱦᱩᱭᱮᱱᱟ? ᱩᱝᱜᱽᱞᱤ ᱨᱮ ᱜᱤᱱᱛᱤ ᱢᱮ। | बार् उल् आर् पे उल् मेसाव् मे। जॉतॉ तिनाक् हुयेना? उंग्लि रे गिन्ति मे। | glossary | A |
| 25 | numbers | मेज़ पर तीन पत्थर हैं। | ᱴᱮᱵᱤᱞ ᱨᱮ ᱯᱮᱭᱟ ᱫᱷᱤᱨᱤ ᱢᱮᱱᱟᱜᱼᱟ ᱾ | टेबिल् रे पेया धिरि मेनाक्आ। | cached | C |
| 26 | numbers | अपनी उंगलियों पर पाँच तक गिनो। | ᱟᱢᱟᱜ ᱛᱤ ᱨᱮ ᱢᱚᱬᱮ ᱜᱚᱴᱟᱝ ᱫᱷᱟᱹᱵᱤᱡ ᱜᱤᱭᱩᱱ ᱢᱮ ᱾ | आमाक् ति रे मॉणे गॉटां धबिच् गियुन् मे। | model | C |

Public benchmarks for the model alone (not these lines): chrF++ Hindi → Santali 31.3 (IN22-Gen), 32.2 (IN22-Conv), 27.4 (FLORES-200), `eval/results/benchmarks.md`.
