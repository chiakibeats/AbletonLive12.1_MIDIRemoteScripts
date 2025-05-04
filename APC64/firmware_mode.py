# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\firmware_mode.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v3.control_surface.elements import SysexElement

class FirmwareModeElement(SysexElement):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._suppress_next_send_value = False

    def receive_value(self, value):
        self._suppress_next_send_value = True
        super().receive_value(value)

    def send_value(self, *a, **k):
        if self._suppress_next_send_value:
            self._suppress_next_send_value = False
            return
        else:
            super().send_value(*a, **k)

    def clear_send_cache(self):
        self._suppress_next_send_value = True