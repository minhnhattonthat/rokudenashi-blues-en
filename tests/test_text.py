import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import text  # noqa: E402

pytestmark = pytest.mark.skipif(not text.ROM.exists(), reason="needs rom/orig.sfc")


@pytest.fixture(scope="module")
def rom():
    return text.ROM.read_bytes()


def test_roundtrip_every_string(rom):
    for sid, _, addr in text.pointers(rom):
        off = text.lorom(addr)
        raw, n = text.JP.decode(rom, off)
        assert "[" not in raw, (sid, raw)  # no unknown bytes
        assert text.JP.encode(raw) == rom[off:off + n], sid


def test_text_ranges_fully_covered(rom):
    spans = sorted((text.lorom(a), text.lorom(a) + text.JP.decode(rom, text.lorom(a))[1])
                   for _, _, a in text.pointers(rom))
    covered = []
    for s, e in spans:
        if covered and s <= covered[-1][1]:
            covered[-1][1] = max(covered[-1][1], e)
        else:
            covered.append([s, e])
    assert [tuple(c) for c in covered] == text.TEXT_RANGES


def test_identity_repack(rom):
    out = bytearray(rom)
    text.write_script(out, text.original_blobs(rom), [list(r) for r in text.TEXT_RANGES])
    assert out == rom


def test_cpu_lorom_inverse():
    for off in (0x51C1A, 0x587CE, 0x180000, 0x1FFFFF):
        assert text.lorom(text.cpu(off)) == off
