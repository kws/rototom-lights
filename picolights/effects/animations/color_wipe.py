import math
from ..helpers import TimedAnimation
import random


class ColorWipe(TimedAnimation):

    on_cycle_complete_supported = True

    def __init__(self, pixels, **kwargs):
        super().__init__(pixels, **kwargs)

        self.length = len(self.pixel_object)
        self._transition = random.choice([
            self.wipe_forward,
            self.wipe_backwards, 
            self.wipe_out,
            self.wipe_in,
        ])

    def draw(self):
        self.progress_length = min(self.length, self.progress * self.length)
        self._transition()   

    def on_cycle_complete(self):
        # Make sure the last pixel is set
        self.pixel_object.fill(self.color)
        self.show()
        return super().on_cycle_complete()

    def wipe_forward(self):
        for i in range(math.ceil(self.progress_length)):
            self.pixel_object[i] = self.color
    
    def wipe_backwards(self):
        length = min(self.length, self.progress_length)
        for i in range(math.ceil(length)):
            self.pixel_object[self.length-i-1] = self.color

    def wipe_in(self):
        length = self.progress_length / 2
        for i in range(math.ceil(length)):
            self.pixel_object[i] = self.color
            self.pixel_object[self.length-i-1] = self.color

    def wipe_out(self):
        length = self.progress_length / 2
        mid_point = self.length // 2
        for i in range(math.ceil(length)):
            self.pixel_object[mid_point+i] = self.color
            self.pixel_object[mid_point-i] = self.color
