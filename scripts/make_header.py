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


def law_of_cycles(d, phase, cx=776, cy=135):
    """A simplified vector interpretation of the Rebellion emblem, not an official asset."""
    pulse = math.sin(phase * math.tau)
    # A complete revolution per loop, made visible by asymmetric highlights.
    for radius, ink, width in [(82, "#c7a888", 3), (76, "#dfc4ad", 1), (67, "#b77e9e", 2)]:
        d.ellipse((cx-radius, cy-radius, cx+radius, cy+radius), outline=ink, width=width)
    for index in range(48):
        angle = index * math.tau / 48 + phase * math.tau
        d.line([polar(cx, cy, 77, angle), polar(cx, cy, 81, angle)], fill="#b38c72", width=2)
    sweep = phase * 360
    for offset, ink in [(0, "#ad5686"), (180, "#d29ab9")]:
        d.arc((cx-85, cy-85, cx+85, cy+85), start=sweep+offset, end=sweep+offset+48, fill=ink, width=4)
    for tail in range(7):
        angle = phase * math.tau - tail * 0.045
        x, y = polar(cx, cy, 91, angle)
        radius = max(1, 4 - tail * 0.5)
        d.ellipse((x-radius, y-radius, x+radius, y+radius), fill="#bf6e9c" if tail < 3 else "#e5bcd4")
    # Eight-point compass star, with the vertical tips slightly longer.
    star = []
    for index in range(32):
        angle = index * math.tau / 32 - math.pi / 2 + math.radians(8) * pulse
        if index % 4 == 0:
            radius = (100 if index in (0, 16) else 87) * (1 + 0.045 * pulse)
        elif index % 2 == 0:
            radius = 25
        else:
            radius = 13
        star.append(polar(cx, cy, radius, angle))
    ink = tuple(round(base + 18 * pulse) for base in (188, 91, 145))
    d.polygon(star, fill=ink)
    d.ellipse((cx-8, cy-8, cx+8, cy+8), fill="#fff5fc")
    # Crown and small round finial.
    crown = [(cx-17, cy-83), (cx-22, cy-104), (cx-8, cy-94), (cx, cy-115), (cx+8, cy-94), (cx+22, cy-104), (cx+17, cy-83)]
    d.polygon(crown, fill="#f1d3e5", outline="#ba6a98")
    d.line((cx-16, cy-84, cx+16, cy-84), fill="#ba6a98", width=2)
    d.ellipse((cx-3, cy-124, cx+3, cy-118), fill="#b68b9e")

    def curve(points, steps=24):
        a, b, c, e = points
        return [((1-t)**3*a[0] + 3*(1-t)**2*t*b[0] + 3*(1-t)*t*t*c[0] + t**3*e[0],
                 (1-t)**3*a[1] + 3*(1-t)**2*t*b[1] + 3*(1-t)*t*t*c[1] + t**3*e[1])
                for t in (index / steps for index in range(steps+1))]

    # Wings flap from fixed shoulder joints, twice per six-second loop.
    wing = curve([(0, 58), (-37, 63), (-78, 29), (-111, 13)])
    wing += curve([(-111, 13), (-105, 34), (-88, 41), (-78, 43)])
    wing += [(-101, 35), (-85, 54), (-62, 59), (-87, 53), (-70, 70), (-43, 73), (-68, 69), (-46, 85), (-18, 80), (0, 69)]
    for sign in (-1, 1):
        def wing_point(x, y):
            angle = math.radians(24) * math.sin(phase * math.tau * 2)
            shoulder_y = 64
            local_y = y - shoulder_y
            rotated_x = x * math.cos(angle) - local_y * math.sin(angle)
            rotated_y = x * math.sin(angle) + local_y * math.cos(angle)
            return (cx + sign*rotated_x, cy + shoulder_y + rotated_y)
        points = [wing_point(x, y) for x, y in wing]
        d.polygon(points, fill="#fffafd", outline="#b991aa")
        for y, reach in [(45, 82), (58, 66), (70, 47)]:
            feather = curve([(-12, 66), (-29, 68), (-reach+8, y+2), (-reach, y)])
            d.line([wing_point(x, yy) for x, yy in feather], fill="#dfc6d7", width=1)
    # A clear caption replaces illegible imitation runes at banner size.
    caption = "LAW OF CYCLES"
    d.text((cx, cy+105), caption, anchor="mm", font=font(11), fill="#9d6c8d")
    for sx, sy, offset in [(cx-126, cy-51, 0), (cx+111, cy-72, 0.3), (cx+113, cy+87, 0.65)]:
        size = 4 + 1.5 * math.sin((phase + offset) * math.tau)
        d.polygon([(sx, sy-size), (sx+1, sy-1), (sx+size, sy), (sx+1, sy+1), (sx, sy+size), (sx-1, sy+1), (sx-size, sy), (sx-1, sy-1)], fill="#c798b4")


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
        law_of_cycles(d, phase)
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
    for theme, stem in [("dark", "header"), ("light", "header-light-wings")]:
        frames = [frame(index / 60, theme) for index in range(60)]
        frames[0].save(destination / f"{stem}.png")
        # Use a shared palette to keep colors stable across frames.
        palette = frames[0].quantize(colors=128)
        indexed = [item.quantize(palette=palette, dither=Image.Dither.NONE) for item in frames]
        indexed[0].save(destination / f"{stem}.gif", save_all=True, append_images=indexed[1:], duration=100, loop=0, optimize=False, disposal=1)
    emblem_frames = []
    for index in range(60):
        emblem = Image.new("RGB", (320, 280), "#fff9fc")
        law_of_cycles(ImageDraw.Draw(emblem), index / 60, 160, 135)
        emblem_frames.append(emblem)
    emblem_frames[0].save(destination / "law-of-cycles-wings.png")
    palette = emblem_frames[0].quantize(colors=128)
    indexed = [item.quantize(palette=palette, dither=Image.Dither.NONE) for item in emblem_frames]
    indexed[0].save(destination / "law-of-cycles-wings.gif", save_all=True, append_images=indexed[1:], duration=100, loop=0, optimize=False, disposal=1)
    print("Generated animated and static banners for light and dark themes")


if __name__ == "__main__":
    main()
