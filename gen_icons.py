#!/usr/bin/env python3
"""Generate Coach Fred PWA icons from icon-source.png.

icon-source.png is a square master (the boxing-glove tile). This resizes it to
the icon sizes the app references. Requires Pillow:  pip install Pillow
"""
from PIL import Image

SRC = "icon-source.png"
SIZES = [(512, "icon-512.png"), (192, "icon-192.png"), (180, "apple-touch-icon.png")]


def main():
    master = Image.open(SRC).convert("RGB")
    if master.width != master.height:                 # ensure square (centre crop)
        side = min(master.size)
        x0 = (master.width - side) // 2
        y0 = (master.height - side) // 2
        master = master.crop((x0, y0, x0 + side, y0 + side))
    for size, name in SIZES:
        master.resize((size, size), Image.LANCZOS).save(name)
        print("wrote", name)


if __name__ == "__main__":
    main()
