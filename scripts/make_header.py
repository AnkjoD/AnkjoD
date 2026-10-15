"""Build an original geometric banner; requires Pillow. No downloaded artwork."""

import math
import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

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


def homura_clock(canvas, phase):
    """Render at triple resolution for smooth hands and restrained soft light."""
    scale = 3
    layer = Image.new("RGBA", (300*scale, 300*scale))
    pen = ImageDraw.Draw(layer)
    cx, cy = 150, 145

    def box(radius):
        return tuple(value*scale for value in (cx-radius, cy-radius, cx+radius, cy+radius))

    def line(points, fill, width=1):
        pen.line([(x*scale, y*scale) for x,y in points], fill=fill, width=max(1,round(width*scale)))

    # A diffuse halo is kept behind the crisp clock face.
    pen.ellipse(box(100), outline=(145, 101, 184, 65), width=5*scale)
    layer = layer.filter(ImageFilter.GaussianBlur(5*scale))
    pen = ImageDraw.Draw(layer)
    pen.ellipse(box(96), fill=(17, 12, 26, 245), outline="#69507f", width=scale)
    pen.ellipse(box(102), outline="#392743", width=scale)
    pen.ellipse(box(83), outline="#34243f", width=scale)
    for tick in range(60):
        angle = tick*math.tau/60 - math.pi/2
        major = tick % 5 == 0
        line([polar(cx,cy,86 if major else 91,angle), polar(cx,cy,94,angle)], "#b293cb" if major else "#554260", 1.4 if major else 0.6)
    angle = phase*math.tau - math.pi/2
    # A short light trail makes the sweep legible without filling the dial.
    for trail in range(18):
        a = angle - trail*0.014
        alpha = round(105*(1-trail/18))
        line([(cx,cy), polar(cx,cy,71,a)], (184,143,218,alpha), 1)
    line([polar(cx,cy,12,angle+math.pi), polar(cx,cy,73,angle)], "#d6b9ed", 1.8)
    line([(cx,cy),polar(cx,cy,45,-2.2)], "#9274ae", 3)
    pen.ellipse(box(4), fill="#e2c9f4")
    pen.ellipse(box(1.5), fill="#634378")
    sx, sy = 37, 72
    radius = 10 + math.sin(phase*math.tau)
    points=[(sx,sy-radius),(sx+2,sy-2),(sx+radius,sy),(sx+2,sy+2),(sx,sy+radius),(sx-2,sy+2),(sx-radius,sy),(sx-2,sy-2)]
    pen.polygon([(x*scale,y*scale) for x,y in points],fill="#dcaac3")
    layer = layer.resize((300,300), Image.Resampling.LANCZOS)
    canvas.paste(layer,(622,0),layer)


def homura_background(canvas, phase):
    """Looping violet atmosphere and drifting stardust, behind the foreground."""
    angle = phase * math.tau
    haze = Image.new("RGBA", (240, 75))
    glow = ImageDraw.Draw(haze)
    dx, dy = 10 * math.sin(angle), 5 * math.cos(angle)
    glow.ellipse((109+dx, -10+dy, 227+dx, 75+dy), fill=(100, 45, 147, 79))
    glow.ellipse((183-dx, -25-dy, 273-dx, 42-dy), fill=(150, 61, 112, 63))
    haze = haze.filter(ImageFilter.GaussianBlur(12)).resize((WIDTH, HEIGHT), Image.Resampling.BICUBIC)
    canvas.paste(haze, (0, 0), haze)

    sky = Image.new("RGBA", (WIDTH, HEIGHT))
    stars = ImageDraw.Draw(sky)
    # Broad, low-contrast light ribbons leave the name area quiet.
    for ribbon in range(2):
        points = []
        for x in range(440, 990, 3):
            y = 93 + 91*ribbon + 32*math.sin((x-440)*0.006 + ribbon) + 13*math.sin(angle + (x-440)*0.004)
            points.append((x, y))
        stars.line(points, fill=(119, 77, 157, 55) if ribbon == 0 else (166, 96, 141, 43), width=2)
    # Long arcs suggest layers in space, without another clock face.
    stars.arc((604, -22, 964, 316), 193+7*math.sin(angle), 296+7*math.sin(angle), fill=(150, 108, 181, 72), width=1)
    stars.arc((580, -50, 982, 337), 22-5*math.sin(angle), 108-5*math.sin(angle), fill=(139, 98, 170, 63), width=1)
    for index in range(26):
        base_x = 461 + (index*103 % 483)
        base_y = 19 + (index*67 % 259)
        offset = index * 2.39996
        x = base_x + 11*math.sin(angle+offset)
        y = base_y + 7*math.cos(angle+offset)
        brightness = (1+math.sin(angle+offset))/2
        radius = 0.8 + (1.2 if index%5 == 0 else 0.5)*brightness
        alpha = round(58+123*brightness)
        stars.ellipse((x-radius,y-radius,x+radius,y+radius), fill=(214, 171, 223, alpha))
        if index%8 == 0:
            reach = 3+2*brightness
            stars.line((x-reach,y,x+reach,y), fill=(220,180,225,alpha//2), width=1)
            stars.line((x,y-reach,x,y+reach), fill=(220,180,225,alpha//2), width=1)
    canvas.paste(sky, (0,0), sky)


def madoka_background(canvas, phase):
    """Rose-gold haze, drifting petals and light behind the Law of Cycles."""
    angle = phase * math.tau
    haze = Image.new("RGBA", (240, 75))
    glow = ImageDraw.Draw(haze)
    dx, dy = 8*math.sin(angle), 4*math.cos(angle)
    glow.ellipse((112+dx, -14+dy, 233+dx, 78+dy), fill=(235, 160, 202, 68))
    glow.ellipse((171-dx, -15-dy, 257-dx, 66-dy), fill=(255, 221, 155, 86))
    haze = haze.filter(ImageFilter.GaussianBlur(11)).resize((WIDTH, HEIGHT), Image.Resampling.BICUBIC)
    canvas.paste(haze, (0,0), haze)
    layer = Image.new("RGBA", (WIDTH, HEIGHT))
    d = ImageDraw.Draw(layer)
    # Soft paths of light, clear of the name and behind the emblem.
    for ribbon in range(2):
        points = []
        for x in range(440, 990, 3):
            y = 80+127*ribbon+28*math.sin((x-440)*0.006+ribbon)+12*math.sin(angle+(x-440)*0.004)
            points.append((x,y))
        d.line(points, fill=(198, 124, 163, 57) if ribbon == 0 else (200, 162, 99, 68), width=2)
    # Petals drift on periodic paths so there is no jump at the loop boundary.
    for index in range(9):
        offset = index*2.39996
        x = 476+(index*137 % 442)+17*math.sin(angle+offset)
        y = 25+(index*73 % 242)+11*math.cos(angle+offset)
        rotation = offset+0.45*math.sin(angle+offset)
        length = 7+(index%3)*2
        local = [(0,-length), (length*0.6,-length*0.35), (length*0.45,length*0.55), (0,length), (-length*0.35,length*0.3), (-length*0.42,-length*0.3)]
        points = [(x+px*math.cos(rotation)-py*math.sin(rotation), y+px*math.sin(rotation)+py*math.cos(rotation)) for px,py in local]
        d.polygon(points, fill=(206, 135, 173, 68+index%3*17))
    for index in range(20):
        offset = index*2.39996
        x = 455+(index*101 % 490)+8*math.sin(angle+offset)
        y = 17+(index*61 % 264)+6*math.cos(angle+offset)
        light = (1+math.sin(angle+offset))/2
        radius = 0.8+1.1*light
        color = (174, 119, 164, round(60+90*light)) if index%2 else (191, 150, 72, round(65+100*light))
        d.ellipse((x-radius,y-radius,x+radius,y+radius), fill=color)
        if index%7 == 0:
            size = 3+light*2
            d.line((x-size,y,x+size,y), fill=color, width=1)
            d.line((x,y-size,x,y+size), fill=color, width=1)
    canvas.paste(layer,(0,0),layer)


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
        homura_background(canvas, phase)
    else:
        madoka_background(canvas, phase)
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

    homura_clock(canvas, phase)
    d.text((772, 267), "HOMURA", anchor="mm", font=font(11), fill=tone("#a48ab8"))
    d.ellipse((888, 48, 892, 52), fill=tone(PINK))
    d.ellipse((611, 205, 614, 208), fill=tone(PURPLE))
    return canvas


def main():
    destination = ROOT / "assets"
    destination.mkdir(parents=True, exist_ok=True)
    for theme, stem in [("dark", "header-dark-atmosphere"), ("light", "header-light-atmosphere")]:
        count, duration = (150, 40) if theme == "dark" else (60, 100)
        frames = [frame(index / count, theme) for index in range(count)]
        frames[0].save(destination / f"{stem}.png")
        # Use a shared palette to keep colors stable across frames.
        palette = frames[0].quantize(colors=128)
        indexed = [item.quantize(palette=palette, dither=Image.Dither.NONE) for item in frames]
        indexed[0].save(destination / f"{stem}.gif", save_all=True, append_images=indexed[1:], duration=duration, loop=0, optimize=False, disposal=1)
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
