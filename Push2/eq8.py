# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\eq8.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import re
from ableton.v2.base import EventObject, listens, liveobj_valid
from ableton.v2.control_surface import BoolWrappingParameter, EnumWrappingParameter, LiveObjectDecorator, get_parameter_by_name
from .device_component import DeviceComponentWithTrackColorViewData
from .device_decoration import DeviceSwitchOption

class Eq8DeviceDecorator(EventObject, LiveObjectDecorator):
    available_band_indices = list(range(1, 9))
    available_global_modes = ['Stereo', 'Left/Right', 'Mid/Side']

    def __init__(self, *a, **k):
        super(Eq8DeviceDecorator, self).__init__(*a, **k)
        self.band = EnumWrappingParameter(name='Band', parent=self, values_host=self, index_property_host=self.view, values_property='available_band_indices', index_property='selected_band')
        self.mode = EnumWrappingParameter(name='Eq Mode', parent=self, values_host=self, index_property_host=self, values_property='available_global_modes', index_property='global_mode')
        self.edit_switch = BoolWrappingParameter(name='Edit Mode', parent=self, property_host=self, source_property='edit_mode')
        self.oversampling = BoolWrappingParameter(name='Oversampling', parent=self, property_host=self, source_property='oversample')
        self.left_right_curve_switch_option = DeviceSwitchOption(name='Left/Right', labels=['Left', 'Right'], parameter=self.edit_switch)
        self.mid_side_curve_switch_option = DeviceSwitchOption(name='Mid/Side', labels=['Mid', 'Side'], parameter=self.edit_switch)
        self._additional_parameters = (self.band, self.mode, self.edit_switch, self.oversampling)
        self._additional_options = (self.left_right_curve_switch_option, self.mid_side_curve_switch_option)
        self.register_disconnectables(self._additional_parameters + self._additional_options)
        self.__on_parameters_changed.subject = self

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters

    @property
    def options(self):
        return self._additional_options

    @listens('parameters')
    def __on_parameters_changed(self):
        edit_mode_parameter = get_parameter_by_name(self, 'Edit Mode')
        self.left_right_curve_switch_option.set_parameter(edit_mode_parameter)
        self.mid_side_curve_switch_option.set_parameter(edit_mode_parameter)

class Eq8DeviceComponent(DeviceComponentWithTrackColorViewData):
    FILTER_BAND_PARAMETER_NAMES = re.compile('([1-8] [A-z ]+ [A])|(Scale)')

    def _parameter_touched(self, parameter):
        if not liveobj_valid(self._decorated_device) or liveobj_valid(parameter):
                if self.FILTER_BAND_PARAMETER_NAMES.match(parameter.name):
                    self._update_visualisation_view_data({'AdjustingSelectedBand': True})
                    return
                else:  # inserted
                    if parameter.name == 'Band':
                        self._update_visualisation_view_data({'ChangingSelectedBand': True})
                        return
                    else:  # inserted
                        return None
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _parameter_released(self, parameter):
        if not liveobj_valid(self._decorated_device) or liveobj_valid(parameter):
                if not self._any_filter_band_parameter_touched():
                    self._update_visualisation_view_data({'AdjustingSelectedBand': False})
                if parameter.name == 'Band':
                    self._update_visualisation_view_data({'ChangingSelectedBand': False})
                    return
            else:  # inserted
                return
        else:  # inserted
            return None

    def _any_filter_band_parameter_touched(self):
        touched_parameters = [self.parameters[button.index] for button in self.parameter_touch_buttons if button.is_pressed]
        return any([self.FILTER_BAND_PARAMETER_NAMES.match(parameter.name) for parameter in touched_parameters])

    def _initial_visualisation_view_data(self):
        view_data = super(Eq8DeviceComponent, self)._initial_visualisation_view_data()
        view_data['AdjustingSelectedBand'] = False
        view_data['ChangingSelectedBand'] = False
        return view_data

    @property
    def _visualisation_visible(self):
        return True

    @property
    def _shrink_parameters(self):
        return [True] * 8