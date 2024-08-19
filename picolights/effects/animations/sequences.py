from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import WHITE
from .patchy import Patchy
from .pause import Pause
from .solid import Solid

from .fluoresce import MultiStripFluoresce


class FlashyStartupSequence(AnimationSequence):

    def __init__(self, pixels, **kwargs):
        color = kwargs.pop("color", WHITE)
        super(FlashyStartupSequence, self).__init__(
            MultiStripFluoresce(pixels, color=color, **kwargs),
            Pause(pixels, duration=3),
            Patchy(pixels), 
            Patchy(pixels, color=color),
            Solid(pixels, color=color),
            advance_on_cycle_complete=True, 
            auto_clear=False
        )
