"""Build an original geometric banner; requires Pillow. No downloaded artwork."""

import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 960, 300
NAME = "AnkjoD"
PINK = "#eab4c8"
PURPLE = "#c3a5ee"


def font(size, bold=False):
    variable = "PROFILE_FONT_BOLD" if bold else "PROFILE_FONT"
    candidates = [
        os.environ.get(variable, ""),
        "C:/Windows/Fonts/consolab.ttf" if bold else "C:/Windows/Fonts/consola.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/System/Library/Fonts/Menlo.ttc",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).is_file():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default(size=size)


def polar(cx, cy, radius, angle):
    return (cx + radius * math.cos(angle), cy + radius * math.sin(angle))


def frame(phase):
    canvas = Image.new("RGB", (WIDTH, HEIGHT), "#0b0910")
    d = ImageDraw.Draw(canvas)
    # Restrained diagonal panels and hairline grid.
    d.polygon([(600, 0), (960, 0), (960, 300), (440, 300)], fill="#100d18")
    d.polygon([(812, 0), (960, 0), (960, 300), (660, 300)], fill="#171020")
    for x in range(624, 960, 32):
        d.line((x, 0, x, 300), fill="#1c1526")
    for y in range(22, 300, 32):
        d.line((600, y, 960, y), fill="#1c1526")
    d.rectangle((0, 0, 959, 299), outline="#33263f", width=1)
    d.line((42, 42, 90, 42), fill=PURPLE, width=3)
    d.text((104, 33), "HOMURA / MADOKA", font=font(13), fill="#baa6c9")
    d.text((40, 83), NAME, font=font(68, True), fill="#eee7f5")
    d.text((44, 170), "HY VỌNG / THỜI GIAN", font=font(18), fill=PINK)
    d.line((44, 218, 435, 218), fill="#33263f")
    d.text((44, 241), "MADOKA KANAME × HOMURA AKEMI", font=font(12), fill="#b6a6c4")

    cx, cy = 772, 147
    for radius, color in [(111, "#4c385e"), (99, "#74568c"), (84, "#35253f")]:
        d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=color, width=1)
    for tick in range(60):
        a = tick * math.tau / 60 - math.pi / 2
        long = tick % 5 == 0
        d.line([polar(cx, cy, 103 if long else 107, a), polar(cx, cy, 111, a)], fill="#aa89c6" if long else "#4c385e", width=2 if long else 1)
    # The thin hand completes one slow loop; a second hand stays steady.
    a = phase * math.tau - math.pi / 2
    d.line([(cx, cy), polar(cx, cy, 75, a)], fill=PURPLE, width=2)
    d.line([(cx, cy), polar(cx, cy, 47, -2.2)], fill="#7b5c94", width=4)
    d.ellipse((cx-5, cy-5, cx+5, cy+5), fill=PURPLE)
    # A small four-point star suggests Madoka without borrowed character art.
    sx, sy = 676, 99
    r = 22 + 2 * math.sin(phase * math.tau)
    star = [(sx, sy-r), (sx+5, sy-5), (sx+r, sy), (sx+5, sy+5), (sx, sy+r), (sx-5, sy+5), (sx-r, sy), (sx-5, sy-5)]
    d.polygon(star, fill=PINK)
    d.line((650, 242, 895, 242), fill="#473048")
    d.text((683, 260), "H / M", font=font(12), fill="#a48ab8")
    d.ellipse((888, 48, 892, 52), fill=PINK)
    d.ellipse((611, 205, 614, 208), fill=PURPLE)
    return canvas


def main():
    destination = ROOT / "assets"
    destination.mkdir(parents=True, exist_ok=True)
    frames = [frame(index / 60) for index in range(60)]
    frames[0].save(destination / "header.png")
    # Use a shared palette to keep colors stable across frames.
    palette = frames[0].quantize(colors=128)
    indexed = [item.quantize(palette=palette, dither=Image.Dither.NONE) for item in frames]
    indexed[0].save(destination / "header.gif", save_all=True, append_images=indexed[1:], duration=100, loop=0, optimize=False, disposal=1)
    print("Generated header.gif (6-second loop) and header.png")


if __name__ == "__main__":
    main()
