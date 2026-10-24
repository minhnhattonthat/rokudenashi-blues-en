# Decisions

The user's rulings on scope, style and trade-offs, newest last. Read before asking the user anything; if a later
decision replaces one, mark the old one "replaced by D<n>" instead of deleting it. Binding term spellings live in
`glossary.md`; this file holds the why.

| # | Date | Question | Options offered | Decision and reason |
|---|---|---|---|---|
| D1 | 2026-10-09 | Honorifics and name order | keep (-san), drop; JP or Western order | Kept, hyphenated (Chiaki-chan); Japanese order (Maeda Taison), as in the manga. |
| D2 | 2026-10-09 | Romanization source for names | official art, earlier patch, Hepburn | Hepburn, no macrons; readings verified in docs/research-names.md. |
| D3 | 2026-10-09 | Credits | stay Japanese, translate | English. |
| D4 | 2026-10-09 | Abbreviations | engine work first (default), abbreviate | None: full names and terms everywhere (runtime word wrap + VWF). |
| D5 | 2026-10-09 | Graphics text left in Japanese | none (default), list | Not ruled at the time. Replaced by D10. |
| D6 | 2026-10-09 | Specs and plans | need approval, pre-approved | Pre-approved. |
| D7 | 2026-10-09 | Key terms | - | 四天王 Four Kings, 番長 boss, 殿 my lord, 帝拳 Teiken, 米商 Yonekura Commercial (glossary.md). |
| D8 | 2026-10-09 | Review agents | - | multi-openai gpt-6-astra; they can't write files, the controller saves their reports. |
| D9 | 2026-10-24 | Title logo text | romaji (ROKUDENASHI / TAIKETSU! TOKYO SHITENNOU), English subtitle, keep Japanese | English subtitle: ROKUDENASHI / BLUES / SHOWDOWN! TOKYO'S FOUR KINGS; the ブルース reading removed. |
| D10 | 2026-10-24 | Graphics text in scope | - | All of it: the user asked for every Japanese graphic and sprite to be translated. |
| D11 | 2026-10-24 | Publish | - | User asked to release and upload to GitHub minhnhattonthat: public repo rokudenashi-blues-en, first public release v1.0 (v0.9 was never published). |
