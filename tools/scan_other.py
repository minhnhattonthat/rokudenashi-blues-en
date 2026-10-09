"""List FFFF-terminated glyph-word strings outside the script areas, with any 16/24-bit pointers to them.

    python -X utf8 tools/scan_other.py [--min 2]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import text  # noqa: E402

SKIP = text.TEXT_RANGES + [(0x8000, 0xC700)]  # script, font


def scan(rom, minlen):
    hits, i = [], 0
    while i < len(rom) - 1:
        if any(a <= i < b for a, b in SKIP):
            i += 2
            continue
        j, glyphs, kana = i, 0, 0
        while j < len(rom) - 1:
            w = rom[j] | rom[j + 1] << 8
            if 1 <= w <= 0x237:
                glyphs += 1
                kana += 0x25 <= w <= 0xC2 or 0x10D <= w <= 0x11A
            elif not (w in (0, 0x100) or 0xFFF0 <= w <= 0xFFFE):
                break
            j += 2
        if j < len(rom) - 1 and rom[j] | rom[j + 1] << 8 == 0xFFFF and glyphs >= minlen and kana * 2 >= glyphs:
            hits.append((i, j + 2))
            i = j + 2
        else:
            i += 1
    return hits


def refs(rom, off):
    addr = text.cpu(off)
    out = []
    for pat, kind in ((addr.to_bytes(3, "little"), "p24"), ((addr & 0xFFFF).to_bytes(2, "little"), "p16")):
        for m in re.finditer(re.escape(pat), rom):
            # a 16-bit pointer only counts inside the string's own bank
            if kind == "p24" or m.start() >> 15 == off >> 15:
                out.append(f"{kind}@{m.start():X}")
    return out


if __name__ == "__main__":
    rom = text.ROM.read_bytes()
    minlen = int(sys.argv[sys.argv.index("--min") + 1]) if "--min" in sys.argv else 2
    for a, b in scan(rom, minlen):
        s, _ = text.JP.decode(rom, a, b - a)
        r = refs(rom, a)
        print(f"{a:06X} {text.cpu(a):06X} {' '.join(r[:3]) or '-':28} {text.readable(s)[:60]}")
