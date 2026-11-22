"""news-image-20261121 entry program, written for this competition.

The grading sandbox offers Python 3.13 with the standard library only
and no network, so this program does the simplest reliable thing: it
copies the finished front-page image (entry.png, drawn beforehand by
render.py from hand-checked Saturday 21 November 2026 stories) into
the output directory, byte for byte, and verifies the copy's size.

Locally, MAKEFUN_OUTPUT_DIR stands in for /output:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(HERE, "entry.png")


def target_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def main():
    out = target_dir()
    os.makedirs(out, exist_ok=True)
    dest = os.path.join(out, "entry.png")
    shutil.copyfile(IMAGE, dest)
    written = os.path.getsize(dest)
    expected = os.path.getsize(IMAGE)
    if written != expected:
        raise SystemExit("copy size mismatch: %d != %d" % (written, expected))
    print("wrote", dest, written, "bytes")


if __name__ == "__main__":
    main()
