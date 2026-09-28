"""tools/set_video_link.py fills the demo-video placeholder in the README and both decks
(on copies; the real files keep the placeholder until the video exists)."""

import shutil
import sys
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from tools import set_video_link as svl  # noqa: E402

FILES = ["README.md", "docs/deck/Nijbhasha_SIH26042_8-bitPool.pptx", "deck/final_deck.pptx", "docs/deck/SOURCES.md"]


def _copy(tmp_path):
    for f in FILES:
        (tmp_path / f).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(ROOT / f, tmp_path / f)
    return tmp_path


def _slides_text(p):
    z = zipfile.ZipFile(p)
    return "".join(z.read(n).decode("utf-8") for n in z.namelist() if n.startswith("ppt/slides/"))


def test_the_placeholder_is_in_every_file_until_the_video_exists():
    for f in FILES[1:3]:
        assert svl.PLACEHOLDER in _slides_text(ROOT / f), f


def test_set_video_link_fills_readme_and_both_decks(tmp_path):
    root = _copy(tmp_path)
    url = "https://youtu.be/abcDEF12345"
    done = svl.run(url, root)
    assert set(done) == set(FILES)
    for f in FILES[1:3]:
        t = _slides_text(root / f)
        assert svl.PLACEHOLDER not in t and url in t and svl.REL_ID in t
        z = zipfile.ZipFile(root / f)
        assert z.testzip() is None
        assert z.namelist()[0] == zipfile.ZipFile(ROOT / f).namelist()[0]     # part order kept
    assert url in (root / "README.md").read_text(encoding="utf-8")
    assert svl.run(url, root) == []                                           # second run: nothing left


def test_set_video_link_refuses_a_non_link(tmp_path):
    with pytest.raises(SystemExit):
        svl.run("my video", _copy(tmp_path))
