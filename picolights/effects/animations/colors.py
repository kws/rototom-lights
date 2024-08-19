from math import floor
from ..helpers import PicoAnimation
from ...colors import to_color, rgb_to_hsv, hsv_to_rgb

class Colors(PicoAnimation):

    def __init__(self, pixel_object, colors="random,random"):
        super().__init__(pixel_object)
        colors = colors.split(",")
        colors = [c.strip() for c in colors if c.strip()]
        colors = [to_color(c) for c in colors]
        self.colors = colors

        color_hsvs = [rgb_to_hsv(*c) for c in colors]

        if len(colors) == 1:
            self.buffer = [colors[0]]
        else:
            self.buffer = [0] * len(pixel_object)
            segment_length = len(pixel_object) / (len(colors) - 1)
            for pix in range(len(pixel_object)):
                segment_ix = floor(pix / segment_length)
                h1, s1, v1 = color_hsvs[segment_ix]
                h2, s2, v2 = color_hsvs[segment_ix + 1]
                segment_progress = (pix % segment_length) / (segment_length - 1)
                dh = h2 - h1
                if abs(dh) > 180:
                    if (dh > 0):
                        dh = dh - 360
                    else:
                        dh = dh + 360
                
                h = h1 + dh * segment_progress
                s = s1 + (s2 - s1) * segment_progress
                v = v1 + (v2 - v1) * segment_progress
                self.buffer[pix] = hsv_to_rgb(h, s, v)

    def draw(self):
        offset = 0 # self.progress * self.color_count
        for i in range(len(self.pixel_object)):
            color_pos = i - offset

            color_ix = color_pos % len(self.buffer)
            color_ix = int(color_ix)
            color = self.buffer[color_ix]

            self.pixel_object[i] = color

    def __str__(self) -> str:
        str = f"colors colors={','.join(self.colors)}"
        return str