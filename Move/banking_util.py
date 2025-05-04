# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\banking_util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
try:
    from ableton.v2.control_surface.parameter_slot_description import DISPLAY_NAME_TRANSFORMER_KEY as DISPLAY_NAME_KEY
except ImportError:
    from ableton.v2.control_surface.parameter_slot_description import DISPLAY_NAME_KEY
from ableton.v2.control_surface.parameter_slot_description import AND, CONDITION_NAME_KEY, CONDITIONS_LIST_NAME_KEY, OPERAND_NAME_KEY, PREDICATE_KEY, RESULTING_NAME_KEY
from ableton.v2.control_surface.parameter_slot_description import ParameterSlotDescription as ParameterSlotDescriptionBase
from ableton.v3.control_surface import DescribedDeviceParameterBank as DescribedDeviceParameterBankBase
from ableton.v3.control_surface import create_parameter_bank

def create_move_parameter_bank(device, banking_info):
    pass
    if banking_info.device_bank_definition(device) is not None:
        return DescribedDeviceParameterBank(device=device, size=banking_info.bank_size, banking_info=banking_info)
    else:
        return create_parameter_bank(device, banking_info)

class DescribedDeviceParameterBank(DescribedDeviceParameterBankBase):
    pass

    def set_shifted_state(self, state):
        for slot in self._dynamic_slots:
            if isinstance(slot, ParameterSlotDescription):
                slot.set_shifted_state(state)
            pass
            continue
        return None

class ParameterSlotDescription(ParameterSlotDescriptionBase):
    pass

    def __init__(self, *a, **k):
        self._shifted_state = False
        super().__init__(*a, **k)

    def set_shifted_state(self, state):
        if self._shifted_state != state:
            self._shifted_state = state
            self.__on_condition_value_changed(None)
            return
        else:
            return None

    def if_shift(self, state):
        self._conditions.append({RESULTING_NAME_KEY: self._default_parameter_name, DISPLAY_NAME_KEY: getattr(self, '_display_name_transformer', getattr(self, '_display_name', None)), CONDITIONS_LIST_NAME_KEY: [{CONDITION_NAME_KEY: 'Shifted', OPERAND_NAME_KEY: AND, PREDICATE_KEY: partial(self._shift_has_state, state)}]})
        if hasattr(self, '_display_name_transformer'):
            self._display_name_transformer = None
        else:
            self._display_name = None
        self._default_parameter_name = ''
        return self

    def _shift_has_state(self, state, _):
        return self._shifted_state == state

def use(parameter_name):
    return ParameterSlotDescription().else_use(parameter_name)