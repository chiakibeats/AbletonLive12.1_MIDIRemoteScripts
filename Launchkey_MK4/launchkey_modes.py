# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\launchkey_modes.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.mode import ModesComponent

class LaunchkeyModesComponent(ModesComponent):
    pass

    def _handle_mode_selection_control_value(self, value):
        if not self.is_enabled() or value < len(self.modes):
            self.previous_mode = self.selected_mode
            mode = self.modes[value]
            self._get_mode_behaviour(mode).press_immediate(self, mode)