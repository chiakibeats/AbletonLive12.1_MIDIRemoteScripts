# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\controls\mapped.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.control import MappedSensitivitySettingControl as MappedSensitivitySettingControlBase
from ...base import EventObject, listens
from ...live import action, liveobj_valid
from .. import ABSOLUTE_MAP_MODES, EnumWrappingParameter
from . import ButtonControl as ButtonControlBase
from . import is_internal_parameter

class MappableButton(EventObject):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._parameter = None

    def disconnect(self):
        self._parameter = None
        super().disconnect()

    @property
    def mapped_parameter(self):
        pass
        return self._parameter

    @mapped_parameter.setter
    def mapped_parameter(self, parameter):
        self._parameter = parameter if liveobj_valid(parameter) else None
        self.enabled = self._parameter is not None
        self.__on_parameter_value_changed.subject = self._parameter
        self.__on_parameter_value_changed()

    @listens('value')
    def __on_parameter_value_changed(self):
        self.is_on = liveobj_valid(self._parameter) and self._parameter.value

class MappedButtonControl(ButtonControlBase):
    pass

    class State(ButtonControlBase.State, MappableButton):

        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self.enabled = False

        def _call_listener(self, listener_name, *a):
            if listener_name == 'pressed':
                action.toggle_or_cycle_parameter_value(self.mapped_parameter)
            super()._call_listener(listener_name, *a)

class MappedSensitivitySettingControl(MappedSensitivitySettingControlBase):
    pass

    class State(MappedSensitivitySettingControlBase.State):

        def __init__(self, default_sensitivity=None, fine_sensitivity=None, *a, **k):
            super().__init__(*a, **k)
            self.default_sensitivity = default_sensitivity or self.default_sensitivity
            self.fine_sensitivity = fine_sensitivity or self.fine_sensitivity

        def _update_direct_connection(self):
            self._control_value.subject = None
            self._absolute_control_value.subject = None
            self._quantized_stepper.reset()
            if self._control_element:
                if is_internal_parameter(self.mapped_parameter):
                    self._connect_internal_parameter()
                    return
                else:
                    self._update_control_element()

        @staticmethod
        def _is_parameter_valid(parameter):
            return not is_internal_parameter(parameter) or isinstance(parameter, EnumWrappingParameter)

        def _connect_internal_parameter(self):
            self._control_element.release_parameter()
            self._control_element.connect_to(self.mapped_parameter)
            if self._control_element.message_map_mode() in ABSOLUTE_MAP_MODES:
                self._absolute_control_value.subject = self._control_element
            else:
                self._control_value.subject = self._control_element
            self._update_control_sensitivity()

        @listens('value')
        def _absolute_control_value(self, value):
            step_size = self._control_element.max_value() / (self.mapped_parameter.max + 1)
            self.mapped_parameter.value = int(value / step_size)