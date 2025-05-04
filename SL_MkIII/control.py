# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\control.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.control import ConfigurableTextDisplayControl as ConfigurableTextDisplayControlBase
from ableton.v2.control_surface.control import Control
from ableton.v2.control_surface.control import TextDisplayControl as TextDisplayControlBase

class BinaryControl(Control):

    class State(Control.State):
        ON_VALUE = 1
        OFF_VALUE = 0

        def __init__(self, *a, **k):
            super(BinaryControl.State, self).__init__(*a, **k)
            self._is_on = False

        @property
        def is_on(self):
            return self._is_on

        @is_on.setter
        def is_on(self, value):
            if self._is_on != value:
                self._is_on = value
                self._send_current_value()

        def set_control_element(self, control_element):
            super(BinaryControl.State, self).set_control_element(control_element)
            self._send_current_value()

        def update(self):
            super(BinaryControl.State, self).update()
            self._send_current_value()

        def _send_current_value(self):
            if self._control_element:
                self._control_element.send_value(self.ON_VALUE if self.is_on else self.OFF_VALUE)

class TextDisplayControl(TextDisplayControlBase):

    class State(TextDisplayControlBase.State):

        def set_control_element(self, control_element):
            set_control_element(self, control_element)

class ConfigurableTextDisplayControl(ConfigurableTextDisplayControlBase):

    class State(ConfigurableTextDisplayControlBase.State):

        def set_control_element(self, control_element):
            set_control_element(self, control_element)

def set_control_element(self, control_element):
    Control.State.set_control_element(self, control_element)
    if control_element:
        control_element.set_data_sources(self._data_sources)