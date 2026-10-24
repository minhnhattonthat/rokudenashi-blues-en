"""Boot copyright screen: © 森田まさのり 集英社 / © BANDAI 1994 -> the English credit lines, drawn by the VWF.

The screen ($88:D9B8) runs the dialogue engine on the string at $8E:D963 (LDX #addr at $88:D9BE, LDA #bank at
$88:D9C4) with the glyph strip at VRAM $5000 (BG3 chr base, 2bpp): 8-px column k of the strip is tiles 2k (top)
and 2k+1 (bottom). Drawing stops at a {nl} here, so both lines go into one strip, spaces between, and the BG3
tilemap LZ $8E:D7CE (loader $88:D983, to VRAM $4800) puts each line's columns on its row, as the original placed
each 16x16 kanji's columns.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import font  # noqa: E402
import lz  # noqa: E402
import text  # noqa: E402

LINES = [(12, "@ MASANORI MORITA / SHUEISHA"), (16, "@ BANDAI 1994")]  # tilemap row, text (@ = © in the VWF)
STR_OPERAND, BANK_OPERAND = 0x459BE, 0x459C4  # LDX #$D963, LDA #$8E
MAP, MAP_OPERAND = 0x757CE, 0x45983  # LDA #addr / LDX #bank
FIRST_COL = 2  # the engine advances one glyph (2 columns) before the first draw
GAP = "  "  # between the lines in the strip: keeps them in separate columns


def spans():
    """-> (first column, column count) of each line in the strip."""
    w = font.widths()
    x, out = 8 * FIRST_COL, []
    for _, s in LINES:
        end = x + sum(w[c] for c in s)
        out.append((x // 8, -(-end // 8) - x // 8))
        x = end + sum(w[c] for c in GAP)
    for (a, n), (b, _) in zip(out, out[1:]):
        assert a + n <= b, "lines share a strip column"
    return out


def tilemap():
    m = bytearray(2048)
    for (row, _), (first, n) in zip(LINES, spans()):
        x0 = (32 - n) // 2
        for c in range(n):
            for dy in range(2):
                i = 2 * ((row + dy) * 32 + x0 + c)
                m[i:i + 2] = (2 * (first + c) + dy).to_bytes(2, "little")
    return bytes(m)


def patch(rom, place_text, place_gfx, encode):
    s = GAP.join(t for _, t in LINES) + "{end}"
    addr = text.cpu(place_text(encode(s)))
    assert rom[STR_OPERAND] == 0xA2 and rom[BANK_OPERAND] == 0xA9
    rom[STR_OPERAND + 1:STR_OPERAND + 3] = (addr & 0xFFFF).to_bytes(2, "little")
    rom[BANK_OPERAND + 1] = addr >> 16
    assert lz.decompress(rom, MAP)[0][2 * (12 * 32 + 10)] == 0x0C  # 田, column 10 of row 12: the map we replace
    addr = text.cpu(place_gfx(lz.compress(tilemap())))
    assert rom[MAP_OPERAND] == 0xA9 and rom[MAP_OPERAND + 3] == 0xA2
    rom[MAP_OPERAND + 1:MAP_OPERAND + 3] = (addr & 0xFFFF).to_bytes(2, "little")
    rom[MAP_OPERAND + 4:MAP_OPERAND + 6] = (addr >> 16).to_bytes(2, "little")
