import os
import random
import time

colors = [
    (255,0,0),
    (0,255,0),
    (255,100,0),
]

whites = [
    (255, 255, 255),
]

stars = [
    (255, 255, 255),
    (200, 255, 255),
    (255, 200, 255),
    (255, 255, 200),
]

color_mode = os.getenv('COLOR_MODE', "stars")
my_color = os.getenv("MY_COLOR", "255,255,255")
my_color = tuple(int(x) for x in my_color.split(","))
start_pixel = 10

def get_color():
    if color_mode.lower().startswith('c'):
        c = colors
    elif color_mode.lower().startswith('w'):
        c = whites
    else:
        c = stars
    return random.choice(c)


dim_factor = int(os.getenv('DIM_FACTOR', "3"))
rand_factor = float(os.getenv('RAND_FACTOR', "0.35"))

class Meteor:

    def __init__(self, pixels):
        self.pixels = pixels
        self.start_time = time.monotonic()

        self.pos = random.randint(start_pixel, len(self.pixels))

        self.velocity = 10 * random.choice([1, -1])
        self.lifespan = 0.5 + random.random()
        self.length = random.randint(5, 10)

        self.age = 0
        self.range = []

    def capture(self):
        self.age = time.monotonic() - self.start_time
        self.pos = int(self.pos + (self.velocity * self.age))
        self.range = [self.pos + i for i in range(10)]
        self.range = [i for i in self.range if start_pixel < i < len(self.pixels)]

        self.memory = [self.pixels[p] for p in self.range]        


    def reset(self):
        for ix, i in enumerate(self.range):
            self.pixels[i] = self.memory[ix]

    def update(self):
         for ix, i in enumerate(self.range):
            ix = (ix + 1) * (1 if self.velocity < 0 else -1)
            brightness = 255 - (25 * ix)
            self.pixels[i] = (brightness, brightness, brightness)

    @property
    def complete(self):
        return self.age > self.lifespan


class Meteors:

    def __init__(self, pixels):
        self.pixels = pixels
        self.meteors = []
        self.data = None

    def reset(self):
        for m in self.meteors:
            m.reset()

        self.meteors = [m for m in self.meteors if not m.complete]

    def update(self):
        if random.random() > 0.99:
            self.meteors.append(Meteor(self.pixels))

        for m in self.meteors:
            m.capture()

        for m in self.meteors:
            m.update()




def run(pixels):
    numpixels = len(pixels)
    meteors = Meteors(pixels)

    while True:

        meteors.reset()
        
        for p in range(start_pixel, numpixels):
            pix = pixels[p]
            if sum(pix) > 0:
                pixels[p] = [max(0, pix[i] - dim_factor) for i in range(3)]


        if random.random() < rand_factor:
            p = random.randint(start_pixel, numpixels-1)
            pixels[p] = get_color()

        meteors.update()

        pixels[0] = (0,0,0) if time.monotonic() % 2 < 1 else my_color

        pixels.show()

