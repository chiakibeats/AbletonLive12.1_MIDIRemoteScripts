# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\user_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import listens, task
from ableton.v2.control_surface import Component
from . import sysex

class UserComponentBase(Component):
    __events__ = ('mode', 'before_mode_sent', 'after_mode_sent')
    defer_sysex_sending = False

    def __init__(self, value_control=None, *a, **k):
        super(UserComponentBase, self).__init__(*a, **k)
        self._value_control = value_control
        self.__on_value.subject = self._value_control
        self._selected_mode = sysex.LIVE_MODE
        self._pending_mode_to_select = None

    def toggle_mode(self):
        self.mode = sysex.LIVE_MODE if self.mode == sysex.USER_MODE else sysex.USER_MODE

    def _get_mode(self):
        return self._selected_mode

    def _set_mode(self, mode):
        self._do_set_mode(mode)
    mode = property(_get_mode, _set_mode)

    def _do_set_mode(self, mode):
        if self.is_enabled():
            self._apply_mode(mode)
        else:
            self._pending_mode_to_select = mode

    def update(self):
        super(UserComponentBase, self).update()
        if self.is_enabled() and self._pending_mode_to_select:
            self._apply_mode(self._pending_mode_to_select)
            self._pending_mode_to_select = None
            return

    def force_send_mode(self):
        self._do_apply_mode(self._selected_mode)

    def _apply_mode(self, mode):
        if mode != self._selected_mode:
            self._do_apply_mode(mode)

    def _do_apply_mode(self, mode):
        self.notify_before_mode_sent(mode)
        if self.defer_sysex_sending:
            self._tasks.add(task.sequence(task.delay(1), task.run(lambda: self._send_mode_change(mode))))
        else:
            self._send_mode_change(mode)

    def _send_mode_change(self, mode):
        self._selected_mode = mode
        self._value_control.send_value((mode,))
        self.notify_after_mode_sent(mode)

    @listens('value')
    def __on_value(self, value):
        mode = value[0]
        self._selected_mode = mode
        self.notify_mode(mode)