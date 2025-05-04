# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\lockable_button.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import EventObject, listenable_property, task
from .. import DOUBLE_CLICK_DELAY
from ..display import Renderable
from . import ButtonElement

class LockableButtonElementMixin(EventObject, Renderable):
    pass
    is_locked = listenable_property.managed(False)

    def __init__(self, double_click_time=DOUBLE_CLICK_DELAY, *a, **k):
        super().__init__(*a, **k)
        self._locked_color = 'DefaultButton.{}Locked'.format(self.name.title().replace('_', ''))
        self._double_click_count = 0
        self._double_click_task = self._tasks.add(task.wait(double_click_time))
        self._double_click_task.kill()

    def reset(self):
        self._set_is_locked(False, do_notify=False)
        super().reset()

    def receive_value(self, value):
        if value:
            self._on_press()
        else:
            self._on_release()
        super().receive_value(value)

    def _on_press(self):
        self._set_is_locked(False)
        if not self._double_click_task.is_running:
            self._double_click_task.restart()
            self._double_click_count = 0

    def _on_release(self):
        if self._double_click_task.is_running:
            self._double_click_count += 1
            if self._double_click_count == 2:
                self._set_is_locked(True)
                self._double_click_task.kill()
                return
        else:
            return

    def _set_is_locked(self, is_locked, do_notify=True):
        if self.is_locked != is_locked:
            self.is_locked = is_locked
            if do_notify:
                self.notify(self.notifications.Element.button_lock, self.name, is_locked)

    def _set_skin_light(self, value):
        if self.is_locked:
            value = self._locked_color
        super()._set_skin_light(value)

class LockableButtonElement(LockableButtonElementMixin, ButtonElement):
    pass