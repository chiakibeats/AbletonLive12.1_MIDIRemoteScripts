# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\device.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v2.base import clamp, listens, liveobj_valid
from ableton.v2.control_surface import ParameterInfo
from ableton.v2.control_surface.components import DeviceComponent as DeviceComponentBase
from ableton.v2.control_surface.control import ButtonControl, TextDisplayControl, ToggleButtonControl

class DeviceComponent(DeviceComponentBase):
    prev_bank_button = ButtonControl(color='Action.Off', pressed_color='Action.On')
    next_bank_button = ButtonControl(color='Action.Off', pressed_color='Action.On')
    bank_name_display = TextDisplayControl()
    device_lock_button = ToggleButtonControl()

    def __init__(self, toggle_lock=None, *a, **k):
        super(DeviceComponent, self).__init__(*a, **k)
        self._toggle_lock = toggle_lock
        self.__on_is_locked_to_device_changed.subject = self._device_provider
        self.__on_is_locked_to_device_changed()

    @prev_bank_button.pressed
    def prev_bank_button(self, _):
        self._scroll_bank(-1)

    @next_bank_button.pressed
    def next_bank_button(self, _):
        self._scroll_bank(1)

    @device_lock_button.toggled
    def device_lock_button(self, toggled, _):
        self._toggle_lock()
        self._update_device_lock_button()

    def _create_parameter_info(self, parameter, name):
        return ParameterInfo(parameter=parameter, name=name, default_encoder_sensitivity=1.0)

    def _set_bank_index(self, index):
        super(DeviceComponent, self)._set_bank_index(index)
        self._update_bank_name_display()

    def _scroll_bank(self, offset):
        bank = self._bank
        if bank:
            new_index = clamp(bank.index + offset, 0, bank.bank_count() - 1)
            self._device_bank_registry.set_device_bank(self.device(), new_index)

    def _update_bank_name_display(self):
        bank_name = ''
        device = self.device()
        if liveobj_valid(device):
            device_bank_names = self._banking_info.device_bank_names(device)
            if device_bank_names:
                bank_name = device_bank_names[self._device_bank_registry.get_device_bank(device)]
        self.bank_name_display[0] = bank_name
        return

    def _update_device_lock_button(self):
        self.device_lock_button.is_toggled = self._device_provider.is_locked_to_device

    @listens('is_locked_to_device')
    def __on_is_locked_to_device_changed(self):
        self._update_device_lock_button()