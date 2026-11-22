"""render.py - local renderer for the news-image-20261121 entry.

Runs ONLY on this build machine (Pillow is not available in the grading
sandbox). It draws entry.png, a one-page front page summing up Saturday
21 November 2026. main.py never imports this file; it copies the PNG.

Design rule for this slug (LESSONS N3): readability beats density.
27 stories, every one fully readable: 3 leads with summaries, 12 cards
with full headlines, 12 short 'also' lines. No world map: the canvas
goes to text instead. Date is one big block in the masthead.
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

# ---------------- lead 1: COP31 ----------------
d.rectangle([24, 146, 520, 366], fill=(224, 238, 236),
            outline=TEAL, width=2)
d.rectangle([24, 146, 520, 174], fill=TEAL)
d.text((36, 153), "1  ANTALYA, TURKEY - CLIMATE TALKS",
       font=F(SANS_B, 13), fill=WHITE)
text_block(d, 36, 184, "COP31 runs into overtime with no deal "
           "on fossil fuels", F(SERIF_B, 25), INK, 472, 30)
text_block(d, 36, 252,
           "Nearly 200 countries stayed past Friday's deadline in "
           "Antalya. A draft had dropped any mention of ending fossil "
           "fuel use and a $120bn adaptation-finance goal. EU climate "
           "chief Hoekstra: \"a good deal or no deal.\"",
           F(SANS, 14), (40, 44, 48), 472, 19)
text_block(d, 36, 322,
           "100 civil-society groups warned the hosts, Turkey and "
           "Australia, the summit could become a low point in 30 "
           "years of climate talks.",
           F(SANS_B, 13), TEAL, 472, 18)

# ---------------- lead 2: Riyadh ----------------
d.rectangle([536, 146, 1000, 250], fill=WHITE, outline=(200, 194, 178))
d.rectangle([536, 146, 1000, 172], fill=RED)
d.text((548, 152), "2  RIYADH, SAUDI ARABIA - CONFLICT",
       font=F(SANS_B, 12), fill=WHITE)
text_block(d, 548, 180, "Saudi coalition says it intercepted three "
           "Houthi missiles fired at Riyadh", F(SANS_B, 19), INK, 440, 23)
text_block(d, 548, 228, "Second attack on the capital in days, after a "
           "tower was struck on Thursday.", F(SANS, 12), GREY, 440, 15)

# ---------------- lead 3: Peru ----------------
d.rectangle([536, 262, 1000, 366], fill=WHITE, outline=(200, 194, 178))
d.rectangle([536, 262, 1000, 288], fill=ORANGE)
d.text((548, 268), "3  JUNIN, PERU - EARTHQUAKE",
       font=F(SANS_B, 12), fill=WHITE)
text_block(d, 548, 296, "Magnitude 6.7 quake shakes Peru's Andes; "
           "no casualties reported", F(SANS_B, 19), INK, 440, 23)
text_block(d, 548, 344, "7:09pm local (00:09 GMT Sat), 108 km deep, "
           "felt in Lima.", F(SANS, 12), GREY, 440, 15)

# ---------------- 12 cards, full headlines ----------------
CARDS = [
    ("KRYVYI RIH, UKRAINE", RED,
     "Russian missile hits Zelensky's home city: two killed, "
     "dozens wounded, officials say"),
    ("MERCURY, SPACE", TEAL,
     "BepiColombo enters Mercury orbit after an eight-year "
     "voyage, ESA and JAXA say"),
    ("DR CONGO, HEALTH", GREEN,
     "WHO warns 7 in 10 infected under-fives have died in "
     "Congo's Bundibugyo Ebola outbreak"),
    ("BRUSSELS, TRADE", ORANGE,
     "EU and Indonesia sign trade deal after 10 years, cutting "
     "over 90% of tariffs"),
    ("NEW YORK, MARKETS", PURPLE,
     "Saturday reckoning: Nasdaq's 5.3% Friday fall erases its "
     "2026 gains; S&P in correction"),
    ("LONDON, RUGBY", NAVY,
     "England rout All Blacks 37-12 at Twickenham, their "
     "record margin over New Zealand"),
    ("DUBLIN, RUGBY", NAVY,
     "Ireland beat South Africa 20-17, yet the Springboks "
     "still reach the Nations final"),
    ("LONDON, FOOTBALL", NAVY,
     "Leeds stun Chelsea 4-1 at Stamford Bridge; Newcastle "
     "hold Arsenal 2-2"),
    ("BASRA, IRAQ", RED,
     "Fire at Hartha power station kills at least four and "
     "injures 35, officials say"),
    ("BAYELSA, NIGERIA", GREEN,
     "Nigeria boat disaster toll rises to 24 dead, emergency "
     "agency NEMA says"),
    ("COPENHAGEN, EUROPE", NAVY,
     "Denmark expels Russian attache over foiled rapper plot; "
     "Russia denies any role"),
    ("GAZA CITY, CONFLICT", RED,
     "Strike on a food vehicle in Gaza City kills three, "
     "Palestinian reports say"),
]
cx0, cy0, cw, chh, gap = 24, 378, 236, 121, 10
for i, (place, col, head) in enumerate(CARDS):
    cx = cx0 + (i % 4) * (cw + gap)
    cy = cy0 + (i // 4) * (chh + gap)
    d.rectangle([cx, cy, cx + cw, cy + chh], fill=WHITE,
                outline=(200, 194, 178))
    d.rectangle([cx, cy, cx + cw, cy + 5], fill=col)
    d.text((cx + 9, cy + 11), place, font=F(SANS_B, 11), fill=col)
    text_block(d, cx + 9, cy + 30, head, F(SANS_B, 14), INK,
               cw - 18, 18, max_lines=5)

# ---------------- also on Saturday ----------------
d.rectangle([24, 770, 1000, 798], fill=NAVY)
d.text((36, 777), "ALSO ON SATURDAY 21 NOVEMBER - AROUND THE WORLD",
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
ax0, ay0, aw = 24, 808, 483
for i, (place, head) in enumerate(ALSO):
    ax = ax0 + (i // 6) * (aw + 10)
    ay = ay0 + (i % 6) * 27
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
d.text((24, 978),
       "Sources actually used: Reuters, AP, AFP, USGS, ESA, Nature, "
       "WHO, European Commission, LiveScore, England Rugby.",
       font=F(SANS, 11), fill=GREY)
d.text((24, 994),
       "Where reports conflict, the image says who says it: Riyadh, "
       "Bahrain, Gaza and the Bayelsa tolls are attributed above.",
       font=F(SANS, 11), fill=GREY)

out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "entry.png")
img.save(out)
print("wrote", out, os.path.getsize(out), "bytes")
