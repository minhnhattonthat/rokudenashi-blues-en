# Visual-QA reviewer brief - Rokudenashi Blues: Taiketsu! Tokyo Shitennou (SNES)

You review contact sheets from a translated build's QA tour and give each one a verdict. Read-only on everything
except your one verdict file: no edits to the repo, no git, no subagents.

## Inputs (in your dispatch)
- A chunk file: one `id<TAB>path` line per sheet. Read every sheet in it; none may be skipped.
- Your verdict file: `work/qa/verdicts/<chunk>.tsv`.
- Optional: the original ROM's sheets (`work/qa/tour_jp/`, same ids) and `glossary.md`.

## How to look
- Read each sheet whole first. Where text is small, zoom into it with
  `python -X utf8 $SKILL/scripts/sheet.py SHEET.png --crop x,y,w,h --zoom 3 --out <scratch>.png` and read that.
- When something looks wrong, open the same id from `tour_jp/` (`sheet.py EN.png --compare JP.png`). If the
  original shows the same thing, it is the game's own behaviour: `ok`, with a note.

## Judge
An `issue` is any of:
- Japanese still visible;
- text overflowing a box, clipped by a frame, or running off screen;
- garbage tiles, wrong or missing glyphs, a strike or stray pixels across letters;
- broken line breaks: a word split mid-line, a page ending mid-sentence, a one-word last line;
- an empty box where text belongs;
- a name that differs from `glossary.md`.

Standing non-bugs, `ok` (the controller adds the game's own below):
- text still typing out, a box mid-fade or mid-scroll, a cursor caught mid-blink;
- a map or scene still loading after a warp;
- anything identical in the original's sheet.
- the fights have no win banner: only FIGHT!, WAIT! and DOUBLE KO exist (original design);
- the "DODGE" option appears twice (R and L): the original labels both かいひ;
- the RAGE badge, VS banners and title logo are English graphics on purpose; ROKUDENASHI / BLUES romaji is a ruling;
- the playtest used a fight cheat: fighters freezing at low HP, one-hit stuns and KOs are the cheat, not a bug;
- the anti-copier warning screen is known untranslated (copier hardware only);
- staff credits fade in and out letter by letter; faint text mid-fade is fine.
- String tour (`work/qa/strtour/cN/sheet*.png`, tiles `pNNNN`): every string is forced into one teacher Talk
  scene (tools/debug/strtour.py), so the portrait, speaker and background never match the line: not a bug. Each
  tile is one page; `cN/pages.tsv` has `page<TAB>string id<TAB>expected lines` (" / " = line break). An `issue`
  is a tile whose text differs from its expected lines (missing, cut, extra), plus everything in Judge above.
  Name the page and string id in the note.
- The build balances line breaks (tools/build.py balance()); a multi-word place name split across lines where
  every break choice splits one (2-035, 5-034, 7-006) and the "Scenario N / Title" cards are ok.
- CONTINUE / EXIT is a fixed-cell font: the gap around the narrow "I" is the original design.
- No original-ROM tour exists here: judge from the build and glossary.md; when unsure, `issue` with a note.

## Verdicts
Write your verdict file once you have read every sheet, one line per id in the chunk:
`id<TAB>ok|issue<TAB>what and where` (for an issue: which tile, which text, what is wrong).
Then return a short summary: counts, and the issues one per line.
