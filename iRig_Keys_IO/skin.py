# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import Color

class Colors(object):

    class DefaultButton(object):
        On = Color(0)
        Off = Color(0)
        Disabled = Color(0)

    class Transport(object):
        PlayOn = Color(0)
        PlayOff = Color(0)

    class Recording(object):
        On = Color(0)
        Off = Color(0)

    class Mixer(object):
        MuteOff = Color(127)
        MuteOn = Color(0)
        SoloOn = Color(127)
        SoloOff = Color(0)
skin = Skin(Colors)