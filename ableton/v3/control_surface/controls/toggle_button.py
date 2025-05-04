# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\controls\toggle_button.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from . import ButtonControl, Connectable, control_event

class ToggleButtonControl(ButtonControl):
    pass
    toggled = control_event('toggled')

    class State(ButtonControl.State, Connectable):
        pass
        requires_listenable_connected_property = True

        def connect_property(self, *a):
            pass
            super().connect_property(*a)
            self.is_on = self.connected_property_value

        def on_connected_property_changed(self, value):
            self.is_on = value

        def _on_pressed(self):
            super()._on_pressed()
            self.is_on = not self._is_on
            self._call_listener('toggled', self.is_on)
            self.connected_property_value = self.is_on