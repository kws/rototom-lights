import traceback
from picolights.colors import to_color
from picolights.devices.controller import PropertyManager
from adafruit_logging import getLogger

logger = getLogger(__name__)


class PixelBufferController:
    """
    A controller for a pixel buffer. This is a base class for all pixel devices. It adds 
    common 'remote-control' properties to the buffer allowing it to be controlled via a messaging channel.
    """

    def __init__(self, pixels, controller=None, animation=None, on_animation=None, off_animation=None) -> None:
        self.pixels = pixels
        self.__pixels_show = pixels.show
        self.pixels.show = self.__show

        self._on_animation = on_animation
        self._off_animation = off_animation
        self.controller = controller
        self._animation = None

        self.property_manager = PropertyManager(self,  ["animation", "brightness", "color", "switch"])

        if animation:
            self.animation = animation

    def __show(self):
        self.__pixels_show()
        self.property_manager.update("switch")

    @property
    def animation(self):
        return self._animation
    
    @animation.setter
    def animation(self, value):
        from picolights.effects.registry import create_animation
        if isinstance(value, str):
            value = create_animation(self.pixels, value)
            if hasattr(value, "controller"):
                value.controller = self.controller
        self._animation = value
        if self._animation:
            self._animation.add_cycle_complete_receiver(self._animation_complete)
        self.property_manager.update("animation", "animation_name")

    @property
    def brightness(self):
        return self.pixels.brightness * 100
    
    @brightness.setter
    def brightness(self, message):
        message = float(message)
        self.pixels.brightness = message / 100
        self.pixels.show()
        self.property_manager.update("brightness", "switch")

    @property
    def color(self):
        return ",".join([str(v) for v in self.average])
    
    @color.setter
    def color(self, message):
        color = to_color(message)
        self.animation = None
        self.pixels.fill(color)
        self.pixels.show()
        self.property_manager.update("animation", "color", "switch")
        
    @property
    def switch(self):
        return  "ON" if sum(self.first_on) else "OFF"
    
    @switch.setter
    def switch(self, value):
        if not isinstance(value, bool):
            value = str(value).lower() in ("on", "true", "1")
        self.turn_on() if value else self.turn_off()
        self.property_manager.update("animation", "color", "switch")

    def turn_on(self):
        if self.pixels.brightness == 0:
            self.pixels.brightness = 1
        if self._on_animation:
            self.animation = self._on_animation
        else:
            self.pixels.fill(0xFFFFFF)
            self.pixels.show()

    def turn_off(self):
        if self._off_animation:
            self.animation = self._off_animation
        else:
            self.pixels.fill(0)
            self.pixels.show()
    
    def _animation_complete(self, *args, **kwargs):
        logger.info("Animation complete")
        if hasattr(self.animation, "next"):
            if callable(self.animation.next):
                self.animation = self.animation.next()
            else:
                self.animation = self.animation.next
        else:
            self.animation = None

    @property
    def average(self):
        step = self.pixels.bpp
        length = len(self.pixels)
        sums = [0] * step

        for byte_part in range(0, step):
            sums[byte_part] = sum([pixel[byte_part] for pixel in self.pixels]) // length
        
        return sums
   
    @property
    def first_on(self):
        for pixel in self.pixels:
            if sum(pixel):
                return pixel
        return []
        

    def loop(self):
        if self.animation is not None:
            try:
                self.animation.animate()
            except Exception as e:
                logger.error("Animation error: %s", e)
                traceback.print_exception(e)
                self.animation = None



