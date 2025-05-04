# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\device_parameters.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import zip_longest
from ...base import listens
from .. import Component, ParameterProvider
from ..controls import MappedSensitivitySettingControl, control_list

class DeviceParametersComponent(Component):
    pass
    controls = control_list(MappedSensitivitySettingControl, 8)

    def __init__(self, parameter_provider=None, name='Device_Parameters', *a, **k):
        super().__init__(*a, name=name, **k)
        self.parameter_provider = parameter_provider

    @property
    def parameter_provider(self):
        pass
        return self._parameter_provider

    @parameter_provider.setter
    def parameter_provider(self, provider):
        self._parameter_provider = provider or ParameterProvider()
        self.__on_parameters_changed.subject = self._parameter_provider
        self._update_parameters()

    def set_parameter_controls(self, encoders):
        if encoders and len(encoders) > self.controls.control_count:
            self.controls.control_count = len(encoders)
        self.controls.set_control_element(encoders)
        self._connect_parameters()

    def _connect_parameters(self):
        parameters = self._parameter_provider.parameters[:self.controls.control_count]
        for control, parameter_info in zip_longest(self.controls, parameters):
            parameter = parameter_info.parameter if parameter_info else None
            control.mapped_parameter = parameter
            if parameter:
                control.update_sensitivities(parameter_info.default_encoder_sensitivity, parameter_info.fine_grain_encoder_sensitivity)
            continue

    def update(self):
        super().update()
        self._update_parameters()

    def _update_parameters(self):
        if self.is_enabled():
            self._connect_parameters()

    @listens('parameters')
    def __on_parameters_changed(self):
        self._update_parameters()