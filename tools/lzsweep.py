"""Static graphics sweep: find every LZ block the code loads with an immediate address and render each as a tile
sheet, so Japanese drawn as tiles can be spotted without playing to it.

Call forms found (JSL $80:9A92, A = address, X = bank): `LDA #addr / LDX #bank` and `LDA #bank / AND #$FF / TAX /
LDA #addr`. Calls fed from tables or direct page are printed as skipped with their call site.

    python -X utf8 tools/lzsweep.py [--out work/gfx/sweep] [--bpp 4] [--log work/qa/X/log.txt ..]
--log adds the blocks a tools/lua/lzlog.lua run saw (table-driven loads the static scan can't follow).
"""
import argparse
import re
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent))
import lz  # noqa: E402
import text  # noqa: E402
from tilesheet import tile  # noqa: E402

CALL = re.compile(rb"\x22\x92\x9a[\x80\x00]")
BANK_TAX = b"\xc2\x20\x29\xff\x00\xaa\xa9"


def sources(rom):
    """-> ({file offset: [call sites]}, [skipped call sites])"""
    found, skipped = {}, []
    for m in CALL.finditer(rom):
        p = m.start()
        pre = rom[p - 11:p]
        if pre[5] == 0xA9 and pre[8] == 0xA2:  # LDA #addr / LDX #bank,00
            addr = pre[6] | pre[7] << 8 | pre[9] << 16
        elif pre[2] == 0xA9 and pre[5] == 0xA2 and pre[8] == 0xA0:  # LDA #addr / LDX #bank,00 / LDY #imm
            addr = pre[3] | pre[4] << 8 | pre[6] << 16
        elif pre[0] == 0xA9 and pre[2:9] == BANK_TAX:  # LDA #bank / REP / AND #$FF / TAX / LDA #addr
            addr = pre[9] | pre[10] << 8 | pre[1] << 16
        else:
            skipped.append(p)
            continue
        found.setdefault(text.lorom(addr), []).append(p)
    return found, skipped


def sheet(data, bpp, scale=2):
    count = len(data) // (8 * bpp)
    img = Image.new("L", (16 * 8 * scale, max(1, (count + 15) // 16) * 8 * scale), 40)
    px = img.load()
    top = (1 << bpp) - 1
    for n in range(count):
        t = tile(data, n, bpp)
        x0, y0 = (n % 16) * 8 * scale, (n // 16) * 8 * scale
        for y in range(8 * scale):
            for x in range(8 * scale):
                px[x0 + x, y0 + y] = t[y // scale][x // scale] * 255 // top
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path, default=text.ROOT / "work" / "gfx" / "sweep")
    ap.add_argument("--bpp", type=int, default=4)
    ap.add_argument("--log", type=Path, nargs="*", default=[])
    a = ap.parse_args()
    rom = text.ROM.read_bytes()
    found, skipped = sources(rom)
    for log in a.log:
        for m in re.finditer(r"lz src=\w+ off=(\w+) ret=(\w+)", log.read_text(encoding="utf-8")):
            found.setdefault(int(m[1], 16), []).append(text.lorom(int(m[2], 16)))
    a.out.mkdir(parents=True, exist_ok=True)
    for off, calls in sorted(found.items()):
        data, n = lz.decompress(rom, off)
        sheet(data, a.bpp).save(a.out / f"lz_{off:06X}.png")
        print(f"{off:06X}  {len(data):5d} bytes <- {n:5d}  calls {' '.join(f'{c:06X}' for c in calls)}")
    for p in skipped:
        print(f"skipped call {p:06X} (address from a table or direct page)")


if __name__ == "__main__":
    main()
