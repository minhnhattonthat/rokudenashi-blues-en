"""Build the English ROM: pad to 2 MB, font + asar asm/main.asm, then encode and pack the script.

    python -X utf8 tools/build.py [--marker] [--out build/rb_en.sfc]

Script `en` text is free-flowing: the game wraps it at runtime to whatever box is open (asm wrap_read; layout()
emulates it). `{nl}` forces a line break, `{page}` a page break. Empty `en` keeps the Japanese (or a marker).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_rom  # noqa: E402
import font  # noqa: E402
import hud  # noqa: E402
import options  # noqa: E402
import text  # noqa: E402
import titlelogo  # noqa: E402
import titlemenu  # noqa: E402
from tbl import Table  # noqa: E402

ROOT = text.ROOT
BUILD = ROOT / "build"
ASAR = ROOT / "tools" / "asar" / "asar.exe"
SIZE = 0x200000
# dialogue boxes as ($0F98 cells per line, $0F99 cells on a page's last line); px limit = cells * 16 - 12
BOXES = {"narration": (15, 13), "portrait": (13, 11)}
MIN_LINE_PX = 11 * 16 - 12
# where packed strings may go: the original areas up to their bank ends, then banks $B1-$BF
REGIONS = [(0x51C1A, 0x58000), (0x587CE, 0x60000), (0x188000, SIZE)]
GFX_REGION = (0x184000, 0x188000)  # $B0:C000-$B0:FFFF: relocated graphics (asm code + font use $B0:8000-)
SHOUT_REGIONS =[(0x75999, 0x75A23), (0x77895, 0x78000)]  # bank $8E: the original shouts, then end-of-bank FF
MENU_GLYPH, MENU_PX = 0x240, 64  # command labels use font glyphs 0x240-0x273 (blank in the original font)
WIDTHS = font.widths()
EN = Table([f"{i:02X}03={ch}" for ch, i in ((c, ord(c) - 0x20) for c in WIDTHS)]
           + [line for line in (ROOT / "tbl" / "jp.tbl").read_text(encoding="utf-8").splitlines() if "={" in line]
           + ["E0FF={page}"])
MARKER = "The quick brown fox jumps over the lazy dog while the fifth gang boss waits by the station gate."


def tokens(s):
    """Split into ('ctrl', '{..}') and ('word', text) / ('space', ' ') pieces."""
    out, i = [], 0
    while i < len(s):
        if s[i] == "{":
            j = s.index("}", i) + 1
            out.append(("ctrl", s[i:j]))
            i = j
        elif s[i] == " ":
            out.append(("space", " "))
            i += 1
        else:
            j = i
            while j < len(s) and s[j] not in " {":
                j += 1
            out.append(("word", s[i:j]))
            i = j
    return out


def px(word):
    return sum(WIDTHS[c] for c in word)


def layout(s, box=BOXES["portrait"]):
    """Emulate the runtime wrap (asm wrap_read) -> list of pages, each a list of line strings."""
    pages, lines, cur, w = [], [], "", 0
    normal, last = (c * 16 - 12 for c in box)

    def newline():
        nonlocal cur, w, lines
        lines.append(cur)
        cur, w = "", 0
        if len(lines) == 3:
            pages.append(lines)
            lines = []

    toks = tokens(s)
    for i, (kind, t) in enumerate(toks):
        limit = last if len(lines) == 2 else normal
        if kind == "space":
            nxt = toks[i + 1][1] if i + 1 < len(toks) and toks[i + 1][0] == "word" else ""
            if w and w + WIDTHS[" "] + px(nxt) > limit:
                newline()
            else:
                cur, w = cur + " ", w + WIDTHS[" "]
        elif t == "{nl}":
            newline()
        elif t == "{page}":
            if lines or cur:
                newline()
                while lines:
                    newline()
        elif kind == "ctrl":
            cur += t
        else:
            cur, w = cur + t, w + px(t)
    if cur or lines:
        lines.append(cur)
        pages.append(lines)
    return pages


def check_words(s):
    """Raise if a word can't fit even the narrowest line (the portrait box's last line)."""
    for kind, t in tokens(s):
        if kind == "word" and px(t) > MIN_LINE_PX:
            raise ValueError(f"word {t!r} ({px(t)}px) wider than a line ({MIN_LINE_PX}px)")


def ctrl_prefix(jp):
    """Leading control tokens of a JP line ({face:..}), kept in marker text."""
    out = ""
    for kind, t in tokens(jp):
        if kind != "ctrl" or t in ("{nl}",):
            break
        out += t
    return out


def load_script():
    entries = []
    for path in sorted((ROOT / "script").glob("g*.json")):
        entries += json.loads(path.read_text(encoding="utf-8"))
    return entries


def encode_script(rom, marker):
    orig = text.original_blobs(rom)
    by_id = {e["id"]: e for e in load_script()}
    blobs = {}
    for sid, raw in orig.items():  # original address order
        e = by_id[sid]
        en = e["en"] or (ctrl_prefix(e["jp"]) + f"[{sid}] {MARKER}" if marker else "")
        if en:
            check_words(en)
        blobs[sid] = EN.encode(en + "{end}") if en else raw
    return blobs


def menu_label(rom, k, en, addr):
    """Pre-render a command label into 4 spare 16x16 font glyphs and point its fixed 4-glyph field at them."""
    art = font.parse()
    cols = [[0] * 16 for _ in range(MENU_PX)]
    x = 0
    for ch in en:
        for r, row in enumerate(art[ch]):
            for c, p in enumerate(row):
                if p == "#":
                    cols[x + c][r] = 1
        x += WIDTHS[ch]
    for j in range(4):
        code = MENU_GLYPH + 4 * k + j
        g = 0x8000 + code * 32
        for r in range(16):
            for half in range(2):
                rom[g + 16 * half + r] = sum(0x80 >> c for c in range(8) if cols[16 * j + 8 * half + c][r])
        rom[text.lorom(addr) + 2 * j:text.lorom(addr) + 2 * j + 2] = code.to_bytes(2, "little")


def insert_other(rom, marker, free):
    """Credits (24-bit pointers, anywhere), shouts (16-bit, bank $8E), command labels (pre-rendered glyphs)."""
    by_id = {e["id"]: e for e in json.loads((ROOT / "script" / "other.json").read_text(encoding="utf-8"))}
    shout_free = [list(r) for r in SHOUT_REGIONS]
    for sid, slot, size, addr in list(text.other_pointers(rom)):
        en = by_id[sid]["en"] or (f"[{sid}]" if marker else "")
        if not en:
            continue
        if sid[0] == "M":
            menu_label(rom, int(sid[1:]), en, addr)
            continue
        off = text.pack(rom, {sid: EN.encode(en + "{end}")}, free if size == 3 else shout_free)[sid]
        rom[slot:slot + size] = text.cpu(off).to_bytes(3, "little")[:size]


def build(out, marker=False):
    check_rom.check()
    BUILD.mkdir(exist_ok=True)
    rom = bytearray(text.ROM.read_bytes())
    rom += b"\xFF" * (SIZE - len(rom))
    font_bin, widths_bin = font.pack()
    (BUILD / "en_font.bin").write_bytes(font_bin)
    (BUILD / "en_widths.bin").write_bytes(widths_bin)
    out.write_bytes(rom)
    r = subprocess.run([str(ASAR), "--fix-checksum=off", str(ROOT / "asm" / "main.asm"), str(out)],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"asar failed:\n{r.stdout}{r.stderr}")
    rom = bytearray(out.read_bytes())
    free = [list(r) for r in REGIONS]
    text.write_script(rom, encode_script(rom, marker), free)
    insert_other(rom, marker, free)
    titlemenu.patch(rom)
    hud.patch(rom)
    assert set(rom[GFX_REGION[0]:GFX_REGION[1]]) == {0xFF}, "asm code grew into the graphics region"
    gfx_free = [list(GFX_REGION)]
    place = lambda data: text.pack(rom, {"gfx": data}, gfx_free)["gfx"]  # noqa: E731
    options.patch(rom, place)
    titlelogo.patch(rom, place)
    out.write_bytes(rom)
    return rom


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--marker", action="store_true")
    ap.add_argument("--out", type=Path, default=BUILD / "rb_en.sfc")
    a = ap.parse_args()
    build(a.out, a.marker)
    print(f"built {a.out}")
