# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\BackgroundComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.BackgroundComponent import BackgroundComponent as BackgroundComponentBase
from _Framework.SubjectSlot import SubjectSlotError

class BackgroundComponent(BackgroundComponentBase):

    def _clear_control(self, name, control):
        if control:
            super(BackgroundComponent, self)._clear_control(name, control)
            return
        else:
            slot = self._control_slots.get(name, None)
            if slot:
                del self._control_slots[name]
                self.disconnect_disconnectable(slot)
            if name in self._control_map:
                del self._control_map[name]
                return

class ModifierBackgroundComponent(BackgroundComponentBase):

    def __init__(self, *a, **k):
        super(ModifierBackgroundComponent, self).__init__(*a, **k)

    def _clear_control(self, name, control):
        super(ModifierBackgroundComponent, self)._clear_control(name, control)
        if control:
            try:
                self._control_slots[name] = self.register_slot(control, lambda *a, **k: self._on_value_listener(control, *a, **k), 'value')
            except SubjectSlotError:
                return None

    def _reset_control(self, control):
        if len(control.resource.owners) > 1:
            control.set_light(control.is_pressed())
            return
        else:
            control.reset()

    def _on_value_listener(self, sender, value, *a, **k):
        if len(sender.resource.owners) > 1:
            sender.set_light(sender.is_pressed())