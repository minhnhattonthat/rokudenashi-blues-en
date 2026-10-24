# Bugs

Tick `- [x] (fixed in <build>)` once re-checked from the cited state.

## 2026-10-24 playtest - pt.sfc sha1 c1e84c3c5a03
Evidence: `work/playtest/story1-bugs/NNNN.png|.sheetK.png|.<state>`, presses in `log.tsv`.

Clipping root cause: the wrap limit was cells*16-12 but boxes show one cell less (text clips at x=240); now
cells*16-16 (asm wrap_read, build.py MARGIN).

- [x] (fixed in 2812353d) step 0012 - text - school courtyard, blond thug (top box) - line 2 runs into the right box border, final "e" of "you're" clipped - "we've got business with you, so you're"
- [ ] (won't fix for now: auto-paging) step 0013 - wording - school courtyard, thug's threat - page ends mid-sentence with no punctuation, rest on next page; a player reads page 1 as complete - "we can't promise what happens" / next page "to the girl..."
- [x] (fixed in 2812353d) step 0016 - text - cafe, Yoneji (top box) - line 2 runs into the right border, "you" clipped to "yo" - "grabbed Chiaki-chan, and they said you"
- [ ] (won't fix for now: auto-paging) step 0016 - wording - cafe, Yoneji - page ends mid-sentence with no punctuation, last word on next page alone - "have to come to the club room" / next page "alone..."
- [ ] (won't fix for now: auto-paging) step 0033-0034 - wording - school corridor, teacher (Talk) - same mid-sentence page split (looks systematic: 3-line page full, sentence carries over) - "don't go picking fights" / next page "with the boxing club guys!"
- [x] (fixed in 2812353d: labels drawn 8 px in) step 0031,0035 - text - field command panel - "Talk" label starts flush against the portrait frame, no gap (cramped; check other labels too) - "Talk"
- [ ] (won't fix for now: auto-paging) step 0054 - text - boxing club room, blond boxer (Hamada/Ohashi) - line too long for 3-line box, overflow spills one word onto its own page (same cause as the earlier mid-sentence splits: auto-paging on overflow) - "How about we show you that side of" / next page "us?"
- [x] (fixed in 2812353d) step 0056 - text - boxing club room, Chiaki (top box) - line 1 runs into the right border, "have" clipped - "I'm sorry, Maeda-kun... You don't... have"
- [x] (fixed in 2812353d) step 0058 - text - boxing club room, Taison (bottom box) - line 1 runs into the right border, "with" clipped to "wit" - "Bring it on. I'm gonna settle things with"
- [ ] (won't fix for now: auto-paging) step 0057-0058 - wording - boxing club room, beaten boxer - overflow split mid-sentence - "he'll kill you along with" / next page "Wajima and his crew!"
- [x] (fixed in 2812353d: 1-054 reworded) step 0061 - wording - boxing club room, Taison flustered - stammer reads as gibberish to an English player; check intent vs JP - "How'd you kn-knowa-da-la-raaa?!"
- [ ] (won't fix for now: auto-paging) step 0061-0062 - wording - boxing club "The next day", Hamada - one speech overflows across 3 pages, both breaks mid-sentence - "Some seriously dangerous guy" / "enrolled as a first-year..." / "But as long as you're" / "back, we got nothing to be scared of!"
- [x] (fixed in 2812353d: clipping; the page split stays) step 0075-0076 - text - corridor, teacher (top box) - lines 1-2 run into the right border, last letters of "one" and "the" clipped; and the sentence overflows to next page mid-clause - "causes trouble one" / "Even if the" / "...and the cheer squad" / next page "just clash..."

## 2026-10-24 playtest - pt.sfc sha1 c1e84c3c5a03
Evidence: `work/playtest/opt1-bugs/NNNN.png|.sheetK.png|.<state>`, presses in `log.tsv`.

- [x] (fixed in 2812353d: S05/S06 "YOU'RE the one..." / "...who gets offa-da-laaa!") step 0025 - wording - intro cutscene, flying motorbike - meaning flipped: JP てめえが、/ おりちゃられらーっ！ is a slurred "YOU get off!"; EN made the speaker ask to be let off - "You..." / "Lemme offa-da-laaa!"
- [x] (not a bug: the original also labels both かいひ) step 0002 - wording - Options, Controller - two identical labels for R and L - "DODGE -------R" / "DODGE -------L"
- [x] (not a bug: the original's own English graphics) step 0002 - wording - Options - singular header, unusual word - "OPTION", "MONAURAL"

## 2026-10-24 playtest - pt.sfc sha1 c1e84c3c5a03
Evidence: `work/playtest/vs1-bugs/NNNN.png|.sheetK.png|.<state>`, presses in `log.tsv`.

- [x] (not a bug: original labels; SUPER PUNCH fills the 7-cell field, so no leader) step 0039 - wording - Options, CONTROLLER list - two identical "DODGE" rows (R and L) give the player no way to tell what each does; also "SUPER PUNCH" has no dot leader and butts against its button letter while the other rows have one - "DODGE -------R" / "DODGE -------L", "SUPER PUNCH X"

## 2026-10-24 playtest - pt2.sfc sha1 2812353d (story3: Scenario 1 end to Scenario 3, fight cheat on; vs2: 1P Blues wins)
Evidence: `work/playtest/story3/NNNN.png|.sheetK.png|.mss`. vs2: no issues.

- [x] (fixed in f8dcf0cd: tools/sfx.py, all 9 story sound effects) step 0102 - text - Scenario 3, corridor, Akane slaps Koheiji - katakana sound-effect graphic left - "バキッ"
- [x] (fixed in f8dcf0cd: "Relax, it's fine!") step 0093 - wording - Scenario 2 end, courtyard, Koheiji to his worried crony - reads as a health reply; JP だいじょーぶだよ - "I'm fine!"
- [x] (fixed in f8dcf0cd) step 0132 - wording - Scenario 3, toilet, Taison flustered - stammer reads as gibberish - "Y-You... wh-what're you sayi-ya-da-la-pyaaa!"
- [x] (fixed in f8dcf0cd: "Behold! The battle dance!") step 0145 - wording - Scenario 3, corridor, Akane announcing her own move - "Whoa! The battle dance!"

## 2026-10-24 playtest - Scenarios 3-7, ending and credits (fight cheat on)
Evidence: `work/playtest/sc3..sc7/NNNN.png|.sheetK.png|.mss`; credits re-check `work/qa/credits/`.

- [x] (fixed: credits indents/blank lines use `{jsp}` = JP 16 px blank cell 0000, not 4 px spaces) sc7 step 0114 - layout - staff roll - indented names and blank lines garbled
- [x] (fixed: "...h-hit me alweady!!") sc6 step 0142 - wording - Azuma Bridge ending, Taison stammer - "J-Just shut up and h-hit me-ya-da-la!!"
- [x] (fixed: "Maeda-san! We followed you all the way here!") sc6 step 0082 - wording - temple, Ebihara - "Maeda-san, we came after you, Maeda-san!"
- [x] (fixed: "Too late for that.") sc6 step 0131 - wording - Azuma Bridge, reply to "better if you'd never been around" - "Can't help ya there."
- [x] (fixed: "...with no interruptions.") sc6 step 0130 - wording - Azuma Bridge - "Finally we can go at it in peace."
- [x] (fixed earlier, 1-216 "POWER") sc6 step 0019 - wording - trash can Search - "Taison's stamina went down."
- [x] (fixed: "D-Did ya... Did ya get that?! Huh?!"; stammer is in the JP) sc6 step 0065 - wording - Hanayashiki bridge - "G-Got... You got that?! Huh?!"
- (sc5 continuation, steps 0143-0221: Ebihara fight to Scenario 6 narration, no issues; 5-154/155, 5-172 not triggered)
