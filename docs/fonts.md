# Fonts

Every font or glyph sheet the build reads ends up inside the released patch, so its licence must allow that. One row
per file; a font with no known licence doesn't go into a release.

| File | Source (URL, version) | Licence | Redistributable in a patch | Used for | Changes made |
|---|---|---|---|---|---|
| `font/vwf.txt` | drawn for the Little Master fan translation (sibling project) | MIT, same as repo | yes | dialogue VWF (tools/font.py) | - |
| `font/Anton-Regular.ttf` | https://github.com/googlefonts/AntonFont | OFL 1.1 (`font/LICENSE-Anton.txt`) | yes, as rendered glyphs | title logo ROKUDENASHI + subtitle (tools/titlelogo.py), fight banners (tools/hud.py) | rendered without antialiasing; logo sheared and squeezed |
| Game 16x16 font (file 0x8000) | original game | Bandai; not in this repo | not redistributed | Japanese text, command labels rendered into glyphs 0x240-0x273 | - |
