import random
import time
from ..easing import easing as easing_lookup, easing_choices, LinearInOut


class PicoAnimation:

    def __init__(self, pixel_object, notify_cycles=0):
        self.pixel_object = pixel_object
        self.draw_count = 0
        self.cycle_count = 0
        self._cycle_complete_receivers = []
        self.notify_cycles = notify_cycles


    def animate(self, show=True):
        self.before_draw()
        self.draw()
        self.after_draw()
        if show:
            self.pixel_object.show()
        return True
    
    def before_draw(self):
        self.draw_count += 1

    def after_draw(self):
        pass

    def on_cycle_complete(self):
        self.cycle_count += 1
        if self.notify_cycles > 0 and self.cycle_count % self.notify_cycles == 0:
            for receiver in self._cycle_complete_receivers:
                receiver(self)

    def add_cycle_complete_receiver(self, receiver):
        self._cycle_complete_receivers.append(receiver)



class TimedAnimation(PicoAnimation):

    def __init__(self, pixel_object, duration=1, easing=None, **kwargs):
        super(TimedAnimation, self).__init__(pixel_object, **kwargs)

        self.duration = duration

        self.start_time = None
        self.cycle_ends = None
        self.total_elapsed = None
        self.elapsed = None
        self.progress = None

        if easing == "random":
            easing = random.choice(easing_choices)
        elif isinstance(easing, str):
            easing = easing_lookup(easing)

        if easing is None:
            easing = LinearInOut

        self.easing = easing(start=0, end=1, duration=duration)


    def before_draw(self):
        self.draw_start = time.monotonic()
        if self.start_time is None:
            self.start_time = self.draw_start
            self.cycle_ends = self.start_time + self.duration

        self.total_elapsed = self.draw_start - self.start_time
        self.elapsed = self.total_elapsed % self.duration
        self.progress = self.easing(self.elapsed)


    def after_draw(self):
        if self.draw_start >= self.cycle_ends:
            self.on_cycle_complete()

    def on_cycle_complete(self):
        super().on_cycle_complete()
        self.cycle_ends = self.start_time + (self.duration * (self.cycle_count+2))