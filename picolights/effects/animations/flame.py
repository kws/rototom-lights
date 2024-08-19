
from ..helpers import PicoAnimation
from ...colors import to_color, adjust_brightness
import random
import math

def box_muller():
    u1 = random.uniform(0, 1)
    u2 = random.uniform(0, 1)
    
    z0 = (-2 * math.log(u1))**0.5 * math.cos(2 * math.pi * u2)
    z1 = (-2 * math.log(u1))**0.5 * math.sin(2 * math.pi * u2)
    
    return z0, z1

def normal(mu=0, sigma=1):
    z0, z1 = box_muller()
    return mu + sigma * z0


# A range of orangey colours
_flame_colors = [
    "#8B0000",  # Deep Red
    "#8B0000",  # Deep Red
    "#8B0000",  # Deep Red
    "#FF4500",  # Bright Red
    "#FF4500",  # Bright Red
    "#FF4500",  # Bright Red
    "#FF8C00",  # Dark Orange
    "#FF8C00",  # Dark Orange
    "#FF8C00",  # Dark Orange
    "#FFA500",  # Bright Orange
    "#FFA500",  # Bright Orange
    "#FFA500",  # Bright Orange
    "#FFFF00",  # Yellow
    "#FFFF00",  # Yellow
    "#FFD700",  # Golden Yellow
    "#FFD700",  # Golden Yellow
    "#FFFAF0",  # Pale Yellow
    "#ADD8E6",  # Light Blue
    "#0000FF",  # Bright Blue
    "#00008B"   # Deep Blue
]

class Flame(PicoAnimation):

    def __init__(
        self, 
        pixels, 
        color="#001", 
        start_height=0, 
        min_height=0.1, 
        max_height=0.5, 
        brightness=1.0,
        flicker=0.09,
    ):
        super(Flame, self).__init__(pixels)
    
        self.color = color = to_color(color)
        self.my_height = start_height
        self.max_height = min(len(self.pixel_object) - 1, max_height * len(self.pixel_object))
        self.min_height = max(0, min_height * len(self.pixel_object))
        self.flicker = float(flicker)

        self.flame_colors = [to_color(c) for c in _flame_colors]
        if brightness < 1:
            self.flame_colors = [adjust_brightness(color, brightness) for color in self.flame_colors]

    @classmethod
    def create_animation(cls, *args, **kwargs):
       return cls(*args, **kwargs)

    def draw(self):
        self.my_height += normal(0, 1)
        self.my_height = min(self.max_height, self.my_height)
        self.my_height = max(self.min_height, self.my_height)

        my_height = int(self.my_height)
        for i in range(my_height):
            if random.random() < self.flicker:
                self.pixel_object[i] = random.choice(self.flame_colors)
        for i in range(my_height, len(self.pixel_object)):
            self.pixel_object[i] = self.color

