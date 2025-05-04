# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK2\Skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.Skin import Skin
from .Colors import Rgb

class Colors(object):

    class Session(object):
        SceneTriggered = Rgb.GREEN_BLINK
        NoScene = Rgb.BLACK
        ClipStarted = Rgb.GREEN_PULSE
        ClipRecording = Rgb.RED_PULSE
        ClipTriggeredPlay = Rgb.GREEN_BLINK
        ClipTriggeredRecord = Rgb.RED_BLINK
        ClipEmpty = Rgb.BLACK
        RecordButton = Rgb.RED_HALF
        StopClip = Rgb.GREEN
        StopClipTriggered = Rgb.GREEN_BLINK
        StoppedClip = Rgb.GREEN_HALF
        Enabled = Rgb.YELLOW

    class Mode(object):
        DeviceMode = Rgb.PURPLE_HALF
        DeviceModeOn = Rgb.PURPLE
        PanMode = Rgb.ORANGE_HALF
        PanModeOn = Rgb.ORANGE
        Send0Mode = Rgb.DARK_BLUE_HALF
        Send0ModeOn = Rgb.BRIGHT_PURPLE
        Send1Mode = Rgb.BLUE_HALF
        Send1ModeOn = Rgb.BLUE
        Send2Mode = Rgb.LIGHT_BLUE_HALF
        Send2ModeOn = Rgb.LIGHT_BLUE
        Send3Mode = Rgb.MINT_HALF
        Send3ModeOn = Rgb.MINT
        Send4Mode = Rgb.DARK_YELLOW_HALF
        Send4ModeOn = Rgb.DARK_YELLOW
        Send5Mode = Rgb.YELLOW_HALF
        Send5ModeOn = Rgb.YELLOW
        Disabled = Rgb.BLACK

    class Device(object):
        Bank = Rgb.DARK_PURPLE
        BestOfBank = Rgb.PURPLE_HALF
        BankSelected = Rgb.PURPLE

def make_skin():
    return Skin(Colors)