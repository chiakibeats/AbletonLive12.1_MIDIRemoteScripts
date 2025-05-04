# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_3\sysex.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.elements import SysexElement as SysexElementBase
from .midi import COMMAND_ID_TO_DAW_PROGRAM_ID

class SysexElement(SysexElementBase):
    pass

    def receive_value(self, value):
        if len(value) == 2 and value[0] in COMMAND_ID_TO_DAW_PROGRAM_ID:
            super().receive_value(int(value[1] == COMMAND_ID_TO_DAW_PROGRAM_ID[value[0]]))