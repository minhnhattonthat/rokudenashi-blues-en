"""Fight HUD (BG3, 2bpp, raw tiles at file 0x29B37 = $85:9B37, tile n at +16n): the 怒 gauge badge and the fight
banners, redrawn in place.

The story HUD loads tiles 0-$4F of the sheet (DMA at $88:8094/$88:85A2), VS mode tiles 0-$7F ($AF:887E). Banners are
drawn by tilemap records at $AF:F040- (VRAM word, byte count, source): 始め tiles $34-$45 and 待て $46-$57 are 6x3
cells, 共倒れ $58-$6F is 8x3. The badge is cells $23 $1F $20 $23(flipped) over $23 $21 $22 $23: only the 16x16
middle carries the kanji, the shared $23 ends stay.

    python -X utf8 tools/hud.py preview OUT.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import text  # noqa: E402
from titlelogo import mask  # noqa: E402

SHEET = 0x29B37
# first tile, cells wide, text, cap height, horizontal squeeze
BANNERS = [(0x34, 6, "FIGHT!", 15, 1.0), (0x46, 6, "WAIT!", 15, 1.0), (0x58, 8, "DOUBLE KO", 12, 1.0)]
FILL, SHADE, EDGE = 1, 2, 3  # banner palette 6: yellow, brown, dark blue (as the kana)
BADGE = (0x1F, 0x20, 0x21, 0x22)  # 2x2 middle of the 怒 badge: TL TR BL BR
BADGE_INK = 2  # badge palette 5: 1 orange, 2 yellow, 3 dark red background
BADGE_BG = 3
RAGE = {  # 3x7 caps, so the four letters fit the 16-px middle of the badge
    "R": ["##.", "#.#", "#.#", "##.", "#.#", "#.#", "#.#"],
    "A": [".#.", "#.#", "#.#", "###", "#.#", "#.#", "#.#"],
    "G": [".##", "#..", "#..", "#.#", "#.#", "#.#", ".##"],
    "E": ["###", "#..", "#..", "##.", "#..", "#..", "###"],
}


def encode2(px):
    """8x8 indices -> 16 bytes of SNES 2bpp."""
    b = bytearray(16)
    for y in range(8):
        for x in range(8):
            for p in range(2):
                if px[y][x] >> p & 1:
                    b[2 * y + p] |= 0x80 >> x
    return bytes(b)


def decode2(data):
    return [[(data[2 * y] >> (7 - x) & 1) | (data[2 * y + 1] >> (7 - x) & 1) << 1 for x in range(8)] for y in range(8)]


def banner(s, w, cap, xscale):
    """-> 24 rows x 8w px: outlined lettering with a brown lower edge, like the kana banners."""
    m = mask(s, cap, track=1, xscale=xscale)
    width = 8 * w
    assert len(m[0]) + 2 <= width, (s, len(m[0]), width)
    x0, y0 = (width - len(m[0])) // 2, 4
    ink = [[0] * width for _ in range(24)]
    for y, row in enumerate(m):
        for x, p in enumerate(row):
            ink[y0 + y][x0 + x] = p
    out = [[0] * width for _ in range(24)]
    for y in range(24):
        for x in range(width):
            if ink[y][x]:
                out[y][x] = FILL if y + 1 < 24 and ink[y + 1][x] else SHADE
            elif any(ink[yy][xx] for yy in range(max(0, y - 1), min(24, y + 2))
                     for xx in range(max(0, x - 1), min(width, x + 2))):
                out[y][x] = EDGE
    return out


def badge():
    """-> 16x16: RAGE in yellow on the badge's dark red, rows 4-10."""
    out = [[BADGE_BG] * 16 for _ in range(16)]
    x = 1
    for ch in "RAGE":
        for r, row in enumerate(RAGE[ch]):
            for c, p in enumerate(row):
                if p == "#":
                    out[4 + r][x + c] = BADGE_INK
        x += 4
    return out


def patch(rom):
    for first, w, s, cap, xscale in BANNERS:
        px = banner(s, w, cap, xscale)
        for cy in range(3):
            for cx in range(w):
                o = SHEET + 16 * (first + cy * w + cx)
                rom[o:o + 16] = encode2([row[8 * cx:8 * cx + 8] for row in px[8 * cy:8 * cy + 8]])
    px = badge()
    old = [decode2(rom[SHEET + 16 * t:SHEET + 16 * t + 16]) for t in BADGE]
    for k, t in enumerate(BADGE):
        cell = [row[8 * (k & 1):8 * (k & 1) + 8] for row in px[8 * (k >> 1):8 * (k >> 1) + 8]]
        # keep the badge's own outline/background where the old cell had no kanji ink (index 0 = transparent)
        cell = [[0 if old[k][y][x] == 0 else cell[y][x] for x in range(8)] for y in range(8)]
        rom[SHEET + 16 * t:SHEET + 16 * t + 16] = encode2(cell)


def preview(out):
    from PIL import Image
    rom = bytearray(text.ROM.read_bytes())
    patch(rom)
    pals = {"banner": [(0, 0, 0), (224, 224, 96), (104, 72, 0), (0, 0, 128)],
            "badge": [(0, 0, 0), (216, 64, 0), (248, 248, 64), (144, 32, 32)]}
    img = Image.new("RGB", (64 + 8, 3 * 28 + 20), (60, 60, 60))
    y = 0
    for first, w, *_ in BANNERS:
        for cy in range(3):
            for cx in range(w):
                t = decode2(rom[SHEET + 16 * (first + cy * w + cx):][:16])
                for yy in range(8):
                    for xx in range(8):
                        img.putpixel((8 * cx + xx, y + 8 * cy + yy), pals["banner"][t[yy][xx]])
        y += 28
    for k, t in enumerate((0x23, 0x1F, 0x20, 0x23, 0x23, 0x21, 0x22, 0x23)):
        c = decode2(rom[SHEET + 16 * t:][:16])
        flip = k in (3, 7)
        for yy in range(8):
            for xx in range(8):
                img.putpixel((8 * (k % 4) + xx, y + 8 * (k // 4) + yy), pals["badge"][c[yy][7 - xx if flip else xx]])
    img.resize((img.width * 4, img.height * 4), Image.NEAREST).save(out)


if __name__ == "__main__":
    if sys.argv[1:2] == ["preview"]:
        preview(sys.argv[2])
    else:
        sys.exit(__doc__)
