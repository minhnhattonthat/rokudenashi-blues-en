"""String tour: every translated string shown by the game's own reader, one shot per page.

    python -X utf8 tools/debug/strtour.py [--chunks 0,1,2,3]

Builds build/strtour.sfc = build/rb_en.sfc + the strings joined by {page} in chunks of < 8 KB (free banks from
$198000), then per chunk boots work/states/talk_teacher.mss (portrait box: the narrower one, so a page that fits
here fits the narration box too), points the first dialogue at the chunk (strtour.lua) and pages through it with A.
Out: work/qa/strtour/cN/pNNNN.png, cN/pages.tsv (page, string id, expected lines), cN/sheet*.png (both boxes).
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build  # noqa: E402
import text  # noqa: E402

ROOT = build.ROOT
OUT = ROOT / "work" / "qa" / "strtour"
STATE = ROOT / "work" / "states" / "talk_teacher.mss"  # story1 step 0032: A opens the teacher's Talk (1-064)
BASE = 0x198000  # first free bank after the packed script
MAX = 0x2000  # the reader's word index $1E0A wraps at $1000 (tour 2026-10-24: chunk restarted at word $1000)


def chunks():
    """[(file offset, bytes, [(id, pages)])], each chunk < 8 KB so inside one bank."""
    out, cur, ids = [], b"", []
    for e in build.load_script():
        if not e["en"]:
            continue
        # face codes switch portrait and box mode mid-tour (garbled frames); this tour checks text layout only
        en = build.balance(e["en"])
        b = build.EN.encode(re.sub(r"\{face:[0-9A-Fa-f]+\}", "", en) + "{page}")
        if len(cur) + len(b) + 2 > MAX:
            out.append((cur, ids))
            cur, ids = b"", []
        cur += b
        ids.append((e["id"], [p for s in en.split("{page}") for p in build.layout(s)]))
    out.append((cur, ids))
    return [(BASE + MAX * k, c + build.EN.encode("{end}"), ids) for k, (c, ids) in enumerate(out)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chunks", default=None)
    ap.add_argument("--pages", type=int, default=None, help="only the first N pages of each chunk (a quick test)")
    a = ap.parse_args()
    rom = bytearray((build.BUILD / "rb_en.sfc").read_bytes())
    cs = chunks()
    for off, data, _ in cs:
        assert set(rom[off:off + len(data)]) == {0xFF}, hex(off)
        rom[off:off + len(data)] = data
    dbg = build.BUILD / "strtour.sfc"
    dbg.write_bytes(rom)
    skill = subprocess.run([sys.executable, str(ROOT / "tools" / "skill.py")], capture_output=True, text=True).stdout.strip()
    want = range(len(cs)) if a.chunks is None else map(int, a.chunks.split(","))
    for k in want:
        off, _, ids = cs[k]
        d = OUT / f"c{k}"
        rows = [(sid, p) for sid, pages in ids for p in pages][:a.pages]
        d.mkdir(parents=True, exist_ok=True)
        (d / "pages.tsv").write_text("".join(f"{j:04d}\t{sid}\t{' / '.join(p)}\n" for j, (sid, p) in enumerate(rows)),
                                     encoding="utf-8")
        route = f"6 a;{600 * len(rows)} -"  # A opens the Talk; strtour.lua pages and stops at {end}
        cmd = [sys.executable, "-X", "utf8", os.path.join(skill, "scripts", "emu.py"), str(dbg), "--state-in", str(STATE),
               "--route-str", route, "--out", str(d), "--timeout", "3000", "--var", f"CHUNK=0x{text.cpu(off):06X}",
               "--script", str(ROOT / "tools" / "debug" / "strtour.lua")]
        print(f"chunk {k}: {len(ids)} strings, {len(rows)} pages")
        subprocess.run(cmd, check=True)
        subprocess.run([sys.executable, "-X", "utf8", os.path.join(skill, "scripts", "sheet.py"), *sorted(map(str, d.glob("p*.png"))),
                        "--crop", "0,88,256,128", "--zoom", "1", "--cols", "4", "--max", "16", "--out", str(d / "sheet.png")],
                       check=True)


if __name__ == "__main__":
    main()
