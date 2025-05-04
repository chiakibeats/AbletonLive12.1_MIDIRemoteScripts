# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\device_decorators.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface import DelayDeviceDecorator
from ableton.v2.control_surface import DeviceDecoratorFactory as DeviceDecoratorFactoryBase
from ableton.v2.control_surface import LiveObjectDecorator, SimplerDeviceDecorator

class DeviceDecorator(LiveObjectDecorator):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.create_additional_parameters()
        self.register_disconnectables(self.options)

    def create_additional_parameters(self):
        pass
        raise NotImplementedError('Must implement this method to create additional parameters for the device')

class TransmuteDeviceDecorator(DeviceDecorator):
    pass

    def create_additional_parameters(self):
        self._add_non_automatable_enum_parameter(name='Hz/Note Mode', list='frequency_dial_mode_list', index='frequency_dial_mode')
        self._add_non_automatable_enum_parameter(name='Pitch Mode', list='pitch_mode_list', index='pitch_mode')

class DriftDeviceDecorator(DeviceDecorator):
    pass

    def create_additional_parameters(self):
        self._add_non_automatable_enum_parameter(name='Voice Mode', list='voice_mode_list', index='voice_mode_index')
        self._add_non_automatable_enum_parameter(name='Voice Count', list='voice_count_list', index='voice_count_index')
        self._add_non_automatable_enum_parameter(name='LP Mod Src 1', list='mod_matrix_filter_source_1_list', index='mod_matrix_filter_source_1_index')
        self._add_non_automatable_enum_parameter(name='LP Mod Src 2', list='mod_matrix_filter_source_2_list', index='mod_matrix_filter_source_2_index')

class RoarDeviceDecorator(DeviceDecorator):
    pass

    def create_additional_parameters(self):
        self._add_non_automatable_enum_parameter(name='Routing', list='routing_mode_list', index='routing_mode_index')

class DeviceDecoratorFactory(DeviceDecoratorFactoryBase):
    pass
    DECORATOR_CLASSES = {'Delay': DelayDeviceDecorator, 'Drift': DriftDeviceDecorator, 'OriginalSimpler': SimplerDeviceDecorator, 'Roar': RoarDeviceDecorator, 'Transmute': TransmuteDeviceDecorator}