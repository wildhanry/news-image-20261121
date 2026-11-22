# news-image-20261121 — make.fun entry

Entry for the make.fun competition **news-image-20261121**
("Sum up 21 November's world news in one image"):
https://make.fun/bounty/news-image-20261121

One image sums up Saturday 21 November 2026: 27 stories, all fully
readable — 3 leads with summaries (COP31 overtime in Antalya, the
Saudi coalition's reported interception of three Houthi missiles
over Riyadh, the magnitude 6.7 Peru earthquake), 12 headline cards
and 12 short world lines, under one big date block.

## How it runs

- `main.py` (Python 3.13, standard library only) copies `entry.png`
  to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR/entry.png`).
- `render.py` is the local Pillow renderer that drew `entry.png`
  from the hand-checked stories; it is not used by the grader.
- `SOURCES.md` lists the two-plus named sources checked per story
  and how conflicting reports are attributed on the image.

## Design notes

Readability over density: fewer stories than a maximal front page,
but every headline is set at 13 px or larger and the date at 33 px,
so the page still reads when shrunk to about 300 px wide. No world
map — the canvas goes to text instead.

License: MIT (see LICENSE).
