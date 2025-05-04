# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Mini_MK3\notifying_background.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from ableton.v2.base import nop
from ableton.v2.control_surface.components import BackgroundComponent
from ableton.v2.control_surface.elements import ButtonMatrixElement

class NotifyingBackgroundComponent(BackgroundComponent):
    __events__ = ('value',)

    def register_slot(self, control, *a):
        return nop if isinstance(control, ButtonMatrixElement) else partial(self.__on_control_value, control) for listener in super(BackgroundComponent, self).register_slot(control, listener, 'value')

    def __on_control_value(self, control, value):
        self.notify_value(control, value)