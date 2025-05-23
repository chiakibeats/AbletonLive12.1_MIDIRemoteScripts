# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\device_component_provider.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import depends, listenable_property, listens, liveobj_changed
from ableton.v2.control_surface.mode import ModesComponent
from .auto_filter import AutoFilterDeviceComponent
from .channel_eq import ChannelEqDeviceComponent
from .chorus2 import Chorus2DeviceComponent
from .compressor import CompressorDeviceComponent
from .corpus import CorpusDeviceComponent
from .delay import DelayDeviceComponent
from .device_component import GenericDeviceComponent
from .drift import DriftDeviceComponent
from .echo import EchoDeviceComponent
from .eq8 import Eq8DeviceComponent
from .hybrid_reverb import HybridReverbDeviceComponent
from .operator import OperatorDeviceComponent
from .real_time_channel import RealTimeDataComponent
from .roar import RoarDeviceComponent
from .shifter import ShifterDeviceComponent
from .simpler import SimplerDeviceComponent
from .wavetable import WavetableDeviceComponent
DEVICE_COMPONENT_MODES = {'Generic': GenericDeviceComponent, 'OriginalSimpler': SimplerDeviceComponent, 'Eq8': Eq8DeviceComponent, 'Compressor2': CompressorDeviceComponent, 'Chorus2': Chorus2DeviceComponent, 'Corpus': CorpusDeviceComponent, 'InstrumentVector': WavetableDeviceComponent, 'Operator': OperatorDeviceComponent, 'Echo': EchoDeviceComponent, 'AutoFilter': AutoFilterDeviceComponent, 'ChannelEq': ChannelEqDeviceComponent, 'Delay': DelayDeviceComponent, 'Hybrid': HybridReverbDeviceComponent, 'Shifter': ShifterDeviceComponent, 'Drift': DriftDeviceComponent, 'Roar': RoarDeviceComponent}

class DeviceComponentProvider(ModesComponent):
    pass
    __events__ = ('device',)
    DEFAULT_SHRINK_PARAMETERS = [False] * 8

    @depends(device_provider=None)
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    def __init__(self, device_component_layer=None, device_decorator_factory=None, banking_info=None, device_bank_registry=None, device_provider=None, delete_button=None, decoupled_parameter_list_change_notifications=False, *a, **k):
        super(DeviceComponentProvider, self).__init__(*a, **k)
        self._shrink_parameters_dirty = False
        self._decoupled_parameter_list_change_notifications = decoupled_parameter_list_change_notifications
        self._is_drum_pad_selected = False
        self._device_provider = device_provider
        self._visualisation_real_time_data = RealTimeDataComponent(channel_type='visualisation', parent=self)
        self.__on_visualisation_attached.subject = self._visualisation_real_time_data
        self.__on_visualisation_channel_changed.subject = self._visualisation_real_time_data
        self._device_component_modes = {}
        for mode_name, component_class in DEVICE_COMPONENT_MODES.items():
            self._device_component_modes[mode_name] = component_class(parent=self, device_decorator_factory=device_decorator_factory, banking_info=banking_info, device_bank_registry=device_bank_registry, device_provider=device_provider, name='{}DeviceComponent'.format(mode_name), visualisation_real_time_data=self._visualisation_real_time_data, is_enabled=False, delete_button=delete_button, decoupled_parameter_list_change_notifications=self._decoupled_parameter_list_change_notifications)
        for mode_name, device_component in self._device_component_modes.items():
            self.add_mode(mode_name, [device_component, (device_component, device_component_layer)])
        self.selected_mode = 'Generic'
        self.__on_provided_device_changed.subject = device_provider
        self.__on_provided_device_changed()
        self.__on_selected_track_changed.subject = self.song.view

    def set_device(self, device):
        self._device_provider.device = device

    def _set_device(self, device):
        name = device.class_name if device and device.class_name in self._device_component_modes else 'Generic'
        self.selected_mode = name
        device_component = self._device_component_modes[name]
        self.__on_parameters_changed.subject = device_component
        self.__on_shrink_parameters_changed.subject = device_component
        self.__on_options_changed.subject = device_component
        self.__on_visualisation_visible_changed.subject = device_component
        device_component.set_device(device)
        self._notify_or_mark_as_dirty_shrink_parameters()
        self._visualisation_real_time_data.set_data(device)

    def set_drum_pad_selected(self, is_selected):
        if self._is_drum_pad_selected!= is_selected:
            self._is_drum_pad_selected = is_selected
            self._notify_or_mark_as_dirty_shrink_parameters()
            self.notify_visualisation_real_time_channel_id()

    @property
    def device_component(self):
        return self._device_component_modes[self.selected_mode or 'Generic']

    @listenable_property
    def parameters(self):
        return self.device_component.parameters

    @listenable_property
    def shrink_parameters(self):
        return self.device_component.shrink_parameters if not self._is_drum_pad_selected else self.DEFAULT_SHRINK_PARAMETERS

    @listenable_property
    def options(self):
        return self.device_component.options

    def device(self):
        return self.device_component.device()

    def device_changed(self, device):
        current_device = getattr(self.device(), '_live_object', self.device())
        return liveobj_changed(current_device, device)

    def notify_changes(self):
        pass
        if self._shrink_parameters_dirty:
            self._shrink_parameters_dirty = False
            self.notify_shrink_parameters()

    @listens('device')
    def __on_provided_device_changed(self):
        device = self._device_provider.device
        if self.device_changed(device):
            self._set_device(device)
            self.notify_device()
            return

    @listens('parameters')
    def __on_parameters_changed(self):
        self.notify_parameters()
        self.device_component.parameters_changed()

    def _notify_or_mark_as_dirty_shrink_parameters(self):
        if self._decoupled_parameter_list_change_notifications:
            self._shrink_parameters_dirty = True
            return
        else:  # inserted
            self.notify_shrink_parameters()

    @listens('shrink_parameters')
    def __on_shrink_parameters_changed(self):
        self._notify_or_mark_as_dirty_shrink_parameters()

    @listens('options')
    def __on_options_changed(self):
        self.notify_options()

    @listens('attached')
    def __on_visualisation_attached(self):
        self.device_component.initialize_visualisation_view_data()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self.device_component.initialize_visualisation_view_data()

    @listens('channel_id')
    def __on_visualisation_channel_changed(self):
        self.notify_visualisation_real_time_channel_id()

    @listenable_property
    def visualisation_real_time_channel_id(self):
        return self._visualisation_real_time_data.channel_id if not self.device_component.visualisation_visible or not self._is_drum_pad_selected else None
        else:  # inserted
            return None

    @listens('visualisation_visible')
    def __on_visualisation_visible_changed(self):
        self.notify_visualisation_real_time_channel_id()

    def disconnect(self):
        super(DeviceComponentProvider, self).disconnect()
        self._visualisation_real_time_data.set_data(None)