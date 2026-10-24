# Graphics text

Survey 2026-10-24: tours (boot, attract, title, story start, VS select/fight/continue) + static sweep of every LZ
block (`tools/lzsweep.py`, immediate-address loads plus the blocks `tools/lua/lzlog.lua` logged in a long story run
and a VS run; table-driven loads covered only as far as those runs reached). Raw (uncompressed) graphics were not
swept, only found by VRAM dump + `vramfind.py` on screens seen.

| Screen | Japanese | Source | Tool | State |
|---|---|---|---|---|
| Boot | © 森田まさのり 集英社 / © BANDAI 1994 | dialogue engine string $8E:D963 + BG3 map LZ $8E:D7CE | `bootscreen.py` | English, verified in emulator |
| Title | ろくでなし, ブルース reading | BG1/BG2 tiles LZ $8E:9F67, map LZ $8E:A5F2 | `titlelogo.py` | English, verified |
| Title | 対決！東京四天王 | OBJ LZ $90:8200 + metasprite $90:88D2 | `titlelogo.py` | English, verified |
| Title menu | ストーリーモード... | OBJ LZ $90:89F5 + metasprite $90:8F3C | `titlemenu.py` | English (earlier) |
| Options | button labels | BG3 LZ $8F:B6F9 / $8F:B9EC | `options.py` | English (earlier) |
| Fight HUD (story + VS) | 怒 gauge badge | raw 2bpp $85:9B37 tiles $1F-$22 | `hud.py` | RAGE, verified in both |
| VS fight | 始め / 待て / 共倒れ banners | raw 2bpp $85:9B37 tiles $34-$6F, map records $AF:F040- | `hud.py` | FIGHT! / WAIT! / DOUBLE KO, verified with `tools/lua/bannerpoke.lua` (WAIT! and DOUBLE KO not reached in play) |
| Ending? (loader $88:FA6D) | mini ろくでなし BLUES ブルース | BG1 tiles LZ $AD:9F73, map LZ $AD:B233 | `titlelogo.py` | English, verified offline only (render of the built blocks); screen not reached |
| Copier warning | コピーしちゃいけないんだぞぉー | string at file 0x434BD | - | left: no pointer to it anywhere in the ROM (unused or built at run time); shown only on copier hardware |

Backgrounds (LZ $82:8000, $83:A1C3, $83:E69A, $84:C1A6, $84:E22F...) show no Japanese signage in the sweep sheets.
