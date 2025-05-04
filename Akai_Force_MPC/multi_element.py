# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\multi_element.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v2.base import old_hasattr
from ableton.v2.control_surface.elements import MultiElement as MultiElementBase

class MultiElement(MultiElementBase):

    def __init__(self, *a, **k):
        super(MultiElement, self).__init__(*a, **k)
        self._parameter_to_map_to = None

    @property
    def touch_element(self):
        for control in self.owned_control_elements():
            if old_hasattr(control, 'touch_element'):
                return control.touch_element
            else:
                continue
        return None

    def connect_to(self, parameter):
        self._parameter_to_map_to = parameter
        for control in self.owned_control_elements():
            control.connect_to(parameter)

    def release_parameter(self):
        self._parameter_to_map_to = None
        for control in self.owned_control_elements():
            control.release_parameter()

    def mapped_parameter(self):
        return self._parameter_to_map_to