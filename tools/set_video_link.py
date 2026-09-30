"""Put the demo video's link everywhere it is still a placeholder, in one step.

    python tools/set_video_link.py https://youtu.be/XXXXXXXXXXX

Updates, in place:
  README.md                                  the header table and requirement 6
  docs/deck/Nijbhasha_SIH26042_8-bitPool.pptx  slide 6, "Demo video" (text + clickable)
  deck/final_deck.pptx                       slide 14, "Demo video" (text + clickable)
  docs/deck/SOURCES.md                       the "Still to fill" line
It refuses a link that is not http(s), and tells you if a placeholder is already gone.
Afterwards export the PDFs again from PowerPoint (File -> Export -> PDF), then commit.
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
PLACEHOLDER = "[add link after recording]"
REL_ID = "rIdDemoVideo"
REL_TYPE = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"


def _pptx(path, url):
    """Replace the placeholder in whichever slide has it; link the whole shape. True if changed."""
    zin = zipfile.ZipFile(path)
    items = [(i, zin.read(i.filename)) for i in zin.infolist()]
    zin.close()
    changed = False
    out = []
    slides = {i.filename: d for i, d in items}
    for info, data in items:
        name = info.filename
        if re.fullmatch(r"ppt/slides/slide\d+\.xml", name) and PLACEHOLDER.encode() in data:
            x = data.decode("utf-8")
            i = x.index(PLACEHOLDER)
            s, e = x.rfind("<p:sp>", 0, i), x.find("</p:sp>", i)
            sp = x[s:e]
            sp = sp.replace(PLACEHOLDER, escape(url))
            # link the shape: <p:cNvPr .../> -> <p:cNvPr ...><a:hlinkClick r:id="..."/></p:cNvPr>
            if "hlinkClick" not in sp.split("<p:cNvSpPr")[0]:
                sp = re.sub(r"<p:cNvPr([^>]*?)/>", rf'<p:cNvPr\1><a:hlinkClick r:id="{REL_ID}"/></p:cNvPr>', sp, count=1)
            x = x[:s] + sp + x[e:]
            data = x.encode("utf-8")
            rels = name.replace("slides/", "slides/_rels/") + ".rels"
            r = slides[rels].decode("utf-8")
            if REL_ID not in r:
                r = r.replace("</Relationships>", f'<Relationship Id="{REL_ID}" Type="{REL_TYPE}" '
                              f'Target="{escape(url)}" TargetMode="External"/></Relationships>')
            slides[rels] = r.encode("utf-8")
            changed = True
        out.append((info, data))
    if not changed:
        return False
    tmp = path.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in out:
            z.writestr(info, slides.get(info.filename, data) if info.filename.endswith(".rels") else data)
    tmp.replace(path)
    return True


def _text(path, pairs):
    s = path.read_text(encoding="utf-8")
    n = 0
    for old, new in pairs:
        if old in s:
            s = s.replace(old, new)
            n += 1
    if n:
        path.write_text(s, encoding="utf-8", newline="\n")
    return n


def run(url, root=ROOT):
    if not re.match(r"^https?://\S+$", url):
        raise SystemExit("Give the full link, e.g. https://youtu.be/XXXXXXXXXXX")
    root = Path(root)
    done = []
    for p in (root / "docs/deck/Nijbhasha_SIH26042_8-bitPool.pptx", root / "deck/final_deck.pptx"):
        if p.exists() and _pptx(p, url):
            done.append(str(p.relative_to(root)))
    readme = root / "README.md"
    pairs = [("Demo video: recorded 30 Sep on the laptop hub and the Realme tablet (shots and captions: `docs/demo_video_script.md`); link added here once uploaded",
              f"Demo video: {url}")]
    if readme.exists() and "| Demo video |" not in readme.read_text(encoding="utf-8"):
        pairs.append(("| Interface languages |", f"| Demo video | {url} |\n| Interface languages |"))
    if readme.exists() and _text(readme, pairs):
        done.append("README.md")
    src = root / "docs/deck/SOURCES.md"
    if src.exists() and _text(src, [('Still to fill: the demo video link on slide 6 (placeholder "[add link after recording]").',
                                     f"Demo video: {url} (slide 6).")]):
        done.append("docs/deck/SOURCES.md")
    return done


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("url")
    ap.add_argument("--root", default=str(ROOT), help=argparse.SUPPRESS)
    a = ap.parse_args()
    done = run(a.url, a.root)
    if not done:
        print("Nothing changed: the placeholders are already filled.")
        sys.exit(1)
    print("Updated:\n  " + "\n  ".join(done))
    print("Next: open both .pptx in PowerPoint, File -> Export -> PDF (replace the PDFs next to them), then\n"
          "  git add -A && git commit -m \"Demo video link\" && git push")


if __name__ == "__main__":
    main()
