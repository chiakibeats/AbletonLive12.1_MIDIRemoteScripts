# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_parameter_bank_with_options.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import find_if, listenable_property, liveobj_valid
from ableton.v2.control_surface import DescribedDeviceParameterBank, create_device_bank
from .custom_bank_definitions import OPTIONS_KEY, VIEW_DESCRIPTION_KEY
OPTIONS_PER_BANK = 7

class DescribedDeviceParameterBankWithOptions(DescribedDeviceParameterBank):
    _options = []

    @listenable_property
    def options(self):
        return self._options

    @property
    def bank_view_description(self):
        bank = self._definition.value_by_index(self.index)
        return str(bank.get(VIEW_DESCRIPTION_KEY, ''))

    def _current_option_slots(self):
        bank = self._definition.value_by_index(self.index)
        return bank.get(OPTIONS_KEY) or ('',) * OPTIONS_PER_BANK

    def _content_slots(self):
        return self._current_option_slots() + super(DescribedDeviceParameterBankWithOptions, self)._content_slots()

    def _collect_options(self):
        option_slots = self._current_option_slots()
        options = getattr(self._device, 'options', [])
        return [find_if(lambda o: o.name == str(slot_definition), options) for slot_definition in option_slots]

    def _update_parameters(self):
        super(DescribedDeviceParameterBankWithOptions, self)._update_parameters()
        self._options = self._collect_options()
        self.notify_options()

def create_device_bank_with_options(device, banking_info):
    if liveobj_valid(device) and banking_info.device_bank_definition(device) is not None:
        bank = DescribedDeviceParameterBankWithOptions(device=device, size=8, banking_info=banking_info)
    else:
        bank = create_device_bank(device, banking_info)
    return bank