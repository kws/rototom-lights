import time
from ..helpers import PicoAnimation
from ...easing import SineEaseOut
from ...colors import to_color, to_hex
import random

class _Star:

    def __init__(self, pixel_object, color, transition, duration):
        self._start = time.monotonic()
        self.pixel_object = pixel_object
        self.position = random.randint(0, len(pixel_object)-1)
        self.color = to_color(color or "random")
        self.transition = transition
        self.duration = duration

    def draw(self):
        elapsed = time.monotonic() - self._start
        brightness = self.transition(elapsed)
        self.pixel_object[self.position] = (
            self.color[0] * brightness,
            self.color[1] * brightness,
            self.color[2] * brightness,
        )
        return elapsed <= self.duration


class Twinkle(PicoAnimation):

    def __init__(self, pixel_object, color="random", brightness = 0.05, twinkle_color = None, duration=2, probability=2):
        super().__init__(pixel_object)
        self.__start = self.__last = 0

        self.color = to_color(color)
        self.color = (
            int(self.color[0] * brightness),
            int(self.color[1] * brightness),
            int(self.color[2] * brightness),
        )

        self.twinkle_color = twinkle_color
        self.propability = probability
        self.duration = duration
        self.transition = SineEaseOut(start=1, end=0, duration=duration)
        self.comets = []


    def draw(self):
        if self.__start == 0:
            self.__start = self.__last = time.monotonic()
        elapsed = time.monotonic() - self.__last
        self.__last = time.monotonic()

        self.pixel_object.fill(self.color)

        spawn = random.random() < (self.propability * elapsed)
        if spawn:
            self.comets.append(_Star(
                self.pixel_object, 
                transition=self.transition,
                duration=self.duration,
                color=self.twinkle_color
            ))

        next_comets = []
        for comet in self.comets:
            if comet.draw():
                next_comets.append(comet)
        self.comets = next_comets


    def __str__(self) -> str:
        print(self.color)
        try:
            str = f"twinkle color={to_hex(self.color)} twinkle_color={to_hex(self.twinkle_color)} duration={self.duration} probability={self.propability}"
        except:
            str = "twinkle"
        return str
        
