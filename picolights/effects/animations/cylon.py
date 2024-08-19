import math
from picolights.easing import CubicEaseInOut
from picolights.colors import BlendStrip, hsv_to_rgb, to_color, to_hex
from ..helpers import PicoAnimation
import time

class Eye:
    
        def __init__(self, end_pos, start_time, duration, color, length=None):
            self.start_time = start_time
            self.start_pos = 0
            self.end_pos = end_pos

            if not length:
                self.length = (self.end_pos - self.start_pos) // 10
            else:
                self.length = int(length)

            self.color = color
            self.duration = duration
            self._real_end = self.end_pos - self.length
            self._real_length = self._real_end - self.start_pos
            self.easing = CubicEaseInOut(start=self.start_pos, end=self._real_end+1, duration=self.duration)

        def draw(self, pixel_object):
            elapsed = time.monotonic() - self.start_time
            cycle = elapsed // self.duration
            elapsed = elapsed % self.duration
            current_pos = math.floor(self.easing(elapsed))
            reverse = cycle % 2 == 1

            if reverse:
                start_pos = self._real_length - current_pos
            else:
                current_pos = current_pos + self.start_pos
                start_pos = current_pos

            end_pos = start_pos + self.length

            for pos in range(start_pos, end_pos):
                if 0 <= pos < self.end_pos:
                    pixel_object[pos] = self.color 


class Cylon(PicoAnimation):

    def __init__(self, pixel_object, duration=1, eye_count=None, eye_colors="red,blue", eye_length=None):
        super().__init__(pixel_object)
        start_time = time.monotonic()
        self.duration = duration

        if eye_count is None:
            eye_colors = [to_color(c.strip()) for c in eye_colors.split(",")]
            eye_count = len(eye_colors)
        else:
            eye_count = int(eye_count)
            color_step = 360 // eye_count
            eye_colors = [hsv_to_rgb(i*color_step, 1, 1) for i in range(eye_count)]

        self.eyes = [
            Eye(
                end_pos=len(pixel_object), 
                start_time=start_time-i*(duration*2/eye_count), 
                duration=duration, 
                color=eye_colors[i],
                length=eye_length,
            ) for i in range(eye_count)
        ]
        self.eye_colors = eye_colors


    def draw(self):
        pixels = BlendStrip(len(self.pixel_object))
        for eye in self.eyes:
            eye.draw(pixels)

        for i in range(len(self.pixel_object)):
            self.pixel_object[i] = pixels[i] 
        

    def __str__(self) -> str:
        print(self.eye_colors)
        return f"cylon duration={self.duration} eye_colors={','.join([to_hex(c) for c in self.eye_colors])}"
    
