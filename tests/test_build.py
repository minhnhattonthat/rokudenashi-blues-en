import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import build  # noqa: E402
import text  # noqa: E402


def test_layout_respects_box_widths():
    for name, (normal, last) in build.BOXES.items():
        pages = build.layout("{face:0100}" + " ".join(["Taison"] * 40) + "{page}Next page", build.BOXES[name])
        for page in pages:
            for i, line in enumerate(page):
                limit = (last if i == 2 else normal) * 16 - build.MARGIN
                assert build.px(line.replace("{face:0100}", "")) <= limit, (name, line)
        assert pages[0][0].startswith("{face:0100}Taison")
        assert pages[-1] == ["Next page"]  # {page} finished the page before it


def test_check_words_rejects_overlong_word():
    with pytest.raises(ValueError):
        build.check_words("W" * 40)
    build.check_words("Short words only.")


@pytest.mark.skipif(not text.ROM.exists() or not build.ASAR.exists(), reason="needs ROM and asar")
def test_marker_build_repoints_every_string(tmp_path):
    rom = build.build(tmp_path / "m.sfc", marker=True)
    assert len(rom) == build.SIZE
    en = {e["id"]: e["en"] for e in build.load_script()}
    for sid, _, addr in text.pointers(rom):
        s, _ = build.EN.decode(rom, text.lorom(addr))
        assert s == en[sid] + "{end}" if en[sid] else f"[{sid}]" in s, sid
