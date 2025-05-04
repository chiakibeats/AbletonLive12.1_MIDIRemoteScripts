# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from functools import partial
from .colors import Rgb, create_color_for_liveobj

class Skin:

    class DefaultButton:
        On = Rgb.ON
        Off = Rgb.OFF
        Disabled = Rgb.OFF

    class Transport:
        PlayOn = Rgb.GREEN
        PlayOff = Rgb.GREEN_DIM
        LoopOn = Rgb.GREEN
        LoopOff = Rgb.GREEN_DIM

    class Mixer:
        Selected = Rgb.ON
        NotSelected = Rgb.OFF

    class Session:
        Slot = Rgb.OFF
        SlotRecordButton = Rgb.RED_HALF
        NoSlot = Rgb.OFF
        ClipStopped = create_color_for_liveobj
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipPlaying = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        Scene = partial(create_color_for_liveobj, is_scene=True)
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.OFF
        StopClipTriggered = Rgb.RED_BLINK
        StopClip = Rgb.RED
        StopClipDisabled = Rgb.RED_HALF

    class ViewToggle:
        DetailOn = Rgb.YELLOW
        DetailOff = Rgb.YELLOW_HALF
        SessionOn = Rgb.BLUE
        SessionOff = Rgb.BLUE_HALF
        ClipOn = Rgb.PURPLE
        ClipOff = Rgb.PURPLE_HALF
        BrowserOn = Rgb.GREEN
        BrowserOff = Rgb.GREEN_HALF

    class LowerPadModes:

        class Select:
            On = Rgb.RED_HALF

        class Stop:
            On = Rgb.RED