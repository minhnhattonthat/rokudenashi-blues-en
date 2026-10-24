"""Title logo: ろくでなし -> ROKUDENASHI (BG), ブルース reading removed, 対決！東京四天王 -> SHOWDOWN! / TOKYO'S
FOUR KINGS (sprites). Lettering: font/Anton-Regular.ttf (OFL), rendered without antialiasing.

BG1 and BG2 (the grey drop shadow: same map, palette + 1) share one tilemap, LZ $8E:A5F2 (loader $88:DF8B), and
chr at VRAM $6000: $8E:93E3 (BLUES, tiles 0-$FF) and $8E:9F67 (ろくでなし, tiles $100-, loader $88:DEFD; its
tiles $140-$154 also draw BLUES). The subtitle and the copyright line are one metasprite at $90:88D2 (origin
x 128, y 138) over OBJ tiles $100- from LZ $90:8200 (loader $88:DE0F, DMA to VRAM $5000, room for 128 tiles
before the title menu block at $5800).

Mini logo (screen at $88:FA6D, likely the ending; caller not found, verified offline only): BG1 tiles LZ $AD:9F73
to VRAM 0 (LDA #bank $88:FA86, LDA #addr $88:FA8E), map LZ $AD:B233 to VRAM $2000 (LDA #bank $88:FAC0, LDA #addr
$88:FAC8). ろくでなし = map rows 3-4 cols 4-11, 16 tiles drawn nowhere else; ブルース = row 9 cols 10-12.

    python -X utf8 tools/titlelogo.py preview OUT.png    # both new pieces in their palettes (from ROM data)
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import lz  # noqa: E402
import text  # noqa: E402
from titlemenu import encode_tile  # noqa: E402

FONT = text.ROOT / "font" / "Anton-Regular.ttf"
TITLE, SUBTITLE = "ROKUDENASHI", ("SHOWDOWN!", "TOKYO'S FOUR KINGS")

BG_TILES, BG_TILES_OPERAND = 0x71F67, 0x45EFD  # LDA #addr / LDX #bank
BG_MAP, BG_MAP_BANK, BG_MAP_ADDR = 0x725F2, 0x45F8B, 0x45F90  # LDX #bank ... LDA #addr
BG_KEEP = range(0x40, 0x55)  # block tiles that BLUES uses
LOGO_ROWS, LOGO_COLS = range(2, 6), range(4, 26)  # map cells rewritten for ROKUDENASHI (old art: rows 2-5)
LOGO_TOP, LOGO_H = 2, 29  # pixel rows of the old lettering inside the 32-px band
READING = [(14, c) for c in range(27, 31)]  # ブルース
BG_ATTR = 0x0800  # palette 2

OBJ_BLOCK, OBJ_OPERAND = 0x80200, 0x45E0F
META, META_END = 0x808D2, 0x809F5  # entries size, x, y, tile, attr; $80 ends
COPY_FIRST, COPY_COUNT, COPY_TO = 0x46, 0x19, 0x60  # copyright letters: moved to tiles $60-
SUB_W, SUB_ROWS = 192, 2  # canvas: 12 x 2 sprites of 16x16, x -96..95, y -16..15
OBJ_ATTR = 0x30

MINI_TILES, MINI_TILES_BANK, MINI_TILES_ADDR = 0x169F73, 0x47A86, 0x47A8E  # LDA #bank ... LDA #addr
MINI_MAP, MINI_MAP_BANK, MINI_MAP_ADDR = 0x16B233, 0x47AC0, 0x47AC8
MINI_ROWS, MINI_COLS = range(3, 5), range(3, 13)  # old art cols 4-11; 3 and 12 are blank, new tiles go last
MINI_READING = [(9, c) for c in range(10, 13)]
MINI_BANDS = [2, 2, 3, 3, 3, 4, 5, 5, 5, 6, 6, 6]  # the old lettering's colour per row (palette 1)
MINI_SHEAR = 0.3
_C = "##..##"
MINI_FONT = {  # bold 6x12 caps (a TrueType font at 12 px loses its counters)
    "R": ["#####.", "######", _C, _C, _C, "#####.", "####..", "##.##.", "##.##.", _C, _C, _C],
    "O": [".####.", "######"] + [_C] * 8 + ["######", ".####."],
    "K": [_C, _C, "##.##.", "##.##.", "####..", "###...", "####..", "##.##.", "##.##.", _C, _C, _C],
    "U": [_C] * 10 + ["######", ".####."],
    "D": ["#####.", "######"] + [_C] * 8 + ["######", "#####."],
    "E": ["######", "######", "##....", "##....", "##....", "#####.", "#####.", "##....", "##....", "##....",
          "######", "######"],
    "N": [_C, "###.##", "###.##", "######", "######", "##.###", "##.###", _C, _C, _C, _C, _C],
    "A": [".####.", "######", _C, _C, _C, "######", "######", _C, _C, _C, _C, _C],
    "S": [".####.", "######", _C, "##....", "###...", ".####.", "..###.", "....##", "....##", _C, "######",
          ".####."],
    "H": [_C] * 5 + ["######", "######"] + [_C] * 5,
    "I": ["##"] * 12,
}


def mask(s, cap, shear=0.0, track=1, xscale=1.0):
    """Black-and-white text: -> rows of 0/1, exactly `cap` rows tall (caps only), squeezed by xscale, sheared to
    the right going up."""
    size = cap * 2
    while True:  # find the point size whose cap height is `cap`
        f = ImageFont.truetype(str(FONT), size)
        top, bottom = f.getbbox("H")[1], f.getbbox("H")[3]
        if bottom - top <= cap:
            break
        size -= 1
    w = sum(int(f.getlength(ch)) + track for ch in s) + cap
    img = Image.new("1", (w + 8, bottom + 8), 0)
    d = ImageDraw.Draw(img)
    d.fontmode = "1"
    x = 2
    for ch in s:
        d.text((x, 0), ch, font=f, fill=1)
        x += int(f.getlength(ch)) + track
    img = img.crop((0, top, img.width, top + cap))
    if xscale != 1.0:
        img = img.resize((round(img.width * xscale), cap), Image.NEAREST)
    if shear:
        extra = int(cap * shear) + 1
        img = img.transform((img.width + extra, cap), Image.AFFINE, (1, shear, -shear * cap, 0, 1, 0))
    px = img.load()
    cols = [x for x in range(img.width) if any(px[x, y] for y in range(cap))]
    return [[1 if px[x, y] else 0 for x in range(cols[0], cols[-1] + 1)] for y in range(cap)]


def bands(y, x):
    """ROKUDENASHI fill: the old lettering's red bands 1-4 with a dithered row pair between bands."""
    for edge, lo in ((10, 1), (20, 2)):
        if y < edge:
            return lo
        if y < edge + 2:
            return lo + ((x + y) & 1)
    return 3 if y < 28 else 4


def title_canvas():
    m = mask(TITLE, LOGO_H, shear=0.3, track=1, xscale=0.88)
    w = len(LOGO_COLS) * 8
    assert len(m[0]) <= w, f"ROKUDENASHI is {len(m[0])} px, band is {w}"
    x0 = (w - len(m[0])) // 2
    out = [[0] * w for _ in range(32)]
    for y, row in enumerate(m):
        for x, p in enumerate(row):
            if p:
                out[LOGO_TOP + y][x0 + x] = bands(y, x)
    return out


def subtitle_canvas():
    out = [[0] * SUB_W for _ in range(32)]
    for line, s in enumerate(SUBTITLE):
        m = mask(s, 12, track=1)
        x0, y0 = (SUB_W - len(m[0])) // 2, 16 * line + 2
        assert len(m[0]) + 2 <= SUB_W, (s, len(m[0]))
        for y, row in enumerate(m):
            for x, p in enumerate(row):
                if p:
                    out[y0 + y][x0 + x] = min(11, 5 + y * 7 // 12)  # yellow (5) to red (11), as the kanji
        for y in range(y0 - 1, y0 + 13):  # dark red outline
            for x in range(x0 - 1, x0 + len(m[0]) + 1):
                if not out[y][x] and any(0 <= y + dy - y0 < 12 and 0 <= x + dx - x0 < len(m[0])
                                         and m[y + dy - y0][x + dx - x0]
                                         for dy in (-1, 0, 1) for dx in (-1, 0, 1)):
                    out[y][x] = 1
    return out


def cells(canvas, cx, cy, w=8, h=8):
    return [row[cx * w:cx * w + w] for row in canvas[cy * h:cy * h + h]]


def put(rom, off, data):
    rom[off:off + len(data)] = data


def operand(rom, lda, ldx, addr):
    """Point an LDA #addr (at file offset lda) and LDX #bank (at ldx) at CPU address addr."""
    assert rom[lda] == 0xA9 and rom[ldx] == 0xA2
    put(rom, lda + 1, (addr & 0xFFFF).to_bytes(2, "little"))
    put(rom, ldx + 1, (addr >> 16).to_bytes(2, "little"))


def patch_bg(rom, place):
    tiles = bytearray(lz.decompress(rom, BG_TILES)[0])
    tmap = bytearray(lz.decompress(rom, BG_MAP)[0])
    canvas = title_canvas()
    free = [n for n in range(256) if n not in BG_KEEP]
    used = {}
    for r in LOGO_ROWS:
        for i, c in enumerate(LOGO_COLS):
            px = cells(canvas, i, r - LOGO_ROWS[0])
            enc = encode_tile(px)
            word = 0
            if any(map(any, px)):
                if enc not in used:
                    used[enc] = free.pop(0)
                    n = used[enc]
                    tiles[32 * n:32 * n + 32] = enc.ljust(32, b"\0") if 32 * n < len(tiles) else b""
                    if 32 * n >= len(tiles):
                        tiles += bytes(32 * n - len(tiles)) + enc
                word = BG_ATTR | (0x100 + used[enc])
            put(tmap, 2 * (r * 32 + c), word.to_bytes(2, "little"))
    for r, c in READING:
        put(tmap, 2 * (r * 32 + c), b"\0\0")
    for i in set(range(0x40)) - set(used.values()):  # old ろくでなし tiles nobody draws any more
        tiles[32 * i:32 * i + 32] = bytes(32)
    off = place(lz.compress(bytes(tiles)))
    operand(rom, BG_TILES_OPERAND, BG_TILES_OPERAND + 3, text.cpu(off))
    off = place(lz.compress(bytes(tmap)))
    assert rom[BG_MAP_ADDR] == 0xA9 and rom[BG_MAP_BANK] == 0xA2
    put(rom, BG_MAP_ADDR + 1, (text.cpu(off) & 0xFFFF).to_bytes(2, "little"))
    put(rom, BG_MAP_BANK + 1, (text.cpu(off) >> 16).to_bytes(2, "little"))


def patch_obj(rom, place):
    old = lz.decompress(rom, OBJ_BLOCK)[0]
    entries, p = [], META
    while rom[p] != 0x80:
        entries.append(bytes(rom[p:p + 5]))
        p += 5
    copyright = [e for e in entries if e[2] in (24, 40)]  # its two rows; everything above is the old subtitle
    assert all(e[0] == 0 and COPY_FIRST <= e[3] < COPY_FIRST + COPY_COUNT for e in copyright)
    block = bytearray(32 * 128)
    put(block, 32 * COPY_TO, old[32 * COPY_FIRST:32 * (COPY_FIRST + COPY_COUNT)])
    canvas = subtitle_canvas()
    meta = bytearray()
    slot = 0
    for sy in range(SUB_ROWS):
        for sx in range(SUB_W // 16):
            px = cells(canvas, sx, sy, 16, 16)
            if not any(map(any, px)):
                continue
            t = (slot % 8) * 2 + (slot // 8) * 32
            slot += 1
            assert t + 17 < COPY_TO, "subtitle tiles run into the copyright letters"
            for dy in range(2):
                for dx in range(2):
                    put(block, 32 * (t + dx + 16 * dy), encode_tile([row[8 * dx:8 * dx + 8] for row in px[8 * dy:8 * dy + 8]]))
            meta += bytes([1, (16 * sx - SUB_W // 2) & 0xFF, (16 * sy - 16) & 0xFF, t, OBJ_ATTR])
    for e in copyright:
        meta += bytes([e[0], e[1], e[2], e[3] - COPY_FIRST + COPY_TO, e[4]])
    meta.append(0x80)
    assert META + len(meta) <= META_END, f"metasprite {len(meta)} > {META_END - META} bytes"
    put(rom, META, meta)
    off = place(lz.compress(bytes(block)))
    operand(rom, OBJ_OPERAND, OBJ_OPERAND + 3, text.cpu(off))


def mini_canvas():
    h = len(MINI_BANDS)
    lean = round((h - 1) * MINI_SHEAR)
    plain = [""] * h
    for ch in TITLE:
        plain = [row + g + "." for row, g in zip(plain, MINI_FONT[ch])]
    m = [[0] * (round((h - 1 - y) * MINI_SHEAR)) + [int(p == "#") for p in row.rstrip(".")]
         + [0] * (lean - round((h - 1 - y) * MINI_SHEAR)) for y, row in enumerate(plain)]
    m = [row + [0] * (max(map(len, m)) - len(row)) for row in m]
    w = 8 * len(MINI_COLS)
    assert len(m[0]) <= w, f"mini ROKUDENASHI is {len(m[0])} px, band is {w}"
    x0 = (w - len(m[0])) // 2
    out = [[0] * w for _ in range(16)]
    for y, row in enumerate(m):
        for x, p in enumerate(row):
            if p:
                out[3 + y][x0 + x] = MINI_BANDS[y]
    return out


def lda_operand(rom, bank_at, addr_at, addr):
    """Point an `LDA #bank` (8-bit, at bank_at) ... `LDA #addr` (at addr_at) pair at CPU address addr."""
    assert rom[bank_at] == 0xA9 and rom[addr_at] == 0xA9
    rom[bank_at + 1] = addr >> 16
    put(rom, addr_at + 1, (addr & 0xFFFF).to_bytes(2, "little"))


def patch_mini(rom, place):
    tiles = bytearray(lz.decompress(rom, MINI_TILES)[0])
    tmap = bytearray(lz.decompress(rom, MINI_MAP)[0])
    word = lambda r, c: tmap[2 * (r * 32 + c)] | tmap[2 * (r * 32 + c) + 1] << 8  # noqa: E731
    attr = word(MINI_ROWS[0], 5) & 0xFC00
    blank = word(*MINI_READING[-1]) & 0xFC00 | word(0, 0) & 0x3FF  # an empty cell with the screen's attributes
    slots = [word(r, c) & 0x3FF for r in MINI_ROWS for c in MINI_COLS if word(r, c) & 0x3FF]
    every = [tmap[i] | (tmap[i + 1] & 3) << 8 for i in range(0, len(tmap), 2)]
    assert all(every.count(t) == 1 for t in slots), "a ろくでなし tile is drawn elsewhere too"
    canvas = mini_canvas()
    for r in MINI_ROWS:
        for i, c in enumerate(MINI_COLS):
            if not slots:  # VRAM after the block is unused on this screen (loader $88:FA6D loads nothing else)
                slots.append(len(tiles) // 32)
                tiles += bytes(32)
            n = slots.pop(0)
            put(tiles, 32 * n, encode_tile(cells(canvas, i, r - MINI_ROWS[0])))
            put(tmap, 2 * (r * 32 + c), (attr | n).to_bytes(2, "little"))
    for r, c in MINI_READING:
        put(tmap, 2 * (r * 32 + c), blank.to_bytes(2, "little"))
    lda_operand(rom, MINI_TILES_BANK, MINI_TILES_ADDR, text.cpu(place(lz.compress(bytes(tiles)))))
    lda_operand(rom, MINI_MAP_BANK, MINI_MAP_ADDR, text.cpu(place(lz.compress(bytes(tmap)))))


def patch(rom, place):
    """place(data) -> file offset of a free spot for data (must not cross a bank)."""
    patch_bg(rom, place)
    patch_obj(rom, place)
    patch_mini(rom, place)


def preview(out):
    rom = text.ROM.read_bytes()
    pal = rom  # palettes come from a dump; preview in fixed approximations instead
    del pal
    red = {0: (0, 0, 0), 1: (248, 0, 0), 2: (232, 0, 0), 3: (216, 0, 0), 4: (200, 0, 0)}
    sub = {0: (0, 0, 0), 1: (160, 0, 0), 5: (248, 248, 24), 6: (248, 216, 0), 7: (248, 184, 0), 8: (248, 152, 0),
           9: (248, 112, 0), 10: (248, 80, 0), 11: (248, 40, 0)}
    a, b = title_canvas(), subtitle_canvas()
    img = Image.new("RGB", (max(len(a[0]), len(b[0])), 32 + 8 + 32), (40, 0, 40))
    for y, row in enumerate(a):
        for x, v in enumerate(row):
            img.putpixel((x, y), red[v])
    for y, row in enumerate(b):
        for x, v in enumerate(row):
            img.putpixel((x, 40 + y), sub[v])
    img.resize((img.width * 4, img.height * 4), Image.NEAREST).save(out)


if __name__ == "__main__":
    if sys.argv[1:2] == ["preview"]:
        preview(sys.argv[2])
    else:
        sys.exit(__doc__)
