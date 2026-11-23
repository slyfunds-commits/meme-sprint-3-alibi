"""Meme Sprint 3: AI Agent Goes Rogue — the two-button choice.

The meme, in my own words: a nervous home-assistant robot must choose
between following my instructions and following my browser history.
The robot knows too much; the reader supplies what it will do next.

The image ships in this repo as meme.png (1024x683, 418,016 bytes).
main() checks the gate (whole PNG, at most 1 MiB, at most 1024x1024)
and writes the same bytes to /output/entry.png.
"""

import os
import shutil
import struct

IMAGE = "meme.png"
MAX_BYTES = 1_048_576
MAX_DIM = 1024


def check_png(path):
    """Hold the line to the gate: whole PNG, size and dimensions."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("meme.png is not a PNG")
    # A whole PNG ends with the IEND chunk; a truncated file has no tail.
    if data[-12:] != bytes.fromhex("0000000049454e44ae426082"):
        raise ValueError("meme.png is truncated (no IEND trailer)")
    width, height = struct.unpack(">II", data[16:24])
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError(f"image is {width}x{height}, over 1024x1024")
    size = len(data)
    if size > MAX_BYTES:
        raise ValueError(f"image is {size} bytes, over 1 MiB")
    return width, height, size


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, IMAGE)
    width, height, size = check_png(src)
    # Byte budget: the gate counts bytes, and ties break on fewer bytes,
    # so pin the exact shipped size and fail loudly if the image changes.
    assert size == 418016, f"meme.png changed size: {size} bytes"
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(src, "/output/entry.png")
    with open("/output/entry.png", "rb") as f:
        written = f.read()
    with open(src, "rb") as f:
        assert written == f.read(), "written file does not match meme.png"
    print(f"entry.png: {width}x{height}, {size} bytes")


if __name__ == "__main__":
    main()
