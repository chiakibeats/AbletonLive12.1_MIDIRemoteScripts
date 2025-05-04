# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Generic\SpecialMixerComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.MixerComponent import MixerComponent
from .SelectChanStripComponent import SelectChanStripComponent

class SpecialMixerComponent(MixerComponent):
    pass

    def _create_strip(self):
        return SelectChanStripComponent()

    def set_bank_up_button(self, button):
        self.set_bank_buttons(button, self._bank_down_button)

    def set_bank_down_button(self, button):
        self.set_bank_buttons(self._bank_up_button, button)