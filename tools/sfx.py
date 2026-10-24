"""Story cutscene sound effects (BG3, 2bpp): バキッ, ドカッ... redrawn as English.

The effects are 6x2-cell BG3 tilemaps in a table at $88:C30F (file 0x4430F, 24 bytes each: a row of 6 words, then
the row below). Map words $3Exx = tile $200+xx, palette 7: a sheet of 16x16 katakana at VRAM $A000 (BG3 chr base
$8000), uploaded raw from file 0x2EF9C (sheet tile n at +16n; a glyph's bottom half is tile n+$10). Fill is colour 2,
the outline colour 3. We draw one English letter per 8x16 cell (the dialogue font's art) into the katakana tiles
($10-$1F and $30-$34 tops, bottoms at +$10) and rewrite the maps.

    python -X utf8 tools/sfx.py preview OUT.png
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import font  # noqa: E402
import text  # noqa: E402
from hud import decode2, encode2  # noqa: E402

SHEET, TABLE = 0x2EF9C, 0x4430F
WORDS = ["WHAP!", "CLANG!", "BONK!", "BONG!", "WHAM!", "THUD!", "CRACK!", "WHACK", "SMACK!"]  # ガッ ガン ゴッ ゴン ドカッ ドス バキッ バコ バシッ
SLOTS = list(range(0x10, 0x20)) + list(range(0x30, 0x35))
BLANK, ATTR = 0x02A0, 0x3E00
FILL, EDGE = 2, 3


def letter(ch):
    """-> 16 rows x 8 px: the dialogue font's letter, emboldened, in FILL with a 1-px EDGE outline."""
    art = font.parse()[ch]
    cols = [x for x in range(len(art[0])) if any(r[x] == "#" for r in art)]
    m = [[1 if r[x] == "#" else 0 for x in range(cols[0], cols[-1] + 1)] for r in art]
    if len(m[0]) <= 5:  # bold: a second copy 1 px right, where the cell has room
        m = [[a | (row[x - 1] if x else 0) for x, a in enumerate(row + [0])] for row in m]
    w = len(m[0])
    assert w <= 8, (ch, w)
    x0 = (8 - w) // 2  # W and M fill the cell; their outline is cut at its edges
    ink = [[0] * 8 for _ in range(16)]
    for y, row in enumerate(m):
        for x, p in enumerate(row):
            ink[y][x0 + x] = p
    return [[FILL if ink[y][x] else EDGE if any(ink[yy][xx] for yy in range(max(0, y - 1), min(16, y + 2))
                                                for xx in range(max(0, x - 1), min(8, x + 2))) else 0
             for x in range(8)] for y in range(16)]


def patch(rom):
    chars = sorted(set("".join(WORDS)))
    assert len(chars) <= len(SLOTS), chars
    slot = dict(zip(chars, SLOTS))
    for ch, t in slot.items():
        px = letter(ch)
        for half in range(2):
            o = SHEET + 16 * (t + 0x10 * half)
            rom[o:o + 16] = encode2(px[8 * half:8 * half + 8])
    for k, word in enumerate(WORDS):
        assert len(word) <= 6, word
        for row in range(2):
            cells = [ATTR | (slot[ch] + 0x10 * row) for ch in word] + [BLANK] * (6 - len(word))
            o = TABLE + 24 * k + 12 * row
            rom[o:o + 12] = b"".join(c.to_bytes(2, "little") for c in cells)


def preview(out):
    from PIL import Image
    rom = bytearray(text.ROM.read_bytes())
    patch(rom)
    pal = [(40, 40, 40), (0, 0, 0), (248, 232, 0), (216, 0, 0)]
    img = Image.new("RGB", (48, 18 * len(WORDS)), pal[0])
    for k in range(len(WORDS)):
        for row in range(2):
            for c in range(6):
                o = TABLE + 24 * k + 12 * row + 2 * c
                t = (int.from_bytes(rom[o:o + 2], "little") & 0x3FF) - 0x200
                if t == (BLANK & 0x3FF) - 0x200:
                    continue
                px = decode2(rom[SHEET + 16 * t:][:16])
                for y in range(8):
                    for x in range(8):
                        img.putpixel((8 * c + x, 18 * k + 8 * row + y), pal[px[y][x]])
    img.resize((img.width * 4, img.height * 4), Image.NEAREST).save(out)


if __name__ == "__main__":
    if sys.argv[1:2] == ["preview"]:
        preview(sys.argv[2])
    else:
        sys.exit(__doc__)
