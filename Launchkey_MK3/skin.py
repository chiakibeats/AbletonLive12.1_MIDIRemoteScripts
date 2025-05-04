# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import Skin, merge_skins
from novation.colors import Mono, Rgb
from novation.skin import skin as base_skin

class Colors:

    class DefaultButton:
        On = Mono.ON

    class TrackNavigation:
        On = Mono.HALF
        Pressed = Mono.ON

    class Device:
        Navigation = Rgb.PURPLE_HALF
        NavigationPressed = Rgb.PURPLE

    class DrumGroup:
        PadSelected = Rgb.WHITE
        PadSelectedNotSoloed = Rgb.WHITE
        PadMutedSelected = Rgb.WHITE
        PadSoloedSelected = Rgb.WHITE

    class Mode:

        class Device:

            class Bank:
                Selected = Rgb.PURPLE
                Available = Rgb.PURPLE_HALF
skin = merge_skins(*(base_skin, Skin(Colors)))