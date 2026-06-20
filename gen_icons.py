#!/usr/bin/env python3
"""Generate Coach Fred PWA icons (no external deps). Bell roundel on dark canvas."""
import zlib, struct

BG    = (22, 19, 17, 255)     # --canvas #161311
RED   = (226, 59, 46, 255)    # --work   #e23b2e
CREAM = (244, 239, 230, 255)  # --tape   #f4efe6


def in_disc(nx, ny):
    dx, dy = nx - 0.5, ny - 0.5
    return dx * dx + dy * dy <= 0.40 * 0.40


def in_bell(nx, ny):
    # mount cap
    if 0.465 <= nx <= 0.535 and 0.265 <= ny <= 0.345:
        return True
    # rounded shoulders (upper dome)
    if (nx - 0.5) ** 2 + (ny - 0.50) ** 2 <= 0.165 ** 2 and ny <= 0.50:
        return True
    # flaring body down to the rim
    if 0.40 <= ny <= 0.63:
        hw = 0.165 + (ny - 0.40) / (0.63 - 0.40) * (0.255 - 0.165)
        if abs(nx - 0.5) <= hw:
            return True
    # rim
    if 0.63 <= ny <= 0.678 and abs(nx - 0.5) <= 0.285:
        return True
    return False


def in_clapper(nx, ny):
    return (nx - 0.5) ** 2 + (ny - 0.715) ** 2 <= 0.040 ** 2


def render(size, ss):
    W = size * ss
    buf = bytearray(W * W * 4)
    for j in range(W):
        ny = (j + 0.5) / W
        for i in range(W):
            nx = (i + 0.5) / W
            col = BG
            if in_disc(nx, ny):
                col = RED
            if in_bell(nx, ny) or in_clapper(nx, ny):
                col = CREAM
            o = (j * W + i) * 4
            buf[o:o + 4] = bytes(col)
    out = bytearray(size * size * 4)
    n = ss * ss
    for y in range(size):
        for x in range(size):
            r = g = b = a = 0
            for dy in range(ss):
                base = ((y * ss + dy) * W + x * ss) * 4
                for dx in range(ss):
                    o = base + dx * 4
                    r += buf[o]; g += buf[o + 1]; b += buf[o + 2]; a += buf[o + 3]
            oo = (y * size + x) * 4
            out[oo] = r // n; out[oo + 1] = g // n; out[oo + 2] = b // n; out[oo + 3] = a // n
    return out


def write_png(path, size, rgba):
    raw = bytearray()
    for y in range(size):
        raw.append(0)
        raw.extend(rgba[y * size * 4:(y + 1) * size * 4])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(typ, data):
        return struct.pack(">I", len(data)) + typ + data + struct.pack(">I", zlib.crc32(typ + data) & 0xffffffff)

    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n")
        f.write(chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)))
        f.write(chunk(b"IDAT", comp))
        f.write(chunk(b"IEND", b""))


for size, ss, name in [(512, 2, "icon-512.png"), (192, 3, "icon-192.png"), (180, 3, "apple-touch-icon.png")]:
    write_png(name, size, render(size, ss))
    print("wrote", name)
