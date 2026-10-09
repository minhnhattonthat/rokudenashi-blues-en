# Translator brief - Rokudenashi Blues: Taiketsu! Tokyo Shitennou (SNES, Bandai 1994)

You translate part of the Japanese script of this game into English for a fan patch. It's a beat-'em-up adventure
based on Masanori Morita's delinquent manga ろくでなしBLUES: Maeda Taison, a hot-headed first-year at Teiken High in
Kichijoji who wants to be a pro boxer, brawls his way through rival schools and Tokyo's "Four Kings" while bumbling
around Chiaki, the girl he likes. Tone: rough schoolyard-delinquent comedy with sincere moments.
Work only on the batch named in your dispatch. Do all translation yourself; do not dispatch subagents.

## Read first
1. `docs/style-reference.md` - voices and approved example pairs (the pilot). Match this voice.
2. `work/tl/terms_<batch>.txt` - binding glossary rows for this batch. `glossary.md` has the rulings and the full
   tables; `docs/research-names.md` has character background (who speaks Kansai, who calls whom what, puns).

## Input: `work/tl/<batch>.tsv`
`id<TAB>expr<TAB>Japanese`. Lines are in story order within a scenario: use neighbours for context, and work out
who is speaking from content (the game doesn't name speakers). ` / ` marks the original line breaks of a 15-char
box: ignore them for English. `expr` is the first portrait-expression code; `{face:XXXX}` codes inside the text
change the speaker's portrait expression at that point.

## Output: `work/tl/<batch>.out.tsv`, written with your file-write tool (never a shell heredoc)
`id<TAB>English`, every input id exactly once, same order. Plain ASCII: straight quotes, `...`, `--`; no tabs or
backslashes inside the English, no Japanese or fullwidth characters, no `\uXXXX`, no `[` `]`.
- **Free-flowing text.** The game word-wraps English at runtime to whatever box is open and pages every 3 lines.
  Don't insert line breaks to fit. `{nl}` only for a deliberate break (scenario title cards, lists).
- **`{page}`** starts a new page. Use it where the Japanese deliberately pushes a new beat onto a fresh page:
  a run of empty lines (` /  / `) before the next sentence, or an expression change after empty lines. See 1-009.
- **Copy every `{face:XXXX}` exactly**, in the same position relative to the sentence it precedes. Each one must
  appear the same number of times as in the Japanese.
- No length limit, but keep it tight: about as long as natural English needs, not padded.

## Validate
Run `python -X utf8 tools/batches.py check <batch>` from the repo root and fix every reported id until it prints OK.
It checks ids, control codes, characters and glossary terms (when a glossary JP term is in a line, its English form
must be in your line).

## Style
- Faithful: keep the information, attitude and order of ideas; adapt idiom, not meaning. Don't add details the
  Japanese doesn't state; don't summarise or skip. Jokes, insults and puns must still land in English (adapt them;
  no translator notes).
- Names: Japanese order (Maeda Taison), exactly as in the glossary. Use only the name form the line uses (most
  characters appear by surname OR given name only; don't add the other half).
- Honorifics kept, hyphenated: Maeda-san, Maeda-kun, Chiaki-chan, Hei-chan, -senpai. Bare names stay bare.
  "様" after a name = -sama (Koheiji-sama, used by braggarts about themselves). 殿 = "my lord".
- Register: delinquent manga. Contractions, slang, punchy short sentences; てめえ/この野郎 = "you bastard"/"you punk"
  style; mild swearing OK where the JP is rude. Chiaki and Kazumi talk like ordinary high-school girls. Narration
  (no portrait, third person) in plain past tense.
- Kansai speakers (Akane, Suhara, Yoko, Taison when furious): casual, blunt, a little drawn-out ("ya", "ain't",
  "gonna"), never phonetic dialect spelling.
- Taison's flustered ～ちゃれらー gag (e.g. 知っちゃれらー) is a tongue-tied stammer, not dialect: render as a
  garbled stammer ("I-I dunno-ya-da-la!").
- Punctuation: ‥/・・・ -> `...`; ！？/⁉ -> `?!`; ‼ -> `!!`; ーーっ stretched vowels -> letters (`Daaah!`, `Whaaat?!`)
  or `--` for a cut-off. Stammers: `Wh-What`.
- Shouts/onomatopoeia: English equivalents (ぐわっ -> `Gwah!`, きゃあっ -> `Eek!`).
- Money stays yen ("880 yen").

## Consistency
Never edit `glossary.md` or any file except your output. For a recurring name or term not in the glossary, pick a
form, use it consistently, and report it.

## Report (reply with only this)
Files written and entry count; then any lines: `NEW TERM: jp -> en`, `UNSURE: id - note`, `PUN: id - how adapted`.
