from math import floor, ceil
from picolights.colors import random_color, to_color
from adafruit_led_animation.animation import Animation
from adafruit_led_animation.helper import PixelSubset

import time
from ...easing import easing as easing_lookup, CubicEaseOut

class ZipOut(Animation):

    on_cycle_complete_supported = True

    def __init__(self, pixels, speed=0, color=None, duration=2, easing=CubicEaseOut):
        if color==None:
            color = random_color()
        super(ZipOut, self).__init__(pixels, speed=speed, color=to_color(color))

        self.done = False
        self.duration = duration
        self.last_pixel = len(pixels)

        if isinstance(easing, str):
            easing = easing_lookup(easing)

        self._easing = easing(start=0, end=len(pixels)/2, duration=duration)

    @staticmethod
    def create_animation(pixels, **kwargs):
        return ZipOut(pixels, **kwargs)
 
    def draw(self):
        if self.done:
            return
        
        if self.draw_count == 1:
            self.start = time.monotonic()

        elapsed = time.monotonic() - self.start
        progress = self._easing(elapsed)
  
        length = max(1, ceil(progress))
        
        PixelSubset(self.pixel_object, 0, length).fill(self.color)
        PixelSubset(self.pixel_object, self.last_pixel-length-1, self.last_pixel).fill(self.color)

        if elapsed > self.duration:
            self.cycle_complete = True
            self.done = True
            