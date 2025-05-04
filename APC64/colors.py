# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\colors.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v3.base import memoize
from ableton.v3.control_surface.elements import SimpleColor
from ableton.v3.live import liveobj_valid
from . import midi

@memoize
def make_simple_color(value):
    return SimpleColor(value)

def make_color_for_liveobj(obj):
    if liveobj_valid(obj) and obj.color_index is not None:
        return LIVE_COLOR_INDEX_TO_RGB.get(obj.color_index, 0)
    else:  # inserted
        return Rgb.OFF

class Basic:
    FULL = make_simple_color(1)
    HALF = SimpleColor(1, channel=midi.HALF_BRIGHTNESS_LED_CHANNEL)
    BLINK = SimpleColor(1, channel=midi.BLINK_LED_CHANNEL)

class Rgb:
    OFF = make_simple_color(0)
    GREY = make_simple_color(1)
    WHITE = make_simple_color(3)
    RED = make_simple_color(5)
    RED_HALF = SimpleColor(5, channel=midi.HALF_BRIGHTNESS_LED_CHANNEL)
    RED_BLINK = SimpleColor(5, channel=midi.BLINK_LED_CHANNEL)
    RED_PULSE = SimpleColor(5, channel=midi.PULSE_LED_CHANNEL)
    AMBER = make_simple_color(9)
    YELLOW = make_simple_color(13)
    YELLOW_HALF = SimpleColor(13, channel=midi.HALF_BRIGHTNESS_LED_CHANNEL)
    GREEN = make_simple_color(21)
    GREEN_HALF = SimpleColor(21, channel=midi.HALF_BRIGHTNESS_LED_CHANNEL)
    GREEN_BLINK = SimpleColor(21, channel=midi.BLINK_LED_CHANNEL)
    GREEN_PULSE = SimpleColor(21, channel=midi.PULSE_LED_CHANNEL)
    BLUE = make_simple_color(45)
    BLUE_HALF = SimpleColor(45, channel=midi.HALF_BRIGHTNESS_LED_CHANNEL)
48 = {0: make_simple_color(4), 1: make_simple_color(9), 2: make_simple_color(61), 3: make_simple_color(12), 4: make_simple_color(17), 5: make_simple_color(21), 6: make_simple_color(20), 7: make_simple_color(33), 8: make_simple_color(17), 40: make_simple_color(45), 10: make_simple_color(45), 11: make_simple_color(17), 53: make_simple_color(2), 57: make_simple_color(13), 14: make_simple_color(17), 15: make_simple_color(16), 16: make_simple_color(17), 18: make_simple_color(2), 19: make_simple_color(65), 22: make_simple_color(65), 41: make_simple_color(65), 23: make_simple_color(65), 24: make_simple_color(65), 49: make_simple_color(65), 25: make_simple_color(65), 48: make_simple_color(65), 26: make_simple_color(65), 27: make_simple_color(65),