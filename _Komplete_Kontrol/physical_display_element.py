# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\physical_display_element.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
from ableton.v2.control_surface.elements import PhysicalDisplayElement as PhysicalDisplayElementBase

class PhysicalDisplayElement(PhysicalDisplayElementBase):

    def _build_display_message(self, display):
        return chain(*map(lambda x: self._translate_string(str(x).strip()), display._logical_segments))

    def _request_send_message(self):
        self._send_message()