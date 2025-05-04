# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\controls\button.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from ...base import listenable_property, listens
from ..display import Renderable
from ..elements.touch import TouchElement
from . import ButtonControlBase, control_color, control_event

class ButtonControl(ButtonControlBase):
    pass

    class State(ButtonControlBase.State, Renderable):
        pass
        is_held = listenable_property.managed(False)
        color = control_color('DefaultButton.On')
        on_color = control_color(None)

        def __init__(self, color='DefaultButton.On', on_color=None, *a, **k):
            super().__init__(*a, **k)
            self.color = color
            self.on_color = on_color
            self._is_on = False

        @listenable_property
        def is_pressed(self):
            return self._is_pressed

        @property
        def is_on(self):
            pass
            return self._is_on

        @is_on.setter
        def is_on(self, is_on):
            if is_on != self._is_on:
                self._is_on = is_on
                self._send_current_color()

        def _send_button_color(self):
            if self.on_color is not None and self.is_on:
                self._control_element.set_light(self.on_color)
                return
            elif self.color is not None:
                self._control_element.set_light(self.color)
                return
            else:
                return None

        def _has_delayed_event(self):
            return True

        def _call_listener(self, listener_name, *a):
            super()._call_listener(listener_name, *a)
            if listener_name == 'pressed':
                self.notify_is_pressed()
            elif listener_name == 'pressed_delayed':
                self.is_held = True
                return
            elif listener_name == 'released':
                self.is_held = False
                self.notify_is_pressed()
                return

class LockableButtonControl(ButtonControl):
    pass
    is_locked = control_event('is_locked')

    class State(ButtonControl.State):

        @property
        def is_locked(self):
            pass
            return self._control_element is not None and self._control_element.is_locked

        def set_control_element(self, control_element):
            super().set_control_element(control_element)
            self.__on_is_locked_changed.subject = control_element
            self._notify_is_locked()

        def _notify_is_locked(self):
            self._call_listener('is_locked', self.is_locked)

        @listens('is_locked')
        def __on_is_locked_changed(self, _):
            self._notify_is_locked()

class TouchControl(ButtonControl):
    pass

    class State(ButtonControl.State):

        def set_control_element(self, control_element):
            super().set_control_element(control_element)