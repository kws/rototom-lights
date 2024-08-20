import os
import time
from colorsys import hsv_to_rgb

import rtc
import socketpool
import wifi

import adafruit_ntp

time_set = False

PURPLE = (255,0,255)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (5, 0, 0)
BLACK = 0

def hsv_to_rgb_transition(fraction):
    # Ensure fraction is within the valid range
    if fraction < 0:
        fraction = 0
    elif fraction > 0.75:
        fraction = 0.75
    
    # Calculate Hue based on the fraction
    if fraction <= 0.375:
        # Green to Yellow transition (0 to 0.375)
        H = (1/3) - (2/3) * (fraction / 0.375)
    else:
        # Yellow to Red transition (0.375 to 0.75)
        H = (1/6) - (1/6) * ((fraction - 0.375) / 0.375)
    
    S = 1.0  # Full saturation
    V = 1.0  # Full value (brightness)
    
    # Convert HSV to RGB using the colorsys module
    return hsv_to_rgb(H, S, V)

def set_time():
    global time_set
    pool = socketpool.SocketPool(wifi.radio)
    ntp = adafruit_ntp.NTP(pool, tz_offset=0, cache_seconds=86400)
    rtc.RTC().datetime = ntp.datetime
    time_set = True

def do_clock(pixels, pixels_per_segment):
    pixels.fill(BLACK)
    tm_year, tm_mon, tm_mday, tm_hour, tm_min, tm_sec, tm_wday, tm_yday, tm_isdst = time.localtime()
    fraction = tm_min / 60
    if tm_min < 45:
        fract_45 = min(tm_min / 45, 1)
        color =  hsv_to_rgb(0.33*(1-fract_45), 1, 1)
    else:
        color = RED if tm_sec % 2 >= 1 else DARK_RED
    
    to_fill = int(len(pixels) * fraction)
    for i in range(0, to_fill):
        pixels[i] = color

    if tm_sec % 2 < 1:
        pixels[0] = WHITE
        pixels[pixels_per_segment] = WHITE
        pixels[pixels_per_segment*2] = WHITE
        pixels[pixels_per_segment*3] = WHITE
        pixels[pixels_per_segment*4] = WHITE

def run(pixels):
    numpixels = len(pixels)
    pixels_per_segment = numpixels // 4

    while True:
        if time_set:
            do_clock(pixels, pixels_per_segment)
        else:
            pixels.fill(PURPLE if time.monotonic() % 2 < 1 else 0)
            set_time()
        pixels.show()

