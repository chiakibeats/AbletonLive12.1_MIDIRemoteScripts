# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC_Key_25_mk2\colors.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v3.base import memoize
from ableton.v3.control_surface import STANDARD_COLOR_PALETTE, STANDARD_FALLBACK_COLOR_TABLE
from ableton.v3.control_surface.elements import SimpleColor
from ableton.v3.live import liveobj_color_to_value_from_palette
HALF_BRIGHTNESS_CHANNEL = 1
FULL_BRIGHTNESS_CHANNEL = 6
PULSE_CHANNEL = 10
BLINK_CHANNEL = 14

@memoize
def make_simple_color(value):
    return SimpleColor(value)

def make_color_for_liveobj(obj):
    return make_simple_color(liveobj_color_to_value_from_palette(obj, palette=STANDARD_COLOR_PALETTE, fallback_table=STANDARD_FALLBACK_COLOR_TABLE))

class Basic:
    ON = make_simple_color(1)
    BLINK = make_simple_color(2)

class Rgb:
    BLACK = make_simple_color(0)
    RED = make_simple_color(5)
    RED_BLINK = SimpleColor(5, channel=BLINK_CHANNEL)
    RED_PULSE = SimpleColor(5, channel=PULSE_CHANNEL)
    RED_HALF = SimpleColor(5, channel=HALF_BRIGHTNESS_CHANNEL)
    GREEN = make_simple_color(21)
    GREEN_BLINK = SimpleColor(21, channel=BLINK_CHANNEL)
    GREEN_PULSE = SimpleColor(21, channel=PULSE_CHANNEL)

class Skin:

    class Session:
        SlotRecordButton = Rgb.RED_HALF
        ClipStopped = make_color_for_liveobj
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipPlaying = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        SceneTriggered = Basic.BLINK
        StopClipTriggered = Basic.BLINK
        StopClip = Basic.ON