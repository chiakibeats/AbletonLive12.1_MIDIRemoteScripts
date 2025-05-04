# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\redux2.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import EventObject
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name
from .device_options import DeviceOnOffOption

class Redux2DeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        super(Redux2DeviceDecorator, self).__init__(*a, **k)
        self.postFilter_on_option = DeviceOnOffOption(name='Post-Filter', property_host=get_parameter_by_name(self, 'Post-Filter On'))
        self.register_disconnectables(self.options)

    @property
    def options(self):
        return (self.postFilter_on_option,)

    @property
    def parameters(self):
        return tuple(self._live_object.parameters)