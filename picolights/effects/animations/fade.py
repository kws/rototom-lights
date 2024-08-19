from ..helpers import PicoAnimation

class Fade(PicoAnimation):

    on_cycle_complete_supported = True


    def draw(self):
        if self.pixel_object.brightness > 0:
            self.pixel_object.brightness -= 0.01
        else:
            self.cycle_complete = True

        


