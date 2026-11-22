#!/usr/bin/env python3
"""Draw entry.png: "The World on Saturday" — a front-page poster summing up
the world news of Saturday 21 November 2026.

Run with the project venv:  ~/workspace/makefun/.venv/bin/python draw_image.py
Writes entry.png (1024x1024) next to this file. The grader never runs this
script; main.ts copies the finished entry.png to /output/entry.png.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

S = 2  # supersampling factor; canvas is drawn at 2048 and shrunk to 1024
W = 1024

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

INK = (26, 26, 30)
PAPER = (248, 245, 238)
PANEL = (255, 255, 255)
RULE = (26, 26, 30)
RED = (168, 32, 40)
NAVY = (31, 58, 95)
GOLD = (198, 152, 40)
SLATE = (52, 60, 72)
GREY = (96, 96, 100)


def F(path, size):
    return ImageFont.truetype(path, size * S)


def text_w(d, s, font):
    return d.textlength(s, font=font)


def wrap(d, s, font, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if text_w(d, t, font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def centered(d, cx, y, s, font, fill, tracking=0):
    """Draw one line centered at cx; returns its height."""
    if tracking:
        total = sum(text_w(d, ch, font) for ch in s) + tracking * S * (len(s) - 1)
        x = cx - total / 2
        for ch in s:
            d.text((x, y), ch, font=font, fill=fill)
            x += text_w(d, ch, font) + tracking * S
        return font.size
    w_ = text_w(d, s, font)
    d.text((cx - w_ / 2, y), s, font=font, fill=fill)
    return font.size


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------- pictograms
# Each icon draws itself around (cx, cy) on its own transparent layer of
# 240x150 design units; render_icon() scales it into the panel.
def icon_badge(d, cx, cy):
    """Police shield with a star: a cartel boss captured."""
    pts = [(cx - 56, cy - 52), (cx + 56, cy - 52), (cx + 56, cy + 6),
           (cx, cy + 62), (cx - 56, cy + 6)]
    d.polygon(pts, fill=NAVY)
    inner = [(cx - 42, cy - 40), (cx + 42, cy - 40), (cx + 42, cy + 4),
             (cx, cy + 48), (cx - 42, cy + 4)]
    d.polygon(inner, fill=(70, 105, 150))
    star(d, cx, cy - 2, 17, (255, 255, 255))
    d.ellipse([cx - 5, cy + 20, cx + 5, cy + 30], fill=GOLD)


def icon_strike(d, cx, cy):
    """Skyline, an incoming missile and a burst."""
    base = cy + 58
    blocks = [(-86, 34), (-58, 52), (-26, 26), (2, 46), (34, 30), (60, 40)]
    for off, h in blocks:
        d.rectangle([cx + off, base - h, cx + off + 22, base], fill=SLATE)
    d.rectangle([cx - 92, base, cx + 92, base + 5], fill=INK)
    # missile descending from top right toward the city
    mx, my = cx + 52, cy - 62
    d.polygon([(mx, my), (mx + 32, my - 32), (mx + 48, my - 16), (mx + 16, my + 16)],
              fill=RED)
    d.polygon([(mx + 2, my + 14), (mx - 14, my + 30), (mx + 16, my + 16)], fill=GOLD)
    for t in (0.4, 0.7, 1.0):  # trail
        px, py = mx + 36 * t + 10, my - 36 * t - 10
        d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(170, 170, 175))
    # burst above the skyline
    bx, by = cx - 8, base - 56
    for i in range(8):
        ang = i * math.pi / 4 + 0.3
        d.line([bx, by, bx + 19 * math.cos(ang), by + 19 * math.sin(ang)],
               fill=RED, width=4 * S)
    d.ellipse([bx - 7, by - 7, bx + 7, by + 7], fill=GOLD)


def icon_globe(d, cx, cy):
    """A globe with a green leaf: climate talks."""
    r = 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 110, 160))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 255, 255), width=3 * S)
    d.ellipse([cx - 20, cy - r, cx + 20, cy + r], outline=(255, 255, 255), width=3 * S)
    d.line([cx - r, cy, cx + r, cy], fill=(255, 255, 255), width=3 * S)
    d.line([cx - r + 14, cy - 30, cx + r - 14, cy - 30], fill=(255, 255, 255),
           width=2 * S)
    d.line([cx - r + 14, cy + 30, cx + r - 14, cy + 30], fill=(255, 255, 255),
           width=2 * S)
    # leaf sprouting at the top right
    lx, ly = cx + 34, cy - 58
    d.polygon([(lx, ly + 12), (lx + 4, ly - 12), (lx + 26, ly - 6), (lx + 20, ly + 12)],
              fill=(60, 160, 90))
    d.line([lx + 2, ly + 12, lx - 8, ly + 22], fill=(60, 160, 90), width=3 * S)


def icon_chart(d, cx, cy):
    """Descending bars and a falling arrow: markets slide."""
    base = cy + 55
    heights = [66, 52, 40, 26, 14]
    for i, h in enumerate(heights):
        x = cx - 80 + i * 34
        d.rectangle([x, base - h, x + 24, base], fill=RED)
    d.rectangle([cx - 88, base, cx + 88, base + 5], fill=INK)
    # falling arrow above the bars
    ax0, ay0, ax1, ay1 = cx - 84, cy - 58, cx + 78, cy - 2
    d.line([ax0, ay0, ax1, ay1], fill=RED, width=5 * S)
    d.polygon([(ax1, ay1), (ax1 - 22, ay1 - 2), (ax1 - 6, ay1 - 20)], fill=RED)


def icon_quake(d, cx, cy):
    """Seismograph trace in a chart box."""
    d.rectangle([cx - 92, cy - 46, cx + 92, cy + 46], outline=INK, width=3 * S)
    d.line([cx - 92, cy, cx + 92, cy], fill=(200, 200, 205), width=2 * S)
    pts = [(-84, 0), (-70, 0), (-60, -26), (-50, 20), (-40, -6), (-30, 0),
           (-16, 0), (-6, -32), (4, 28), (14, -10), (28, 0), (44, 0),
           (54, -18), (64, 12), (80, 0)]
    xy = [(cx + dx, cy + dy) for dx, dy in pts]
    d.line(xy, fill=RED, width=4 * S, joint="curve")
    # cracks below the box
    d.line([cx - 52, cy + 52, cx - 40, cy + 66], fill=INK, width=3 * S)
    d.line([cx + 8, cy + 52, cx + 22, cy + 66], fill=INK, width=3 * S)


def icon_mercury(d, cx, cy):
    """Mercury with craters, an orbit ring and a small probe."""
    # orbit ellipse first, planet drawn over it
    d.ellipse([cx - 96, cy - 44, cx + 96, cy + 44], outline=GOLD, width=4 * S)
    r = 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(168, 148, 120))
    for dx, dy, rr in [(-16, -10, 9), (12, 6, 11), (-4, 18, 6), (18, -18, 5),
                       (-22, 14, 4)]:
        d.ellipse([cx + dx - rr, cy + dy - rr, cx + dx + rr, cy + dy + rr],
                  fill=(120, 100, 80))
    # small probe riding the orbit, top right
    px, py = cx + 66, cy - 38
    d.rectangle([px - 10, py - 6, px + 10, py + 6], fill=NAVY)
    d.rectangle([px - 22, py - 3, px - 10, py + 3], fill=SLATE)
    d.rectangle([px + 10, py - 3, px + 22, py + 3], fill=SLATE)


def render_icon(img, icon, ccx, cy, max_w=205, max_h=86):
    """Draw an icon on its own layer, trim its transparent margins, and
    paste it scaled to fit a max_w x max_h box, centered at (ccx, cy)."""
    layer = Image.new("RGBA", (240 * S, 150 * S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    icon(ld, 120 * S, 75 * S)
    bbox = layer.getbbox()
    if bbox:
        layer = layer.crop(bbox)
    scale = min(max_w * S / layer.width, max_h * S / layer.height)
    layer = layer.resize((round(layer.width * scale), round(layer.height * scale)),
                         Image.LANCZOS)
    img.paste(layer, (round(ccx * S - layer.width / 2), round(cy * S - layer.height / 2)),
              layer)


# ------------------------------------------------------------------- layout
STORIES = [
    ("MEXICO · SINALOA", RED, icon_badge,
     "MEXICO CAPTURES FBI MOST-WANTED BOSS",
     "'El Chapo Isidro' seized in Guasave, Sinaloa, with US help."),
    ("WAR · UKRAINE", RED, icon_strike,
     "MISSILES HIT ZELENSKYY'S HOMETOWN",
     "Double-tap strike on Kryvyi Rih kills 2, wounds 60."),
    ("CLIMATE · ANTALYA", NAVY, icon_globe,
     "COP31 CLIMATE TALKS RUN INTO OVERTIME",
     "Antalya summit passes deadline; fossil fuels absent from draft."),
    ("MARKETS · WORLD", RED, icon_chart,
     "AI SELL-OFF DRAGS MARKETS DOWN",
     "S&P 500 falls 3.7%; Nikkei drops 5.06% as chip shares plunge."),
    ("EARTHQUAKE · PERU", NAVY, icon_quake,
     "6.7 QUAKE SHAKES PERU",
     "Quake near Junín felt in Lima, reported 21 Nov; no deaths."),
    ("SPACE · MERCURY", NAVY, icon_mercury,
     "BEPICOLOMBO REACHES MERCURY",
     "After 8 years in space, ESA–JAXA probe enters Mercury orbit."),
]


def main():
    img = Image.new("RGB", (W * S, W * S), PAPER)
    d = ImageDraw.Draw(img)

    def X(v):
        return v * S

    # masthead
    d.rectangle([X(30), X(24), X(994), X(28)], fill=RULE)
    centered(d, X(512), X(36), "THE WORLD ON SATURDAY", F(SERIF_B, 54), INK, tracking=2)
    d.rectangle([X(30), X(106), X(994), X(110)], fill=RULE)

    # date band
    d.rectangle([X(30), X(120), X(994), X(182)], fill=INK)
    centered(d, X(512), X(129), "SATURDAY 21 NOVEMBER 2026", F(SANS_B, 48), (255, 255, 255),
             tracking=1)

    # panels: 2 cols x 3 rows, 192..980
    gx, gy = 14, 14
    px0, py0 = 30, 192
    pw = (1024 - 60 - gx) // 2
    ph = (980 - py0 - 2 * gy) // 3
    kick_f, head_f, sub_f = F(SANS_B, 18), F(SANS_B, 30), F(SANS, 21)
    for i, (kicker, accent, icon, head, sub) in enumerate(STORIES):
        cx0 = px0 + (i % 2) * (pw + gx)
        cy0 = py0 + (i // 2) * (ph + gy)
        d.rectangle([X(cx0), X(cy0), X(cx0 + pw), X(cy0 + ph)], fill=PANEL,
                    outline=(200, 195, 185), width=S)
        d.rectangle([X(cx0), X(cy0), X(cx0 + pw), X(cy0 + 6)], fill=accent)
        ccx = cx0 + pw // 2
        centered(d, X(ccx), X(cy0 + 11), kicker, kick_f, accent, tracking=2)
        render_icon(img, icon, ccx, cy0 + 71)
        y = cy0 + 116
        for line in wrap(d, head, head_f, X(pw - 36)):
            centered(d, X(ccx), X(y), line, head_f, INK)
            y += 38
        y += 3
        for line in wrap(d, sub, sub_f, X(pw - 44)):
            centered(d, X(ccx), X(y), line, sub_f, (60, 60, 66))
            y += 26

    # footer
    d.rectangle([X(30), X(988), X(994), X(991)], fill=RULE)
    centered(d, X(512), X(995),
             "SIX STORIES · ONE DAY · AS REPORTED BY AP, REUTERS, AFP, NPR, ESA AND USGS",
             F(SANS_B, 14), GREY, tracking=1)

    img = img.resize((W, W), Image.LANCZOS)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
