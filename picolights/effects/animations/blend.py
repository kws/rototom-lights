from picolights.colors import rgb_to_hsv, hsv_to_rgb, to_color
from ..helpers import TimedAnimation
_fraq = 360 / 6


class Blend(TimedAnimation):

    def __init__(self, pixels, color="random", **kwargs):
        super(Blend, self).__init__(pixels, **kwargs)

        self.color = color = to_color(color)
        h, s, v = rgb_to_hsv(*color)
        self._start_col = hsv_to_rgb(h - _fraq, s, v)
        self._end_col = hsv_to_rgb(h + _fraq, s, v)

        self.length = len(self.pixel_object)
        self.__half_point = self.length / 2

    def draw(self):
        if self.cycle_count >= 1:
            self.pixel_object.fill(self.color)
            return
    
        cur_pix = self.progress * self.length
        for i in range(self.length):
            if cur_pix < self.__half_point:
                if i < cur_pix:
                    self.pixel_object[i] = self._start_col
                elif i > (self.length - cur_pix):
                    self.pixel_object[i] = self._end_col
            else:
                if i < cur_pix and i > (self.length - cur_pix):
                    self.pixel_object[i] = self.color
                


