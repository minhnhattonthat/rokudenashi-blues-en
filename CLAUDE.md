# Rokudenashi Blues: Taiketsu! Tokyo Shitennou (SNES) English translation

Skill: translate-retro-game (H:/translation/rokudenashi-blues/.claude/skills/translate-retro-game/SKILL.md). Read it before ROM, text or QA work.

## Commands (run from repo root; always `python -X utf8`)
- Check:  `python -X utf8 tools/check.py` (pytest tests/; the pre-commit hook runs this)
- Dump:   `python -X utf8 tools/text.py dump [--force]` -> script/gN.json (refuses to overwrite without --force)
- Smoke:  `python -X utf8 .claude/skills/translate-retro-game/scripts/emu.py ROM --out work/qa/smoke --route tools/routes/boot.txt --smoke --sheet`
- Font grid: `tools/fontview.py rom/orig.sfc out.png`. Table: `tools/mktbl.py` -> tbl/jp.tbl. Disasm: `tools/dis65816.py ROM 88A168 [n]`.
- Lua: tools/lua/romreads.lua (prepend `F0=.. F1=..`: ROM readers + DMAs in a frame window), dmalog, readrange, vramdump.

## Paths
- ROM: `rom/orig.sfc` (copy of the No-Intro dump, gitignored). Mesen2: tools/mesen2, asar: tools/asar.
- Text: script/g1..g7.json (id = group-index, jp, en). Table: tbl/jp.tbl. RE notes: docs/re/text.md.

## Rulings (user, 2026-10-09)
- Japanese name order, keep honorifics (-san, -kun, -chan). Hepburn romanization. Credits in English. Plans pre-approved.
- Full names and terms, no abbreviations (engine work first). No suffix glued onto a variable.
- Review agents: multi-openai gpt-6-astra.

## Status
- Done: Step 0, recon of dialogue engine, table, extract + roundtrip/coverage/identity tests.
- Next: engine spike (VWF on the column-strip path, ROM expansion to 2 MB for 16-bit English text), marker build,
  extract command menu / battle shouts / credits, glossary research.
