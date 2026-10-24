# Rokudenashi Blues: Taiketsu! Tokyo Shitennou (SNES) English translation

Skill: translate-retro-game (Claude Code: plugin, enabled in .claude/settings.json; other agents: `<SKILL_DIR>/SKILL.md`; `$SKILL` = the directory holding its SKILL.md, default `~/.claude/plugins/marketplaces/retro-translation/skills/translate-retro-game`; tools/release.py reads `$SKILL` too). Read it before ROM, text or QA work.

## Commands (run from repo root; always `python -X utf8`)
- Build:    `python -X utf8 tools/build.py [--marker] [--out build/rb_en.sfc]` -> build/rb_en.sfc (checks the dump against `rom.sha1` first; font -> asar asm/main.asm -> text, other.json, title menu, options)
- Check:    `python -X utf8 tools/check.py` (pytest tests/ + `batches.py lint`; the pre-commit hook runs this)
- Text:     `tools/batches.py list|split|check|merge|pairs <batch>` (b1a b1b b2..b6 b7a b7b other), `apply FILE` (id<TAB>EN fixes)
- Smoke:    `python -X utf8 $SKILL/scripts/emu.py build/rb_en.sfc --out work/qa/smoke --route tools/routes/boot.txt --smoke`
- Release:  `python -X utf8 tools/release.py --version X.Y` -> release/ (BPS + README zip; never publish without the user)
- Clean:    `python -X utf8 tools/clean.py` (published projects: lists rebuildable/downloadable files; `--yes` deletes)
- Dump:     `tools/text.py dump [--force]`. Graphics: `tools/lz.py` (LZSS codec), `tilesheet.py`, `bgview.py`, `fontview.py`.
- Lua (tools/lua, use with emu.py --script): textlog (string pointers), boxlog, lzlog, oamdump, vramdump, romreads (prepend F0=/F1=), wramuse.

## Paths
- Original ROM: `rom/orig.sfc` (No-Intro dump, CRC32 2C85EC10; gitignored; SHA-1 in `rom.sha1`, checked by `tools/check_rom.py`). Emulator: this repo's own copy in `tools/mesen2/` (gitignored). asar: `tools/asar/`. Savestates: `work/states/` (s1_start, long1_end = free roam street).
- Text: `script/g1..g7.json` (1200 strings), `script/other.json` (C credits, S shouts, M command labels). Table: `tbl/jp.tbl`. Glossary: `glossary.md` (names research: docs/research-names.md). Briefs: docs/translator-brief.md, reviewer-brief.md, style-reference.md. RE notes index: `docs/re/README.md`. Fonts and their licences: `docs/fonts.md`. Allowed ROM writes: `tools/allowed_ranges.txt`. Player README template: `docs/README.release.txt`.

## Rulings
- Edit source files (.py .lua .asm .tbl .json) only with the file-edit tool; scripts here read and analyse, never `.replace()` and write back.
- The user's decisions, with the options and reasons: `docs/decisions.md`. Read it before asking the user anything; add each new ruling there the same session.
- Player bug reports: GitHub issues (`gh issue list --label bug`). Copy the attached save into `work/states/`, reproduce in the emulator, fix, commit with `Fixes #N`, and update `docs/status.md`.
- glossary.md is binding. Review agents: multi-openai gpt-6-astra (they can't write files: save reports yourself).

## Engine (asm/main.asm)
- English = codes $0300+ascii-$20 through a VWF (2-column strip at VRAM $1E12); JP codes use the original path.
- Runtime word wrap per box ($0F98/$0F99 cells, limit cells*16-16 px), {page} = FFE0. Typing 2 frames/glyph.
- Command labels pre-rendered into font glyphs 0x240-0x273. Title menu = sprite block 0x809F5 + metasprite 0x80F3C.
  Options labels = BG3 font/tilemap relocated to bank $B0:C000+.

## Status
`docs/status.md`: done, next, open bugs. Update it at the end of every session.
