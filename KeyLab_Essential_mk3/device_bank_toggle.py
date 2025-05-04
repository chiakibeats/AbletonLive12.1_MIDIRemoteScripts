# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential_mk3\device_bank_toggle.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import listenable_property
from ableton.v3.control_surface.components import DeviceBankNavigationComponent
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.control_surface.display import Renderable

class DeviceBankToggleComponent(DeviceBankNavigationComponent, Renderable):
    pass
    bank_index = listenable_property.managed(0)
    has_changed_bank_index = listenable_property.managed(False)
    bank_toggle_button = ButtonControl()

    def set_bank_toggle_button(self, button):
        self.bank_toggle_button.set_control_element(button)

    @bank_toggle_button.pressed
    def bank_toggle_button(self, _):
        self._bank_provider.index = 2 if self._bank_provider.index == 0 else 0
        self.has_changed_bank_index = True

    def update(self):
        super().update()
        can_bank = self._bank_provider is not None and self._adjusted_bank_count() > 1
        self.bank_index = self._bank_provider.index if can_bank else 0
        self.bank_toggle_button.enabled = can_bank
        if can_bank:
            self.bank_toggle_button.color = 'Banking.PageOne' if self._bank_provider.index == 0 else 'Banking.PageTwo'