# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\mode.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.control import InputControl
from ableton.v2.control_surface.mode import ModesComponent as ModesComponentBase

class ModesComponent(ModesComponentBase):
    __events__ = ('mode_byte',)
    mode_selection_control = InputControl()

    @mode_selection_control.value
    def mode_selection_control(self, value, _):
        modes = self.modes
        if value < len(modes):
            self.selected_mode = modes[value]
            self.notify_mode_byte(value)