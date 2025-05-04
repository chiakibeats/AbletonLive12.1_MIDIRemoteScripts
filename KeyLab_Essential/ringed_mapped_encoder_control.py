# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential\ringed_mapped_encoder_control.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import listens
from ableton.v2.control_surface.control import MappedControl

class RingedMappedEncoderControl(MappedControl):

    class State(MappedControl.State):

        def _update_direct_connection(self):
            super(RingedMappedEncoderControl.State, self)._update_direct_connection()
            self._on_parameter_value.subject = self._direct_mapping
            if self._direct_mapping:
                self._on_parameter_value()

        @listens('value')
        def _on_parameter_value(self):
            if self._control_element and self.enabled:
                self._control_element.set_ring_value(self._direct_mapping)
                return
            else:
                return