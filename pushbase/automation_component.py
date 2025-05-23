# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\automation_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.utils import old_div
import Live
from ableton.v2.base import clamp, liveobj_valid, task
from ableton.v2.control_surface.control import EncoderControl, control_list
from .device_parameter_component import DeviceParameterComponent
from .setting import EnumerableSetting
AutomationState = Live.DeviceParameter.AutomationState

class AutomationComponent(DeviceParameterComponent):
    ENCODER_SENSITIVITY_FACTOR = 1.0
    _clip = None
    encoders = control_list(EncoderControl)

    @staticmethod
    def parameter_is_automateable(parameter):
        return liveobj_valid(parameter) and isinstance(parameter, Live.DeviceParameter.DeviceParameter)

    def __init__(self, *a, **k):
        super(AutomationComponent, self).__init__(*a, **k)
        self._selected_time = []
        self._parameter_floats = []
        self._update_parameter_values_task = self._tasks.add(task.run(self._update_parameter_values))
        self._update_parameter_values_task.kill()

    def _get_clip(self):
        return self._clip

    def _set_clip(self, value):
        self._clip = value
        self._update_parameter_values_task.restart()
    clip = property(_get_clip, _set_clip)

    def _get_selected_time(self):
        return self._selected_time

    def _set_selected_time(self, value):
        self._selected_time = value or []
        self._update_parameter_values()
        self._update_parameter_floats()
    selected_time = property(_get_selected_time, _set_selected_time)

    @property
    def parameters(self):
        return [info.parameter if info else None for info in self._parameter_infos_to_use()]

    @property
    def parameter_infos(self):
        return self._parameter_infos_to_use()

    def _parameter_infos_to_use(self):
        return list(map(lambda info: info if self.parameter_is_automateable(info.parameter if info else None) else None, self._parameter_provider.parameters))

    @property
    def can_automate_parameters(self):
        return self._can_automate_parameters()

    def _can_automate_parameters(self):
        return len(self.parameter_provider.parameters) > 0 and liveobj_valid(self._clip) and (not self._clip.is_arrangement_clip)

    def set_parameter_controls(self, encoders):
        self.encoders.set_control_element(encoders)

    def _update_parameters(self):
        super(AutomationComponent, self)._update_parameters()
        self._update_parameter_floats()

    def _connect_parameters(self):
        return

    def parameter_to_string(self, parameter):
        if not parameter:
            return ''
        else:  # inserted
            if len(self._selected_time) == 0:
                return '-'
            else:  # inserted
                return parameter.str_for_value(self.parameter_to_value(parameter))

    def parameter_to_value(self, parameter):
        if self._clip and len(self.selected_time) > 0 and liveobj_valid(parameter):
            envelope = self._clip.automation_envelope(parameter)
            if liveobj_valid(envelope):
                return self._value_at_time(envelope, self.selected_time[0])
            else:  # inserted
                return parameter.value
        else:  # inserted
            return 0.0

    def _value_at_time(self, envelope, time_range):
        return envelope.value_at_time(old_div(time_range[0] + time_range[1], 2))

    def _can_edit_clip_envelope(self, parameter_index):
        parameters = self.parameters
        return 0 <= parameter_index < len(parameters) and self._clip and self._parameter_for_index(parameters, parameter_index)

    def _parameter_for_index(self, parameters, index):
        return parameters[index]

    @encoders.value
    def encoders(self, value, encoder):
        index = encoder.index
        parameters = self.parameters
        if self._can_edit_clip_envelope(index):
            param = self._parameter_for_index(parameters, index)
            envelope = self._clip.automation_envelope(param)
            if not liveobj_valid(envelope):
                envelope = self._clip.create_automation_envelope(param)
            if liveobj_valid(envelope):
                if param.automation_state == AutomationState.overridden:
                    param.re_enable_automation()
                for time_index, time_range in enumerate(self.selected_time):
                    self._insert_step(time_range, time_index, index, envelope, value)
            self._update_parameter_values()
            return

    @encoders.touched
    def encoders(self, encoder):
        index = encoder.index
        parameters = self.parameters
        if self._can_edit_clip_envelope(index):
            self._clip.view.select_envelope_parameter(self._parameter_for_index(parameters, index))
            self._update_parameter_floats()

    def _update_parameter_floats(self):
        self._parameter_floats = []
        if self._clip and self.is_enabled():
                parameters = self.parameters
                for step in self.selected_time:
                    step_parameter_floats = []
                    for index, param in enumerate(parameters):
                        if param is None:
                            value = 0.0
                        else:  # inserted
                            parameter = self._parameter_for_index(parameters, index)
                            envelope = self._clip.automation_envelope(parameter)
                            if liveobj_valid(envelope):
                                value = self._value_at_time(envelope, step)
                            else:  # inserted
                                value = parameter.value
                        step_parameter_floats.append(value)
                        continue
                    self._parameter_floats.append(step_parameter_floats)
                    continue
                return None
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _insert_step(self, time_range, time_index, param_index, envelope, value):
        param = self._parameter_for_index(self.parameters, param_index)
        envelope_value = self._parameter_floats[time_index][param_index]
        sensitivity = self.parameter_infos[param_index].default_encoder_sensitivity * self.ENCODER_SENSITIVITY_FACTOR
        if param.is_quantized:
            value_to_insert = clamp(envelope_value + old_div(value, EnumerableSetting.STEP_SIZE), param.min, param.max)
        else:  # inserted
            value_range = param.max - param.min
            value_to_insert = clamp(envelope_value + value * value_range * sensitivity, param.min, param.max)
        self._parameter_floats[time_index][param_index] = value_to_insert
        envelope.insert_step(time_range[0], time_range[1] - time_range[0], value_to_insert)