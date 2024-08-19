import time
from ..easing import easing as easing_lookup
from ..easing import *
import random

easing_options = [CubicEaseIn, CubicEaseOut, CubicEaseInOut, LinearInOut, SineEaseIn, SineEaseOut, SineEaseInOut]

class Transition:

    def __init__(self, pixel_object, transition, duration=1, easing=None):
        self.pixel_object = pixel_object
        self.length = len(pixel_object)
        self.pixel_buffer = [0] * self.length
        self.duration = float(duration)

        if isinstance(easing, str):
            easing = easing_lookup(easing)
        if easing is None:
            easing = random.choice(easing_options)
        self.easing = easing(start=0, end=1, duration=self.duration)

        if transition == "random":
            self.transition = random.choice([
                self.wipe_forward,
                self.wipe_backwards, 
                self.wipe_out,
                self.wipe_in,
            ])
        else:
            self.transition = getattr(self, transition)

        self.start = None
        self.complete = False

    def __getitem__(self, index):
        return self.pixel_buffer[index]
    
    def __setitem__(self, index, value):
        self.pixel_buffer[index] = value

    def __len__(self):
        return self.length

    def fill(self, color):
        self.pixel_buffer = [color] * self.length

    def show(self):
        if self.start is None:
            self.start = time.monotonic()
        elapsed = time.monotonic() - self.start

        if elapsed > self.duration:
            return self.reset()

        progress = self.easing(elapsed)
        start, end, reverse = self.transition(progress)

        for ix, val in enumerate(self.pixel_buffer):
            in_range = start <= ix <= end
            if reverse:
                in_range = not in_range
            if not in_range:
                self.pixel_object[ix] = val
    
        return self.pixel_object.show()
    

    def reset(self):
        for ix, val in enumerate(self.pixel_buffer):
            self.pixel_object[ix] = val
        self.pixel_buffer = self.pixel_object
        self.fill = self.pixel_object.fill
        self.show = self.pixel_object.show
        self.complete = True
        
    def wipe_forward(self, progress):
        length = progress * self.length
        return 0, length, True
    
    def wipe_backwards(self, progress):
        start, end, _ = self.wipe_forward(1 - progress)
        return start, end, False
    
    def wipe_out(self, progress):
        length = progress * self.length // 2
        mid_point = self.length // 2
        return mid_point - length, mid_point + length, True
    
    def wipe_in(self, progress):
        start, end, _ = self.wipe_out(1 - progress)
        return start, end, False
