# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Code_Series\skin_default.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import Color

class Colors(object):

    class DefaultButton(object):
        On = Color(127)
        Off = Color(0)
        Disabled = Color(0)

    class Transport(object):
        PlayOn = Color(127)
        PlayOff = Color(0)

    class Mixer(object):
        MuteOff = Color(127)
        MuteOn = Color(0)
        SoloOn = Color(127)
        SoloOff = Color(0)
        ArmOn = Color(127)
        ArmOff = Color(0)

def make_default_skin():
    return Skin(Colors)