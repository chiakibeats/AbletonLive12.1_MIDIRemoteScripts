# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\velocity.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import EventObject, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator, get_parameter_by_name

class VelocityDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        super(VelocityDeviceDecorator, self).__init__(*a, **k)
        self._add_switch_option(name='Operation', pname='Operation', labels=['Vel', 'Rel', 'Both'])
        self.register_disconnectables(self.options)