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


def frame(phase, theme="dark"):
    light_palette = {
        "#0b0910": "#fff9fc", "#100d18": "#f9edf4", "#171020": "#f3dfeb",
        "#1c1526": "#efdfeb", "#33263f": "#dec3d6", "#baa6c9": "#895b7b",
        "#eee7f5": "#2b183a", "#b6a6c4": "#755e84", "#4c385e": "#a88fba",
        "#74568c": "#8e6ba4", "#35253f": "#d4c1df", "#aa89c6": "#76538f",
        "#7b5c94": "#8a6a9e", "#473048": "#d7b4c6", "#a48ab8": "#7c5e90",
        PURPLE: "#765095", PINK: "#ad5c83",
    }

    def tone(color):
        return light_palette.get(color, color) if theme == "light" else color

    canvas = Image.new("RGB", (WIDTH, HEIGHT), tone("#0b0910"))
    d = ImageDraw.Draw(canvas)
    # Restrained diagonal panels and hairline grid.
    d.polygon([(600, 0), (960, 0), (960, 300), (440, 300)], fill=tone("#100d18"))
    d.polygon([(812, 0), (960, 0), (960, 300), (660, 300)], fill=tone("#171020"))
    if theme == "dark":
        for x in range(624, 960, 32):
            d.line((x, 0, x, 300), fill=tone("#1c1526"))
        for y in range(22, 300, 32):
            d.line((600, y, 960, y), fill=tone("#1c1526"))
    d.rectangle((0, 0, 959, 299), outline=tone("#33263f"), width=1)
    d.line((42, 42, 90, 42), fill=tone(PURPLE), width=3)
    d.text((104, 33), "MADOKA KANAME" if theme == "light" else "HOMURA / MADOKA", font=font(13), fill=tone("#baa6c9"))
    d.text((40, 83), NAME, font=font(68, True), fill=tone("#eee7f5"))
    d.text((44, 170), "ÁNH SÁNG / HY VỌNG" if theme == "light" else "HY VỌNG / THỜI GIAN", font=font(18), fill=tone(PINK))
    d.line((44, 218, 435, 218), fill=tone("#33263f"))
    d.text((44, 241), "MADOKA KANAME × HOMURA AKEMI", font=font(12), fill=tone("#b6a6c4"))

    if theme == "light":
        # Madoka's light motif: a rose, ribbon and a luminous gem; no clock.
        cx, cy = 776, 147
        breath = 1 + 0.025 * math.sin(phase * math.tau)
        for radius, ink, weight in [(107, "#ddb2ce", 1), (83, "#bd7ba3", 2)]:
            petals = []
            for index in range(361):
                angle = index * math.tau / 360
                distance = radius * breath * (0.79 + 0.21 * math.cos(5 * (angle + math.pi / 2)))
                petals.append(polar(cx, cy, distance, angle))
            d.line(petals, fill=ink, width=weight, joint="curve")
        # A restrained ribbon bow with two long tails.
        d.polygon([(776, 220), (733, 205), (740, 231), (774, 225)], fill="#ead0df", outline="#bf87a8")
        d.polygon([(778, 220), (819, 205), (812, 231), (778, 225)], fill="#ead0df", outline="#bf87a8")
        d.polygon([(773, 225), (760, 257), (773, 251), (779, 227)], fill="#d8a8c3")
        d.polygon([(780, 225), (794, 253), (799, 246), (784, 223)], fill="#d8a8c3")
        d.ellipse((771, 218, 783, 230), fill="#b8759a")
        d.polygon([(776, 121), (791, 147), (776, 173), (761, 147)], fill="#f1d8e7", outline="#b76d97")
        d.line([(776, 127), (776, 167)], fill="#fff9fc", width=2)
        for sx, sy, offset in [(655, 91, 0), (870, 66, 0.3), (884, 199, 0.65), (681, 218, 0.8)]:
            size = 5 + 2 * math.sin((phase + offset) * math.tau)
            d.polygon([(sx, sy-size), (sx+2, sy-2), (sx+size, sy), (sx+2, sy+2), (sx, sy+size), (sx-2, sy+2), (sx-size, sy), (sx-2, sy-2)], fill="#c38bad")
        return canvas

    cx, cy = 772, 147
    for radius, color in [(111, "#4c385e"), (99, "#74568c"), (84, "#35253f")]:
        d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=tone(color), width=1)
    for tick in range(60):
        a = tick * math.tau / 60 - math.pi / 2
        long = tick % 5 == 0
        d.line([polar(cx, cy, 103 if long else 107, a), polar(cx, cy, 111, a)], fill=tone("#aa89c6" if long else "#4c385e"), width=2 if long else 1)
    # The thin hand completes one slow loop; a second hand stays steady.
    a = phase * math.tau - math.pi / 2
    d.line([(cx, cy), polar(cx, cy, 75, a)], fill=tone(PURPLE), width=2)
    d.line([(cx, cy), polar(cx, cy, 47, -2.2)], fill=tone("#7b5c94"), width=4)
    d.ellipse((cx-5, cy-5, cx+5, cy+5), fill=tone(PURPLE))
    # A small four-point star suggests Madoka without borrowed character art.
    sx, sy = 676, 99
    r = 22 + 2 * math.sin(phase * math.tau)
    star = [(sx, sy-r), (sx+5, sy-5), (sx+r, sy), (sx+5, sy+5), (sx, sy+r), (sx-5, sy+5), (sx-r, sy), (sx-5, sy-5)]
    d.polygon(star, fill=tone(PINK))
    d.line((650, 242, 895, 242), fill=tone("#473048"))
    d.text((683, 260), "H / M", font=font(12), fill=tone("#a48ab8"))
    d.ellipse((888, 48, 892, 52), fill=tone(PINK))
    d.ellipse((611, 205, 614, 208), fill=tone(PURPLE))
    return canvas


def main():
    destination = ROOT / "assets"
    destination.mkdir(parents=True, exist_ok=True)
    for theme, stem in [("dark", "header"), ("light", "header-light")]:
        frames = [frame(index / 60, theme) for index in range(60)]
        frames[0].save(destination / f"{stem}.png")
        # Use a shared palette to keep colors stable across frames.
        palette = frames[0].quantize(colors=128)
        indexed = [item.quantize(palette=palette, dither=Image.Dither.NONE) for item in frames]
        indexed[0].save(destination / f"{stem}.gif", save_all=True, append_images=indexed[1:], duration=100, loop=0, optimize=False, disposal=1)
    print("Generated animated and static banners for light and dark themes")


if __name__ == "__main__":
    main()
