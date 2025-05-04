# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC20\ShiftableZoomingComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from past.utils import old_div
from _Framework.ButtonElement import ButtonElement
from _Framework.SessionZoomingComponent import DeprecatedSessionZoomingComponent

class ShiftableZoomingComponent(DeprecatedSessionZoomingComponent):
    pass

    def __init__(self, session, stop_buttons, *a, **k):
        super(ShiftableZoomingComponent, self).__init__(session, *a, **k)
        self._stop_buttons = stop_buttons
        self._ignore_buttons = False
        for button in self._stop_buttons:
            button.add_value_listener(self._stop_value, identify_sender=True)

    def disconnect(self):
        super(ShiftableZoomingComponent, self).disconnect()
        for button in self._stop_buttons:
            button.remove_value_listener(self._stop_value)

    def set_ignore_buttons(self, ignore):
        if self._ignore_buttons!= ignore:
            self._ignore_buttons = ignore
            if not self._is_zoomed_out:
                self._session.set_enabled(not ignore)
            self.update()

    def update(self):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self).update()
            return
        else:  # inserted
            if not self.is_enabled() or self._scene_bank_buttons!= None:
                    for button in self._scene_bank_buttons:
                        button.turn_off()
                    return None
                else:  # inserted
                    return None
            else:  # inserted
                return None

    def _stop_value(self, value, sender):
        if self.is_enabled() and (not self._ignore_buttons) and self._is_zoomed_out:
                    if value!= 0 or not sender.is_momentary():
                        self.song().stop_all_clips()
                        return
                else:  # inserted
                    return
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _zoom_value(self, value):
        if self.is_enabled():
            if self._zoom_button.is_momentary():
                self._is_zoomed_out = value > 0
            else:  # inserted
                self._is_zoomed_out = not self._is_zoomed_out
            if not self._ignore_buttons:
                if self._is_zoomed_out:
                    self._scene_bank_index = int(old_div(old_div(self._session.scene_offset(), self._session.height()), self._buttons.height()))
                else:  # inserted
                    self._scene_bank_index = 0
                self._session.set_enabled(not self._is_zoomed_out)
                if self._is_zoomed_out:
                    self.update()
                    return
            else:  # inserted
                return
        else:  # inserted
            return None

    def _matrix_value(self, value, x, y, is_momentary):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._matrix_value(value, x, y, is_momentary)

    def _nav_up_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_up_value(value)

    def _nav_down_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_down_value(value)

    def _nav_left_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_left_value(value)

    def _nav_right_value(self, value):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._nav_right_value(value)

    def _scene_bank_value(self, value, sender):
        if not self._ignore_buttons:
            super(ShiftableZoomingComponent, self)._scene_bank_value(value, sender)