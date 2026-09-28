# corpus.py — community voice corpus: adult speakers record lines in their own language.
#
# There is little recorded Santali, Mundari or Ho to build better voices and
# recognisers from. A community member or elder reads a line on the laptop hub;
# the recording stays on this laptop (corpus/, git-ignored) with a manifest line:
# language, the text read, the date, and the two consents. No names, no device id.
#
# Adults only, with consent given on the screen. Children's voices are never kept:
# the reading check deletes its recording after scoring (orf.py), and this module
# refuses a recording without the adult-speaker consent.
# Export is a manual step (GET /corpus/export) and includes only the recordings
# whose speaker also agreed to share them for research.

import io
import json
import threading
import time
import uuid
import zipfile
from pathlib import Path

import config

LANGS = {"sat": "Santali", "unr": "Mundari", "hoc": "Ho"}
EXTS = {"webm", "ogg", "wav", "mp4", "m4a"}
MAX_BYTES = 5 * 1024 * 1024          # about a minute of compressed speech; a line is a few seconds
MAX_TEXT = 300
DIR = config.BASE_DIR / "corpus"
_lock = threading.Lock()


class CorpusError(ValueError):
    pass


def _manifest(d):
    return d / "manifest.jsonl"


def add(audio, ext, text, lang, adult, share, root=None):
    """Store one recording. audio: bytes. Raises CorpusError on anything not allowed.
    Returns the manifest record."""
    d = Path(root or DIR)
    ext = (ext or "").lower().lstrip(".")
    text = (text or "").strip()
    if not adult:
        raise CorpusError("An adult speaker's consent is required; children's voices are not recorded")
    if lang not in LANGS:
        raise CorpusError(f"lang must be one of {sorted(LANGS)}")
    if not text or len(text) > MAX_TEXT:
        raise CorpusError(f"The line read aloud is required (up to {MAX_TEXT} characters)")
    if ext not in EXTS:
        raise CorpusError(f"Audio type must be one of {sorted(EXTS)}")
    if not audio or len(audio) > MAX_BYTES:
        raise CorpusError("The recording is empty or too long")
    rid = uuid.uuid4().hex
    rec = {"id": rid, "file": f"{rid}.{ext}", "lang": lang, "text": text,
           "date": time.strftime("%Y-%m-%d"),
           "consent": {"adult_speaker": True, "share_for_research": bool(share)}}
    with _lock:
        d.mkdir(parents=True, exist_ok=True)
        (d / rec["file"]).write_bytes(audio)
        with _manifest(d).open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def records(root=None):
    m = _manifest(Path(root or DIR))
    if not m.exists():
        return []
    return [json.loads(line) for line in m.read_text(encoding="utf-8").splitlines() if line.strip()]


def summary(root=None):
    """Counts per language, and how many may be shared."""
    rs = records(root)
    return {"total": len(rs),
            "by_lang": {k: sum(r["lang"] == k for r in rs) for k in LANGS},
            "shareable": sum(r["consent"]["share_for_research"] for r in rs)}


def export_zip(root=None):
    """A zip of the shareable recordings and their manifest (README inside)."""
    d = Path(root or DIR)
    keep = [r for r in records(d) if r["consent"]["share_for_research"]]
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("README.txt",
                   f"{config.APP_NAME} community voice corpus. Adult speakers, consent to record and to share "
                   "for research given on screen. No names. Each line of manifest.jsonl: id, file, lang "
                   "(sat Santali, unr Mundari, hoc Ho), the text read, date, consent.\n")
        z.writestr("manifest.jsonl", "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in keep))
        for r in keep:
            p = d / r["file"]
            if p.exists():
                z.write(p, r["file"])
    return buf.getvalue()
