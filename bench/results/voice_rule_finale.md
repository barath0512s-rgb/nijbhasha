# Finale voice rule: C4 Santali voice vs Piper (ASR round-trip CER)

- Rule: `docs/voice_rule_finale.md` (fixed 27 Sep 2026, before any finale data). Pack `content-pack-20260927-0057.zip`: 224 Santali lines; held-out half (SHA-1 of the text odd): **112 lines**, scored once.
- Ours: the C4 voice (`notebooks/santali_voice.ipynb`, Kaggle; one IndicVoices-R Santali speaker, 0.6 h) as fp32 ONNX via onnxruntime, Ol Chiki -> Odia script; Piper: the pack's own audio. Recogniser: IndicConformer 600M (hub). CER after `normalize_for_wer`, spaces removed. **A proxy for intelligibility; native listener ratings: NOT MEASURED.**
- One synthesis per line, VITS noise seeded (20260928).

| Held-out pack lines | Piper | Ours |
|---|---|---|
| CER mean | 0.445 | 0.788 |
| CER median | 0.272 | 0.705 |
| Failure rate (CER > 0.5) | 0.214 (24 of 112) | 0.768 (86 of 112) |
| Audio | 268.6 s | 374.1 s |

Conditions: mean lower by >= 0.02: False; median not higher: False; failure rate not higher: False; MOS-lite clear not lower: n/a (no native listener scores)

**Decision (by the rule): keep Piper.**

Not part of the rule: the 20 held-out recordings' texts (never used in training), Piper synthesised by the app:
Piper CER mean 0.271, median 0.248, failures 2 of 20; Ours mean 0.584, median 0.564, failures 13 of 20 (the rule's conditions on this set: not all hold).
- Run time 386.3 s.
