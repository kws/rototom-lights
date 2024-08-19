from adafruit_led_animation.color import BLACK, RED, GREEN, BLUE
from ..helpers import PicoAnimation

class Ident(PicoAnimation):

    def __init__(self, pixels, step=10):
        super(Ident, self).__init__(pixels)
        self.step = int(step)

    def draw(self):
        pixel_len = len(self.pixel_object)
        self.pixel_object.fill(BLACK)

        for i in range(0, pixel_len, self.step):
            self.pixel_object[i] = BLUE

        for i in range(0, pixel_len, self.step*5):
            self.pixel_object[i] = GREEN

        for i in range(0, pixel_len, self.step*10):
            self.pixel_object[i] = RED


