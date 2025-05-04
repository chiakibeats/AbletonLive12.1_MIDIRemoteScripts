# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Blackstar_Live_Logic\skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import Skin
from ableton.v2.control_surface.elements import Color
LED_ON = Color(127)
LED_OFF = Color(0)

class Colors:

    class DefaultButton:
        On = LED_ON
        Off = LED_OFF
        Disabled = LED_OFF
skin = Skin(Colors)