import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import build  # noqa: E402
import text  # noqa: E402


def test_wrap_respects_line_widths():
    s = build.wrap("{face:0100}" + " ".join(["Taison"] * 40) + "{page}Next page")
    lines = s.split("{nl}")
    for i, line in enumerate(lines):
        assert build.px(line.replace("{face:0100}", "")) <= build.LINE_PX[i % 3], line
    assert lines[0].startswith("{face:0100}Taison")
    assert len(lines) % 3 == 1 and lines[-1] == "Next page"  # {page} padded the page before it


def test_wrap_rejects_overlong_word():
    with pytest.raises(ValueError):
        build.wrap("W" * 60)


@pytest.mark.skipif(not text.ROM.exists() or not build.ASAR.exists(), reason="needs ROM and asar")
def test_marker_build_repoints_every_string(tmp_path):
    rom = build.build(tmp_path / "m.sfc", marker=True)
    assert len(rom) == build.SIZE
    for sid, _, addr in text.pointers(rom):
        s, _ = build.EN.decode(rom, text.lorom(addr))
        assert f"[{sid}]" in s, sid
