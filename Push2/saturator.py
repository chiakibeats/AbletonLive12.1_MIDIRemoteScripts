# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\saturator.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from enum import IntEnum
from ableton.v2.base import EventObject, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator

class SaturatorDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        super(SaturatorDeviceDecorator, self).__init__(*a, **k)
        self._add_switch_option(name='Post Clip Mode', pname='Post Clip Mode', labels=['None', 'Soft', 'Hard'])
        self._add_on_off_option(name='Color On', pname='Color On')
        self.register_disconnectables(self.options)