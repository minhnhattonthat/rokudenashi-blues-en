"""Title menu (sprites): redraw the 16x16 kana glyph block as English items and rewrite the menu metasprite.

Block: LZ at file 0x809F5 ($90:89F5) -> 70 4bpp tiles loaded at OBJ tile $80 (16x16 sprites $80-$BF, 8x8 $C0-$C5;
$C4/$C5 are the selection bar and stay). Metasprite at 0x80F3C ($90:8F3C): entries size(1=16x16), x, y, tile,
attr; $80 ends. Items sit at y = 16 * row, starting at x = -64; each English item gets 4 sprites (64 px).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import font  # noqa: E402
import lz  # noqa: E402

BLOCK, BLOCK_MAX = 0x809F5, 0x80F3C - 0x809F5
META = 0x80F3C
ITEMS = ["Story Mode", "1P Blues", "2P Blues", "Options"]
FILL, EDGE = 1, 6  # the original glyphs' fill and dark outline colours
WIDTH = 64


def render(text):
    """-> 16 rows x 64 cols of palette indices (outlined text, 1 px left margin)."""
    art, wid = font.parse(), font.widths()
    mask = [[0] * WIDTH for _ in range(16)]
    x = 1
    for ch in text:
        for r, row in enumerate(art[ch]):
            for c, p in enumerate(row):
                if p == "#":
                    mask[r][x + c] = 1
        x += wid[ch]
    assert x <= WIDTH, (text, x)
    out = [[0] * WIDTH for _ in range(16)]
    for y in range(16):
        for x in range(WIDTH):
            if mask[y][x]:
                out[y][x] = FILL
            elif any(mask[yy][xx] for yy in range(max(0, y - 1), min(16, y + 2))
                     for xx in range(max(0, x - 1), min(WIDTH, x + 2))):
                out[y][x] = EDGE
    return out


def encode_tile(px):
    """8x8 palette indices -> 32 bytes of SNES 4bpp."""
    b = bytearray(32)
    for y in range(8):
        for x in range(8):
            v = px[y][x]
            for p in range(4):
                if v >> p & 1:
                    b[(p // 2) * 16 + y * 2 + (p & 1)] |= 0x80 >> x
    return bytes(b)


def patch(rom):
    raw = bytearray(lz.decompress(rom, BLOCK)[0])
    meta = bytearray()
    for k, text in enumerate(ITEMS):
        px = render(text)
        for j in range(4):
            s = k * 4 + j
            t = (s % 8) * 2 + (s // 8) * 32  # top-left tile of 16x16 sprite slot s
            for dy in range(2):
                for dx in range(2):
                    cell = [row[16 * j + 8 * dx:16 * j + 8 * dx + 8] for row in px[8 * dy:8 * dy + 8]]
                    raw[32 * (t + dx + 16 * dy):32 * (t + dx + 16 * dy + 1)] = encode_tile(cell)
            meta += bytes([1, (0xC0 + 16 * j) & 0xFF, 16 * k, 0x80 + t, 0x32])
    meta.append(0x80)
    comp = lz.compress(bytes(raw))
    if len(comp) > BLOCK_MAX:
        raise ValueError(f"title menu block {len(comp)} > {BLOCK_MAX} bytes")
    rom[BLOCK:BLOCK + len(comp)] = comp
    rom[META:META + len(meta)] = meta
