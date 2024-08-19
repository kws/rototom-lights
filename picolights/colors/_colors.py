import math
import random
from binascii import unhexlify, hexlify
from ._names import from_color_name

def sgn(val):
    return -1 if val < 0 else (1 if val > 0 else 0)

def superellipse(a, b, n, theta):
    ct = math.cos(theta)
    st = math.sin(theta)
    x = a * sgn(ct) * abs(ct)**(2/n)
    y = b * sgn(st) * abs(st)**(2/n)
    return int(x), int(y)

def colorwheel(color_value, n=2):
    color_value = color_value % 360
    sector_angle = color_value % 120 # 120 = 360 / 3 - we have three sectors
    sector = color_value / 120

    sector_angle = math.radians(sector_angle * 0.75) # 90 / 120 = 0.75
    x, y = superellipse(255, 255, n, sector_angle)

    if sector < 1:
        return x, y ,0
    elif sector < 2:
        return 0, x, y
    else:
        return y, 0, x


def to_color(color):
    if isinstance(color, str):
        if color.startswith("#"):
            color = from_hex(color)
        elif color.lower().strip() == "random":
            color = random_color()
        elif "," in color:
            color = tuple(int(x) for x in color.split(","))
        else:
            color = from_color_name(color)

    if isinstance(color, int):
        color = (color >> 16 & 0xFF, color >> 8 & 0xFF, color & 0xFF)
    return color

def from_hex(color):
    if color.startswith("#"):   
        color = color[1:]
    if len(color) == 3:
        color = color[0] * 2 + color[1] * 2 + color[2] * 2
    return int.from_bytes(unhexlify(color), "big")

def to_hex(color):
    if isinstance(color, tuple):
        color = (color[0] << 16) + (color[1] << 8) + color[2]
    return "#" + hexlify(int.to_bytes(color, 3, "big")).decode("ascii")


def random_color():
    return colorwheel(random.randint(0, 360))


def adjust_brightness(color, brightness):
    color = to_color(color)
    h, s, v = rgb_to_hsv(*color)
    v *= brightness
    return hsv_to_rgb(h, s, v)


def rgb_to_hsv(r: int, g: int, b:int):
    r, g, b = r / 255, g / 255, b / 255
    c_max = max(r, g, b)
    c_min = min(r, g, b)
    delta = c_max - c_min

    if delta == 0:
        h = 0
    elif c_max == r:
        h = 60 * (((g - b) / delta) % 6)
    elif c_max == g:
        h = 60 * (((b - r) / delta) + 2)
    else:
        h = 60 * (((r - g) / delta) + 4)

    if c_max == 0:
        s = 0
    else:
        s = delta / c_max

    v = c_max

    return round(h), s, v


def hsv_to_rgb(h: int, s: float, v: float):
    """
    Hue is in the range 0 to 360
    """
    h = h % 360

    c = v * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = v - c

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    return round((r + m) * 255), round((g + m) * 255), round((b + m) * 255)
