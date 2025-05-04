# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\control\radio_button.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import nop
from .button import ButtonControlBase
from .control import control_color, control_event

class RadioButtonControl(ButtonControlBase):
    checked = control_event('checked')

    class State(ButtonControlBase.State):
        unchecked_color = control_color('DefaultButton.Off')
        checked_color = control_color('DefaultButton.On')

        def __init__(self, unchecked_color=None, checked_color=None, *a, **k):
            super(RadioButtonControl.State, self).__init__(*a, **k)
            if unchecked_color is not None:
                self.unchecked_color = unchecked_color
            if checked_color is not None:
                self.checked_color = checked_color
            self._checked = False
            self._on_checked = nop

        @property
        def is_checked(self):
            return self._checked

        @is_checked.setter
        def is_checked(self, value):
            if self._checked != value:
                self._checked = value
                if self._checked:
                    self._on_checked()
                self._send_current_color()

        def _send_button_color(self):
            self._control_element.set_light(self.checked_color if self._checked else self.unchecked_color)

        def _on_pressed(self):
            super(RadioButtonControl.State, self)._on_pressed()
            if not self._checked:
                self._checked = True
                self._notify_checked()

        def _notify_checked(self):
            if self._checked:
                self._call_listener('checked')
                self._on_checked()