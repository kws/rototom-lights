from picolights.colors import random_color

from adafruit_led_animation.helper import PixelSubset

import time
import random

from ..helpers import PicoAnimation

class Patchy(PicoAnimation):

    on_cycle_complete_supported = True

    def __init__(self, pixels, patch_size=15, duration=2, **kwargs):
        super(Patchy, self).__init__(pixels, **kwargs)
        self.patch_size = patch_size
        self.duration = duration
        self._start = 0
        self._random_patches = "color" not in kwargs

    def draw(self):
        if self.draw_count == 1:
            self._start = time.monotonic()
        if time.monotonic() - self._start > self.duration:
            self.cycle_complete = True
            return

        pixel_len = len(self.pixel_object)

        start_pos = random.randint(-self.patch_size, pixel_len-1)
        start_pos = max(start_pos, 0)
        end_pos = min(start_pos + self.patch_size, pixel_len)

        color =  random_color() if self._random_patches else self.color
        PixelSubset(self.pixel_object, start_pos, end_pos).fill(color)
        

