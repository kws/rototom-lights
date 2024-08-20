import board
import neopixel
import random
import time
from rainbowio import colorwheel
import os
from picolights.effects.animations import cylon
from picolights.effects.animations import rainbow
from picolights.effects.animations import fluoresce
from picolights.effects.animations import patchy

numpixels=int(os.getenv('NUM_PIXELS', "300"))
run_mode = os.getenv("RUN_MODE", "stars")

def run(pixels):
    anim = cylon.Cylon(pixels, eye_colors="red,yellow,green")
    # anim = rainbow.Rainbow(pixels, duration=0.5, scale=2)
    # anim = fluoresce.MultiStripFluoresce(pixels)
    # anim = patchy.Patchy(pixels, duration=9999)

    while True:
        anim.animate()

