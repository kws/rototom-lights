import board
import neopixel
from helpers import CombinedPixels
import random
import time
from rainbowio import colorwheel
import os

numpixels=int(os.getenv('NUM_PIXELS', "300"))
run_mode = os.getenv("RUN_MODE", "stars")
pins = os.getenv("PINS", "GP0")

pixels = [neopixel.NeoPixel(getattr(board, p), numpixels, brightness=1, auto_write=False) for p in pins.split(",")]
if len(pixels) > 1:
    pixels = CombinedPixels(*pixels)
else:
    pixels = pixels[0]

try:
    if run_mode == "clock":
        from clock import run
    elif run_mode == "party":
        from party import run
    else:
        from stars import run

    run(pixels)
finally:
    pixels.deinit()
