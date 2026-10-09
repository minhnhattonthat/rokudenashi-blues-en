# Translation reviewer brief - Rokudenashi Blues: Taiketsu! Tokyo Shitennou

You review one batch of a JP->EN fan translation of a 1994 SNES beat-'em-up adventure based on the delinquent manga
ろくでなしBLUES (Maeda Taison, Teiken High, Kichijoji). Read-only: no edits, no git, no subagents. Mechanical validity
(ids, control codes, ASCII, glossary spellings) is already enforced by a check tool - judge translation quality.

## Inputs (repo H:/translation/rokudenashi-blues)
- Pairs file `work/tl/<batch>.pairs.txt`: each entry as `>> id | JP` / `>> EN`, with +-2 context lines (`   `).
  Read ALL of it, in passes if large. `{nl}` = line break, `{page}` = page break, `{face:XXXX}` = portrait
  expression change (position matters: it should sit before the same sentence as in the JP).
- `glossary.md` (rulings at the top: Japanese name order, honorifics kept, Hepburn), `docs/style-reference.md`,
  `docs/research-names.md` (characters, who speaks Kansai, puns), `docs/translator-brief.md` (the rules they had).
- The speaker is never named in the data; infer from context. The English is free-flowing (the game wraps at runtime),
  so ignore line-break placement except deliberate `{nl}` in title cards.

## Judge
- Accuracy: mistranslation, omission, addition, wrong speaker or addressee, reversed meaning, wrong tense/subject.
  Quote the JP and say what it means.
- Consistency: glossary names/terms exactly; honorific relationships stable (Chiaki says Maeda-kun, Katsuji/Yoneji say
  Maeda-san); same term for the same thing within the batch.
- Things players catch that reviewers miss: jokes/puns/insults losing their punch; stock phrases that read awkwardly
  in English; names off by a letter; a line that only makes sense in Japanese.
- Naturalness and voice: would a fan-translation reader stumble? Delinquent register, Kansai speakers casual.

## Report (reply with only this)
### Issues
#### Critical (meaning reversed, wrong speaker/addressee, broken scene logic)
#### Important (clear mistranslation, omission, glossary/honorific inconsistency, lost joke)
#### Minor (style; deferred to one polish pass)
Each: `id - JP gist - problem - suggested EN` (the suggested EN must be the full replacement line, plain ASCII,
keeping every control code).
### Assessment
Approved | Needs fixes - one sentence why.
