"""render.py - local renderer for the news-image-20261121 entry.

Runs ONLY on this build machine (Pillow is not available in the grading
sandbox). It draws entry.png, a one-page front page summing up Saturday
21 November 2026. main.py never imports this file; it copies the PNG.

Revision 2 design (LESSONS N3 + N5 + N6): readability beats density,
and the big stories carry illustrations drawn by this session's own
code. 27 stories, every one fully readable: 3 illustrated leads with
summaries, 12 headline cards (the first row illustrated), 12 short
'also' lines. Illustrations are paid for by reallocating canvas
(spare panel space, tighter line heights), never by shrinking text
below its floor: lead headlines 20-25 px, lead summaries 14 px, card
headlines 14 px. Date is one big block in the masthead.
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (13, 29, 56)
PAPER = (248, 245, 236)
INK = (18, 18, 18)
GOLD = (198, 158, 38)
RED = (156, 28, 28)
GREY = (92, 90, 84)
LIGHT = (238, 233, 219)
TEAL = (16, 106, 106)
GREEN = (44, 108, 64)
ORANGE = (190, 92, 18)
PURPLE = (94, 62, 138)
WHITE = (255, 255, 255)
SKY = (176, 205, 224)

SERIF_B = "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, fill, max_w, lh, max_lines=None):
    lines = wrap(d, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def chip(d, x, y, text, fill, size=11):
    f = F(SANS_B, size)
    w = d.textlength(text, font=f) + 14
    d.rectangle([x, y, x + w, y + size + 9], fill=fill)
    d.text((x + 7, y + 4), text, font=f, fill=WHITE)
    return x + w + 8


# ---------- scenes, drawn by this session's own code ----------
def scene_cop31(d, x, y, w, h):
    """Climate talks: sun over a long conference table of delegates."""
    d.rectangle([x, y, x + w, y + h], fill=(206, 228, 222))
    d.ellipse([x + w - 36, y + 3, x + w - 8, y + 31], fill=GOLD)
    d.polygon([(x + 14, y + h - 4), (x + 28, y + h - 22),
               (x + 42, y + h - 4)], fill=GREEN)
    for i in range(6):
        hx = x + 70 + i * (w - 130) / 5
        d.ellipse([hx - 7, y + h - 25, hx + 7, y + h - 11],
                  fill=(60, 60, 66))
        d.rectangle([hx - 9, y + h - 11, hx + 9, y + h - 4],
                    fill=(60, 60, 66))
    d.rectangle([x + 52, y + h - 6, x + w - 52, y + h - 2],
                fill=(90, 62, 34))


def scene_riyadh(d, x, y, w, h):
    """Night sky over a skyline: missile trail met by an interceptor."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 30, 58))
    for bx, bw, bh in [(6, 16, 26), (26, 12, 36), (42, 18, 20),
                       (64, 12, 30), (80, 16, 22), (100, 12, 34)]:
        d.rectangle([x + bx, y + h - bh, x + bx + bw, y + h],
                    fill=(8, 10, 20))
    for wx in range(10, int(w) - 8, 14):
        d.point((x + wx, y + h - 8), fill=GOLD)
        d.point((x + wx, y + h - 16), fill=GOLD)
    cx, cy = x + w * 0.52, y + h * 0.34
    d.arc([x + 8, y + 4, x + w * 0.72, y + h * 0.95], 300, 60,
          fill=ORANGE, width=3)
    d.line([x + w - 8, y + h - 4, cx + 4, cy + 4], fill=WHITE, width=2)
    for dx, dy in [(0, -9), (0, 9), (-9, 0), (9, 0), (-7, -7), (7, 7),
                   (-7, 7), (7, -7)]:
        d.line([cx, cy, cx + dx, cy + dy], fill=(255, 214, 90),
               width=2)


def scene_peru(d, x, y, w, h):
    """Andes ridges with snow caps and a red fault crack."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    d.polygon([(x, y + h), (x + w * 0.28, y + 8), (x + w * 0.52,
               y + h)], fill=(122, 116, 108))
    d.polygon([(x + w * 0.34, y + h), (x + w * 0.62, y + 4),
               (x + w * 0.88, y + h)], fill=(104, 98, 92))
    d.polygon([(x + w * 0.62, y + 4), (x + w * 0.68, y + 14),
               (x + w * 0.56, y + 14)], fill=WHITE)
    d.polygon([(x + w * 0.28, y + 8), (x + w * 0.33, y + 17),
               (x + w * 0.23, y + 17)], fill=WHITE)
    pts = [(x + 6, y + h - 6), (x + w * 0.25, y + h - 16),
           (x + w * 0.42, y + h - 8), (x + w * 0.60, y + h - 18),
           (x + w * 0.78, y + h - 9), (x + w - 6, y + h - 15)]
    d.line(pts, fill=RED, width=3)


def strip_missile(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(46, 34, 44))
    for bx in range(8, int(w) - 10, 26):
        bh = 10 + (bx * 7) % 14
        d.rectangle([x + bx, y + h - bh, x + bx + 16, y + h],
                    fill=(16, 14, 20))
    d.arc([x + 10, y + 2, x + w * 0.6, y + h], 300, 55, fill=ORANGE,
          width=2)
    d.ellipse([x + w * 0.52, y + 6, x + w * 0.52 + 9, y + 15],
              fill=(255, 214, 90))


def strip_space(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 26))
    for sx in range(12, int(w) - 60, 23):
        d.point((x + sx, y + 6 + (sx % 13)), fill=WHITE)
        d.point((x + sx + 8, y + 20 - (sx % 9)), fill=WHITE)
    d.ellipse([x + w - 52, y + 3, x + w - 8, y + h - 3],
              fill=(168, 160, 148))
    d.ellipse([x + w - 42, y + 10, x + w - 34, y + 17],
              fill=(140, 132, 120))
    d.rectangle([x + 60, y + 13, x + 84, y + 21], fill=(210, 210, 215))
    d.rectangle([x + 40, y + 10, x + 58, y + 24], fill=(70, 110, 190))
    d.rectangle([x + 86, y + 10, x + 104, y + 24], fill=(70, 110, 190))


def strip_virus(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 240, 232))
    for cx in [x + 40, x + w // 2, x + w - 40]:
        cy = y + h // 2
        for ang in range(0, 360, 45):
            import math
            ex = cx + int(13 * math.cos(math.radians(ang)))
            ey = cy + int(13 * math.sin(math.radians(ang)))
            d.line([cx, cy, ex, ey], fill=RED, width=2)
            d.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=RED)
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(196, 70, 60))


def strip_trade(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(240, 238, 228))
    d.rectangle([x + 18, y + 6, x + 74, y + h - 6], fill=(30, 50, 140))
    import math
    for i in range(8):
        ang = math.radians(i * 45)
        sx = x + 46 + int(11 * math.cos(ang))
        sy = y + h // 2 + int(8 * math.sin(ang))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
    d.rectangle([x + w - 74, y + 6, x + w - 18, y + h - 6], fill=WHITE,
                outline=GREY)
    d.rectangle([x + w - 74, y + 6, x + w - 18, y + h // 2],
                fill=(206, 30, 40))
    d.line([x + 88, y + h // 2, x + w - 88, y + h // 2], fill=GOLD,
           width=3)
    d.polygon([(x + w - 88, y + h // 2), (x + w - 98, y + h // 2 - 4),
               (x + w - 98, y + h // 2 + 4)], fill=GOLD)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---------------- masthead: the date is one big block ----------------
d.rectangle([0, 0, W, 104], fill=NAVY)
d.text((24, 16), "THE WORLD IN ONE DAY", font=F(SERIF_B, 37), fill=WHITE)
d.text((24, 64), "ONE IMAGE - 27 STORIES - EVERY STORY FROM SATURDAY",
       font=F(SANS_B, 14), fill=GOLD)
d.text((648, 10), "SATURDAY", font=F(SANS_B, 23), fill=WHITE)
d.text((648, 40), "21 NOVEMBER 2026", font=F(SANS_B, 33), fill=GOLD)
d.text((648, 80), "THE DAY IN WORLD NEWS", font=F(SANS_B, 12),
       fill=(205, 210, 220))

# ---------------- region bar ----------------
regions = [("AMERICAS 4", PURPLE), ("EUROPE 12", NAVY),
           ("MIDDLE EAST 5", RED), ("AFRICA 4", GREEN),
           ("ASIA-PACIFIC 1", ORANGE), ("SPACE 1", TEAL)]
x = 24
for name, col in regions:
    x = chip(d, x, 114, name, col, 12)

# ---------------- lead 1: COP31, illustrated ----------------
d.rectangle([24, 142, 520, 396], fill=(224, 238, 236),
            outline=TEAL, width=2)
d.rectangle([24, 142, 520, 170], fill=TEAL)
d.text((36, 149), "1  ANTALYA, TURKEY - CLIMATE TALKS",
       font=F(SANS_B, 13), fill=WHITE)
scene_cop31(d, 36, 176, 472, 34)
text_block(d, 36, 216, "COP31 runs into overtime with no deal "
           "on fossil fuels", F(SERIF_B, 25), INK, 472, 27)
text_block(d, 36, 274,
           "Nearly 200 countries stayed past Friday's deadline in "
           "Antalya. A draft had dropped any mention of ending fossil "
           "fuel use and a $120bn adaptation-finance goal. EU climate "
           "chief Hoekstra: \"a good deal or no deal.\"",
           F(SANS, 14), (40, 44, 48), 472, 18)
text_block(d, 36, 350,
           "100 civil-society groups warned the hosts, Turkey and "
           "Australia, the summit could become a low point in 30 "
           "years of climate talks.",
           F(SANS_B, 13), TEAL, 472, 16)

# ---------------- lead 2: Riyadh, illustrated ----------------
d.rectangle([536, 142, 1000, 270], fill=WHITE, outline=(200, 194, 178))
d.rectangle([536, 142, 1000, 164], fill=RED)
d.text((548, 147), "2  RIYADH, SAUDI ARABIA - CONFLICT",
       font=F(SANS_B, 12), fill=WHITE)
scene_riyadh(d, 872, 168, 116, 63)
text_block(d, 548, 168, "Saudi coalition says it intercepted three "
           "Houthi missiles fired at Riyadh", F(SANS_B, 20), INK,
           316, 21)
text_block(d, 548, 235, "Second attack on the capital in days, "
           "after a tower was struck on Thursday.", F(SANS, 14),
           GREY, 440, 16)

# ---------------- lead 3: Peru, illustrated ----------------
d.rectangle([536, 278, 1000, 396], fill=WHITE, outline=(200, 194, 178))
d.rectangle([536, 278, 1000, 300], fill=ORANGE)
d.text((548, 283), "3  JUNIN, PERU - EARTHQUAKE",
       font=F(SANS_B, 12), fill=WHITE)
scene_peru(d, 872, 304, 116, 63)
text_block(d, 548, 304, "Magnitude 6.7 quake shakes Peru's Andes; "
           "no casualties reported", F(SANS_B, 20), INK, 316, 21)
text_block(d, 548, 371, "7:09pm local (00:09 GMT Sat), 108 km deep, "
           "felt in Lima.", F(SANS, 14), GREY, 440, 16)

# ---------------- 12 cards; first row illustrated ----------------
CARDS = [
    ("KRYVYI RIH, UKRAINE", RED,
     "Russian missile hits Zelensky's home city: two killed, "
     "dozens wounded, officials say", strip_missile),
    ("MERCURY, SPACE", TEAL,
     "BepiColombo enters Mercury orbit after an eight-year "
     "voyage, ESA and JAXA say", strip_space),
    ("DR CONGO, HEALTH", GREEN,
     "WHO warns 7 in 10 infected under-fives have died in "
     "Congo's Bundibugyo Ebola outbreak", strip_virus),
    ("BRUSSELS, TRADE", ORANGE,
     "EU and Indonesia sign trade deal after 10 years, cutting "
     "over 90% of tariffs", strip_trade),
    ("NEW YORK, MARKETS", PURPLE,
     "Saturday reckoning: Nasdaq's 5.3% Friday fall erases its "
     "2026 gains; S&P in correction", None),
    ("LONDON, RUGBY", NAVY,
     "England rout All Blacks 37-12 at Twickenham, their "
     "record margin over New Zealand", None),
    ("DUBLIN, RUGBY", NAVY,
     "Ireland beat South Africa 20-17, yet the Springboks "
     "still reach the Nations final", None),
    ("LONDON, FOOTBALL", NAVY,
     "Leeds stun Chelsea 4-1 at Stamford Bridge; Newcastle "
     "hold Arsenal 2-2", None),
    ("BASRA, IRAQ", RED,
     "Fire at Hartha power station kills at least four and "
     "injures 35, officials say", None),
    ("BAYELSA, NIGERIA", GREEN,
     "Nigeria boat disaster toll rises to 24 dead, emergency "
     "agency NEMA says", None),
    ("COPENHAGEN, EUROPE", NAVY,
     "Denmark expels Russian attache over foiled rapper plot; "
     "Russia denies any role", None),
    ("GAZA CITY, CONFLICT", RED,
     "Strike on a food vehicle in Gaza City kills three, "
     "Palestinian reports say", None),
]
ROW_H = [140, 112, 112]
cy = 404
for row in range(3):
    chh = ROW_H[row]
    for col_i in range(4):
        i = row * 4 + col_i
        place, col, head, strip = CARDS[i]
        cx = 24 + col_i * (236 + 10)
        d.rectangle([cx, cy, cx + 236, cy + chh], fill=WHITE,
                    outline=(200, 194, 178))
        d.rectangle([cx, cy, cx + 236, cy + 5], fill=col)
        top = cy + 9
        if strip is not None:
            strip(d, cx + 9, cy + 9, 218, 34)
            top = cy + 49
        d.text((cx + 9, top), place, font=F(SANS_B, 11), fill=col)
        text_block(d, cx + 9, top + 17, head, F(SANS_B, 14), INK,
                   218, 17, max_lines=5)
    cy += chh + 10

# ---------------- also on Saturday ----------------
d.rectangle([24, 796, 1000, 820], fill=NAVY)
d.text((36, 802), "ALSO ON SATURDAY 21 NOVEMBER - AROUND THE WORLD",
       font=F(SANS_B, 14), fill=WHITE)
ALSO = [
    ("GULF OF FINLAND", "Drones hit Russian cargo ship Sparta II; "
     "it catches fire and drifts into Finnish waters"),
    ("BAHRAIN, GULF", "Iran says it struck US bases; Bahrain "
     "reports a fire at an industrial site, no injuries"),
    ("POLAND, NATO", "Poland appeals for NATO AWACS and F-35s "
     "after Russian missiles fell on its soil"),
    ("STRAIT OF HORMUZ", "UKMTO reports two more tanker strikes; "
     "a tanker fire is put out north of Oman"),
    ("FINLAND, EUROPE", "Finland probes a suspected Russian "
     "helicopter incursion 4.1 km into its airspace"),
    ("PARMA, FOOTBALL", "Malen scores four as Roma win 5-1 at "
     "Parma; Real Madrid beat Celta Vigo 2-1"),
    ("U-17 WORLD CUP", "Morocco rout Fiji 6-0 and Mali beat New "
     "Zealand 3-0 in Saturday's group games"),
    ("UTAH, US SPORT", "No. 10 BYU outlast Kansas 31-29 in triple "
     "overtime in a Big 12 thriller"),
    ("WASHINGTON, AI", "Trump says US will penalise firms that "
     "build data centres abroad: \"a tremendous tax\""),
    ("BRUSSELS, EU BUDGET", "Costa proposes a 1.78 trillion euro "
     "EU budget for 2028-2034; agreement still pending"),
    ("HODEIDAH, YEMEN", "Coalition strikes Hodeidah port after "
     "the Riyadh attack, Houthi outlets report"),
    ("NICE, FOOTBALL", "PSG win 3-2 at Nice in Ligue 1 but lose "
     "Doue to a knee injury, AFP reports"),
]
ax0, ay0, aw = 24, 828, 483
for i, (place, head) in enumerate(ALSO):
    ax = ax0 + (i // 6) * (aw + 10)
    ay = ay0 + (i % 6) * 26
    d.text((ax + 12, ay), place + " - ", font=F(SANS_B, 12), fill=NAVY)
    pw = d.textlength(place + " - ", font=F(SANS_B, 12))
    first_w = aw - 24 - pw
    words, line1, rest = head.split(" "), "", ""
    for wd in words:
        trial = wd if not line1 else line1 + " " + wd
        if d.textlength(trial, font=F(SANS, 12)) <= first_w:
            line1 = trial
        else:
            rest = (rest + " " + wd).strip()
    d.text((ax + 12 + pw, ay), line1, font=F(SANS, 12), fill=INK)
    if rest:
        d.text((ax + 12, ay + 15), rest, font=F(SANS, 12), fill=INK)

# ---------------- footer ----------------
d.text((24, 990),
       "Sources actually used: Reuters, AP, AFP, USGS, ESA, Nature, "
       "WHO, European Commission, LiveScore, England Rugby.",
       font=F(SANS, 11), fill=GREY)
d.text((24, 1005),
       "Where reports conflict, the image says who says it: Riyadh, "
       "Bahrain, Gaza and the Bayelsa tolls are attributed above.",
       font=F(SANS, 11), fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "entry.png")
img.save(out)
print("wrote", out, os.path.getsize(out), "bytes")
