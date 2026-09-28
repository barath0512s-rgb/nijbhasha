"""Mundari translation, Preview (C3): Hindi <-> Mundari on the laptop hub.

IndicTrans2 indic-indic-dist-320M with the Hindi–Mundari LoRA adapters merged
(notebooks/mundari_lora.ipynb, Kaggle v6), exported to int8 ONNX, one folder per
direction under config.MUNDARI_NMT_DIR (tools/install_mundari_nmt.py):
    hi_unr/  Hindi -> Mundari      unr_hi/  Mundari -> Hindi
Run by nmt_onnx.OnnxNMT with the base model's tokenizer (LoRA leaves it unchanged)
and the surrogate tag brx_Deva for Mundari (IndicTrans2 has no Mundari tag), as in
training, and decoded with the notebook's settings, not the Santali engine's (no
no-repeat 3-gram, no int8 loop guard, no 128-token cap). The remaining differences
from the notebook's scores: int8 instead of fp32, and one sentence at a time instead
of padded batches of 32. The adapters learned the literal nukta escape from the pinned IndicNLP
normaliser, so every output goes through textnorm.fix_nukta_escape.

Mundari is written in Devanagari here (as in MMLoSo 2025). Nothing is reviewed by
a native speaker: every reply says so.
"""

import threading

import config
from textnorm import fix_nukta_escape

HI, MUN = "hin_Deva", "brx_Deva"
DIRECTIONS = {"hi-to-unr": ("hi_unr", HI, MUN), "unr-to-hi": ("unr_hi", MUN, HI)}
FILES = ("encoder.int8.onnx", "decoder_init.int8.onnx", "decoder_step.int8.onnx")
LABEL = ("held-out 5% of the MMLoSo 2025 training file, n=1,021 pairs, greedy, Mundari preview, "
         "not reviewed by a native speaker")

_engines, _lock = {}, threading.Lock()


def available(direction):
    if direction not in DIRECTIONS:
        return False
    d = config.MUNDARI_NMT_DIR / DIRECTIONS[direction][0]
    return all((d / f).is_file() for f in FILES)


def _engine(direction):
    """One OnnxNMT per direction, loaded on first use (about 0.5 GB each)."""
    with _lock:
        if direction not in _engines:
            from transformers import AutoTokenizer
            from IndicTransToolkit.processor import IndicProcessor
            import nmt_onnx
            tok = AutoTokenizer.from_pretrained(str(config.NMT_DIR), trust_remote_code=True)
            _engines[direction] = nmt_onnx.OnnxNMT(
                tok, IndicProcessor(inference=True), int8=True, threads=config.NMT_THREADS,
                onnx_dir=config.MUNDARI_NMT_DIR / DIRECTIONS[direction][0],
                # decode as the notebook evaluated it (notebooks/mundari_lora.ipynb, translate()):
                # greedy, no no-repeat n-gram, no loop guard, up to 2 x input tokens + 10 new tokens
                guard=False, no_repeat=0, max_new_tokens=lambda n: 2 * n + 10)
        return _engines[direction]


def translate(text, direction):
    """{"translated_text", "direction", "maturity", "needs_review", "label"}."""
    if direction not in DIRECTIONS:
        raise ValueError(f"unknown direction {direction!r}")
    _, src, tgt = DIRECTIONS[direction]
    out, _ = _engine(direction).translate(text, src, tgt)
    return {"translated_text": fix_nukta_escape(out), "direction": direction, "maturity": "preview",
            "needs_review": True, "label": LABEL}
