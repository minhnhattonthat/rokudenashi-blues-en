"""Options screen: English controller labels on BG3 (2bpp 8x8).

The loader at $8F:AC9F decompresses (tools/lz.py) the BG3 font $8F:B6F9 (34 tiles -> VRAM $4000; text colour 2 with
a colour-3 shadow on the right) and the BG3 tilemap $8F:B9EC (-> VRAM $2800). Labels sit in rows 17-22, 7 cells
from column 7 (1P) and column 20 (2P), dot leaders up to the button letter. We append tiles for each English label
(a 4x7 font, shadowed like the original) after tile $21 and point those cells at them. Both blocks move to free
space in bank $B0 (patched LDA #addr / LDX #bank operands at $8F:AD72 and $8F:ADA7).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import lz  # noqa: E402
import text  # noqa: E402

FONT_SRC, MAP_SRC = 0x7B6F9, 0x7B9EC
FONT_OPERAND, MAP_OPERAND = 0x8FAD73, 0x8FADA8  # LDA #imm16; the LDX #bank operand follows 3 bytes later
ROWS = {17: "PUNCH", 18: "KICK", 19: "SUPER PUNCH", 20: "SUPER KICK", 21: "DODGE", 22: "DODGE"}
COLS = (7, 20)
CELLS = 7
GLYPHS = {
    "P": ["###.", "#..#", "#..#", "###.", "#...", "#...", "#..."],
    "U": ["#..#", "#..#", "#..#", "#..#", "#..#", "#..#", ".##."],
    "N": ["#..#", "##.#", "##.#", "#.##", "#.##", "#..#", "#..#"],
    "C": [".##.", "#..#", "#...", "#...", "#...", "#..#", ".##."],
    "H": ["#..#", "#..#", "#..#", "####", "#..#", "#..#", "#..#"],
    "K": ["#..#", "#.#.", "##..", "##..", "#.#.", "#..#", "#..#"],
    "I": ["###", ".#.", ".#.", ".#.", ".#.", ".#.", "###"],
    "S": [".##.", "#..#", "#...", ".##.", "...#", "#..#", ".##."],
    "E": ["####", "#...", "#...", "###.", "#...", "#...", "####"],
    "R": ["###.", "#..#", "#..#", "###.", "#.#.", "#..#", "#..#"],
    "D": ["###.", "#..#", "#..#", "#..#", "#..#", "#..#", "###."],
    "O": [".##.", "#..#", "#..#", "#..#", "#..#", "#..#", ".##."],
    "G": [".##.", "#..#", "#...", "#.##", "#..#", "#..#", ".###"],
}
SPACE = 3


def label_pixels(word):
    """-> 8 rows x 56 px of colour indices: text (2, shadow 3 on the right), then dot leaders like tile $21."""
    w = CELLS * 8
    ink = [[0] * w for _ in range(8)]
    x = 0
    for ch in word:
        if ch == " ":
            x += SPACE
            continue
        g = GLYPHS[ch]
        for r, row in enumerate(g):
            for c, p in enumerate(row):
                if p == "#":
                    ink[r][x + c] = 1
        x += len(g[0]) + 1
    assert x <= w, (word, x)
    px = [[2 if ink[r][c] else (3 if c and ink[r][c - 1] else 0) for c in range(w)] for r in range(8)]
    for c in range(x + 2, w - 1):
        if c % 4 == 1:
            px[4][c], px[4][c + 1] = 2, 3
    return px


def encode2(px):
    b = bytearray(16)
    for y in range(8):
        for x in range(8):
            for p in range(2):
                if px[y][x] >> p & 1:
                    b[y * 2 + p] |= 0x80 >> x
    return bytes(b)


def patch(rom, place):
    """place(data) -> file offset of a free spot for data (must not cross a bank)."""
    font = bytearray(lz.decompress(rom, FONT_SRC)[0])
    tmap = bytearray(lz.decompress(rom, MAP_SRC)[0])
    tiles = {}
    for word in dict.fromkeys(ROWS.values()):
        px = label_pixels(word)
        tiles[word] = len(font) // 16
        for k in range(CELLS):
            font += encode2([row[8 * k:8 * k + 8] for row in px])
    for row, word in ROWS.items():
        for col in COLS:
            for k in range(CELLS):
                i = 2 * (row * 32 + col + k)
                tmap[i] = tiles[word] + k
                assert tiles[word] + k < 0x100
    for data, operand in ((font, FONT_OPERAND), (tmap, MAP_OPERAND)):
        comp = lz.compress(bytes(data))
        off = place(comp)
        rom[off:off + len(comp)] = comp
        addr = text.cpu(off)
        o = text.lorom(operand)
        rom[o:o + 2] = (addr & 0xFFFF).to_bytes(2, "little")
        assert rom[o + 2] == 0xA2  # LDX #bank
        rom[o + 3:o + 5] = (addr >> 16).to_bytes(2, "little")
