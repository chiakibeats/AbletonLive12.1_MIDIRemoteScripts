# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\internal_parameter.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface import InternalParameter
from ableton.v3.control_surface.controls import StepEncoderControl
from ableton.v3.live import liveobj_valid

def register_internal_parameter(parent, name, display_fn):
    pass
    return parent.register_disconnectable(InternalParameter(name=name, display_value_conversion=display_fn))

class InternalParameterControl(StepEncoderControl):
    pass

    class State(StepEncoderControl.State):
        def __init__(self, num_steps=64, *a, **k):
            super().__init__(*a, num_steps=num_steps, **k)
            self._parameter = None

        @property
        def parameter(self):
            return self._parameter

        @parameter.setter
        def parameter(self, parameter):
            self._parameter = parameter

        def set_control_element(self, control_element):
            if self._control_element:
                self._control_element.release_parameter()
            super().set_control_element(control_element)
            if self._control_element and liveobj_valid(self._parameter):
                    self._control_element.connect_to(self._parameter)
                    return
                else:  # inserted
                    return None
            else:  # inserted
                return None