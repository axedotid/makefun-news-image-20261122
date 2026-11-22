#!/usr/bin/env python3
"""Build a 1024x1024 newspaper front page as entry.png using Pillow."""

from PIL import Image, ImageDraw, ImageFont

# Canvas
W, H = 1024, 1024
img = Image.new("RGB", (W, H), "#e8d9b5")  # newsprint tan
draw = ImageDraw.Draw(img)

# Fonts
BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG_PATH  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def bold(size):  return ImageFont.truetype(BOLD_PATH, size)
def regular(size): return ImageFont.truetype(REG_PATH, size)

# ── Top band ────────────────────────────────────────────────────────────────
band = Image.new("RGB", (W, 170), "#1a1a1a")
img.paste(band, (0, 0))

tag_font = bold(20)
date_font = bold(82)

# "THE WORLD IN ONE DAY" – letterspaced, white, centred in band
tag_text = "THE WORLD IN ONE DAY"
# approximate letter-spacing by inserting spaces
spaced_tag = tag_text  # normal spacing reads better than letterspacing at this size
bw, bh = draw.textbbox((0, 0), spaced_tag, font=tag_font)[2:]
draw.text(((W - bw) // 2, 18), spaced_tag, font=tag_font, fill="#d0d0d0")

# "22 NOVEMBER 2026" – huge
date_text = "22 NOVEMBER 2026"
dw, dh = draw.textbbox((0, 0), date_text, font=date_font)[2:]
draw.text(((W - dw) // 2, 65), date_text, font=date_font, fill="#f0f0f0")

# ── Card grid ────────────────────────────────────────────────────────────────
cards = [
    ("EUROPE",       "#c0392b", "BALTIC SHIP HIT"),
    ("EUROPE",       "#c0392b", "LVIV BARRAGE"),
    ("MIDDLE EAST",  "#d35400", "IRAN HITS BAHRAIN"),
    ("MIDDLE EAST",  "#d35400", "F-16 CLAIM DENIED"),
    ("MIDDLE EAST",  "#d35400", "HORMUZ TALKS"),
    ("AFRICA",       "#27ae60", "NIGERIA BOAT"),
    ("ASIA",         "#8e44ad", "MALUKU QUAKE"),
    ("AMERICAS",     "#2980b9", "SINALOA CAPTURE"),
    ("TECH",         "#16a085", "LONDON AI MARCH"),
    ("SPACE",        "#2c3e50", "MERCURY ORBIT"),
]

# Grid layout
MARGIN  = 28
TOP     = 180   # y where cards start
GAP     = 14
COLS    = 2
ROWS    = 5
card_w  = (W - MARGIN * 2 - GAP) // COLS
FOOTER_H = 60
card_h  = (H - FOOTER_H - TOP - GAP * (ROWS - 1)) // ROWS

def draw_mark(d, x, y, w, h, color, idx):
    """Simple geometric mark from PIL primitives."""
    cx, cy = x + w // 2, y + h // 2
    r = min(w, h) // 3
    if idx % 3 == 0:
        # diagonal cross
        d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=color, width=4)
        d.line([(cx + r, cy - r), (cx - r, cy + r)], fill=color, width=4)
    elif idx % 3 == 1:
        # filled circle
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    else:
        # rectangle
        d.rectangle([cx - r, cy - r // 2, cx + r, cy + r // 2], fill=color)

for i, (region, color, label) in enumerate(cards):
    col = i % COLS
    row = i // COLS
    cx = MARGIN + col * (card_w + GAP)
    cy = TOP + row * (card_h + GAP)

    # card background
    draw.rectangle([cx, cy, cx + card_w - 1, cy + card_h - 1], fill="#f5e6c8", outline="#aaa")

    # region tag (small-caps via uppercase)
    tag_sz = 18
    tag_f  = bold(tag_sz)
    tag_txt = region.upper()
    tw, th = draw.textbbox((0, 0), tag_txt, font=tag_f)[2:]
    draw.text((cx + 12, cy + 10), tag_txt, font=tag_f, fill=color)

    # mark sits in the upper part of the card, label owns the strip below it
    label_f  = bold(38)
    max_lw   = card_w - 24
    label_h  = 44
    mark_top = cy + 30
    mark_h   = card_h - 30 - label_h - 8
    mark_w   = card_w - 24
    mark_x   = cx + 12
    mark_y   = mark_top

    draw_mark(draw, mark_x, mark_y, mark_w, mark_h, color, i)

    # one line, shrink once if it would run past the card
    f = label_f
    lw = draw.textbbox((0, 0), label, font=f)[2]
    if lw > max_lw:
        f = bold(30)
        lw = draw.textbbox((0, 0), label, font=f)[2]
    ly = cy + card_h - label_h + 4
    draw.text((cx + (card_w - lw) // 2, ly), label, font=f, fill="#111")

# ── Footer strip ─────────────────────────────────────────────────────────────
footer_top = H - 60
draw.rectangle([0, footer_top, W - 1, H - 1], fill="#1a1a1a")

foot_f = regular(22)

# "ALSO" then dot-separated items
also_label = "ALSO"
also_w, _ = draw.textbbox((0, 0), also_label, font=foot_f)[2:]
draw.text((MARGIN, footer_top + 16), also_label, font=foot_f, fill="#f0f0f0")

items = ["NATO ON POLAND", "SAUDI STRIKES", "BRUSSELS STRIKE", "JAPAN PETITION"]
sep = "  \u00b7  "  # middle dot separator with padding
all_items = sep.join(items)
draw.text((MARGIN + also_w + 14, footer_top + 16), all_items, font=foot_f, fill="#d0d0d0")

# ── Save ──────────────────────────────────────────────────────────────────────
out = "entry.png"
img.save(out, "PNG")
size = len(open(out, "rb").read())

print(f"Font path: {BOLD_PATH}")
print(f"PNG byte size: {size}")
