# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\vinyl.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from enum import IntEnum
from ableton.v2.base import EventObject, liveobj_valid
from ableton.v2.control_surface import LiveObjectDecorator

class VinylDistortionDecorator(LiveObjectDecorator, EventObject):

    class ModuleSelect(IntEnum):
        tracing = 0
        pinch = 1

    def __init__(self, *a, **k):
        super(VinylDistortionDecorator, self).__init__(*a, **k)
        self._add_enum_parameter(name='Module', values=['Tracing', 'Pinch'], default_value=self.ModuleSelect.tracing)
        self._add_switch_option(name='Pinch Mode', pname='Pinch Soft On', labels=['Soft', 'Hard'])
        self._add_switch_option(name='Pinch Ch', pname='Pinch Mono On', labels=['Mono', 'Stereo'])
        self._add_on_off_option(name='Tracing', pname='Tracing On')
        self._add_on_off_option(name='Pinch', pname='Pinch On')
        self.register_disconnectables(self.options)