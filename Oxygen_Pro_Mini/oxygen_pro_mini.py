# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_Pro_Mini\oxygen_pro_mini.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from Oxygen_Pro.mode import ReenterBehaviour
from Oxygen_Pro.oxygen_pro import Oxygen_Pro
from .simple_device import SimpleDeviceParameterComponent

class Oxygen_Pro_Mini(Oxygen_Pro):
    session_width = 4
    pad_ids = ((40, 41, 42, 43), (48, 49, 50, 51))
    device_parameter_component = SimpleDeviceParameterComponent

    def _get_device_mode_behaviour(self):
        return ReenterBehaviour(on_reenter=self._on_reenter_device_mode)

    def _on_reenter_device_mode(self):
        self._device_parameters.toggle_parameter_offset()