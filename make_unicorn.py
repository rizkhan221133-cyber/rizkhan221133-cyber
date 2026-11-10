"""Pixel-art unicorn header for a GitHub profile.

Draws a rider on a flying unicorn that leaves a rainbow trail and writes a
name in the sky. Makes two GIFs: assets/day-flight.gif and assets/night-flight.gif.

    pip install pillow
    python make_unicorn.py "RIZWAN KHAN"
"""
import math
import os
import random
import sys

from PIL import Image, ImageDraw

NAME = (sys.argv[1] if len(sys.argv) > 1 else "RIZWAN KHAN").upper()
W, H, SCALE = 200, 72, 4          # low-res canvas, scaled up 4x -> 800x288
FRAMES, MS = 110, 100             # 11 second loop
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

OUTLINE = (34, 24, 48)

# ---------------------------------------------------------------- font 5x7
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "11110", "10001", "10001", "10001", "11110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "11110", "10000", "10000", "10000", "11111"],
    "F": ["11111", "10000", "11110", "10000", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10011", "10001", "10001", "01111"],
    "H": ["10001", "10001", "11111", "10001", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00001", "00001", "00001", "10001", "10001", "01110"],
    "K": ["10001", "10010", "11100", "10010", "10001", "10001", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10001", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10010", "10001", "10001"],
    "S": ["01111", "10000", "01110", "00001", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "01010", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10001", "10101", "11011", "10001"],
    "X": ["10001", "01010", "00100", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "01010", "00100", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    " ": ["000", "000", "000", "000", "000", "000", "000"],
}
RAINBOW = [(255, 120, 160), (255, 170, 90), (255, 225, 100),
           (130, 220, 130), (110, 180, 255), (180, 140, 255)]


def text_mask(name):
    """Return set of (x,y) pixels for the name at 2x, plus width/height."""
    px, x = set(), 0
    for ch in name:
        g = FONT.get(ch, FONT[" "])
        for gy, row in enumerate(g):
            for gx, c in enumerate(row):
                if c == "1":
                    for dx in (0, 1):
                        for dy in (0, 1):
                            px.add((x + gx * 2 + dx, gy * 2 + dy))
        x += len(g[0]) * 2 + 2
    return px, x - 2, 14


# ---------------------------------------------------------------- helpers
def outline_layer(layer):
    """Add a 1px dark outline around every opaque pixel of an RGBA layer."""
    w, h = layer.size
    src = layer.load()
    out = layer.copy()
    o = out.load()
    for y in range(h):
        for x in range(w):
            if src[x, y][3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and src[nx, ny][3]:
                        o[x, y] = OUTLINE + (255,)
                        break
    return out


DY = 5  # sprite parts are drawn 5px lower so the horn and head fit


class Shifted:
    """ImageDraw wrapper that moves every coordinate down by DY."""
    def __init__(self, d):
        self.d = d

    @staticmethod
    def _xy(xy):
        if isinstance(xy[0], (tuple, list)):
            return [(x, y + DY) for x, y in xy]
        return [v + DY if i % 2 else v for i, v in enumerate(xy)]

    def __getattr__(self, name):
        fn = getattr(self.d, name)
        return lambda xy, *a, **k: fn(self._xy(xy), *a, **k)


def part(size, fn):
    lay = Image.new("RGBA", size, (0, 0, 0, 0))
    fn(Shifted(ImageDraw.Draw(lay)))
    return outline_layer(lay)


# ---------------------------------------------------------------- unicorn
SW, SH = 64, 50
WHITE, SHADE, PINK = (250, 247, 255), (214, 200, 240), (255, 160, 190)
GOLD, GOLD2 = (255, 214, 90), (230, 160, 40)
SKIN, HAIR, HOOD, HOOD2 = (198, 134, 66), (40, 28, 26), (60, 170, 160), (40, 130, 125)
SCARF, PANTS = (240, 80, 110), (60, 60, 100)


def unicorn(frame):
    """Return the unicorn+rider sprite (RGBA, SWxSH) for an animation frame."""
    flap = [0, 1, 2, 1][frame % 4]
    sway = frame % 6 < 3
    spr = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))

    # tail: rainbow strands flowing back
    def tail(d):
        for i, c in enumerate(RAINBOW):
            y = 20 + i
            wob = 1 if (sway and i % 2) else 0
            d.line([(4, y + wob), (9, y - 1), (14, y - 2)], fill=c)
            d.point((3, y + wob + 1), fill=c)
    spr.alpha_composite(part((SW, SH), tail))

    # far legs (shaded)
    def far_legs(d):
        d.rectangle([17, 32, 19, 37], fill=SHADE)
        d.rectangle([35, 31, 37, 34], fill=SHADE)
        d.rectangle([37, 34, 40, 36], fill=SHADE)
    spr.alpha_composite(part((SW, SH), far_legs))

    # body + neck + head
    def body(d):
        d.ellipse([12, 19, 42, 34], fill=WHITE)
        d.ellipse([16, 28, 38, 34], fill=SHADE)
        d.polygon([(35, 23), (41, 12), (47, 13), (43, 28)], fill=WHITE)
        d.ellipse([40, 7, 51, 17], fill=WHITE)
        d.rectangle([47, 11, 55, 16], fill=WHITE)
        d.rectangle([52, 15, 55, 16], fill=SHADE)
        d.polygon([(42, 8), (43, 4), (45, 8)], fill=WHITE)      # ear
    spr.alpha_composite(part((SW, SH), body))
    p = spr.load()
    p[48, 11 + DY] = OUTLINE + (255,)       # eye
    p[48, 10 + DY] = OUTLINE + (255,)
    p[49, 13 + DY] = PINK + (255,)           # blush
    p[54, 13 + DY] = OUTLINE + (255,)        # nostril

    # near legs, bent like a galloping leap, golden hooves
    def legs(d):
        d.rectangle([14, 31, 17, 35], fill=WHITE)
        d.rectangle([11, 35, 15, 37], fill=WHITE)
        d.rectangle([10, 35, 11, 37], fill=GOLD)
        d.rectangle([38, 29, 41, 33], fill=WHITE)
        d.rectangle([41, 32, 45, 34], fill=WHITE)
        d.rectangle([45, 32, 46, 34], fill=GOLD)
    spr.alpha_composite(part((SW, SH), legs))

    # horn
    def horn(d):
        d.polygon([(46, 8), (49, 7), (53, -1)], fill=GOLD)
    spr.alpha_composite(part((SW, SH), horn))
    p = spr.load()
    for (x, y) in ((48, 6), (49, 4), (51, 2)):
        if p[x, y + DY][3]:
            p[x, y + DY] = GOLD2 + (255,)

    # mane: rainbow strands down the neck
    def mane(d):
        pts = [(43, 7), (41, 10), (39, 13), (37, 16), (35, 19), (33, 21)]
        for i, (x, y) in enumerate(pts):
            c = RAINBOW[i % 6]
            off = 1 if sway else 0
            d.rectangle([x - 2 - off, y, x, y + 2], fill=c)
    spr.alpha_composite(part((SW, SH), mane))

    # wing (behind the rider), 3 flap poses
    def wing(d):
        base = (28, 21)
        if flap == 0:      # up
            poly = [base, (22, 2), (27, 4), (31, 6), (35, 10), (33, 21)]
            feathers = [((24, 5), (27, 16)), ((28, 7), (30, 17))]
        elif flap == 1:    # mid
            poly = [base, (14, 9), (18, 8), (24, 9), (31, 13), (33, 21)]
            feathers = [((18, 11), (26, 18)), ((23, 11), (29, 18))]
        else:              # down
            poly = [base, (12, 25), (16, 28), (22, 29), (28, 27), (33, 21)]
            feathers = [((16, 26), (26, 23)), ((21, 28), (29, 24))]
        d.polygon(poly, fill=WHITE)
        for a, b in feathers:
            d.line([a, b], fill=SHADE)
        tip = poly[1]
        d.rectangle([tip[0], tip[1], tip[0] + 2, tip[1] + 1], fill=(200, 220, 255))
    spr.alpha_composite(part((SW, SH), wing))

    # rider
    def rider(d):
        d.rectangle([28, 16, 35, 19], fill=PANTS)        # thigh
        d.rectangle([33, 19, 35, 25], fill=PANTS)        # shin
        d.rectangle([33, 25, 37, 26], fill=(90, 60, 40)) # boot
        d.rectangle([26, 8, 32, 18], fill=HOOD)          # torso
        d.rectangle([26, 15, 32, 18], fill=HOOD2)
        d.rectangle([32, 11, 36, 13], fill=HOOD)         # arm reaching to mane
        d.rectangle([36, 11, 37, 13], fill=SKIN)
        d.rectangle([27, -1, 34, 7], fill=SKIN)          # head
        d.rectangle([26, -2, 34, 0], fill=HAIR)          # hair
        d.rectangle([26, -2, 28, 5], fill=HAIR)
        d.point((33, 1), fill=HAIR)
    spr.alpha_composite(part((SW, SH), rider))
    p = spr.load()
    p[32, 2 + DY] = OUTLINE + (255,)          # eye
    p[32, 3 + DY] = OUTLINE + (255,)
    p[33, 5 + DY] = (150, 80, 60, 255)       # smile

    # scarf flowing behind
    def scarf(d):
        wave = 1 if sway else 0
        d.rectangle([26, 8, 33, 9], fill=SCARF)
        d.line([(25, 8), (21, 9 + wave), (17, 8 + wave), (14, 9)], fill=SCARF)
        d.line([(25, 9), (21, 10 + wave), (18, 9 + wave)], fill=SCARF)
    spr.alpha_composite(part((SW, SH), scarf))
    return spr


# ---------------------------------------------------------------- scenery
def cloud_shape(d, x, y, s, fill, shade):
    d.ellipse([x, y + 4 * s, x + 10 * s, y + 10 * s], fill=fill)
    d.ellipse([x + 5 * s, y, x + 15 * s, y + 9 * s], fill=fill)
    d.ellipse([x + 11 * s, y + 3 * s, x + 20 * s, y + 10 * s], fill=fill)
    d.rectangle([x + 2 * s, y + 7 * s, x + 18 * s, y + 10 * s], fill=fill)
    d.rectangle([x + 2 * s, y + 9 * s, x + 18 * s, y + 10 * s], fill=shade)


THEMES = {
    "day": dict(
        sky=[(110, 170, 235), (125, 182, 240), (140, 194, 244), (157, 206, 248), (175, 218, 251)],
        far=((228, 238, 252), (200, 218, 244)),
        near=((255, 255, 255), (214, 228, 248)),
        orb="sun", text_hi=(255, 255, 255)),
    "night": dict(
        sky=[(14, 16, 40), (18, 22, 50), (22, 28, 60), (28, 34, 70), (34, 40, 80)],
        far=((44, 50, 84), (36, 40, 70)),
        near=((62, 66, 104), (48, 52, 88)),
        orb="moon", text_hi=(255, 250, 230)),
}

random.seed(7)
STARS = [(random.randrange(W), random.randrange(H - 20), random.randrange(6)) for _ in range(60)]
BIRDS = [(60, 8), (68, 5), (150, 12)]


def draw_sky(img, t, th, f):
    d = ImageDraw.Draw(img)
    bands = th["sky"]
    bh = H / len(bands)
    for i, c in enumerate(bands):
        d.rectangle([0, int(i * bh), W, int((i + 1) * bh)], fill=c)
    if th["orb"] == "sun":
        cx, cy = 168, 12
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 236, 140))
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 214, 80))
        for b, (bx, by) in enumerate(BIRDS):     # slow birds
            x = (bx - f * 0.3) % (W + 20) - 10
            up = (f // 3 + b) % 2
            d.point([(x, by + up), (x + 1, by), (x + 3, by), (x + 4, by + up)], fill=(60, 80, 120))
            d.point((x + 2, by + 1), fill=(60, 80, 120))
    else:
        for (x, y, ph) in STARS:
            on = (f // 4 + ph) % 6
            c = (255, 255, 230) if on < 4 else (110, 120, 170)
            d.point((x, y), fill=c)
            if on == 0 and ph % 2 == 0:
                d.point([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)], fill=(170, 180, 230))
        cx, cy = 168, 13
        d.ellipse([cx - 7, cy - 7, cx + 7, cy + 7], fill=(255, 240, 190))
        d.ellipse([cx - 4, cy - 9, cx + 9, cy + 4], fill=bands[0])


def draw_clouds(img, f, th):
    d = ImageDraw.Draw(img)
    # loop-safe: far clouds move 100px per loop, near clouds 200px (tile=W)
    far_off = (f * 100 / FRAMES) % 100
    for k in range(-1, 4):
        x = k * 100 - far_off
        cloud_shape(d, int(x) + 10, 50, 1, *th["far"])
        cloud_shape(d, int(x) + 55, 54, 1, *th["far"])
    near_off = (f * W / FRAMES) % W
    for k in range(-1, 3):
        x = k * W - near_off
        for (cx, cy, s) in ((0, 58, 2), (70, 61, 1), (110, 57, 2), (165, 62, 1)):
            cloud_shape(d, int(x + cx), cy, s, *th["near"])


# ---------------------------------------------------------------- frame
TEXT_PX, TW, TH = text_mask(NAME)
TX, TY = (W - TW) // 2, 44
WRITE_END = 72          # frame at which the unicorn has left the screen
FADE_START = 98


def unicorn_x(f):
    # from off-screen left to off-screen right during the writing phase
    return -SW + (W + SW + 10) * min(f, WRITE_END) / WRITE_END


def frame(f, th):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    draw_sky(img, f, th, f)
    draw_clouds(img, f, th)

    ux = unicorn_x(f)
    bob = int(round(2 * math.sin(f * 2 * math.pi / 8)))
    uy = -3 + bob
    tail_x = ux + 6            # where the rainbow leaves the unicorn
    reveal = tail_x - TX       # text columns revealed so far
    if f >= WRITE_END:
        reveal = TW + 10

    # text fade at the end of the loop (pixel dissolve)
    fade = 0.0
    if f >= FADE_START:
        fade = (f - FADE_START + 1) / (FRAMES - FADE_START)

    # text layer with outline
    tl = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tp = tl.load()
    rnd = random.Random(1)
    for (x, y) in TEXT_PX:
        if x < reveal and rnd.random() >= fade:
            c = RAINBOW[min(5, y * 6 // TH)]
            if y == 0 or (x + y) % 9 == 0:
                c = th["text_hi"]
            tp[TX + x, TY + y] = c + (255,)
    img.alpha_composite(outline_layer(tl))

    # rainbow ribbon from the text front up to the unicorn's tail
    d = ImageDraw.Draw(img)
    if f < WRITE_END + 4:
        start = max(-10, tail_x - 70)
        for xx in range(int(start), int(tail_x)):
            if xx < 0 or xx >= W:
                continue
            age = (tail_x - xx) / 70
            if age > 1:
                continue
            # ribbon curves from tail height down toward the text line
            base = uy + DY + 20
            wave = math.sin(xx * 0.25 - f * 0.9) * 1.5 * age
            for i, c in enumerate(RAINBOW):
                if age > 0.55 and (xx + i + f) % 3 == 0:
                    continue
                yy = int(base + i + wave)
                if 0 <= yy < H:
                    d.point((xx, yy), fill=c)
        # sparkle dust falling onto the letters
        sp = random.Random(f)
        for _ in range(7):
            sx = tail_x - sp.randint(2, 30)
            sy = uy + DY + 26 + sp.randint(0, 16)
            if 0 <= sx < W and sy < H:
                c = (255, 255, 255) if sp.random() < .5 else (255, 230, 120)
                d.point((sx, sy), fill=c)
                if sp.random() < .3:
                    d.point([(sx - 1, sy), (sx + 1, sy), (sx, sy - 1), (sx, sy + 1)], fill=c)

    # twinkles on finished text
    if WRITE_END <= f < FADE_START:
        sp = random.Random(f // 2)
        for _ in range(3):
            x, y = sp.choice(list(TEXT_PX))
            sx, sy = TX + x, TY + y
            d.point([(sx, sy - 2), (sx, sy + 2), (sx - 2, sy), (sx + 2, sy), (sx, sy)], fill=(255, 255, 255))

    if f < WRITE_END + 2:
        img.alpha_composite(unicorn(f), (int(ux), uy))
    return img.resize((W * SCALE, H * SCALE), Image.NEAREST).convert("RGB")


def build(theme):
    th = THEMES[theme]
    frames = [frame(f, th) for f in range(FRAMES)]
    pal = [fr.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for fr in frames]
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, f"{theme}-flight.gif")
    pal[0].save(path, save_all=True, append_images=pal[1:], duration=MS, loop=0,
                optimize=True, disposal=1)
    print("wrote", path, os.path.getsize(path) // 1024, "KB")


if __name__ == "__main__":
    for t in ("day", "night"):
        build(t)
