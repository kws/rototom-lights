from ..helpers import PicoAnimation


class Clone(PicoAnimation):

    def __init__(self, pixel_object, source, offset=0, **kwargs):
        super().__init__(pixel_object)
        self.source = source
        self.offset = int(offset)
        self.controller = None
        self._source_pixels = None
        

    def draw(self):
        if self._source_pixels is None:
            self._source_pixels = self.controller[self.source].pixels

        max_pixel = min(len(self.pixel_object), len(self._source_pixels)-self.offset)
        for i in range(max_pixel):
            self.pixel_object[i] = self._source_pixels[i+self.offset]
