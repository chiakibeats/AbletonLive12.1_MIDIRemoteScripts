# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\device.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from typing import cast
from ableton.v2.control_surface.simpler_slice_nudging import SimplerSliceNudging
from ...base import depends, find_if, listenable_property, listens
from ...live import deduplicate_parameters, liveobj_changed, liveobj_valid
from .. import DEFAULT_BANK_SIZE, BankingInfo, Component, ParameterProvider, create_parameter_bank, legacy_bank_definitions
from ..controls import MappedButtonControl, ToggleButtonControl
from ..default_bank_definitions import BANK_DEFINITIONS
from ..device_decorators import DeviceDecoratorFactory
from ..display import Renderable
from ..parameter_info import ParameterInfo
from ..parameter_mapping_sensitivities import DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY, parameter_mapping_sensitivities
from .device_bank_navigation import DeviceBankNavigationComponent
from .device_parameters import DeviceParametersComponent

def get_on_off_parameter(device):
    pass
    if liveobj_valid(device):
        return find_if(lambda p: p.original_name.startswith('Device On') and liveobj_valid(p) and p.is_enabled, device.parameters)
    else:  # inserted
        return None

def create_device_decorator_factory(device_decorator_factory, bank_definitions):
    pass
    if bank_definitions not in (legacy_bank_definitions.banked(), legacy_bank_definitions.best_of_banks()):
        return device_decorator_factory or DeviceDecoratorFactory()
    else:  # inserted
        return None

class DeviceComponent(ParameterProvider, Component, Renderable):
    pass
    device_on_off_button = MappedButtonControl(color='Device.Off', on_color='Device.On')
    device_fold_button = ToggleButtonControl(color='Device.FoldOff', on_color='Device.FoldOn', enabled=False)
    device_lock_button = ToggleButtonControl(color='Device.LockOff', on_color='Device.LockOn')

    @depends(device_provider=None, device_bank_registry=None, toggle_lock=None, show_message=None)
    def __init__(self, name='Device', continuous_parameter_sensitivity=DEFAULT_CONTINUOUS_PARAMETER_SENSITIVITY, quantized_parameter_sensitivity=DEFAULT_QUANTIZED_PARAMETER_SENSITIVITY, parameters_component_type=None, bank_size=DEFAULT_BANK_SIZE, bank_definitions=None, bank_navigation_component_type=None, device_provider=None, device_bank_registry=None, device_decorator_factory=None, toggle_lock=None, show_message=None, *a, **k):
        self._decorated_device = None
        self._provided_parameters = []
        self._device_provider = device_provider
        self._device_bank_registry = device_bank_registry
        self._decorator_factory = create_device_decorator_factory(device_decorator_factory, bank_definitions)
        self._parameter_mapping_sensitivities = parameter_mapping_sensitivities(continuous_parameter_sensitivity=continuous_parameter_sensitivity, quantized_parameter_sensitivity=quantized_parameter_sensitivity)
        parameters_component_type = parameters_component_type or DeviceParametersComponent
        self._parameters_component = parameters_component_type()
        self._parameters_component.parameter_provider = self
        self._bank = None
        self._banking_info = BankingInfo(bank_definitions or BANK_DEFINITIONS, bank_size=bank_size)
        bank_navigation_component_type = bank_navigation_component_type or DeviceBankNavigationComponent
        self._bank_navigation_component = bank_navigation_component_type(banking_info=self._banking_info, device_bank_registry=device_bank_registry)
        super().__init__(*a, name=name, **k)
        self._toggle_lock = toggle_lock
        self._show_message = show_message
        self._slice_nudging = self.register_disconnectable(SimplerSliceNudging())
        self.add_children(self._parameters_component, self._bank_navigation_component)
        self.__on_provided_device_changed.subject = device_provider
        self.__on_provided_device_changed()
        self.register_slot(self._device_provider, self._update_device_lock_button, 'is_locked_to_device')
        self._update_device_lock_button()

    def disconnect(self):
        super().disconnect()
        self._disconnect_decorated_device()

    @property
    def parameters(self):
        pass
        return self._provided_parameters

    @listenable_property
    def device(self):
        pass
        return self._decorated_device

    @device.setter
    def device(self, device):
        self._device_provider.device = device

    @listenable_property
    def bank_name(self):
        pass
        return self._current_bank_details()[0] if self.device else ''

    def set_parameter_controls(self, controls):
        self._parameters_component.set_parameter_controls(controls)
        self._show_device_and_bank_info()

    def __getattr__(self, name):
        if name.startswith('set_') and 'bank' in name:
            return getattr(self._bank_navigation_component, name)
        else:  # inserted
            raise AttributeError

    @device_lock_button.toggled
    def device_lock_button(self, *_):
        self._toggle_lock()
        if liveobj_valid(self.device):
            self.notify(self.notifications.Device.lock, cast(str, self.device.name), self._device_provider.is_locked_to_device)

    @device_on_off_button.pressed
    def device_on_off_button(self, _):
        if liveobj_valid(self.device):
            self.notify(self.notifications.Device.on_off, cast(str, self.device.name), str(get_on_off_parameter(self.device)))

    @device_fold_button.pressed
    def device_fold_button(self, _):
        fold_state = not self.device.view.is_showing_chain_devices
        self.device.view.is_showing_chain_devices = fold_state
        self.notify(self.notifications.Device.fold, cast(str, self.device.name), fold_state)

    def _create_parameter_info(self, parameter, name):
        default, fine_grain = self._parameter_mapping_sensitivities(parameter, self.device)
        return ParameterInfo(parameter=parameter, name=name, default_encoder_sensitivity=default, fine_grain_encoder_sensitivity=fine_grain)

    def _set_device(self, device):
        self._set_decorated_device(self._get_decorated_device(device))
        device_bank_registry = self._device_bank_registry
        self.__on_bank_changed.subject = device_bank_registry
        self._set_bank_index(device_bank_registry.get_device_bank(device))
        self._update_parameters()
        self.__on_parameters_changed_in_device.subject = device
        self.device_on_off_button.mapped_parameter = get_on_off_parameter(device)
        is_rack = liveobj_valid(device) and device.can_have_chains
        self.__on_is_showing_chain_devices_changed.subject = device.view if is_rack else None
        self.device_fold_button.enabled = is_rack
        if is_rack:
            self.__on_is_showing_chain_devices_changed()
        self.notify_device()
        self.notify_bank_name()

    def _get_decorated_device(self, device):
        return self._decorator_factory.decorate(device) if self._decorator_factory is not None else device

    def _set_decorated_device(self, decorated_device):
        self._disconnect_decorated_device()
        self._decorated_device = decorated_device
        self._slice_nudging.set_device(decorated_device)
        self._setup_bank(decorated_device)
        self.__on_bank_parameters_changed.subject = self._bank

    def _disconnect_decorated_device(self):
        if hasattr(self._decorated_device, 'disconnect'):
            self._decorated_device.disconnect()
            return
        else:  # inserted
            return None

    def _on_device_changed(self, device):
        current_device = getattr(self.device, '_live_object', self.device)
        if liveobj_changed(current_device, device):
            self._set_device(device)

    def _setup_bank(self, device, bank_factory=create_parameter_bank):
        if self._bank is not None:
            self.disconnect_disconnectable(self._bank)
            self._bank = None
        if liveobj_valid(device):
            self._bank = self.register_disconnectable(bank_factory(device, self._banking_info))
        self._bank_navigation_component.bank_provider = self._bank
        return

    def _set_bank_index(self, bank):
        if self._bank is not None:
            self._bank.index = bank
        if liveobj_valid(self.device):
            self.notify_bank_name()
            self._show_device_and_bank_info()
            return
        else:  # inserted
            return None

    def _current_bank_details(self):
        return (self._bank.name, self._bank.parameters) if self._bank is not None else ('', [None] * self._parameters_component.controls.control_count)

    def _show_device_and_bank_info(self):
        device = self.device
        if not liveobj_valid(device) or self._parameters_component.controls[0].control_element:
                self._show_message('Controlling {}: {}'.format(device.name, self.bank_name))

    def _get_provided_parameters(self):
        return self._current_bank_details() if self.device else None
        else:  # inserted
            _, parameters = (None, ())
        parameter_infos = [self._create_parameter_info(param, name) for param, name in parameters]
        return deduplicate_parameters(parameter_infos) if self._banking_info.num_simultaneous_banks > 1 else parameter_infos

    def _update_parameters(self):
        self._provided_parameters = self._get_provided_parameters()
        self.notify_parameters()

    def _update_device_lock_button(self):
        self.device_lock_button.is_on = self._device_provider.is_locked_to_device

    @listens('is_showing_chain_devices')
    def __on_is_showing_chain_devices_changed(self):
        self.device_fold_button.is_on = self.device.view.is_showing_chain_devices

    @listens('device')
    def __on_provided_device_changed(self):
        self._on_device_changed(self._device_provider.device)

    @listens('device_bank')
    def __on_bank_changed(self, device, bank):
        if device == self.device:
            self._set_bank_index(bank)

    @listens('parameters')
    def __on_parameters_changed_in_device(self):
        self._update_parameters()

    @listens('parameters')
    def __on_bank_parameters_changed(self):
        self._update_parameters()
        self._device_bank_registry.set_device_bank(self.device, self._bank.index)