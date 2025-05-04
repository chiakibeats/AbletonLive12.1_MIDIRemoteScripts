# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\physical_display.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from itertools import chain, starmap
from ableton.v2.base import clamp, group
from ableton.v2.control_surface.elements import PhysicalDisplayElement as PhysicalDisplayElementBase

def message_length(message):
    length = len(message)
    return (clamp(length // 128, 0, 127), length % 128)

class PhysicalDisplayElement(PhysicalDisplayElementBase):

    def _build_display_message(self, display):
        message_string = display.display_string.strip()
        return chain(message_length(message_string), self._translate_string(message_string))