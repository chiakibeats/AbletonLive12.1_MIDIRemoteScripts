# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AIRA_MX_1\SkinDefault.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:24:29 UTC (1744269869)

from _Framework.Skin import Skin
from .Colors import Rgb

class Colors:

    class Session:
        ClipEmpty = Rgb.BLACK
        ClipStopped = Rgb.GREEN_HALF
        ClipStarted = Rgb.GREEN
        ClipRecording = Rgb.RED
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        NoScene = Rgb.BLACK
        Scene = Rgb.BLUE_HALF
        SceneTriggered = Rgb.BLUE_BLINK
        ScenePlaying = Rgb.BLUE
        StopClip = Rgb.RED
        StopClipTriggered = Rgb.RED_BLINK

def make_default_skin():
    return Skin(Colors)