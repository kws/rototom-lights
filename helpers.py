class CombinedPixels:

    def __init__(self, *pixels):
        assert len(pixels) > 0
        self._pixels = pixels

    def __len__(self):
        return len(self._pixels[0])
    
    def fill(self, *args, **kwargs):
        for p in self._pixels:
            p.fill(*args, **kwargs)

    def show(self):
        for p in self._pixels:
            p.show()

    def __getitem__(self, key):
        return self._pixels[0][key]

    def __setitem__(self, key, value):
        for p in self._pixels:
            p[key] = value

    def deinit(self):
        for p in self._pixels:
            p.deinit()