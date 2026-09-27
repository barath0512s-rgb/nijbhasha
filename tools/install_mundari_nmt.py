"""Install the Mundari translation preview (C3) from the notebook's output.

    python tools/install_mundari_nmt.py                  # reads dist/mundari/mundari_onnx.zip

Copies the int8 graphs of both directions (onnx_hi_unr/, onnx_unr_hi/: encoder,
decoder_init, decoder_step) to config.MUNDARI_NMT_DIR/{hi_unr,unr_hi}/ and checks
that every file is there. models/ is git-ignored: weights are never committed.
"""

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import config  # noqa: E402
import mundari_nmt  # noqa: E402

ZIP = ROOT / "dist" / "mundari" / "mundari_onnx.zip"


def main():
    z = zipfile.ZipFile(sys.argv[1] if len(sys.argv) > 1 else ZIP)
    names = set(z.namelist())
    for direction, (folder, _, _) in mundari_nmt.DIRECTIONS.items():
        dst = config.MUNDARI_NMT_DIR / folder
        dst.mkdir(parents=True, exist_ok=True)
        for f in mundari_nmt.FILES:
            name = f"onnx_{folder}/{f}"
            if name not in names:
                raise SystemExit(f"{name} is missing from the zip")
            with z.open(name) as src, open(dst / f, "wb") as out:
                while chunk := src.read(1 << 24):
                    out.write(chunk)
            print(f"  {direction:10} {f:24} {(dst / f).stat().st_size / 1e6:7.1f} MB")
        assert mundari_nmt.available(direction), direction
    print("installed in", config.MUNDARI_NMT_DIR)


if __name__ == "__main__":
    main()
