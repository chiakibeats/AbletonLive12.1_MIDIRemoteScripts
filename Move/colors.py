# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\colors.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from colorsys import hsv_to_rgb, rgb_to_hsv
from enum import IntEnum
from functools import partial
from ableton.v3.base import hex_to_rgb
from ableton.v3.control_surface.elements import ColorPart, ComplexColor, FallbackColor, SimpleColor
from ableton.v3.live import liveobj_valid
from .step_button import ColorWithAnimatedIcon, ColorWithSimpleIcon
TRANSLATED_WHITE_INDEX = 7
WHITE_RGB_VALUE = 122
DARK_GREY_RGB_VALUE = 124
DARK_GREY_MONO_VALUE = 16
PULSE_BASE_CHANNEL = 6
BLINK_BASE_CHANNEL = 11

class AnimationSpeed(IntEnum):
    pass
    quarter = 3
    half = 4

def make_animated_color(primary_color, secondary_color, speed=AnimationSpeed.quarter, base_channel=0):
    pass
    return ComplexColor((ColorPart(secondary_color.midi_value), ColorPart(primary_color.midi_value, channel=speed + base_channel)))
make_pulsing_color = partial(make_animated_color, base_channel=PULSE_BASE_CHANNEL)
make_blinking_color = partial(make_animated_color, base_channel=BLINK_BASE_CHANNEL)

def make_color_for_liveobj(obj):
    return SimpleColor(translate_color_index(obj))

def make_dimmed_color_for_liveobj(obj, shade_level=2):
    return SimpleColor(determine_shaded_color_index(translate_color_index(obj), shade_level))

def make_pulsing_color_for_liveobj(obj):
    return make_pulsing_color(make_color_for_liveobj(obj), make_dimmed_color_for_liveobj(obj))

def translate_color_index(obj):
    pass
    if liveobj_valid(obj) and obj.color_index in range(len(COLOR_INDEX_TO_MOVE_INDEX)):
        return COLOR_INDEX_TO_MOVE_INDEX[obj.color_index]
    else:  # inserted
        return TRANSLATED_WHITE_INDEX

def determine_shaded_color_index(color_index, shade_level):
    pass
    if color_index == WHITE_RGB_VALUE:
        return color_index + shade_level
    else:  # inserted
        return (color_index - 1) * 2 + 64 + shade_level

def hex_to_hsv(hex_value):
    pass
    return rgb_to_hsv(*tuple((c / 255.0 for c in hex_to_rgb(hex_value))))

def adjust_hsv_brightness(h, s, v, amount):
    pass
    return (int(v * 255.0) for v in hsv_to_rgb(h, s, v * amount))

def rgb_to_move(r, g, b):
    pass
    return (r & 127, r >> 7 & 1, g & 127, g >> 7 & 1, b & 127, b >> 7 & 1)

class Colors:
    OFF = SimpleColor(0)
    WHITE = SimpleColor(WHITE_RGB_VALUE)
    WHITE_PULSE_HALF = make_pulsing_color(WHITE, SimpleColor(DARK_GREY_MONO_VALUE), speed=AnimationSpeed.half)
    LIGHT_GREY = SimpleColor(123)
    DARK_GREY = FallbackColor(SimpleColor(DARK_GREY_RGB_VALUE), SimpleColor(DARK_GREY_MONO_VALUE))
    GREEN = SimpleColor(126)
    GREEN_BLINK_QUARTER = make_blinking_color(OFF, GREEN)
    RED = SimpleColor(127)
    RED_SHADE = SimpleColor(27)
    RED_BLINK_QUARTER = make_blinking_color(OFF, RED)
    BLUE = SimpleColor(125)
    WHITE_WITH_ICON = ColorWithSimpleIcon(WHITE_RGB_VALUE)
    WHITE_WITH_ICON_PULSE_HALF = ColorWithAnimatedIcon((ColorPart(DARK_GREY_MONO_VALUE), ColorPart(WHITE_RGB_VALUE, channel=AnimationSpeed.half + PULSE_BASE_CHANNEL)))
    DARK_GREY_WITH_ICON = ColorWithSimpleIcon(DARK_GREY_RGB_VALUE)
COLOR_INDEX_TO_MOVE_INDEX = (1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 7, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 5, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 22, 25, 17, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 21, 2, 4, 6, 8, 10, 12, 14, 20, 19, 18, 22, 23, 26, 6)
for 7995160 in ((0, 0, 0), (1, 16728114, 2), (2, 8389632, 4), (3, 13188096, 6), (4, 11280128, 8), (5, 9195544, 10), (6, 4790276, 12), (7, 16440379, 14), (8, 16762134, 16), (9, 11992846, 18), (10, 7995160, 20), (11, 3457558, 22), (5212676, 24, 13), (24, 6487893, 26), (2719059, 28, 15), (2530930, 30, 3255807), (32, 17, 3564540), (34, 1717503, 36), (19, 1838310, 38), (1391001, 40, 21), (3749887, 42, 5710591), (44, 23, 9907199), (46, 8724856, 48),