# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\sysex_element.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v2.control_surface.elements import SysexElement

class IdentifyingSysexElement(SysexElement):

    def receive_value(self, _):
        value = self._msg_sysex_identifier[3]
        self.notify_value(value)