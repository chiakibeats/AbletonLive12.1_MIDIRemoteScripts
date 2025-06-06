# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\spectral.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import EventObject
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_options import DeviceOnOffOption, DeviceSwitchOption

class SpectralDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        super(SpectralDeviceDecorator, self).__init__(*a, **k)
        self.freeze_option = DeviceOnOffOption(name='Frozen', property_host=get_parameter_by_name(self, 'Frozen'))
        self.unit_option = DeviceSwitchOption(name='Unit', parameter=get_parameter_by_name(self, 'Unit'), labels=['ms', 'Notes'])
        self.delay_unit_option = DeviceSwitchOption(name='Delay Dly. Unit', parameter=get_parameter_by_name(self, 'Delay Dly. Unit'), labels=['ms', 'Notes', '16th', 'Tr', 'Dt'])
        self.fade_type_option = DeviceSwitchOption(name='Fade Type', parameter=get_parameter_by_name(self, 'Fade Type'), labels=['X-Fade', 'Env'])
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.freeze_option, self.unit_option, self.delay_unit_option, self.fade_type_option)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters) + self._additional_parameters