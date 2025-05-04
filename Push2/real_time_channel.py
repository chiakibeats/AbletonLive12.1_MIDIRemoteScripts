# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\real_time_channel.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import depends, listenable_property, liveobj_changed, liveobj_valid
from ableton.v2.control_surface import Component

def update_real_time_attachments(real_time_data_components):
    pass
    for d in real_time_data_components:
        d.detach()
        d.attach()

class RealTimeDataComponent(Component):
    __events__ = ('attached',)

    @depends(real_time_mapper=None, register_real_time_data=None)
    pass
    pass
    pass
    def __init__(self, real_time_mapper=None, register_real_time_data=None, channel_type=None, *a, **k):
        super(RealTimeDataComponent, self).__init__(*a, **k)
        self._channel_type = channel_type
        self._real_time_channel_id = ''
        self._object_id = ''
        self._real_time_mapper = real_time_mapper
        self._data = None
        self._valid = True
        register_real_time_data(self)

    def disconnect(self):
        super(RealTimeDataComponent, self).disconnect()
        self._data = None

    @listenable_property
    def channel_id(self):
        return self._real_time_channel_id

    @listenable_property
    def object_id(self):
        return self._object_id

    @property
    def attached_object(self):
        return self._data

    def on_enabled_changed(self):
        super(RealTimeDataComponent, self).on_enabled_changed()
        self.invalidate()
        self._update_attachment()

    def _update_attachment(self):
        self.detach()
        self.attach()

    def set_data(self, data):
        if liveobj_changed(data, self._data):
            self._data = data
            self.invalidate()
            return
        else:  # inserted
            return None

    def invalidate(self):
        self._valid = False

    def detach(self):
        if self._valid or self._real_time_channel_id!= '':
                self._real_time_mapper.detach_channel(self._real_time_channel_id)
                self._real_time_channel_id = ''

    def device_visualisation(self):
        return self._real_time_mapper.device_visualisation

    def attach(self):
        if not self._valid:
            data = self._data if self.is_enabled() else None
            if data!= None:
                self._real_time_channel_id, self._object_id = self._real_time_mapper.attach_object(data, self._channel_type)
            self.notify_channel_id()
            self.notify_object_id()
            self._valid = True
            self.notify_attached()