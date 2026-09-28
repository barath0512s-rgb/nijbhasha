"""The Mundari notebook's held-out split, rebuilt exactly (notebooks/mundari_lora.ipynb, data cell).

    python eval/mundari_split.py            # checks the split against the v6 leakage hashes

Reads the MMLoSo 2025 Hindi–Mundari training file from data/mmloso/ (git-ignored;
CC BY-SA 4.0, never committed). Same steps as the notebook: read_norm (drop the saved
index column, lower-case the headers), dropna and de-duplicate on (hindi, mundari),
held out when sha1(nkey(hindi)) % 20 == 0.
"""

import glob
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "mmloso"
LEAK = ROOT / "dist" / "mundari" / "leakage_hashes.json"
EXPECTED_HELD = 1021


def read_norm(path):
    import pandas as pd
    d = pd.read_csv(path)
    d = d.loc[:, [c for c in d.columns if not str(c).lower().startswith("unnamed")]]
    d.columns = [str(c).strip().lower().replace(" ", "_") for c in d.columns]
    return d


def nkey(s):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", str(s)).strip().lower())


def heldout(h):
    return int(hashlib.sha1(nkey(h).encode()).hexdigest(), 16) % 20 == 0


def held_out_pairs():
    """The held-out DataFrame (columns hindi, mundari), in file order, as the notebook builds it."""
    files = sorted(glob.glob(str(DATA / "*.csv")))
    files = [f for f in files if "mundari" in Path(f).name.lower() and "test" not in f.lower()]
    if not files:
        raise SystemExit(f"no Hindi–Mundari training CSV in {DATA}")
    df = read_norm(files[0])
    assert {"hindi", "mundari"} <= set(df.columns), df.columns
    df = df.dropna(subset=["hindi", "mundari"]).drop_duplicates(subset=["hindi", "mundari"])
    return df[df.hindi.map(heldout)], len(df), files[0]


def check():
    held, total, path = held_out_pairs()
    leak = set(json.loads(LEAK.read_text(encoding="utf-8"))["hashes"])
    sha1 = lambda t: hashlib.sha1(nkey(t).encode()).hexdigest()
    miss_hi = [t for t in held.hindi if sha1(t) not in leak]
    miss_unr = [t for t in held.mundari if sha1(t) not in leak]
    return {"file": Path(path).name, "pairs_after_dedupe": total, "held_out": len(held),
            "held_out_expected": EXPECTED_HELD, "hindi_not_in_leakage_set": len(miss_hi),
            "mundari_not_in_leakage_set": len(miss_unr),
            "ok": len(held) == EXPECTED_HELD and not miss_hi and not miss_unr}


if __name__ == "__main__":
    r = check()
    print(json.dumps(r, indent=1))
    sys.exit(0 if r["ok"] else 1)
