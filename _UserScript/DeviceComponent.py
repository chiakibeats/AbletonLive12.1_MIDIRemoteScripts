# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_UserScript\DeviceComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.DeviceComponent import DeviceComponent as DeviceComponentBase
from ableton.v2.base import liveobj_valid, nop

class DeviceComponent(DeviceComponentBase):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._num_banks_to_control = 1
        self._empty_control_slots = self.register_slot_manager()

    def set_parameter_controls(self, controls):
        self._num_banks_to_control = 2 if controls and controls.width() > 8 else 1
        super().set_parameter_controls(controls)

    def _bank_up_value(self, value):
        if not self.is_enabled() or value:
                if self._bank_down_button is None:
                    self._cycle_bank_index()
                    return
                else:  # inserted
                    if self._can_bank_up():
                        self._increment_bank_index(1)
                        return
                    else:  # inserted
                        return None
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _bank_down_value(self, value):
        if self.is_enabled() and value and self._can_bank_down():
                    self._increment_bank_index((-1))

    def _increment_bank_index(self, delta):
        if liveobj_valid(self._device):
            delta = self._num_banks_to_control * delta
            self._bank_name = ''
            if self._bank_index is None:
                self._bank_index = 0
            else:  # inserted
                self._bank_index = max(0, min(self._number_of_parameter_banks() - 1, self._bank_index + delta))
            self.update()

    def _cycle_bank_index(self):
        if liveobj_valid(self._device):
            self._bank_name = ''
            if self._bank_index is None:
                self._bank_index = 0
            else:  # inserted
                self._bank_index = (self._bank_index + 1) % self._number_of_parameter_banks()
            self.update()
            return

    def _can_bank_up(self):
        return self._bank_index is None or self._number_of_parameter_banks() > self._bank_index + self._num_banks_to_control

    def _can_bank_down(self):
        return self._bank_index is None or self._bank_index > 0

    def update(self):
        self._empty_control_slots.disconnect()
        super().update()

    def _assign_parameters(self):
        self._bank_name, bank = self._current_bank_details()
        for control, parameter in zip(self._parameter_controls, bank):
            if control:
                if liveobj_valid(parameter):
                    control.connect_to(parameter)
                    continue
                else:  # inserted
                    control.release_parameter()
                    self._empty_control_slots.register_slot(control, nop, 'value')
            continue
        self._release_parameters(self._parameter_controls[len(bank):])

    def _release_parameters(self, controls):
        for control in controls or []:
            if control:
                control.release_parameter()
                self._empty_control_slots.register_slot(control, nop, 'value')
            continue

    def _current_bank_details(self):
        bank_name = self._bank_name
        bank = []
        best_of = self._best_of_parameter_bank()
        banks = self._parameter_banks()
        if banks:
            multiple_banks = self._num_banks_to_control > 1
            if self._bank_index is None or (not self._is_banking_enabled() and (not multiple_banks)):
                pass  # postinserted
            if not best_of:
                if self._bank_index is None or None:
                    pass  # postinserted
                else:  # inserted
                    index = 0
                bank = list(banks[index])
                bank_name = self._parameter_bank_names()[index]
                if multiple_banks and index < self._number_of_parameter_banks() - 1:
                    bank.extend(banks[index + 1])
                    bank_name += '  /  {}'.format(self._parameter_bank_names()[index + 1])
                pass
            else:  # inserted
                bank = best_of
                bank_name = 'Best of Parameters'
        return (bank_name, bank)

    def _update_device_bank_nav_buttons(self):
        if self.is_enabled():
            if self._bank_up_button:
                if liveobj_valid(self._device):
                    if self._bank_down_button is None:
                        self._bank_up_button.set_light(self._number_of_parameter_banks() > 1)
                    else:  # inserted
                        self._bank_up_button.set_light(self._can_bank_up())
                else:  # inserted
                    self._bank_up_button.set_light(False)
            if self._bank_down_button:
                self._bank_down_button.set_light(liveobj_valid(self._device) and self._can_bank_down())
                return
        else:  # inserted
            return