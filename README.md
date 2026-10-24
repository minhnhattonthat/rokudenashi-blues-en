# Rokudenashi Blues: Taiketsu! Tokyo Shitennou English translation

Unofficial English fan translation of **Rokudenashi Blues: Taiketsu! Tokyo Shitennou** (ろくでなしBLUES 対決！東京四天王,
Super Famicom, Bandai, 1994), based on Masanori Morita's manga: the source text and tools that build the patch.

**Just want to play?** Download the patch from [Releases](../../releases) and follow its README. This repository holds
no game data you can play; you need your own dump of the Japanese game.

**Found a bug?** [Report it](../../issues/new/choose): untranslated text, typos, overflow, crashes. Attaching a savestate
helps most.

## What's here

| Path | What it is |
|---|---|
| `script/` | Every text block: original Japanese and English. Translation fixes go here. |
| `glossary.md` | Binding names, terms and style rules. |
| `asm/` | VWF and runtime word-wrap engine (asar). |
| `font/`, `tbl/` | English font art; Japanese text table. |
| `tools/` | Python build chain: extract, insert, lint, release. |
| `tests/` | pytest suite (ROM-dependent tests skip when the ROM is absent). |
| `docs/re/` | Reverse-engineering notes. |
| `docs/decisions.md`, `docs/status.md` | Rulings with their reasons; current progress and open bugs. |
| `docs/fonts.md` | Fonts used and their licences. |
| `AGENTS.md` | Instructions for coding agents (`CLAUDE.md` points to it). |

## Build your own patched ROM

Needs Python 3.12+, [asar](https://github.com/RPGHacker/asar) in `tools/asar/`, and your own dump of the Japanese game.
Releases also need the [translate-retro-game](https://github.com/minhnhattonthat/translate-retro-game) skill (Claude
Code plugin, or set `SKILL` to its directory).

```sh
git clone https://github.com/minhnhattonthat/rokudenashi-blues
cd rokudenashi-blues
# copy your dump to: rom/orig.sfc
#   (1,572,864 bytes, SHA-1 7f6dc245de117d29b573d986b0b0c4048679d27d; the build refuses any other dump, see rom.sha1)
python -X utf8 tools/build.py                          # -> build/rb_en.sfc
python -X utf8 tools/check.py                          # tests + text lint
```

## Support

If you enjoy this translation, you can support my work on Ko-fi:

[![Support me on Ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/minhnhattonthat)

## Licence

Tools and English translation: MIT. The original Japanese text in `script/` is Bandai's and is included only so the
translation can be checked against it. Rokudenashi Blues is (c) Masanori Morita / Shueisha; the game is (c) Bandai
1994; this project is not affiliated with them. Do not share patched ROMs.

The translation was made with extensive AI assistance (Claude by Anthropic). Corrections are very welcome.
