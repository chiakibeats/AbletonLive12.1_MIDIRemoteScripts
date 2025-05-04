# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\control\button.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from ...base import lazy_attribute, task
from ..defaults import DOUBLE_CLICK_DELAY, MOMENTARY_DELAY
from ..input_control_element import ScriptForwarding
from .control import InputControl, control_color, control_event
__all__ = ('ButtonControl', 'PlayableControl', 'ButtonControlBase', 'DoubleClickContext')

class DoubleClickContext(object):
    pass
    control_state = None
    click_count = 0

    def set_new_context(self, control_state):
        self.control_state = control_state
        self.click_count = 0

class ButtonControlBase(InputControl):
    pass
    DELAY_TIME = MOMENTARY_DELAY
    pass
    DOUBLE_CLICK_TIME = DOUBLE_CLICK_DELAY
    pass
    REPEAT_RATE = 0.1
    pass
    pressed = control_event('pressed')
    pass
    released = control_event('released')
    pass
    pressed_delayed = control_event('pressed_delayed')
    pass
    released_delayed = control_event('released_delayed')
    pass
    released_immediately = control_event('released_immediately')
    pass
    double_clicked = control_event('double_clicked')
    pass

    class State(InputControl.State):
        pass
        disabled_color = control_color('DefaultButton.Disabled')
        pass
        pressed_color = control_color(None)
        pass
        pass
        pass
        pass
        pass
        pass
        pass

        def __init__(self, pressed_color=None, disabled_color=None, repeat=False, enabled=True, double_click_context=None, delay_time=None, *a, **k):
            super(ButtonControlBase.State, self).__init__(*a, **k)
            if disabled_color is not None:
                self.disabled_color = disabled_color
            self.pressed_color = pressed_color
            self._repeat = repeat
            self._is_pressed = False
            self._enabled = enabled
            self._double_click_context = double_click_context or DoubleClickContext()
            self._delay_time = delay_time if delay_time is not None else ButtonControlBase.DELAY_TIME

        @property
        def enabled(self):
            pass
            return self._enabled

        @enabled.setter
        def enabled(self, enabled):
            if self._enabled != enabled:
                if not enabled:
                    self._release_button()
                self._enabled = enabled
                self._send_current_color()
                return
            else:
                return None

        @property
        def is_momentary(self):
            pass
            return self._control_element and self._control_element.is_momentary()

        @property
        def is_pressed(self):
            pass
            return self._is_pressed

        def _event_listener_required(self):
            return True

        def set_control_element(self, control_element):
            pass
            if self._control_element != control_element:
                self._release_button()
                self._kill_all_tasks()
            super(ButtonControlBase.State, self).set_control_element(control_element)
            self._send_current_color()

        def _send_current_color(self):
            if self._control_element:
                if not self._enabled:
                    self._control_element.set_light(self.disabled_color)
                    return
                elif self.pressed_color is not None and self.is_pressed:
                    self._control_element.set_light(self.pressed_color)
                    return
                else:
                    self._send_button_color()
                    return

        def _send_button_color(self):
            raise NotImplementedError

        def _on_value(self, value, *a, **k):
            if self._notifications_enabled():
                if not self.is_momentary:
                    self._press_button()
                    self._release_button()
                elif value:
                    self._press_button()
                else:
                    self._release_button()
                super(ButtonControlBase.State, self)._on_value(value, *a, **k)
            self._send_current_color()

        def _press_button(self):
            is_pressed = self._is_pressed
            self._is_pressed = True
            if not self._notifications_enabled() or not is_pressed:
                self._on_pressed()

        def _on_pressed(self):
            if self._repeat:
                self._repeat_task.restart()
            self._call_listener('pressed')
            if self._has_delayed_event():
                self._delay_task.restart()
            self._check_double_click_press()

        def _release_button(self):
            is_pressed = self._is_pressed
            self._is_pressed = False
            if not self._notifications_enabled() or is_pressed:
                self._on_released()

        def _on_released(self):
            self._call_listener('released')
            if self._repeat:
                self._repeat_task.kill()
            if self._has_delayed_event():
                if self._delay_task.is_running:
                    self._call_listener('released_immediately')
                    self._delay_task.kill()
                else:
                    self._call_listener('released_delayed')
            self._check_double_click_release()

        def _check_double_click_press(self):
            if self._has_listener('double_clicked') and (not self._double_click_task.is_running):
                self._double_click_task.restart()
                self._double_click_context.click_count = 0
            if self._double_click_context.control_state != self:
                self._double_click_context.set_new_context(self)
                return
            else:
                return None

        def _check_double_click_release(self):
            if self._has_listener('double_clicked') and self._double_click_task.is_running and (self._double_click_context.control_state == self):
                self._double_click_context.click_count += 1
                if self._double_click_context.click_count == 2:
                    self._call_listener('double_clicked')
                    self._double_click_task.kill()
                    return
            else:
                return

        def set_double_click_context(self, context):
            self._double_click_context = context

        @lazy_attribute
        def _delay_task(self):
            return self.tasks.add(task.sequence(task.wait(self._delay_time), task.run(self._on_pressed_delayed)))

        @lazy_attribute
        def _repeat_task(self):
            notify_pressed = partial(self._call_listener, 'pressed')
            return self.tasks.add(task.sequence(task.wait(self._delay_time), task.loop(task.wait(ButtonControlBase.REPEAT_RATE), task.run(notify_pressed))))

        def _kill_all_tasks(self):
            if self._repeat:
                self._repeat_task.kill()
            if self._has_delayed_event():
                self._delay_task.kill()
                return
            else:
                return None

        @lazy_attribute
        def _double_click_task(self):
            return self.tasks.add(task.wait(ButtonControlBase.DOUBLE_CLICK_TIME))

        def _has_delayed_event(self):
            return self._has_listener('pressed_delayed') or self._has_listener('released_delayed') or self._has_listener('released_immediately')

        def _on_pressed_delayed(self):
            if self._is_pressed:
                self._call_listener('pressed_delayed')

        def update(self):
            self._send_current_color()

    def __init__(self, *a, **k):
        super(ButtonControlBase, self).__init__(extra_args=a, extra_kws=k)

class ButtonControl(ButtonControlBase):
    pass

    class State(ButtonControlBase.State):
        pass
        color = control_color('DefaultButton.On')
        pass

        def __init__(self, color='DefaultButton.On', *a, **k):
            super(ButtonControl.State, self).__init__(*a, **k)
            self.color = color

        def _send_button_color(self):
            if self.color is not None:
                self._control_element.set_light(self.color)

class PlayableControl(ButtonControl):
    pass

    class Mode(int):
        pass
    Mode.playable = Mode(0)
    pass
    Mode.listenable = Mode(1)
    pass
    Mode.playable_and_listenable = Mode(2)
    pass

    class State(ButtonControl.State):
        pass

        def __init__(self, mode=None, *a, **k):
            super(PlayableControl.State, self).__init__(*a, **k)
            self._enabled = True
            self._mode = PlayableControl.Mode.playable if mode is None else mode
            self._mode_to_forwarding = {PlayableControl.Mode.playable: ScriptForwarding.none, PlayableControl.Mode.listenable: ScriptForwarding.exclusive, PlayableControl.Mode.playable_and_listenable: ScriptForwarding.non_consuming}

        def set_control_element(self, control_element):
            pass
            super(PlayableControl.State, self).set_control_element(control_element)
            self._update_script_forwarding()

        def _update_script_forwarding(self):
            if self._control_element and self._enabled:
                self._control_element.script_forwarding = self._mode_to_forwarding[self._mode]
                return
            else:
                return

        @property
        def enabled(self):
            pass
            return self._enabled

        @enabled.setter
        def enabled(self, enabled):
            super(PlayableControl.State, PlayableControl.State).enabled.fset(self, enabled)
            if not enabled and self._control_element:
                self._control_element.reset_state()
                self._send_current_color()
                return
            else:
                self.set_control_element(self._control_element)

        def set_mode(self, value):
            pass
            self._mode = value
            self._update_script_forwarding()

        def _is_listenable(self):
            return self._mode != PlayableControl.Mode.playable

        def _notifications_enabled(self):
            return super(PlayableControl.State, self)._notifications_enabled() and self._is_listenable()