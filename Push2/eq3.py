# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\eq3.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from enum import IntEnum
from ableton.v2.base import EventObject, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator

class EqThreeDeviceDecorator(LiveObjectDecorator, EventObject):

    def __init__(self, *a, **k):
        super(EqThreeDeviceDecorator, self).__init__(*a, **k)
        self._add_switch_option(name='Slope', pname='Slope', labels=['24dB', '48dB'])
        self._add_on_off_option(name='Low', pname='LowOn')
        self._add_on_off_option(name='Mid', pname='MidOn')
        self._add_on_off_option(name='High', pname='HighOn')
        self.register_disconnectables(self.options)