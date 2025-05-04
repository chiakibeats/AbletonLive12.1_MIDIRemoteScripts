# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\scroll.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import task
from .. import MOMENTARY_DELAY, Component
from ..controls import ButtonControl, StepEncoderControl

class Scrollable:
    pass
    can_scroll_up = lambda: False
    can_scroll_down = lambda: False
    scroll_up = NotImplemented
    scroll_down = NotImplemented

class ScrollComponent(Component, Scrollable):
    pass
    scrolling_delay = MOMENTARY_DELAY
    pass
    scrolling_step_delay = 0.1
    pass
    scroll_encoder = StepEncoderControl(num_steps=64)
    scroll_up_button = ButtonControl()
    scroll_down_button = ButtonControl()

    def __init__(self, scrollable=None, scroll_skin_name=None, *a, **k):
        super().__init__(*a, **k)
        if scroll_skin_name:
            pressed_colored = '{}Pressed'.format(scroll_skin_name)
            self.scroll_up_button.color = scroll_skin_name
            self.scroll_down_button.color = scroll_skin_name
            self.scroll_up_button.pressed_color = pressed_colored
            self.scroll_down_button.pressed_color = pressed_colored
        self._scroll_task_up = self._make_scroll_task(self._do_scroll_up)
        self._scroll_task_down = self._make_scroll_task(self._do_scroll_down)
        self._scrollable = scrollable or self

    def _make_scroll_task(self, scroll_step):
        t = self._tasks.add(task.sequence(task.wait(self.scrolling_delay), task.loop(task.wait(self.scrolling_step_delay), task.run(scroll_step))))
        t.kill()
        return t

    @property
    def scrollable(self):
        pass
        return self._scrollable

    def can_scroll_up(self):
        return self._scrollable.can_scroll_up()

    def can_scroll_down(self):
        return self._scrollable.can_scroll_down()

    def scroll_up(self):
        return self._scrollable.scroll_up()

    def scroll_down(self):
        return self._scrollable.scroll_down()

    def set_scroll_up_button(self, button):
        self.scroll_up_button.set_control_element(button)
        self._update_scroll_controls()

    def set_scroll_down_button(self, button):
        self.scroll_down_button.set_control_element(button)
        self._update_scroll_controls()

    def set_scroll_encoder(self, encoder):
        self.scroll_encoder.set_control_element(encoder)
        self._update_scroll_controls()

    def _update_scroll_controls(self):
        self.scroll_up_button.enabled = self.can_scroll_up()
        self.scroll_down_button.enabled = self.can_scroll_down()
        self.scroll_encoder.enabled = self.can_scroll_up() or self.can_scroll_down()

    @scroll_up_button.pressed
    def scroll_up_button(self, button):
        self._on_scroll_pressed(button, self._do_scroll_up, self._scroll_task_up)

    @scroll_up_button.released
    def scroll_up_button(self, _):
        self._on_scroll_released(self._scroll_task_up)

    @scroll_down_button.pressed
    def scroll_down_button(self, button):
        self._on_scroll_pressed(button, self._do_scroll_down, self._scroll_task_down)

    @scroll_down_button.released
    def scroll_down_button(self, _):
        self._on_scroll_released(self._scroll_task_down)

    @scroll_encoder.value
    def scroll_encoder(self, value, _):
        if value < 0:
            if self.can_scroll_up():
                self._do_scroll_up()
        elif self.can_scroll_down():
            self._do_scroll_down()
        else:
            return None

    def _do_scroll_up(self):
        self.scroll_up()
        self._update_scroll_controls()

    def _do_scroll_down(self):
        self.scroll_down()
        self._update_scroll_controls()

    def update(self):
        super().update()
        self._update_scroll_controls()

    def _on_scroll_pressed(self, button, scroll_step, scroll_task):
        is_scrolling = not self._scroll_task_up.is_killed or not self._scroll_task_down.is_killed
        if not is_scrolling:
            scroll_step()
        if button.enabled:
            scroll_task.restart()
        self._ensure_scroll_one_direction()

    def _on_scroll_released(self, scroll_task):
        scroll_task.kill()
        self._ensure_scroll_one_direction()

    def _ensure_scroll_one_direction(self):
        if self.scroll_up_button.is_pressed and self.scroll_down_button.is_pressed:
            self._scroll_task_up.pause()
            self._scroll_task_down.pause()
            return
        else:
            self._scroll_task_up.resume()
            self._scroll_task_down.resume()