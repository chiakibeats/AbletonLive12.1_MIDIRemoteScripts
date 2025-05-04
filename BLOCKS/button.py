# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\BLOCKS\button.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import in_range
from ableton.v2.control_surface.elements import ButtonElement as ButtonElementBase

class ButtonElement(ButtonElementBase):

    def set_light(self, value):
        if isinstance(value, int) and in_range(value, 0, 128):
            self.send_value(value)
            return
        else:
            super(ButtonElement, self).set_light(value)