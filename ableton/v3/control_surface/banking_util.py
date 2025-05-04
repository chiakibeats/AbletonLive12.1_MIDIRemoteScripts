# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\banking_util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from math import ceil
from ableton.v2.control_surface import BankingInfo as BankingInfoBase
from ableton.v2.control_surface import DescribedDeviceParameterBank as DescribedDeviceParameterBankBase
from ableton.v2.control_surface.device_parameter_bank import DeviceParameterBank
from ableton.v2.control_surface.device_parameter_bank import MaxDeviceParameterBank as MaxDeviceParameterBankBase
from ..live import liveobj_valid
from . import BANK_FORMAT, BANK_PARAMETERS_KEY, all_parameters
BANK_NAME_JOIN_STR = ' and '
DEFAULT_BANK_SIZE = 8
pass

def create_parameter_bank(device, banking_info):
    pass
    bank = None
    if liveobj_valid(device):
        bank_class = DeviceParameterBank
        size = banking_info.bank_size
        if size >= DEFAULT_BANK_SIZE:
            if banking_info.has_bank_count(device):
                bank_class = MaxDeviceParameterBank
            elif banking_info.device_bank_definition(device) is not None:
                bank_class = DescribedDeviceParameterBank
        bank = bank_class(device=device, size=size, banking_info=banking_info)
    return bank

class DescribedDeviceParameterBank(DescribedDeviceParameterBankBase):
    pass

    def _current_parameter_slots(self):
        next_index = self.index + 1
        bank_count = self._banking_info.device_bank_count(self._device)
        if self._size > DEFAULT_BANK_SIZE and next_index < bank_count:
            result = (self._definition.value_by_index(self.index).get(BANK_PARAMETERS_KEY) or tuple()) + (self._definition.value_by_index(next_index).get(BANK_PARAMETERS_KEY) or tuple())
            return result
        else:
            return super()._current_parameter_slots()

    def _calc_name(self):
        if self._size > DEFAULT_BANK_SIZE:
            return self._banking_info.device_bank_names(self._device)[self.index]
        else:
            return super()._calc_name()

class MaxDeviceParameterBank(MaxDeviceParameterBankBase):
    pass

    def _collect_parameters(self):
        bank_count = self._banking_info.device_bank_count(self._device)
        if bank_count == 0:
            return [(None, None)] * self._size
        else:
            bank = self._get_parameters_for_bank_index(self.index)
            next_index = self.index + 1
            if self._size > DEFAULT_BANK_SIZE and next_index < bank_count:
                bank.extend(self._get_parameters_for_bank_index(next_index))
            return bank

    def _get_parameters_for_bank_index(self, bank_index):
        parameters = self._device.parameters
        mx_index = bank_index - int(self._banking_info.has_main_bank(self._device))
        indices = self.device.get_bank_parameters(mx_index)
        parameters = [parameters[index] if index >= 0 else None for index in indices]
        return [(param, None) for param in parameters]

    def _calc_name(self):
        bank_count = self._banking_info.device_bank_count(self._device)
        if self._size > DEFAULT_BANK_SIZE and self.index < bank_count:
            return self._banking_info.device_bank_names(self._device)[self.index]
        else:
            return super()._calc_name()

class BankingInfo(BankingInfoBase):
    pass

    def __init__(self, bank_definitions, bank_size=DEFAULT_BANK_SIZE, *a, **k):
        super().__init__(bank_definitions, *a, **k)
        self._bank_size = bank_size
        self._num_simultaneous_banks = 2 if bank_size > DEFAULT_BANK_SIZE else 1

    @property
    def bank_size(self):
        pass
        return self._bank_size

    @property
    def num_simultaneous_banks(self):
        pass
        return self._num_simultaneous_banks

    def device_bank_count(self, device, **k):
        pass
        if self._bank_size < DEFAULT_BANK_SIZE:
            return ceil(float(len(all_parameters(device))) / self._bank_size)
        else:
            return super().device_bank_count(device, **k)

    def device_bank_names(self, device, **k):
        pass
        if self._bank_size < DEFAULT_BANK_SIZE:
            return [BANK_FORMAT % (index + 1) for index in range(self.device_bank_count(device))]
        else:
            names = super().device_bank_names(device, **k)
            if self._num_simultaneous_banks == 2 and len(names) > 1:
                result = [BANK_NAME_JOIN_STR.join(n) for n in [(names[i], names[i + 1]) for i in range(len(names) - 1)]]
                result.append(names[-1])
                return result
            else:
                return names