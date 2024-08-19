from math import floor
from ..helpers import PicoAnimation
from ...colors import to_color, rgb_to_hsv, hsv_to_rgb

import time

class Locator(PicoAnimation):

    def __init__(
            self, 
            pixel_object, 
            pixel_duration=0.2, 
            initial_duration=2,
            initial_blackout=1, 
            initital_color="#F00",
            background_color="#300",
            flash_color="#FFF",
        ):
        super(Locator, self).__init__(pixel_object)
        self.pixel_duration = float(pixel_duration)
        self.initial_duration = float(initial_duration)
        self.initial_blackout = float(initial_blackout)
        self.cycle_time = (len(pixel_object) * self.pixel_duration) + self.initial_duration
        self.initital_color = to_color(initital_color)
        self.background_color = to_color(background_color)
        self.flash_color = to_color(flash_color)
        self.start_time = time.monotonic()

    def draw(self):
        current_time = (time.monotonic() - self.start_time) % self.cycle_time

        # Initial Sequence helps find light locations and calibrate timer
        if current_time < self.initial_duration:
            if current_time > self.initial_duration - self.initial_blackout:
                self.pixel_object.fill(0)
            else:
                self.pixel_object.fill(self.initital_color)
            return
        
        # Figure out which pixel we're on
        sequence_time = current_time - self.initial_duration
        pixel_index = floor(sequence_time / self.pixel_duration)
        self.pixel_object.fill(self.background_color)
        self.pixel_object[pixel_index] = self.flash_color



