"""English VWF font: font/vwf.txt art -> 8x16 1bpp glyphs + width table, indexed by ascii - 0x20.

Art: 'char X' (or 'char space') then 16 rows; row length = advance width in px (incl. spacing), '#' = ink.
Glyph bytes: 16 rows, bit 7 = leftmost pixel (the dialogue font's own 1bpp column format).

    python -X utf8 tools/font.py OUT_DIR       # writes OUT_DIR/en_font.bin, OUT_DIR/en_widths.bin
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ART = ROOT / "font" / "vwf.txt"
FIRST, COUNT = 0x20, 95


def parse(text=None):
    """-> {char: [16 row strings]}"""
    glyphs, cur = {}, None
    for line in (text or ART.read_text(encoding="utf-8")).splitlines():
        if line.startswith("char "):
            name = line[5:]
            cur = " " if name == "space" else name
            assert len(cur) == 1, line
            glyphs[cur] = []
        elif line and set(line) <= {".", "#"} and cur is not None:
            glyphs[cur].append(line)
    for ch, rows in glyphs.items():
        assert len(rows) == 16 and len(set(map(len, rows))) == 1 and len(rows[0]) <= 8, ch
    return glyphs


def widths():
    return {ch: len(rows[0]) for ch, rows in parse().items()}


def pack():
    glyphs = parse()
    font, wid = bytearray(16 * COUNT), bytearray(COUNT)
    for ch, rows in glyphs.items():
        i = ord(ch) - FIRST
        assert 0 <= i < COUNT, ch
        wid[i] = len(rows[0])
        for r, row in enumerate(rows):
            font[16 * i + r] = sum(0x80 >> c for c, p in enumerate(row) if p == "#")
    return bytes(font), bytes(wid)


if __name__ == "__main__":
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    font, wid = pack()
    (out / "en_font.bin").write_bytes(font)
    (out / "en_widths.bin").write_bytes(wid)
