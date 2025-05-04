# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_DirectLink\DetailViewCntrlComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class DetailViewCntrlComponent(ControlSurfaceComponent):
    pass

    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._left_button = None
        self._right_button = None

    def disconnect(self):
        if self._left_button != None:
            self._left_button.remove_value_listener(self._nav_value)
            self._left_button = None
        if self._right_button != None:
            self._right_button.remove_value_listener(self._nav_value)
            self._right_button = None
            return
        else:
            return None

    def set_device_nav_buttons(self, left_button, right_button):
        identify_sender = True
        if self._left_button != None:
            self._left_button.remove_value_listener(self._nav_value)
        self._left_button = left_button
        if self._left_button != None:
            self._left_button.add_value_listener(self._nav_value, identify_sender)
        if self._right_button != None:
            self._right_button.remove_value_listener(self._nav_value)
        self._right_button = right_button
        if self._right_button != None:
            self._right_button.add_value_listener(self._nav_value, identify_sender)
        self.update()

    def on_enabled_changed(self):
        self.update()

    def update(self):
        super(DetailViewCntrlComponent, self).update()
        if self.is_enabled():
            if self._left_button != None:
                self._left_button.turn_off()
            if self._right_button != None:
                self._right_button.turn_off()
                return
        else:
            return

    def _nav_value(self, value, sender):
        if self.is_enabled() and (not sender.is_momentary() or value != 0):
            modifier_pressed = True
            if not self.application().view.is_view_visible('Detail') or not self.application().view.is_view_visible('Detail/DeviceChain'):
                self.application().view.show_view('Detail')
                self.application().view.show_view('Detail/DeviceChain')
                return
            else:
                direction = Live.Application.Application.View.NavDirection.left
                if sender == self._right_button:
                    direction = Live.Application.Application.View.NavDirection.right
                self.application().view.scroll_view(direction, 'Detail/DeviceChain', not modifier_pressed)
                return
        else:
            return