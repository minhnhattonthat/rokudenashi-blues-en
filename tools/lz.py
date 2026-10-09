"""Graphics LZSS used by $80:9A92 (A = address, X = bank; output to $7E:4400).

Format: u16 output size, then groups of a flag byte (LSB first): 1 = literal byte, 0 = 2-byte reference
b0 b1: length = (b0 & 0x0F) + 3, distance back = (b0 >> 4) | (b1 << 4) (1..4095). A reference reaching before the
start of the output produces zeros there (the window is pre-zeroed).

    python -X utf8 tools/lz.py ROM OFFSET OUT.bin      # decompress one block (prints its compressed size)
"""
import sys


def decompress(data, pos=0):
    """-> (bytes, compressed length)"""
    start = pos
    size = data[pos] | data[pos + 1] << 8
    pos += 2
    out = bytearray()
    flags = bits = 0
    while len(out) < size:
        if not bits:
            flags, bits = data[pos], 8
            pos += 1
        bits -= 1
        lit = flags & 1
        flags >>= 1
        if lit:
            out.append(data[pos])
            pos += 1
        else:
            b0, b1 = data[pos], data[pos + 1]
            pos += 2
            n, dist = (b0 & 0x0F) + 3, (b0 >> 4) | (b1 << 4)
            for _ in range(n):
                src = len(out) - dist
                out.append(out[src] if src >= 0 else 0)
    return bytes(out[:size]), pos - start


def compress(raw):
    """Greedy LZSS with the game's limits (len 3..18, distance 1..4095)."""
    out = bytearray(len(raw).to_bytes(2, "little"))
    i, n = 0, len(raw)
    seen = {}  # 3-byte key -> positions (most recent last)

    def add(p):
        if p + 3 <= n:
            seen.setdefault(raw[p:p + 3], []).append(p)

    while i < n:
        flag_pos = len(out)
        out.append(0)
        for bit in range(8):
            if i >= n:
                break
            best_len = best_dist = 0
            for p in reversed(seen.get(raw[i:i + 3], [])[-256:]):
                dist = i - p
                if dist > 4095:
                    break
                length = 0
                while length < 18 and i + length < n and raw[p + length] == raw[i + length]:
                    length += 1
                if length > best_len:
                    best_len, best_dist = length, dist
                    if length == 18:
                        break
            if best_len >= 3:
                out += bytes([(best_dist & 0x0F) << 4 | (best_len - 3), best_dist >> 4])
                for p in range(i, i + best_len):
                    add(p)
                i += best_len
            else:
                out[flag_pos] |= 1 << bit
                out.append(raw[i])
                add(i)
                i += 1
    return bytes(out)


if __name__ == "__main__":
    rom = open(sys.argv[1], "rb").read()
    raw, used = decompress(rom, int(sys.argv[2], 16))
    open(sys.argv[3], "wb").write(raw)
    print(f"{len(raw)} bytes from {used} compressed")
