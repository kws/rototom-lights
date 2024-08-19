from picolights.colors import rgb_to_hsv, hsv_to_rgb, to_color, colorwheel, to_hex
from ..helpers import TimedAnimation

def linear_interpolate_color(color1, color2, t):
    return tuple(int((1 - t) * c1 + t * c2) for c1, c2 in zip(color1, color2))

class Rainbow(TimedAnimation):

    def __init__(
            self, 
            pixel_object,
            color="random", 
            color_count=60, 
            color_n=1.5,
            duration=60, 
            scale=1, 
            interpolate=False
        ):
        super(Rainbow, self).__init__(pixel_object, duration=duration)
        self._scale = scale
        self._color_n = color_n

        self.length = len(self.pixel_object)
        reversed = color_count < 0
        self.color_count = int(abs(color_count))
        self.scale = scale * self.color_count / self.length
        self.interpolate = interpolate

        self.color = color = to_color(color)
        self.hsv = col_h, col_s, col_v = rgb_to_hsv(*color)

        step_size = 360 / self.color_count
        self.buffer = [colorwheel(col_h + (hue * step_size), n=color_n) for hue in range(0, self.color_count)]
        if col_s < 1 or col_v < 1:
            for i in range(len(self.buffer)):
                h, _, _ = rgb_to_hsv(*self.buffer[i])
                self.buffer[i] = hsv_to_rgb(h, col_s, col_v)

        if reversed:
            self.buffer.reverse()

    def draw(self):
        offset = self.progress * self.color_count
        for i in range(self.length):
            color_pos = (i * self.scale) - offset

            color_ix = color_pos % self.color_count
            if self.interpolate:
                color_remainder = color_ix % 1
                color_ix = int(color_ix)
                next_ix = (color_ix + 1) % self.color_count
                color = linear_interpolate_color(self.buffer[color_ix], self.buffer[next_ix], color_remainder)
            else:
                color_ix = int(color_ix)
                color = self.buffer[color_ix]

            self.pixel_object[i] = color

    def __str__(self) -> str:
        str = f"rainbow duration={self.duration} color={to_hex(self.color)} color_count={self.color_count} color_n={self._color_n} scale={self._scale}"
        return str

