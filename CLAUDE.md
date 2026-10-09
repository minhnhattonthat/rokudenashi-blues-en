# Rokudenashi Blues: Taiketsu! Tokyo Shitennou (SNES) English translation

Skill: translate-retro-game (H:/translation/rokudenashi-blues/.claude/skills/translate-retro-game/SKILL.md). Read it before ROM, text or QA work.

## Commands (run from repo root; always `python -X utf8`)
- Build:   `python -X utf8 tools/build.py [--marker] [--out build/rb_en.sfc]` (font -> asar asm/main.asm -> text, other.json, title menu, options)
- Check:   `python -X utf8 tools/check.py` (pytest tests/ + `batches.py lint`; the pre-commit hook runs this)
- Text:    `tools/batches.py list|split|check|merge|pairs <batch>` (b1a b1b b2..b6 b7a b7b other), `apply FILE` (id<TAB>EN fixes)
- Smoke:   `python -X utf8 .claude/skills/translate-retro-game/scripts/emu.py build/rb_en.sfc --out work/qa/smoke --route tools/routes/boot.txt --smoke`
- Release: `python -X utf8 tools/release.py --version X.Y` -> release/ (BPS + README zip; local only, never publish without the user)
- Dump:    `tools/text.py dump [--force]`. Graphics: `tools/lz.py` (LZSS codec), `tilesheet.py`, `bgview.py`, `fontview.py`.
- Lua (tools/lua, use with emu.py --script): textlog (string pointers), boxlog, lzlog, oamdump, vramdump, romreads (prepend F0=/F1=), wramuse.

## Paths
- ROM: `rom/orig.sfc` (No-Intro dump, CRC32 2C85EC10, gitignored). Mesen2: tools/mesen2, asar: tools/asar.
- Text: script/g1..g7.json (1200 strings), script/other.json (C credits, S shouts, M command labels). Table tbl/jp.tbl.
- Glossary + rulings: glossary.md (names research: docs/research-names.md). Briefs: docs/translator-brief.md, reviewer-brief.md, style-reference.md.
- RE notes: docs/re/text.md. Allowed ROM writes: tools/allowed_ranges.txt. States: work/states/ (s1_start, long1_end = free roam street).

## Rulings (user, 2026-10-09)
- Japanese name order, honorifics kept. Hepburn, no macrons. Credits in English. Plans pre-approved. No abbreviations.
- Terms: 四天王 Four Kings, 番長 boss, 殿 my lord, 帝拳 Teiken, 米商 Yonekura Commercial (glossary.md is binding).
- Review agents: multi-openai gpt-6-astra (they can't write files: save reports yourself).

## Engine (asm/main.asm)
- English = codes $0300+ascii-$20 through a VWF (2-column strip at VRAM $1E12); JP codes use the original path.
- Runtime word wrap per box ($0F98/$0F99 cells, limit cells*16-12 px), {page} = FFE0. Typing 2 frames/glyph.
- Command labels pre-rendered into font glyphs 0x240-0x273. Title menu = sprite block 0x809F5 + metasprite 0x80F3C.
  Options labels = BG3 font/tilemap relocated to bank $B0:C000+.

## Status (2026-10-09)
- Done: all script + other text translated; astra review + fixes for b1a b1b b2 b3 b4 b5 b7a b7b, b6 self-reviewed
  (astra dispatch blocked by classifier outage); title menu, options, shouts in-game checked; release v0.9 built locally.
- Next: astra review of b6; minor polish pass; check command labels and credits in-game
  (HUD command panel not reached yet; credits need the ending); user playtest.
- Known JP left: boot copyright screen (text engine with custom tilemap), copier warning (0x434BF), logo art, HUD 怒 icon.
