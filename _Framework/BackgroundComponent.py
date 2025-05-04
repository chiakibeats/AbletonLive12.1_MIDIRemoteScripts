# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\BackgroundComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from .ControlSurfaceComponent import ControlSurfaceComponent
from .SubjectSlot import SubjectSlotError

class BackgroundComponent(ControlSurfaceComponent):
    pass

    def __init__(self, *a, **k):
        super(BackgroundComponent, self).__init__(*a, **k)
        self._control_slots = {}
        self._control_map = {}

    def __getattr__(self, name):
        if len(name) > 4 and name[:4] == 'set_':
            return partial(self._clear_control, name[4:])
        else:
            raise AttributeError(name)

    def _clear_control(self, name, control):
        slot = self._control_slots.get(name, None)
        if slot:
            del self._control_slots[name]
            self.disconnect_disconnectable(slot)
        if control:
            self._reset_control(control)
            self._control_map[name] = control
            return
        elif name in self._control_map:
            del self._control_map[name]
            return

    def _reset_control(self, control):
        control.reset()

    def update(self):
        super(BackgroundComponent, self).update()
        if self.is_enabled():
            for control in self._control_map.values():
                self._reset_control(control)
        else:
            return

class ModifierBackgroundComponent(BackgroundComponent):
    pass

    def __init__(self, *a, **k):
        super(ModifierBackgroundComponent, self).__init__(*a, **k)

    def _reset_control(self, control):
        if len(control.resource.owners) > 1:
            control.set_light(True)
            return
        else:
            control.reset()