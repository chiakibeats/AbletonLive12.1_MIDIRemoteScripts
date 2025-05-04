# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\roar.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from builtins import range
import re
from enum import IntEnum
import Live
from ableton.v2.base import EventObject, listens, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_component import ButtonRange, DeviceComponentWithTrackColorViewData
from .visualisation_settings import VisualisationGuides

class RoarDeviceDecorator(EventObject, LiveObjectDecorator):

    class stageSel(IntEnum):
        st1 = 0
        st2 = 1
        st3 = 2

    class modSource(IntEnum):
        lfo1 = 0
        lfo2 = 1
        eg = 2
        noise = 3

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.stage_index_enum = self._add_enum_parameter(name='Stage Select', values=['1', '2', '3'], default_value=self.stageSel.st1)
        self._add_non_automatable_enum_parameter(name='Routing', list='routing_mode_list', index='routing_mode_index')
        self.source_index_enum = self._add_enum_parameter(name='Source', values=['LFO 1', 'LFO 2', 'Env', 'Noise'], default_value=self.modSource.lfo1)
        self._add_on_off_option(name='Comp Hp', pname='Comp Hp On')
        self._add_on_off_option(name='Color', pname='Color On')
        self._add_on_off_option(name='Shaper 1', pname='Shaper 1 On')
        self._add_on_off_option(name='Shaper 2', pname='Shaper 2 On')
        self._add_on_off_option(name='Shaper 3', pname='Shaper 3 On')
        self._add_on_off_option(name='Stage 1', pname='Stage 1 On')
        self._add_on_off_option(name='Stage 2', pname='Stage 2 On')
        self._add_on_off_option(name='Stage 3', pname='Stage 3 On')
        self._add_on_off_option(name='Filter 1', pname='Flt 1 On')
        self._add_on_off_option(name='Filter 2', pname='Flt 2 On')
        self._add_on_off_option(name='Filter 3', pname='Flt 3 On')
        self._add_on_off_option(name='Filter 1 Pre', pname='Flt 1 Pre On')
        self._add_on_off_option(name='Filter 2 Pre', pname='Flt 2 Pre On')
        self._add_on_off_option(name='Filter 3 Pre', pname='Flt 3 Pre On')
        self._add_on_off_option(name='Fb Inv', pname='Fb Inv On')
        self._add_on_off_option(name='Fb Gate', pname='Fb Gate On')
        self.register_disconnectables(self.options)

class RoarDeviceComponent(DeviceComponentWithTrackColorViewData):
    SHAPER_VISUALISATION_CONFIGURATION_IN_BANKS = {0: ButtonRange(1, 3), 2: ButtonRange(2, 4)}
    FILTER_VISUALISATION_CONFIGURATION_IN_BANKS = {2: ButtonRange(5, 7)}
    SHAPER_PARAMETER_NAMES = re.compile('^(Shaper (1|2|3) (Type|Amt))')
    BIAS_PARAMETER_NAMES = re.compile('^(Shaper (1|2|3) Bias)')

    def _parameter_touched(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    def _parameter_released(self, parameter):
        self._update_visualisation_view_data(self._adjustment_view_data)

    @property
    def _adjustment_view_data(self):
        active_stage_index = self._decorated_device.stage_index_enum.value
        adjusting_shaper = False
        adjusting_bias = False
        adjusting_filter = False
        touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed]
        for parameter in touched_parameters:
            if self.SHAPER_PARAMETER_NAMES.match(parameter.name):
                adjusting_shaper = True
            if self.BIAS_PARAMETER_NAMES.match(parameter.name):
                adjusting_bias = True
            if parameter.name.startswith('Flt'):
                adjusting_filter = True
            pass
            continue
        return {'ActiveStageIndex': active_stage_index, 'AdjustingShaper': adjusting_shaper, 'AdjustingBias': adjusting_bias, 'AdjustingFilter': adjusting_filter}

    def _set_bank_index(self, bank):
        super(RoarDeviceComponent, self)._set_bank_index(bank)
        self._update_visualisation_view_data(self._configuration_view_data)
        self._update_visualisation_view_data(self._adjustment_view_data)
        self.notify_visualisation_visible()
        self.notify_shrink_parameters()

    def _set_decorated_device(self, decorated_device):
        super()._set_decorated_device(decorated_device)
        self._on_stage_index_parameter_change.subject = self._decorated_device.stage_index_enum

    @property
    def _visualisation_visible(self):
        return self._bank.index in self.SHAPER_VISUALISATION_CONFIGURATION_IN_BANKS or self._bank.index in self.FILTER_VISUALISATION_CONFIGURATION_IN_BANKS

    @property
    def _shrink_parameters(self):
        if self._visualisation_visible:
            shaper_config = self.SHAPER_VISUALISATION_CONFIGURATION_IN_BANKS.get(self._bank.index, ButtonRange(-1, -1))
            filter_config = self.FILTER_VISUALISATION_CONFIGURATION_IN_BANKS.get(self._bank.index, ButtonRange(-1, -1))
            return [shaper_config.left_index <= index <= shaper_config.right_index or filter_config.left_index <= index <= filter_config.right_index for index in range(8)]
        else:
            return [False] * 8

    @property
    def _configuration_view_data(self):
        shaper_left, shaper_right = self._calculate_view_size(self.SHAPER_VISUALISATION_CONFIGURATION_IN_BANKS)
        filter_left, filter_right = self._calculate_view_size(self.FILTER_VISUALISATION_CONFIGURATION_IN_BANKS)
        return {'ShaperLeft': shaper_left, 'ShaperRight': shaper_right, 'FilterLeft': filter_left, 'FilterRight': filter_right}

    def _initial_visualisation_view_data(self):
        view_data = super(RoarDeviceComponent, self)._initial_visualisation_view_data()
        view_data.update(self._configuration_view_data)
        view_data.update(self._adjustment_view_data)
        return view_data

    def _calculate_view_size(self, configuration):
        if self._bank.index not in configuration:
            return (0, 0)
        else:
            config = configuration[self._bank.index]
            return (VisualisationGuides.light_left_x(config.left_index), VisualisationGuides.light_right_x(config.right_index))

    @listens('value')
    def _on_stage_index_parameter_change(self):
        self._update_visualisation_view_data(self._adjustment_view_data)