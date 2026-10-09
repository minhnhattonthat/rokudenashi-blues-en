"""Script text: ROM layout, extract to script/*.json, encode + pack strings back into a ROM image.

    python -X utf8 tools/text.py dump [--force]     # writes script/gN.json (refuses to overwrite without --force)

Layout (docs/re/text.md): message id = group (high nibble) + index; group pointer table at $88:8AC4 (3 bytes per
group, 24-bit), each group a table of 24-bit string pointers. Strings are 16-bit little-endian glyph words ending
in FFFF. Group 0 aliases group 1; groups 8-15 point at unrelated data.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from tbl import Table  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ROM = ROOT / "rom" / "orig.sfc"
SCRIPT = ROOT / "script"
JP = Table.load(ROOT / "tbl" / "jp.tbl")

GROUP_TABLE = 0x40AC4  # $88:8AC4
# group -> (pointer table CPU address, entry count); tables sit back to back, so counts come from the next table
GROUPS = {1: (0x8A95D8, 217), 3: (0x8A9863, 120), 6: (0x8A99CB, 197),
          2: (0x8B8000, 80), 4: (0x8B80F0, 159), 5: (0x8B82CD, 195), 7: (0x8B8516, 232)}
# original string areas (file offsets, end exclusive); each ends in FF padding up to the bank end
TEXT_RANGES = [(0x51C1A, 0x576CC), (0x587CE, 0x5F000)]
# 2-glyph substrings called by FFF0-FFFB ($88:A265 table); expanded for the readable "jp" field
SUBS = ["って", "‥‥", "前田", "った", "ねー", "じゃ", "っ！", "さん", "お前", "だよ", "から", "ない"]


def lorom(addr):
    return ((addr & 0x7F0000) >> 1) | (addr & 0x7FFF)


def cpu(off):
    return 0x800000 | (off << 1) & 0x7F0000 | 0x8000 | off & 0x7FFF


def rd24(rom, off):
    return rom[off] | rom[off + 1] << 8 | rom[off + 2] << 16


def pointers(rom):
    """Yield (id, pointer-slot file offset, string CPU address) for every script string."""
    for g, (table, n) in sorted(GROUPS.items()):
        for k in range(n):
            slot = lorom(table) + 3 * k
            yield f"{g}-{k:03d}", slot, rd24(rom, slot)


CREDITS_TABLE = 0x7D7D2  # $8F:D7D2: entries 00 + 24-bit pointer (bank $92), 80 = page break
SHOUTS = (0x7598B, 7)    # $8E:D98B: 16-bit pointers (bank $8E) to battle/intro shouts
MENU = (0x41FFF, 13)     # $88:9FFF: 16-bit pointers (bank $88) to 4-glyph command labels (own fixed-cell renderer)


def credit_slots(rom):
    o, out = CREDITS_TABLE, []
    while rom[o] in (0x00, 0x80):
        if rom[o] == 0x80:
            o += 1
            continue
        if rom[o + 3] != 0x92:  # 00 08 FF F0..: the next table
            break
        out.append(o + 1)
        o += 4
    return out


def other_pointers(rom):
    """Yield (id, slot offset, slot size 2|3, string CPU address) for the non-script strings."""
    for k, slot in enumerate(credit_slots(rom)):
        yield f"C{k:02d}", slot, 3, rd24(rom, slot)
    for prefix, (table, n) in (("S", SHOUTS), ("M", MENU)):
        bank = cpu(table) & 0xFF0000
        for k in range(n):
            slot = table + 2 * k
            yield f"{prefix}{k:02d}", slot, 2, bank | rom[slot] | rom[slot + 1] << 8


def readable(raw):
    """Raw tbl text -> what a translator reads: substrings expanded, {end} dropped."""
    for i, s in enumerate(SUBS):
        raw = raw.replace(f"{{s{i:X}}}", s)
    return raw.removesuffix("{end}")


def dump(force=False):
    rom = ROM.read_bytes()
    SCRIPT.mkdir(exist_ok=True)
    groups = {}
    for sid, slot, addr in pointers(rom):
        raw, n = JP.decode(rom, lorom(addr))
        groups.setdefault(sid.split("-")[0], []).append(
            {"id": sid, "ptr": f"{addr:06X}", "jp": readable(raw), "en": "", "notes": ""})
    for sid, slot, size, addr in other_pointers(rom):
        raw, n = JP.decode(rom, lorom(addr))
        groups.setdefault("other", []).append(
            {"id": sid, "ptr": f"{addr:06X}", "jp": readable(raw), "en": "", "notes": ""})
    for g, entries in groups.items():
        path = SCRIPT / (f"g{g}.json" if g != "other" else "other.json")
        if path.exists() and not force:
            print(f"skip {path.name} (exists; --force overwrites English)")
            continue
        path.write_text(json.dumps(entries, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
        print(f"wrote {path.name}: {len(entries)}")


def pack(rom, blobs, free):
    """Place blobs (id -> bytes) first-fit into free = [[start, end], ...] (consumed in place) without crossing a
    32 KB bank. Returns id -> file offset. Raises if anything does not fit."""
    where = {}
    for sid, data in blobs.items():
        for r in free:
            start = r[0]
            if (start >> 15) != ((start + len(data) - 1) >> 15):  # would cross a bank: skip to the next bank
                start = (start | 0x7FFF) + 1
            if start + len(data) <= r[1]:
                rom[start:start + len(data)] = data
                where[sid] = start
                r[0] = start + len(data)
                break
        else:
            raise ValueError(f"{sid}: no room for {len(data)} bytes")
    return where


def write_script(rom, blobs, free):
    """Pack encoded strings (id -> bytes, in the order to place them) into free (see pack), repoint every slot."""
    slots = {sid: slot for sid, slot, _ in pointers(rom)}
    where = pack(rom, blobs, free)
    for sid, off in where.items():
        rom[slots[sid]:slots[sid] + 3] = cpu(off).to_bytes(3, "little")
    return where


def original_blobs(rom):
    """id -> original string bytes, in ROM address order (the order that reproduces the original layout)."""
    out = {}
    for sid, _, addr in sorted(pointers(rom), key=lambda p: p[2]):
        raw, n = JP.decode(rom, lorom(addr))
        out[sid] = rom[lorom(addr):lorom(addr) + n]
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["dump"])
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    dump(a.force)
