"""Score the hub's own Mundari engine on the notebook's held-out split (C3).

    python eval/mundari_hub_eval.py          # -> eval/results/mundari_hub_int8.json

The engine is the one POST /preview/translate uses (mundari_nmt.translate: int8 ONNX,
one sentence at a time, nukta clean-up on). The split is rebuilt exactly as the notebook
builds it (eval/mundari_split.py) and checked against the v6 leakage hashes first.
chrF++ (word_order=2) and BLEU, sacrebleu defaults; hypotheses and references get the
same normalisation (textnorm.fix_nukta_escape: the literal nukta escape -> U+093C, NFC).
The result stores the hypotheses with the training file's row ids, not the MMLoSo
sentences themselves (the data stays in data/mmloso/, git-ignored).
"""

import json
import platform
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "eval"))

import config  # noqa: E402
import mundari_nmt  # noqa: E402
import mundari_split  # noqa: E402
from textnorm import fix_nukta_escape  # noqa: E402

OUT = ROOT / "eval" / "results" / "mundari_hub_int8.json"


def main():
    import pandas as pd
    import sacrebleu
    chk = mundari_split.check()
    if not chk["ok"]:
        raise SystemExit(f"split check failed: {chk}")
    held, _, path = mundari_split.held_out_pairs()
    raw = pd.read_csv(path)
    row_id = raw.loc[held.index, raw.columns[0]].astype(str).tolist()     # the file's saved index column
    res = {"engine": "hub int8 ONNX (mundari_nmt.translate, as POST /preview/translate), after nukta fix",
           "label": "hub int8 ONNX, after nukta fix, " + mundari_nmt.LABEL,
           "split": chk, "decoding": "greedy; no no-repeat n-gram, no loop guard, max_new_tokens = 2 x input + 10 "
                                     "(the notebook's translate()); one sentence at a time",
           "threads": config.NMT_THREADS, "machine": platform.processor() or platform.machine(),
           "scoring": "sacrebleu corpus chrF++ (word_order=2) and BLEU, defaults; hyp and ref: fix_nukta_escape",
           "sacrebleu": sacrebleu.__version__}
    for key, direction, src_col, ref_col in (("hi->unr", "hi-to-unr", "hindi", "mundari"),
                                             ("unr->hi", "unr-to-hi", "mundari", "hindi")):
        hyp, secs = [], []
        t0 = time.time()
        for s in held[src_col].astype(str):
            t = time.time()
            hyp.append(fix_nukta_escape(mundari_nmt.translate(s, direction)["translated_text"]))
            secs.append(time.time() - t)
        wall = time.time() - t0
        ref = [fix_nukta_escape(r) for r in held[ref_col].astype(str)]
        secs_sorted = sorted(secs)
        res[key] = {"n": len(hyp),
                    "chrF++": round(sacrebleu.corpus_chrf(hyp, [ref], word_order=2).score, 2),
                    "BLEU": round(sacrebleu.corpus_bleu(hyp, [ref]).score, 2),
                    "run_time_s": round(wall, 1),
                    "per_sentence_s_p50": round(secs_sorted[len(secs) // 2], 3),
                    "escapes_left": sum("\\u" in h for h in hyp),
                    "outputs": [{"row_id": i, "hyp": h} for i, h in zip(row_id, hyp)]}
        print(f"{key}: chrF++ {res[key]['chrF++']}, BLEU {res[key]['BLEU']}, n={len(hyp)}, {wall:.0f} s", flush=True)
    OUT.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("->", OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()
