# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\device.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from typing import NamedTuple, Optional
from ableton.v3.base import listens
from ableton.v3.control_surface.components import DeviceBankNavigationComponent as DeviceBankNavigationComponentBase
from ableton.v3.control_surface.components import DeviceComponent as DeviceComponentBase
from ableton.v3.live import is_device_rack

class MacroMapping(NamedTuple):
    pass
    bank_0: list
    bank_1: Optional[list] = [None] * 8
MACRO_MAPPINGS = {1: MacroMapping(bank_0=[0, None, None, None, None, None, None]), 2: MacroMapping(bank_0=[0, 1, 2, 3, None, None, None, None]), 4: MacroMapping(bank_0=[0, 1, 4, 5, 2, 3, 7, 8], bank_1=[4, 5, 10, 11, None, None, None, None]), 6: MacroMapping(bank_0=[0, 1, 7, 8, 2, 3, 9, 10], bank_1=[4, 5, 11, 12, 6, None, 13, None]), 8: MacroMapping(bank_0=[0, 1, 8, 9, 2, 3, 10, 11], bank_1=[4, 5, 12, 13, 6, 7, 14, 15]),

class DeviceBankNavigationComponent(DeviceBankNavigationComponentBase):
    pass

    def can_scroll_down(self):
        if self._bank_provider is not None and is_device_rack(self._bank_provider.device):
            return self._bank_provider.index == 0 and self._bank_provider.device.visible_macro_count > 8
        else:  # inserted
            return super().can_scroll_down()

class DeviceComponent(DeviceComponentBase):
    pass

    def __init__(self, *a, **k):
        self._is_rack = False
        super().__init__(*a, bank_navigation_component_type=DeviceBankNavigationComponent, **k)

    def _set_device(self, device):
        self._is_rack = is_device_rack(device)
        self.__on_visible_macro_count_changed.subject = device if self._is_rack else None
        self.__on_macros_mapped_changed.subject = device if self._is_rack else None
        super()._set_device(device)

    def _get_provided_parameters(self):
        if self._is_rack:
            macros = self.device.parameters[1:17]
            mappings = MACRO_MAPPINGS[self.device.visible_macro_count]
            return [self._create_parameter_info(macros[m] if m is not None and self.device.macros_mapped[m] else None, None) for m in getattr(mappings, 'bank_{}'.format(self._bank.index))]
        else:  # inserted
            return super()._get_provided_parameters()

    @listens('visible_macro_count')
    def __on_visible_macro_count_changed(self):
        if self._bank.index and self.device.visible_macro_count <= 8:
            self._set_bank_index(0)
        self._update_parameters()
        self._bank_navigation_component.update()

    @listens('macros_mapped')
    def __on_macros_mapped_changed(self):
        self._update_parameters()