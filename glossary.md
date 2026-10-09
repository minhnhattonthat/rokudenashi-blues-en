# Glossary - Rokudenashi Blues: Taiketsu! Tokyo Shitennou

Binding for every translator and reviewer. Agents propose additions in reports; only the controller edits this file.
`tools/batches.py check/lint` enforces it: when a row's JP appears in a line, one of the EN forms (separated by
`/`) must appear in the English; spellings in the Avoid column (comma-separated) fail.

## Rulings (user, 2026-10-09)
- Name order: Japanese (family name first: Maeda Taison). Honorifics kept, hyphenated (Chiaki-chan, Maeda-san, Kasai-senpai).
- Romanization: Hepburn without macrons or doubled long vowels (Kichijoji, Kotaro, Muto); verified readings in docs/research-names.md.
- Credits: English. Plans: pre-approved.
- Abbreviations: none; full names and terms everywhere. No suffix glued onto a control code.

## Style rules
- Delinquent manga register: rough, punchy, slangy male speech; contractions; mild swearing is fine where the JP is rude
  (てめえ, この野郎). Keep Kansai speakers recognisably different (casual, drawn-out, "ya"), no phonetic dialect spelling.
- Punctuation: 「」 -> "...", ‥/・・・ -> ..., ！？/⁉ -> ?!, ‼ -> !!, ー/― stretched vowels -> letters or --
  ("Daaah!", "Wha--"). Plain ASCII only.
- Free-flowing English: the build wraps to the box. `{nl}` only for a deliberate line break (title cards, lists),
  `{page}` where the JP pushes the next beat to a new page with blank lines.

Character notes, voices and sources: docs/research-names.md. Only the names the script itself uses (most
characters appear by surname or given name only; don't add the other half).

## Characters
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| 前田 | Maeda | | Maeda Taison, protagonist (Teiken). Akane is also a Maeda. Rough Tokyo delinquent; Kansai slips when furious | |
| 太尊 | Taison | | | Tyson |
| 千秋 | Chiaki | | heroine; others say Chiaki-chan; she says Maeda-kun | |
| 和美 | Kazumi | | Chiaki's friend | |
| 勝嗣 | Katsuji | | Taison's friend; calls him Maeda-san | |
| 米示 | Yoneji | | Taison's friend; calls him Maeda-san | |
| 小兵二 | Koheiji | | Nakata Koheiji, braggart self-styled boss; uses English BABY/BOY | |
| 中田 | Nakata | | Koheiji's family name | |
| 兵ちゃん | Hei-chan | | Koheiji's nickname | |
| 広成 | Hironari | | Koheiji's sidekick | |
| 畑中 | Hatanaka | | boxing club captain | |
| 浜田 | Hamada | | boxing club | |
| 大橋 | Ohashi | | boxing club | Oohashi |
| 輪島 | Wajima | | cheer squad ex-leader | |
| 武藤 | Muto | | cheer squad | Mutou |
| 中島 | Nakajima | | class rep, photography club | |
| 井岡 | Ioka | | teacher | |
| キング | King | | Principal King | |
| 島袋 | Shimabukuro | | head of Yonekura Commercial; puns on 袋 (たま袋) adapt freely | |
| 赤城 | Akagi | | Kyoei head | |
| ヒロト | Hiroto | | Oba Hiroto, junior; calls Taison 殿 = "my lord" | |
| 大場 | Oba | | = Hiroto | Ohba |
| 松村 | Matsumura | | Hiroto's partner | |
| 茜 | Akane | | Maeda Akane, Taison's cousin, heavy Kansai | |
| 用高 | Yoko | | Taison's younger brother (Kansai) | |
| 小太郎 | Kotaro | | Rakusui student | Kotarou |
| 鬼塚 | Onizuka | | Rakusui head, one of the Four Kings | |
| 上山 | Kamiyama | | Rakusui No.2 | |
| 須原 | Suhara | | Rakusui No.3, Kansai | |
| 海老原 | Ebihara | | bandana freshman | |
| 石松 | Ishimatsu | | gentle giant, halting speech | |
| 薬師寺 | Yakushiji | | Sasazaki head, one of the Four Kings | |
| ヤッくん | Yakkun | | Chiaki's childhood nickname for Yakushiji | |
| 鶴田 | Tsuruta | | Sasazaki | |
| 亀岡 | Kameoka | | Sasazaki | |
| 六車 | Muguruma | | Sasazaki North head | |
| 葛西 | Kasai | | Seidokan head, one of the Four Kings | |
| 坂本 | Sakamoto | | Seidokan, Kasai's friend | |
| レナード | Leonard | | boxer Sugar Ray Leonard, Taison's idol | |

## Schools, gangs, places
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| 帝拳 | Teiken | | 帝拳高校 = Teiken High School | |
| 米商 | Yonekura Commercial | | Shimabukuro's school (never "Yonesho") | Yonesho |
| 米中 | Yonekura Middle School | | Hiroto's middle school | |
| キョウエイ | Kyoei | | Kyoei High School | |
| 楽翠 | Rakusui | | Shibuya Rakusui Academy | |
| 笹崎北 | Sasazaki North | | Muguruma's school | |
| 笹崎 | Sasazaki | | Asakusa Sasazaki High School | |
| 正道館 | Seidokan | | Ikebukuro Seidokan High School | |
| 三迫中 | Misako Middle School | | | |
| 応援団 | cheer squad | | | |
| ボクシング部 | boxing club | | | |
| 小兵二軍団 | Koheiji Corps | | | |
| 吉祥寺 | Kichijoji | | | Kichijouji |
| 渋谷 | Shibuya | | | |
| 浅草 | Asakusa | | | |
| 池袋 | Ikebukuro | | | |
| 吾妻橋 | Azuma Bridge | | Asakusa | |
| 花やしき | Hanayashiki | | Asakusa amusement park | |
| サンシャイン | Sunshine | | Sunshine City, Ikebukuro | |

## Terms
| JP | EN | max | notes | Avoid |
|---|---|---|---|---|
| 四天王 | Four Kings | | 東京四天王 = the Tokyo Four Kings (Taison, Onizuka, Yakushiji, Kasai) | Shitenno, Big Four |
| 番長 | boss | | 影の番長 = shadow boss | bancho |
| 番格 | top dog | | | |
| タイマン | one-on-one | | | |
| 殿 | my lord | | Hiroto/juniors addressing Taison | Tono |
| 決闘状 | challenge letter | | also ちょうせん状 | |
| シナリオ | Scenario | | title cards: "Scenario 1{nl}Ponytail and Guts" | |

## Decisions from earlier batches
