# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\BLOCKS\skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import Color
from .colors import Rgb

class Colors(object):

    class DefaultButton(object):
        On = Rgb.WHITE
        Off = Rgb.BLACK
        Disabled = Rgb.BLACK

    class Session(object):
        RecordButton = Rgb.RED
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipStopped = Rgb.AMBER
        Scene = Rgb.GREEN
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        StopClipTriggered = Rgb.RED_PULSE
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.BLACK
        ClipEmpty = Rgb.BLACK

    class DrumGroup(object):
        PadEmpty = Rgb.BLACK
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.LIGHT_BLUE
        PadSelectedNotSoloed = Rgb.LIGHT_BLUE
        PadMuted = Rgb.DARK_ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.DARK_BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE
        PadInvisible = Rgb.BLACK
        PadAction = Rgb.RED
skin = Skin(Colors)