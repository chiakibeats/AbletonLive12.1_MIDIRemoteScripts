# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launch_Control_XL\SkinDefault.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ButtonElement import Color
from _Framework.Skin import Skin

class Defaults(object):

    class DefaultButton(object):
        On = Color(127)
        Off = Color(0)
        Disabled = Color(0)

class BiLedColors(object):

    class Mixer(object):
        SoloOn = Color(60)
        SoloOff = Color(28)
        MuteOn = Color(29)
        MuteOff = Color(47)
        ArmSelected = Color(15)
        ArmUnselected = Color(13)
        TrackSelected = Color(62)
        TrackUnselected = Color(29)
        NoTrack = Color(0)
        Sends = Color(47)
        Pans = Color(60)

    class Device(object):
        Parameters = Color(13)
        NoDevice = Color(0)
        BankSelected = Color(15)
        BankUnselected = Color(0)

def make_default_skin():
    return Skin(Defaults)

def make_biled_skin():
    return Skin(BiLedColors)