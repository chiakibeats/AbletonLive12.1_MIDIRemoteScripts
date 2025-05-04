# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\resonator.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from enum import IntEnum
from ableton.v2.base import EventObject
from ableton.v2.control_surface import LiveObjectDecorator

class ResonatorDeviceDecorator(LiveObjectDecorator, EventObject):

    class Select(IntEnum):
        pitch = 0
        finetune = 1
        gain = 2

    def __init__(self, *a, **k):
        super(ResonatorDeviceDecorator, self).__init__(*a, **k)
        self._add_enum_parameter(name='Select', values=['Pitch', 'Fine Tune', 'Gain'], default_value=self.Select.pitch)
        self._add_on_off_option(name='Filter', pname='Filter On')
        self._add_on_off_option(name='Constant', pname='Const')
        self._add_on_off_option(name='I', pname='I On')
        self._add_on_off_option(name='II', pname='II On')
        self._add_on_off_option(name='III', pname='III On')
        self._add_on_off_option(name='IV', pname='IV On')
        self._add_on_off_option(name='V', pname='V On')
        self._add_switch_option(name='Mode', pname='Mode', labels=['Mode B', 'Mode A'])
        self.register_disconnectables(self.options)