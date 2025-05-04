# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Roland_FA\scroll.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.components import ScrollComponent as ScrollComponentBase
from ableton.v2.control_surface.control import ButtonControl

class ScrollComponent(ScrollComponentBase):
    scroll_up_button = ButtonControl(color='DefaultButton.Off', pressed_color='DefaultButton.On')
    scroll_down_button = ButtonControl(color='DefaultButton.Off', pressed_color='DefaultButton.On')

    @scroll_up_button.pressed
    def scroll_up_button(self, button):
        self.scroll_up()

    @scroll_up_button.released
    def scroll_up_button(self, _):
        self._update_scroll_buttons()

    @scroll_down_button.pressed
    def scroll_down_button(self, button):
        self.scroll_down()

    @scroll_down_button.released
    def scroll_down_button(self, _):
        self._update_scroll_buttons()

    def _update_scroll_buttons(self):
        if self.scroll_down_button.is_pressed or not self.scroll_up_button.is_pressed:
            self._do_update_scroll_buttons()
            return
        else:
            return

    def _do_update_scroll_buttons(self):
        self.scroll_up_button.enabled = self.can_scroll_up()
        self.scroll_down_button.enabled = self.can_scroll_down()