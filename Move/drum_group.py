# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\drum_group.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from ableton.v3.base import depends
from ableton.v3.control_surface.components import DrumGroupComponent as DrumGroupComponentBase

class DrumGroupComponent(DrumGroupComponentBase):
    pass

    @depends(volume_parameters=None)
    def __init__(self, volume_parameters=None, *a, **k):
        super().__init__(*a, matrix_always_listenable=True, **k)
        self._volume_parameters = volume_parameters

    def _on_matrix_pressed(self, button):
        pad = self._pad_for_button(button)
        parameter = pad.chains[0].mixer_device.volume if not self._any_modifier_pressed() and (not self._clipboard.is_copying) else None
            self._volume_parameters.add_parameter(button, parameter)
        super()._on_matrix_pressed(button)

    def _on_matrix_released(self, button):
        super()._on_matrix_released(button)
        self._volume_parameters.remove_parameter(button)