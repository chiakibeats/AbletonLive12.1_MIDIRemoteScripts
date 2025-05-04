# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\drumcell.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from enum import IntEnum
from ableton.v2.base import EventObject, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator

class DrumCellDeviceDecorator(LiveObjectDecorator, EventObject):

    class select(IntEnum):
        env = 0
        flt = 1
        mod = 2
        sam = 3

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._add_enum_parameter(name='Select', values=['Env', 'Filter', 'Mod', 'Sample'], default_value=self.select.env)
        self._add_switch_option(name='Env Mode', pname='Env Mode', labels=['Trigger', 'Gate'])
        self._add_on_off_option(name='Filter', pname='Filter On')
        self.register_disconnectables(self.options)