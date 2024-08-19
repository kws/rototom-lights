
class Color:

    def __init__(self, value) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"Color({self.value})"


class PixelWrapper:

    def __init__(self, pixels) -> None:
        self.pixels = pixels

    def __setitem__(self, key, value):
        if isinstance(value, Color):
            value = value.value
        elif isinstance(value, (tuple, list)):
            value =[v.value if isinstance(v, Color) else v for v in value]

        self.pixels[key] = value

    def __getattr__(self, name):
        return getattr(self.pixels, name)
    
    def __getitem__(self, name):
        return self.pixels[name]
    
    def __len__(self):
        return len(self.pixels)
            