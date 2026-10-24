"""Translation batches: split -> agents translate -> check -> merge; pairs files for reviewers.

    python -X utf8 tools/batches.py list                # batch names and sizes
    python -X utf8 tools/batches.py split b1a           # work/tl/b1a.tsv + work/tl/terms_b1a.txt
    python -X utf8 tools/batches.py check b1a           # validates work/tl/b1a.out.tsv, prints OK or errors
    python -X utf8 tools/batches.py merge b1a           # check, then write "en" into script/*.json
    python -X utf8 tools/batches.py pairs b1a           # work/tl/b1a.pairs.txt for the reviewer
    python -X utf8 tools/batches.py apply FILE          # id<TAB>EN fixes (any batch), checked, merged
    python -X utf8 tools/batches.py lint                # every non-empty "en" in script/ (build gate)

TSV in (untranslated entries only): id, first portrait-expression code or -, jp with " / " for the original breaks.
TSV out: id<TAB>English (free-flowing; {nl} forces a line break, {page} a page break; control codes copied).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TL = ROOT / "work" / "tl"
SCRIPT = ROOT / "script"
CTRL = re.compile(r"\{[^}]*\}")
LAYOUT = {"{nl}", "{page}", "{jsp}"}  # {jsp}: 16 px JP blank cell (credits indents)


def groups():
    return {p.stem: json.loads(p.read_text(encoding="utf-8")) for p in sorted(SCRIPT.glob("*.json"))}


def half(g, part):
    es = groups()[g]
    n = (len(es) + 1) // 2
    return [e["id"] for e in (es[:n] if part == 0 else es[n:])]


def all_ids(g):
    return [e["id"] for e in groups()[g]]


BATCHES = {
    "b1a": lambda: half("g1", 0), "b1b": lambda: half("g1", 1),
    "b2": lambda: all_ids("g2"), "b3": lambda: all_ids("g3"), "b4": lambda: all_ids("g4"),
    "b5": lambda: all_ids("g5"), "b6": lambda: all_ids("g6"),
    "b7a": lambda: half("g7", 0), "b7b": lambda: half("g7", 1),
    "other": lambda: all_ids("other") if (SCRIPT / "other.json").exists() else [],
}


def entries():
    return {e["id"]: (g, e) for g, es in groups().items() for e in es}


def batch(name):
    by_id = entries()
    return [by_id[i][1] for i in BATCHES[name]()]


def glossary():
    """Rows of every glossary table: (jp, [en alternatives], [avoid])."""
    rows = []
    for line in (ROOT / "glossary.md").read_text(encoding="utf-8").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not line.startswith("|") or len(cells) < 2 or cells[0] in ("JP", "") or set(cells[0]) <= {"-"}:
            continue
        avoid = [a.strip() for a in cells[4].split(",") if a.strip()] if len(cells) > 4 else []
        rows.append((cells[0], [a.strip() for a in cells[1].split("/") if a.strip()], avoid))
    return rows


def speaker(jp):
    m = re.match(r"\{face:(\w+)\}", jp)
    return m[1] if m else "-"


def problems(e, en, gloss):
    """List of error strings for one translated entry."""
    errs = []
    jp_ctrl = Counter(c for c in CTRL.findall(e["jp"]) if c not in LAYOUT)
    en_ctrl = Counter(c for c in CTRL.findall(en) if c not in LAYOUT)
    if jp_ctrl != en_ctrl:
        errs.append(f"control codes differ: jp {dict(jp_ctrl)} en {dict(en_ctrl)}")
    plain = CTRL.sub("", en)
    bad = sorted({c for c in plain if c not in build.WIDTHS})
    if bad:
        errs.append(f"characters not in the font: {bad}")
    if "\t" in en or "\\" in en:
        errs.append("tab or backslash in text")
    if re.search(r"\}(st|nd|rd|th)\b", en):
        errs.append("ordinal suffix glued to a control code")
    if e["id"][0] == "M":  # pre-rendered 4-cell command label
        if build.px(plain) > build.MENU_PX or CTRL.search(en):
            errs.append(f"command label: {build.px(plain)}px (max {build.MENU_PX}), no control codes")
    elif e["id"][0] in "CS":  # credits (15-cell lines) / shouts (11-cell box): explicit lines
        limit = 228 if e["id"][0] == "C" else 164
        for line in en.split("{nl}"):
            w = build.px(CTRL.sub("", line)) + 16 * line.count("{jsp}")
            if w > limit:
                errs.append(f"line {w}px > {limit}: {line!r}")
    else:
        try:
            build.check_words(en)
        except ValueError as x:
            errs.append(str(x))
    for jp, alts, avoid in gloss:
        if jp in e["jp"] and alts and not any(a.lower() in en.lower() for a in alts):
            errs.append(f"glossary: {jp} -> {' / '.join(alts)} missing")
        for a in avoid:
            if re.search(rf"\b{re.escape(a)}\b", en):
                errs.append(f"glossary: avoid {a!r}")
    if e["jp"].strip() and not plain.strip():
        errs.append("empty translation")
    return errs


def read_out(path):
    out = {}
    for n, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        if "\t" not in line:
            raise SystemExit(f"{path.name}:{n}: no tab")
        i, en = line.split("\t", 1)
        if i in out:
            raise SystemExit(f"{path.name}:{n}: duplicate id {i}")
        out[i] = en.strip()
    return out


def check(name, path=None, require_all=True):
    by_id = {i: e for i, (_, e) in entries().items()}
    if name:  # the ids handed out in work/tl/<name>.tsv
        tsv = (TL / f"{name}.tsv").read_text(encoding="utf-8").splitlines()
        es = {line.split("\t")[0]: by_id[line.split("\t")[0]] for line in tsv if line.strip()}
    else:
        es = by_id
    out = read_out(path or TL / f"{name}.out.tsv")
    errs = []
    if require_all:
        errs += [f"{i}: missing" for i in es if i not in out]
    errs += [f"{i}: unknown id" for i in out if i not in es]
    gloss = glossary()
    for i, en in out.items():
        if i in es:
            errs += [f"{i}: {p}" for p in problems(es[i], en, gloss)]
    return out, errs


def merge(out):
    data = groups()
    for es in data.values():
        for e in es:
            if e["id"] in out:
                e["en"] = out[e["id"]]
    for g, es in data.items():
        (SCRIPT / f"{g}.json").write_text(json.dumps(es, ensure_ascii=False, indent=1) + "\n", encoding="utf-8",
                                          newline="\n")


def split(name):
    TL.mkdir(parents=True, exist_ok=True)
    es = [e for e in batch(name) if not e["en"]]
    lines = [f"{e['id']}\t{speaker(e['jp'])}\t{e['jp'].replace('{nl}', ' / ')}" for e in es]
    (TL / f"{name}.tsv").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    text = " ".join(e["jp"] for e in es)
    terms = [line for line in (ROOT / "glossary.md").read_text(encoding="utf-8").splitlines()
             if line.startswith("|") and (cell := line.strip("|").split("|")[0].strip()) and cell in text]
    (TL / f"terms_{name}.txt").write_text("\n".join(terms) + "\n", encoding="utf-8", newline="\n")
    print(f"{name}: {len(es)} entries, {len(terms)} terms -> work/tl/{name}.tsv")


def pairs(name):
    es = batch(name)
    order = [e for g in groups().values() for e in g]
    pos = {e["id"]: k for k, e in enumerate(order)}
    out = []
    for e in es:
        k = pos[e["id"]]
        for c in order[max(0, k - 2):k]:
            out.append(f"   {c['id']} | {c['jp']}\n   {c['en']}")
        out.append(f">> {e['id']} | {e['jp']}\n>> {e['en']}")
        for c in order[k + 1:k + 3]:
            out.append(f"   {c['id']} | {c['jp']}\n   {c['en']}")
        out.append("")
    (TL / f"{name}.pairs.txt").write_text("\n".join(out), encoding="utf-8", newline="\n")
    print(f"work/tl/{name}.pairs.txt")


def lint():
    gloss, errs, n = glossary(), [], 0
    for i, (_, e) in entries().items():
        if e["en"]:
            n += 1
            errs += [f"{i}: {p}" for p in problems(e, e["en"], gloss)]
    return n, errs


def report(errs):
    for x in errs[:60]:
        print(x)
    if len(errs) > 60:
        print(f"... {len(errs) - 60} more")


if __name__ == "__main__":
    cmd, arg = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else None)
    if cmd == "list":
        for b in BATCHES:
            es = batch(b)
            print(b, len(es), sum(len(CTRL.sub("", e["jp"])) for e in es), "jp chars")
    elif cmd == "split":
        split(arg)
    elif cmd == "pairs":
        pairs(arg)
    elif cmd in ("check", "merge", "apply"):
        out, errs = check(None, Path(arg), require_all=False) if cmd == "apply" else check(arg)
        report(errs)
        if errs:
            sys.exit(f"{len(errs)} errors")
        if cmd != "check":
            merge(out)
            print(f"merged {len(out)}")
        else:
            print("OK")
    elif cmd == "lint":
        n, errs = lint()
        report(errs)
        print(f"lint: {n} translated, {len(errs)} errors")
        sys.exit(1 if errs else 0)
