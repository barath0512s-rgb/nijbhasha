# Model card: C4 Santali voice (fine-tuned MMS-TTS), not shipped

**Status: not in the app.** By the finale voice rule (`docs/voice_rule_finale.md`, fixed on 27 Sep 2026
before any result), it does not replace Piper (`bench/results/voice_rule_finale.md`). Kept for the record.
**Not reviewed by a native speaker.** One speaker, 0.6 h: a small-data voice.

## What it is

- VITS text-to-speech, fine-tuned from **facebook/mms-tts-unr** (Mundari; CC BY-NC 4.0: non-commercial use
  only, approved by the team) with `ylacombe/finetune-hf-vits` @ `6f3f51f` (MIT) in
  `notebooks/santali_voice.ipynb` (Kaggle, GPU T4 x2 used as one GPU; run 4461.6 s, of which training 3097 s).
- Input: Santali in Ol Chiki, converted to **Odia script** (`translit/odia.py`, `olchiki_to_odia`), because the
  base vocabulary is Odia letters; character input, no espeak-ng. Output: 16 kHz mono.
- Export: one ONNX graph (`tools/export/export_mms_vits_onnx.py`), 114.2 MB, `tokens.txt` identical to mms-tts-unr's.

## Training data

- **IndicVoices-R**, config Santali, train split (`ai4bharat/indicvoices_r`; **CC BY 4.0**, attribution:
  AI4Bharat, IndicVoices-R). One speaker: **S4257968200377182** (male), the speaker with the most clean audio
  (SNR ≥ 25 dB, clips of 1–20 s): **0.6 h, 281 clips** (0.5977 h as logged), from 17 shards.
- **261 training clips** in metadata.csv; finetune-hf-vits used **259** of them after its length filter
  ("Num examples = 259", from the team's Kaggle log). 20 held out (never trained on; the wavs were moved out of the training folder and the
  count asserted: "wav files left in the training folder: 261 | training rows: 261"). **150 epochs**, batch 16,
  learning rate 2e-5, fp16, one GPU, 2,550 steps.
- Characters outside the base vocabulary: 0.17 % (35 × "।", 2 × "ଓ"), dropped by the tokenizer. The vocabulary
  has no sentence punctuation, so "।" gives no pause.
- Patches to the pinned training code (in the notebook): only the reads of `batch["speaker_id"]`; evaluation off
  (its plotting needs `fig.canvas.tostring_rgb`, which current matplotlib lacks).

## Evaluation

- The 20 held-out samples play: 1.9–9.7 s each, peak 0.73–0.89 (none clipped), RMS 0.095–0.170 (none silent).
- ASR round-trip CER (hub recogniser, IndicConformer 600M; `bench/voice_rule_finale_eval.py`), lower is better:

| | Piper (live voice) | This voice |
|---|---|---|
| Held-out pack lines (n=112, the rule's test): mean / median | **0.445 / 0.272** | 0.788 / 0.705 |
| same: failures (CER > 0.5) | **24 of 112** | 86 of 112 |
| The 20 held-out recordings' texts: mean / median | **0.271 / 0.248** | 0.584 / 0.564 |

- Native listener ratings (MOS): **NOT MEASURED**. Team listening note: none recorded.

## Limits

One speaker, 0.6 h; Odia-script input for a Santali voice; no punctuation pauses; non-commercial licence
(inherited from mms-tts-unr). CER is a proxy for intelligibility, not a listening test.
