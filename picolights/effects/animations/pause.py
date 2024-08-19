from adafruit_led_animation.animation import Animation
import time

class Pause(Animation):

    on_cycle_complete_supported = True

    def __init__(self, pixels, duration: int):
        super(Pause, self).__init__(pixels, speed=0, color=None)
        self.duration = duration
        self._start = 0

    def draw(self):
        if self.cycle_complete:
            return

        if self.draw_count == 1:
            self._start = time.monotonic()

        if self.duration and time.monotonic() - self._start > self.duration:
            self.cycle_complete = True

