# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro_MK3\skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import Skin, merge_skins
from novation.colors import Rgb
from novation.skin import skin as base_skin

class Colors(object):

    class Device(object):
        Navigation = Rgb.DARK_BLUE_HALF
        NavigationPressed = Rgb.WHITE

    class Mode(object):

        class Device(object):
            On = Rgb.DARK_BLUE
            Off = Rgb.WHITE_HALF

            class Bank(object):
                Selected = Rgb.DARK_BLUE
                Available = Rgb.WHITE_HALF

        class Sends(object):
            On = Rgb.VIOLET
            Off = Rgb.WHITE_HALF

            class Bank(object):
                Available = Rgb.WHITE_HALF

    class Recording(object):
        Off = Rgb.WHITE_HALF

    class Transport(object):
        PlayOff = Rgb.WHITE_HALF
        PlayOn = Rgb.GREEN
        ContinueOff = Rgb.AQUA
        ContinueOn = Rgb.RED_HALF
        CaptureOff = Rgb.BLACK
        CaptureOn = Rgb.CREAM
        TapTempo = Rgb.CREAM

    class Quantization(object):
        Off = Rgb.RED_HALF
        On = Rgb.AQUA
skin = merge_skins(*(base_skin, Skin(Colors)))