import board
import neopixel
import random
import time
from rainbowio import colorwheel
import os

numpixels=int(os.getenv('NUM_PIXELS', "300"))
run_mode = os.getenv("RUN_MODE", "stars")

try:
    pixels = neopixel.NeoPixel(board.GP0, numpixels, brightness=1, auto_write=False)
    pixels2 = neopixel.NeoPixel(board.GP1, numpixels, brightness=1, auto_write=False)

    if run_mode == "clock":
        from clock import run
        run(pixels, pixels2)
    else:
        from stars import run
        run(pixels)


finally:
    pixels.deinit()
    pixels2.deinit()