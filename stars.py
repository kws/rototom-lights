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

def run(pixels):
    numpixels = len(pixels)

    while True:
        for p in range(start_pixel, numpixels):
            pix = pixels[p]
            if sum(pix) > 0:
                pixels[p] = [max(0, pix[i] - dim_factor) for i in range(3)]


        if random.random() < rand_factor:
            p = random.randint(start_pixel, numpixels-1)
            pixels[p] = get_color()

        pixels[0] = (0,0,0) if time.monotonic() % 2 < 1 else my_color

        pixels.show()

