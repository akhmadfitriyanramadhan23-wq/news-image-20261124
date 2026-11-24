#!/usr/bin/env python3
"""THE WORLD TODAY - front page for Tuesday 24 November 2026.
Deterministic: fixed seed, no timestamps, no network. PIL only.
Writes entry.png (1024x1024, PNG) next to this script's parent dir.
"""
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "entry.png"

W, H = 1024, 1024
MARGIN = 40
CW = W - 2 * MARGIN  # 944 content width

PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (158, 27, 27)
GREY = (85, 85, 85)
LIGHT_GREY = (120, 115, 105)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

RNG = random.Random(20261124)


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip() if cur else w
        if fnt.getlength(t) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_font(path, text, max_size, max_w, min_size=10):
    """Largest size <= max_size at which text fits max_w."""
    size = max_size
    while size > min_size:
        f = font(path, size)
        if f.getlength(text) <= max_w:
            return f
        size -= 1
    return font(path, min_size)


def draw_centered(d, y, text, fnt, fill=INK):
    d.text((W / 2, y), text, font=fnt, fill=fill, anchor="ma")


def draw_wrapped(d, x, y, text, fnt, max_w, fill=INK, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.28)
    for line in wrap(text, fnt, max_w):
        d.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(d, y, x0, x1, width=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- image setup
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# thin double frame
d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=1)
d.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

y = 26

# ---------------------------------------------------------------- masthead
mast_f = fit_font(SERIF_B, "THE WORLD TODAY", 88, CW)
draw_centered(d, y, "THE WORLD TODAY", mast_f)
y += int(mast_f.size * 1.08)

date_f = font(SANS_B, 28)
draw_centered(d, y, "TUESDAY,  24  NOVEMBER  2026", date_f)
y += 40

tag_f = font(SANS, 16)
draw_centered(d, y, "THE DAY'S WORLD NEWS  —  IN ONE PAGE", tag_f, fill=GREY)
y += 28

rule(d, y, MARGIN, W - MARGIN, width=4, fill=RED)
y += 7
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 16

# ---------------------------------------------------------------- lead story
kick_f = font(SANS_B, 18)
d.text((MARGIN, y), "THE WAR AT SEA", font=kick_f, fill=RED)
y += 26

lead_f = font(SERIF_B, 52)
for line in ["UKRAINE SINKS RUSSIAN", "WARSHIP OFF LIBYA"]:
    d.text((MARGIN, y), line, font=lead_f, fill=INK)
    y += 58
y += 2

deck_f = font(SERIF, 21)
deck = ("Zelensky confirms drone strikes on two Russian warships docked at "
        "Benghazi \u2014 corvette Merkury destroyed in fire \u2014 Kyiv takes "
        "its naval war to the Mediterranean.")
y = draw_wrapped(d, MARGIN, y, deck, deck_f, CW, leading=27)
y += 8

# ---------------------------------------------------------------- illustration: warship on fire at dusk port
box_x0, box_y0 = MARGIN, y
box_x1, box_y1 = W - MARGIN, y + 200
bw, bh = box_x1 - box_x0, box_y1 - box_y0
horizon = box_y0 + 150  # sea starts here

# dusk sky gradient (fixed bands)
sky_top = (46, 38, 66)
sky_mid = (122, 62, 52)
sky_low = (214, 122, 58)
for i in range(horizon - box_y0):
    t = i / max(1, horizon - box_y0 - 1)
    if t < 0.55:
        tt = t / 0.55
        c = tuple(int(sky_top[k] + (sky_mid[k] - sky_top[k]) * tt) for k in range(3))
    else:
        tt = (t - 0.55) / 0.45
        c = tuple(int(sky_mid[k] + (sky_low[k] - sky_mid[k]) * tt) for k in range(3))
    d.line([(box_x0, box_y0 + i), (box_x1, box_y0 + i)], fill=c)

# distant port silhouette: cranes + warehouses on the horizon
d.rectangle([box_x0, horizon - 26, box_x1, horizon], fill=(52, 44, 52))
for cx in (box_x0 + 60, box_x0 + 300, box_x1 - 180):
    d.rectangle([cx, horizon - 58, cx + 8, horizon - 26], fill=(52, 44, 52))
    d.line([(cx + 4, horizon - 58), (cx + 52, horizon - 30)], fill=(52, 44, 52), width=4)
    d.line([(cx + 4, horizon - 58), (cx - 34, horizon - 30)], fill=(52, 44, 52), width=4)
d.rectangle([box_x0 + 120, horizon - 44, box_x0 + 240, horizon - 26], fill=(52, 44, 52))
d.rectangle([box_x1 - 320, horizon - 40, box_x1 - 210, horizon - 26], fill=(52, 44, 52))

# sea
d.rectangle([box_x0, horizon, box_x1, box_y1], fill=(26, 38, 50))
# orange reflection under the fire
for i in range(8):
    rx = box_x0 + 430 + RNG.randint(-70, 70)
    rw = RNG.randint(30, 110)
    ry = horizon + 6 + i * 5
    d.line([(rx, ry), (rx + rw, ry)], fill=(216, 110, 40), width=3)
# calm water lines
for i in range(10):
    wx = box_x0 + RNG.randint(0, bw - 160)
    ww = RNG.randint(50, 160)
    wy = horizon + 12 + i * 4
    d.line([(wx, wy), (wx + ww, wy)], fill=(90, 115, 135), width=2)

# --- warship + fire + smoke on an RGBA overlay, clipped to the box
ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
od = ImageDraw.Draw(ov)
hx0, hx1 = box_x0 + 150, box_x1 - 130   # hull extent
deck_y = horizon - 58
hull_bot = horizon + 16
# hull: trapezoid with raked bow
od.polygon([(hx0, deck_y), (hx1 - 90, deck_y), (hx1, deck_y + 26),
            (hx1 - 18, hull_bot), (hx0 + 14, hull_bot), (hx0, deck_y + 26)],
           fill=(104, 110, 118, 255))
# darker waterline stripe
od.polygon([(hx0 + 4, hull_bot - 12), (hx1 - 20, hull_bot - 12),
            (hx1 - 18, hull_bot), (hx0 + 14, hull_bot)], fill=(52, 56, 62, 255))
# portholes
for px in range(hx0 + 60, hx1 - 140, 42):
    od.ellipse([px, deck_y + 12, px + 7, deck_y + 19], fill=(30, 32, 36, 255))
# superstructure
od.rectangle([hx0 + 190, deck_y - 40, hx0 + 330, deck_y], fill=(150, 156, 164, 255))
od.rectangle([hx0 + 205, deck_y - 54, hx0 + 315, deck_y - 40], fill=(168, 174, 182, 255))
# bridge windows
od.rectangle([hx0 + 212, deck_y - 50, hx0 + 308, deck_y - 44], fill=(24, 28, 34, 255))
# funnel
od.rectangle([hx0 + 380, deck_y - 58, hx0 + 416, deck_y], fill=(120, 60, 46, 255))
od.rectangle([hx0 + 380, deck_y - 58, hx0 + 416, deck_y - 50], fill=(40, 40, 44, 255))
# mast (kept inside the box)
od.line([(hx0 + 260, deck_y - 54), (hx0 + 260, deck_y - 86)], fill=(60, 64, 70, 255), width=5)
od.line([(hx0 + 232, deck_y - 76), (hx0 + 288, deck_y - 76)], fill=(60, 64, 70, 255), width=4)
od.line([(hx0 + 260, deck_y - 86), (hx0 + 246, deck_y - 74)], fill=(60, 64, 70, 255), width=3)
od.line([(hx0 + 260, deck_y - 86), (hx0 + 274, deck_y - 74)], fill=(60, 64, 70, 255), width=3)
# radar dish
od.pieslice([hx0 + 248, deck_y - 90, hx0 + 272, deck_y - 78], 180, 360,
            fill=(150, 156, 164, 255))
# gun turret at the bow
od.polygon([(hx1 - 130, deck_y), (hx1 - 66, deck_y), (hx1 - 74, deck_y - 22),
            (hx1 - 122, deck_y - 22)], fill=(88, 94, 102, 255))
od.line([(hx1 - 78, deck_y - 16), (hx1 - 34, deck_y - 24)], fill=(60, 64, 70, 255), width=6)
# stern flag mast
od.line([(hx0 + 8, deck_y), (hx0 + 8, deck_y - 44)], fill=(60, 64, 70, 255), width=3)

# --- fireball above midship (between superstructure and funnel)
fx, fy = hx0 + 355, deck_y - 8
flame_cols = [(255, 60, 10, 255), (255, 122, 26, 255), (255, 194, 26, 255),
              (255, 232, 120, 255)]
for r, col in [(46, flame_cols[0]), (34, flame_cols[1]), (24, flame_cols[2]),
               (15, flame_cols[3])]:
    od.ellipse([fx - r, fy - 14 - r, fx + r, fy - 14 + r], fill=col)
# flame tongues
for dx, hh, ww in [(-30, 34, 18), (-10, 44, 22), (12, 38, 20), (30, 30, 16)]:
    od.polygon([(fx + dx - ww // 2, fy - 10), (fx + dx, fy - hh),
                (fx + dx + ww // 2, fy - 10)], fill=(255, 140, 30, 255))
# --- soft smoke wisps rising from the fire (light, translucent, inside box)
sx, sy = fx + 8, fy - 50
for i, r in enumerate([10, 12, 14]):
    jx = i * 9 + RNG.randint(-3, 3)
    jy = -i * 8
    od.ellipse([sx + jx - r, sy + jy - r, sx + jx + r, sy + jy + r],
               fill=(150, 148, 152, 110))
    od.ellipse([sx + jx - r + 3, sy + jy - r + 2, sx + jx + r - 2, sy + jy + r - 3],
               fill=(178, 176, 180, 90))
# clip overlay to the illustration box and paste
ov_c = ov.crop((box_x0, box_y0, box_x1, box_y1))
img.paste(ov_c, (box_x0, box_y0), ov_c)
d = ImageDraw.Draw(img)

# thin frame around the illustration
d.rectangle([box_x0, box_y0, box_x1, box_y1], outline=INK, width=2)
y = box_y1 + 14
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 14

# ---------------------------------------------------------------- middle row: COP31 / NATO / NVIDIA
mid_y0 = y
colA_x, colA_w = MARGIN, 356
colB_x, colB_w = 428, 262
colC_x, colC_w = 708, 276
for cx in (412, 692):
    d.line([(cx, mid_y0), (cx, mid_y0 + 148)], fill=LIGHT_GREY, width=1)

# --- COP31 with a small cracked globe
globe_cx, globe_cy, gr = colA_x + 34, mid_y0 + 34, 32
d.ellipse([globe_cx - gr, globe_cy - gr, globe_cx + gr, globe_cy + gr],
          fill=(47, 111, 178), outline=INK, width=2)
d.ellipse([globe_cx - 20, globe_cy - 18, globe_cx - 2, globe_cy + 2], fill=(74, 140, 74))
d.ellipse([globe_cx + 4, globe_cy + 6, globe_cx + 22, globe_cy + 22], fill=(74, 140, 74))
d.ellipse([globe_cx + 8, globe_cy - 26, globe_cx + 24, globe_cy - 8], fill=(74, 140, 74))
# crack across the globe
d.line([(globe_cx - 24, globe_cy - 26), (globe_cx - 6, globe_cy - 6),
        (globe_cx + 6, globe_cy + 10), (globe_cx + 24, globe_cy + 26)],
       fill=RED, width=4)
gx = colA_x + 78
d.text((gx, mid_y0), "CLIMATE", font=font(SANS_B, 16), fill=RED)
hf = font(SERIF_B, 30)
d.text((gx, mid_y0 + 22), "COP31 ENDS", font=hf, fill=INK)
d.text((gx, mid_y0 + 56), "WITH NO DEAL", font=hf, fill=INK)
deck2 = ("Climate talks in Antalya collapse \u2014 no final deal; "
         "talks may be suspended.")
draw_wrapped(d, colA_x, mid_y0 + 96, deck2, font(SANS, 17), colA_w, leading=21)

# --- NATO
d.text((colB_x, mid_y0), "DEFENCE", font=font(SANS_B, 16), fill=RED)
hf2 = font(SERIF_B, 27)
d.text((colB_x, mid_y0 + 22), "NATO VOWS", font=hf2, fill=INK)
d.text((colB_x, mid_y0 + 53), "SPACE DEFENCE", font=hf2, fill=INK)
draw_wrapped(d, colB_x, mid_y0 + 96,
             "Alliance answers report of a Russian nuclear satellite.",
             font(SANS, 17), colB_w, leading=21)

# --- NVIDIA
d.text((colC_x, mid_y0), "TECH", font=font(SANS_B, 16), fill=RED)
d.text((colC_x, mid_y0 + 22), "HUANG BACK AS", font=hf2, fill=INK)
d.text((colC_x, mid_y0 + 53), "NVIDIA CEO", font=hf2, fill=INK)
draw_wrapped(d, colC_x, mid_y0 + 96,
             "Chipmaker reinstates its chief after Trump intervenes.",
             font(SANS, 17), colC_w, leading=21)

y = mid_y0 + 148
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 12

# ---------------------------------------------------------------- bottom band: AROUND THE WORLD
band_f = font(SANS_B, 20)
d.text((MARGIN, y), "AROUND THE WORLD", font=band_f, fill=INK)
rule(d, y + 24, MARGIN, W - MARGIN, width=3, fill=RED)
y += 32

briefs = [
    ("IRAN", "Vows \u201cevery means\u201d vs US Hormuz blockade"),
    ("USA", "Democrats clinch House majority \u2014 258 seats"),
    ("FOOTBALL", "UK to host 2035 Women\u2019s World Cup"),
    ("MANCHESTER", "Thousands flee concert in substance scare"),
    ("INDONESIA", "Factory fire probe \u2014 34 people missing"),
    ("WEST BANK", "Settler arson hits five villages"),
    ("UKRAINE WAR", "490,000 Russian dead; toll may top 740,000"),
    ("GAZA", "Oxfam \u2014 war poisoned air, soil and water"),
]
col_w = (CW - 24) // 2
row_h = 30
for i, (kick, text) in enumerate(briefs):
    bx = MARGIN + (i % 2) * (col_w + 24)
    by = y + (i // 2) * row_h
    line = f"{kick}: {text}"
    # fit the whole line at the largest size that fits the column
    f = fit_font(SANS, line, 19, col_w, min_size=14)
    # draw kicker bold + rest regular by measuring the kicker part
    kf = font(SANS_B, f.size)
    d.text((bx, by), f"{kick}:", font=kf, fill=RED)
    kw = kf.getlength(f"{kick}: ")
    d.text((bx + kw, by), text, font=f, fill=INK)

y += 4 * row_h + 4
rule(d, y, MARGIN, W - MARGIN, width=1)
y += 6

# ---------------------------------------------------------------- footer
foot_f = font(SANS_B, 14)
draw_centered(d, y, "THE WORLD TODAY  \u2022  TUESDAY 24 NOVEMBER 2026", foot_f, fill=GREY)

img.save(OUT, format="PNG", optimize=True)
print("saved", OUT, img.size)
