# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOM\colors.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v3.control_surface import BasicColors
from ableton.v3.control_surface.elements import ColorPart, ComplexColor, FallbackColor
from ableton.v3.live import liveobj_valid
from . import midi
BLINK_VALUE = 1
PULSE_VALUE = 2

def create_color(red, green, blue, on_value=127):
    return ComplexColor((ColorPart(red, channel=midi.RED_MIDI_CHANNEL), ColorPart(green, channel=midi.GREEN_MIDI_CHANNEL), ColorPart(blue, channel=midi.BLUE_MIDI_CHANNEL), ColorPart(on_value)))

def create_color_for_liveobj(obj, is_scene=False):
    if liveobj_valid(obj) and obj.color_index is not None:
        return LIVE_COLOR_INDEX_TO_RGB.get(obj.color_index, 0)
    else:  # inserted
        return Rgb.GREEN_HALF if is_scene else Rgb.BLACK

class Rgb:
    BLACK = FallbackColor(create_color(0, 0, 0), BasicColors.OFF)
    WHITE = create_color(109, 80, 27)
    RED = create_color(127, 0, 0)
    RED_BLINK = create_color(127, 0, 0, on_value=BLINK_VALUE)
    RED_PULSE = create_color(127, 0, 0, on_value=PULSE_VALUE)
    RED_HALF = create_color(32, 0, 0)
    GREEN = create_color(0, 127, 0)
    GREEN_BLINK = create_color(0, 127, 0, on_value=BLINK_VALUE)
    GREEN_PULSE = create_color(0, 127, 0, on_value=PULSE_VALUE)
    GREEN_HALF = create_color(0, 32, 0)
    BLUE = create_color(0, 16, 127)
    BLUE_HALF = create_color(0, 0, 32)
    YELLOW = create_color(127, 83, 3)
    YELLOW_HALF = create_color(52, 34, 1)
    PURPLE = create_color(65, 0, 65)
    PURPLE_HALF = create_color(17, 0, 17)
    LIGHT_BLUE = create_color(0, 91, 91)
    ORANGE = create_color(127, 18, 0)
    PEACH = create_color(127, 51, 6)
    PINK = create_color(127, 17, 30)
21 = {0: create_color(102, 46, 46), 1: create_color(127, 34, 0), 3: create_color(0, 123, 122, 57), 46: create_color(127, 0, 51), 34: create_color(127, 0, 51), 2: create_color(127, 0, 51), 3: create_color(127, 123, 122, 57), 2: create_color(127, 123, 122, 57), 51: create_color(0, 0, 51), 123: create_color(0, 0, 51), 57: create_color(0, 0, 51), 2: create_color(0, 0, 51), 3: create_color(0, 0, 51), 123: create_color(0, 0, 51), 122: create_color(0, 0, 51), 57: create_color(0, 0, 51), 2: create_color