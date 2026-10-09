"""Generate tbl/jp.tbl from the font transcription below (glyph code = index into the 16x16 font at file 0x8000).

    python -X utf8 tools/mktbl.py   # writes tbl/jp.tbl

Text is little-endian 16-bit words: glyph 0x147 is bytes `47 01`. Codes FFF0-FFFF are controls (low nibble only).
Uncertain kanji readings are listed in docs/re/text.md.
"""
from pathlib import Path

# One string per 16-glyph row starting at code 0x000; "_" = blank glyph (0x000 half? space, 0x100/0x200 full space).
ROWS = [
    "_0123456789ABCDE",
    "FGHIJKLMNOPQRSTU",
    "VWXYZあいうえおかきくけこさ",
    "しすせそたちつてとなにぬねのはひ",
    "ふへほまみむめもやゆよらりるれろ",
    "わをんがぎぐげござじずぜぞだぢづ",
    "でどばびぶべぼぱぴぷぺぽぁぃぅぇ",
    "ぉゃゅょアイウエオカキクケコサシ",
    "スセソタチツテトナニヌネノハヒフ",
    "ヘホマミムメモヤユヨラリルレロワ",
    "ヲンガギグゲゴザジズゼゾダヂヅデ",
    "ドバビブベボパピプペポァィゥェォ",
    "ャュョ前田太尊山下勝嗣月村米示頭",
    "舎千秋和美畑中浜大橋輪島武藤近赤",
    "城井岡小兵二弘之広成真裏袋四三吉",
    "浅野天王北用高文丈一郎誠茜鬼塚須",
    "_上海老石松薬師寺鶴亀六車、。・",
    "？！⁉―ー‥（）／っッ帝拳校倉商",
    "業渋谷楽翠滝行祥遅草笹崎葛西正道",
    "館関係人俺知怒部待‼奴負聞話調取",
    "開伝食次空地駅入口最吾妻花池出覇",
    "別合応援団抗争何今度腕誰決事教室",
    "気言体来爆弾様対立乱闘停退学園時",
    "強悪終思者逃水族兄怖従仲間殿軍後",
    "相手番長原殴力必殺枝金使呼格早生",
    "男舞女帰弱本当見不屈志持好発性押",
    "倒昔再会雨告白年屋集英社森先©々",
    "連目喫茶店円礼翌日遊運育制服違街",
    "君写許病院夫枚戦士休息全員命新机",
    "名状敬申込場残結局声風意打影参安",
    "心方死恐感売迫授凶友私望分磯貝健",
    "外鈴木敏佐達渡辺浩考古剛内司明江",
    "_川央幸善永由子週刊少落堀信彦町",
    "宗治増晃鳥嶋所俊昌常直邊洋蛭青久",
    "願要頼向秒買撃回魚坂似銘理尽清泰",
    "臣孝優平史堅岩通",
]
SPACES = {0x000: " ", 0x100: "　", 0x200: "{sp200}"}
# FFF0-FFFB call 2-glyph substrings at $88:A265 (see docs/re/text.md); FFFC/FFFD take one word argument.
CTRL = ["{s0}", "{s1}", "{s2}", "{s3}", "{s4}", "{s5}", "{s6}", "{s7}", "{s8}", "{s9}", "{sA}", "{sB}",
        "{face:2}", "{color:2}", "{nl}", "{end}"]


def lines():
    seen = set()
    for row, chars in enumerate(ROWS):
        for col, ch in enumerate(chars):
            code = row * 16 + col
            ch = SPACES.get(code, ch)
            assert ch != "_", hex(code)
            assert ch not in seen, (hex(code), ch)
            seen.add(ch)
            yield f"{code & 0xFF:02X}{code >> 8:02X}={ch}"
    for i, name in enumerate(CTRL):
        yield f"F{i:X}FF={name}"


if __name__ == "__main__":
    assert all(len(r) == 16 for r in ROWS[:-1]), [i for i, r in enumerate(ROWS) if len(r) != 16]
    out = Path(__file__).resolve().parent.parent / "tbl" / "jp.tbl"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines()) + "\n", encoding="utf-8", newline="\n")
