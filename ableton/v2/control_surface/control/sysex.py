# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\control\sysex.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .control import Control, control_color

class ColorSysexControl(Control):

    class State(Control.State):
        color = control_color('DefaultButton.Disabled')

        def __init__(self, color=None, *a, **k):
            super(ColorSysexControl.State, self).__init__(*a, **k)
            if color is not None:
                self.color = color

        def set_control_element(self, control_element):
            super(ColorSysexControl.State, self).set_control_element(control_element)
            self._send_current_color()

        def update(self):
            super(ColorSysexControl.State, self).update()
            self._send_current_color()

        def _send_current_color(self):
            if self._control_element:
                self._control_element.set_light(self.color)

    def __init__(self, *a, **k):
        super(ColorSysexControl, self).__init__(extra_args=a, extra_kws=k)