from picolights.colors import random_color, to_color, to_hex
from adafruit_led_animation.animation import Animation

import time
from ...easing import easing as easing_lookup, CubicEaseOut

class Flashy(Animation):

    on_cycle_complete_supported = True

    def __init__(self, pixels, color=None, duration=2, easing=CubicEaseOut):
        if color == None:
          color = random_color()
        color = to_color(color)
        super(Flashy, self).__init__(pixels, speed=0, color=color)

        self.done = False
        self.duration = duration
  
        if isinstance(easing, str):
            easing = easing_lookup(easing)

        self._easing = easing(start=0, end=2, duration=duration)

    @staticmethod
    def create_animation(pixels, **kwargs):
        return Flashy(pixels, **kwargs)
 
    def draw(self):
        if self.draw_count == 1:
            self.start = time.monotonic()

        elapsed = time.monotonic() - self.start
        elapsed = elapsed % self.duration
        progress = self._easing(elapsed)

        if progress > 1:
          progress = 2 - progress

        self.pixel_object.fill((
          self.color[0] * progress, 
          self.color[1] * progress,
          self.color[2] * progress,
        ))
  

    def __str__(self) -> str:
      return f"flashy color={to_hex(self.color)} duration={self.duration}"