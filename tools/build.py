"""Build the English ROM: pad to 2 MB, font + asar asm/main.asm, then wrap, encode and pack the script.

    python -X utf8 tools/build.py [--marker] [--out build/rb_en.sfc]

Script `en` text is free-flowing: the build wraps it to the box (LINE_PX per line of a 3-line page).
`{nl}` forces a line break, `{page}` forces a page break. Empty `en` keeps the Japanese (or a marker with --marker).
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import font  # noqa: E402
import text  # noqa: E402
from tbl import Table  # noqa: E402

ROOT = text.ROOT
BUILD = ROOT / "build"
ASAR = ROOT / "tools" / "asar" / "asar.exe"
SIZE = 0x200000
# 3-line dialogue page; the third line leaves room for the page-wait arrow
LINE_PX = (232, 232, 200)
# where packed strings may go: the original areas up to their bank ends, then banks $B1-$BF
REGIONS = [(0x51C1A, 0x58000), (0x587CE, 0x60000), (0x188000, SIZE)]
WIDTHS = font.widths()
EN = Table([f"{i:02X}03={ch}" for ch, i in ((c, ord(c) - 0x20) for c in WIDTHS)]
           + [line for line in (ROOT / "tbl" / "jp.tbl").read_text(encoding="utf-8").splitlines() if "={" in line])
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


def wrap(s):
    """Free-flowing English -> text with {nl} at line ends; pages are 3 lines. Raises if a word can't fit."""
    lines, cur, w, pending_space = [], "", 0, False

    def limit():
        return LINE_PX[len(lines) % 3]

    def newline():
        nonlocal cur, w, pending_space
        lines.append(cur)
        cur, w, pending_space = "", 0, False

    for kind, t in tokens(s):
        if kind == "space":
            pending_space = bool(cur)
        elif kind == "ctrl":
            if t == "{nl}":
                newline()
            elif t == "{page}":
                newline()
                while len(lines) % 3:
                    lines.append("")
            else:
                cur += t
        else:
            need = px(t) + (WIDTHS[" "] if pending_space else 0)
            if w + need > limit() and w:
                newline()
                need = px(t)
            if need > limit():
                raise ValueError(f"word {t!r} ({need}px) wider than the line")
            cur += (" " if pending_space else "") + t
            w += need
            pending_space = False
    lines.append(cur)
    return "{nl}".join(lines)


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
        blobs[sid] = EN.encode(wrap(en) + "{end}") if en else raw
    return blobs


def build(out, marker=False):
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
    text.write_script(rom, encode_script(rom, marker), REGIONS)
    out.write_bytes(rom)
    return rom


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--marker", action="store_true")
    ap.add_argument("--out", type=Path, default=BUILD / "rb_en.sfc")
    a = ap.parse_args()
    build(a.out, a.marker)
    print(f"built {a.out}")
