# Text engine (dialogue)

ROM: LoROM FastROM, 1.5 MB (header size byte says 2 MB). No-Intro CRC32 2C85EC10.

## Font
- 16x16 1bpp at file 0x8000 ($81:8000), 32 bytes/glyph: bytes 0-15 = left 8px column rows 0-15, 16-31 = right column.
- Glyphs 0x000-0x237 (0x000/0x100/0x200 blank). 0x238-0x2DF blank in ROM (zeros); 0x2E0+ is other data.
- Table: `tools/mktbl.py` -> `tbl/jp.tbl`. Readings fixed from context: EB 裏, 124 翠, 176 水, 18C 呼. 21B unread (credits only?).

## Strings
- 16-bit LE words, glyph code = font index. Controls are FFFx (dispatcher $88:A2AD uses the low nibble only):
  - FFF0-FFFB: call 2-glyph substring from 16-bit ptr table $88:A24D (って ‥‥ 前田 った ねー じゃ っ！ さん お前 だよ から ない).
  - FFFC w: portrait/speaker (low byte -> $0FAF table, $AD:CA2D). FFFD w: colour bits -> $1E10/$1E11.
  - FFFE: newline (auto page-break when the box is full). FFFF: end / substring return.
- Reader $88:A168: word at [$1CFB] + $1E0A*2. Glyph draw: $88:A545 copies 32 bytes from $81:8000+code*32 to the
  $1E15 buffer (4 x 8 words = L-top, L-bottom, R-top, R-bottom), $88:A5AB/$A652 make 2bpp with colour, $88:A584 DMAs
  0x40 bytes to VRAM word $1E12 (+0x20 per char). So each 8px column of a line is 2 consecutive tiles (32 bytes):
  a line is a linear strip of columns (VWF-friendly). Newline: $1E12 = ($1E12 & FF00) + 0x100 + $0F9F.

## Script tables
- Message id ($1E08): high nibble = group, low 12 bits = index. Group table $88:8AC4 (24-bit each); group 0 = group 1.
- Groups (pointer table, count): 1 $8A:95D8 217, 3 $8A:9863 120, 6 $8A:99CB 197, 2 $8B:8000 80, 4 $8B:80F0 159,
  5 $8B:82CD 195, 7 $8B:8516 232. 1200 strings, no sharing.
- Strings: file 0x51C1A-0x576CC and 0x587CE-0x5F000, fully covered (test). FF free space after each to the bank end.

## Other text found by scan (not yet extracted)
- Command menu: $88:A00D 16-bit ptr table -> 13 fixed 4-glyph fields + FFFF at file 0x42025.. (話す, なぐる, ...).
- Battle shouts: ptr table file 0x7598D (bank $8E) -> 7 strings at 0x7599B.
- Copy-protection message at file 0x434BF.
- Staff credits around file 0x96C59 ($92).
- Graphics text (title menu, scenario titles?, POWER HUD): not yet mapped.
