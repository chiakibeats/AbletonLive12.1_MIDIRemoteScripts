# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\device_parameter_bank.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ..base import EventObject, clamp, find_if, listenable_property, listens, listens_group, liveobj_valid, old_hasattr
from .banking_util import BANK_FORMAT, BANK_MAIN_KEY, BANK_PARAMETERS_KEY, all_parameters

class DeviceParameterBank(EventObject):

    def __init__(self, size=None, device=None, banking_info=None, *a, **k):
        super(DeviceParameterBank, self).__init__(*a, **k)
        self._size = size
        self._device = device
        self._banking_info = banking_info
        self._index = 0
        self._parameters = None
        self._on_parameters_changed.subject = device
        self._update_parameters()

    def bank_count(self):
        return self._banking_info.device_bank_count(self._device, bank_size=self._size)

    def _adjust_index(self, index):
        return clamp(index, 0, max(0, self.bank_count() - 1))

    def _is_index_valid(self, index):
        if index is None:
            return False
        else:
            return self.bank_count() > index

    def _get_index(self):
        return self._index

    def _set_index(self, index):
        if self._index != index and self._is_index_valid(index):
            index = self._adjust_index(index)
            self._index = index
            self._update_parameters()
    index = property(_get_index, _set_index)

    @listens('parameters')
    def _on_parameters_changed(self):
        self._index = self._adjust_index(self._index)
        self._update_parameters()

    @listenable_property
    def parameters(self):
        return self._parameters

    def _calc_name(self):
        return BANK_FORMAT % (self.index + 1)

    @property
    def name(self):
        return self._calc_name() if liveobj_valid(self._device) else ''

    @property
    def device(self):
        return self._device

    def _collect_parameters(self):
        parameters = all_parameters(self._device)
        offset = self._index * self._size
        params = parameters[offset:]
        params.extend([None] * (self._size - len(params)))
        return [(param, None) for param in params]

    def _update_parameters(self):
        parameters = self._collect_parameters()[:self._size]
        if self._parameters != parameters:
            self._parameters = parameters
            self.notify_parameters()

class DescribedDeviceParameterBank(DeviceParameterBank):

    def __init__(self, device=None, banking_info=None, *a, **k):
        self._definition = banking_info.device_bank_definition(device)
        self._dynamic_slots = []
        super(DescribedDeviceParameterBank, self).__init__(*a, device=device, banking_info=banking_info, **k)
        self._update_parameters()

    @listens_group('content')
    def _on_slot_content_changed(self, _slot):
        self._update_parameters()

    def _current_parameter_slots(self):
        return self._definition.value_by_index(self.index).get(BANK_PARAMETERS_KEY) or tuple()

    def _content_slots(self):
        return self._current_parameter_slots()

    def _setup_dynamic_slots(self):
        for slot in self._dynamic_slots:
            slot.set_parameter_host(None)
            self.unregister_disconnectable(slot)
        self._dynamic_slots = list(filter(lambda s: old_hasattr(s, 'notify_content'), self._content_slots()))
        for slot in self._dynamic_slots:
            self.register_disconnectable(slot)
            slot.set_parameter_host(self.device)
        self._on_slot_content_changed.replace_subjects(self._dynamic_slots)

    def _calc_name(self):
        return self._definition.key_by_index(self.index)

    def _collect_parameters(self):
        parameters = self._device.parameters
        bank_slots = self._current_parameter_slots()

        def _collect_parameter(slot_definition):
            parameter = find_if(lambda p: p.original_name == str(slot_definition), parameters)
            display_name_transformer = getattr(slot_definition, 'display_name_transformer', None)
            return parameter and ((parameter, display_name_transformer and display_name_transformer(parameter.name)) or (None, None))
        return [_collect_parameter(slot_definition) for slot_definition in bank_slots]

    def _update_parameters(self):
        self._setup_dynamic_slots()
        super(DescribedDeviceParameterBank, self)._update_parameters()
        self._on_parameter_name_changed.replace_subjects([parameter for parameter, name in self._parameters])

    @listens_group('name')
    def _on_parameter_name_changed(self, parameter):
        self._update_parameters()

class MaxDeviceParameterBank(DeviceParameterBank):

    def __init__(self, *a, **k):
        super(MaxDeviceParameterBank, self).__init__(*a, **k)
        self._on_bank_parameters_changed.subject = self.device

    def _calc_name(self):
        if self.bank_count() == 0:
            return BANK_MAIN_KEY
        else:
            mx_index = self.index - int(self._banking_info.has_main_bank(self._device))
            provided_name = self.device.get_bank_name(mx_index)
            return provided_name if len(provided_name) > 0 else super(MaxDeviceParameterBank, self)._calc_name()

    @listens('bank_parameters_changed')
    def _on_bank_parameters_changed(self):
        self._update_parameters()

    def _collect_parameters(self):
        if self.bank_count() == 0:
            return [(None, None)] * self._size
        else:
            parameters = self._device.parameters
            mx_index = self.index - int(self._banking_info.has_main_bank(self._device))
            indices = self.device.get_bank_parameters(mx_index)
            parameters = [parameters[index] if index >= 0 else None for index in indices]
            return [(param, None) for param in parameters]

def create_device_bank(device, banking_info):
    bank = None
    if liveobj_valid(device):
        if banking_info.has_bank_count(device):
            bank_class = MaxDeviceParameterBank
        elif banking_info.device_bank_definition(device) is not None:
            bank_class = DescribedDeviceParameterBank
        else:
            bank_class = DeviceParameterBank
        bank = bank_class(device=device, size=8, banking_info=banking_info)
    return bank