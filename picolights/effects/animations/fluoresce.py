from math import ceil
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.helper import PixelSubset
import time
import random

from ..helpers import PicoAnimation


class Fluoresce(PicoAnimation):
   
    on_cycle_complete_supported = True

    def __init__(self, pixel_object, max_duration=3, **kwargs):
        super(Fluoresce, self).__init__(pixel_object, **kwargs)
        self.__start = time.monotonic()
        self.duration=max_duration
        self.__next = time.monotonic() + random.random()
        self.__is_on = False

    def draw(self):
        if time.monotonic() - self.__start >= self.duration:
            self.pixel_object.fill(self.color)
            self.cycle_complete = True
            return

        if time.monotonic() > self.__next:
            self.pixel_object.fill(self.color if not self.__is_on else 0)
            self.__is_on =  not self.__is_on
            self.__next = time.monotonic() + random.random() * 0.5

class MultiStripFluoresce(AnimationGroup):

    def __init__(self, pixels, **kwargs):
        strips = self.create_multi_strip(pixels, **kwargs)
        super(MultiStripFluoresce, self).__init__(strips)


    @staticmethod
    def create_multi_strip(pixels, min_strip_length=50, min_gap=35, **kwargs):
        wall_length = len(pixels)
        if min_strip_length + min_gap > wall_length:
            print("Wall too short for multiple strips. Returning single strip.")
            return Fluoresce(pixels, **kwargs)
        strip_count = wall_length // (min_strip_length + min_gap)
        remaining_pixels = wall_length % (min_strip_length + min_gap)
        remaining_pixels //= 2

        strip_extra = ceil(remaining_pixels * min_strip_length / (min_strip_length + min_gap))
        gap_extra = remaining_pixels - strip_extra

        print(f"Remaining pixels {remaining_pixels} giving {strip_extra} for strip and {gap_extra} for gap")

        strip_length = min_strip_length + strip_extra
        gap_length = min_gap + gap_extra
      
        print(f"Creating {strip_count} strips of length {strip_length} and gap {gap_length}")

        current_pixel = gap_length // 2
        strips = []
        for _ in range(strip_count):
            strip = PixelSubset(pixels, current_pixel, current_pixel+strip_length)
            current_pixel += strip_length + gap_length
            strips.append(Fluoresce(strip, **kwargs))

        return AnimationGroup(*strips)
    
