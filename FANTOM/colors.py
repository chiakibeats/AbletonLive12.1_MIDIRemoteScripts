# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\FANTOM\colors.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.elements import SimpleColor

class Basic:
    OFF = SimpleColor(0)
    ON = SimpleColor(1)
    DISABLED = SimpleColor(2)

class Rgb:
    YELLOW = SimpleColor(3)
    LIGHT_BLUE = SimpleColor(6)
    RED = SimpleColor(13)
    ORANGE = SimpleColor(14)
    GREEN = SimpleColor(4)
    DARK_BLUE = SimpleColor(63)
STOPPED = SimpleColor(4)
TRIGGERED_PLAY = SimpleColor(7)

class Skin:

    class DefaultButton:
        Disabled = Basic.DISABLED

    class Session:
        SlotRecordButton = SimpleColor(2)
        SlotLacksStop = SimpleColor(5)
        SlotTriggeredPlay = SimpleColor(1)
        SlotTriggeredRecord = SimpleColor(3)
        ClipStopped = STOPPED
        ClipTriggeredPlay = TRIGGERED_PLAY
        ClipTriggeredRecord = SimpleColor(9)
        ClipPlaying = SimpleColor(6)
        ClipRecording = SimpleColor(8)
        Scene = STOPPED
        SceneTriggered = TRIGGERED_PLAY

    class DrumGroup:
        PadFilled = Rgb.YELLOW
        PadSelected = Rgb.LIGHT_BLUE
        PadMuted = Rgb.ORANGE
        PadMutedSelected = Rgb.LIGHT_BLUE
        PadSoloed = Rgb.DARK_BLUE
        PadSoloedSelected = Rgb.LIGHT_BLUE