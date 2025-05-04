# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\TrackFilterComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Generic.Devices import get_parameter_by_name
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.EncoderElement import EncoderElement
FILTER_DEVICES = {'AutoFilter': {'Frequency': 'Frequency', 'Resonance': 'Resonance'}, 'Operator': {'Frequency': 'Filter Freq', 'Resonance': 'Filter Res'}, 'OriginalSimpler': {'Frequency': 'Filter Freq', 'Resonance': 'Filter Res'}, 'MultiSampler': {'Frequency': 'Filter Freq', 'Resonance': 'Filter Res'}, 'UltraAnalog': {'Frequency': 'F1 Freq', 'Resonance': 'F1 Resonance'}, 'StringStudio': {'Frequency': 'Filter Freq', 'Resonance': 'Filter Reso'}}

class TrackFilterComponent(ControlSurfaceComponent):
    pass

    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._track = None
        self._device = None
        self._freq_control = None
        self._reso_control = None

    def disconnect(self):
        if self._freq_control != None:
            self._freq_control.release_parameter()
            self._freq_control = None
        if self._reso_control != None:
            self._reso_control.release_parameter()
            self._reso_control = None
        if self._track != None:
            self._track.remove_devices_listener(self._on_devices_changed)
            self._track = None
        self._device = None
        return

    def on_enabled_changed(self):
        self.update()

    def set_track(self, track):
        if self._track != None:
            self._track.remove_devices_listener(self._on_devices_changed)
            if self._device != None:
                if self._freq_control != None:
                    self._freq_control.release_parameter()
                if self._reso_control != None:
                    self._reso_control.release_parameter()
        self._track = track
        if self._track != None:
            self._track.add_devices_listener(self._on_devices_changed)
        self._on_devices_changed()

    def set_filter_controls(self, freq, reso):
        if self._device != None:
            if self._freq_control != None:
                self._freq_control.release_parameter()
            if self._reso_control != None:
                self._reso_control.release_parameter()
        self._freq_control = freq
        self._reso_control = reso
        self.update()

    def update(self):
        super(TrackFilterComponent, self).update()
        if not self.is_enabled() or self._device != None:
            device_dict = FILTER_DEVICES[self._device.class_name]
            if self._freq_control != None:
                self._freq_control.release_parameter()
                parameter = get_parameter_by_name(self._device, device_dict['Frequency'])
                if parameter != None:
                    self._freq_control.connect_to(parameter)
            if self._reso_control != None:
                self._reso_control.release_parameter()
                parameter = get_parameter_by_name(self._device, device_dict['Resonance'])
                if parameter != None:
                    self._reso_control.connect_to(parameter)
                    return
        else:
            return

    def _on_devices_changed(self):
        self._device = None
        if self._track != None:
            for index in range(len(self._track.devices)):
                device = self._track.devices[-1 * (index + 1)]
                if device.class_name in list(FILTER_DEVICES.keys()):
                    self._device = device
                    break
                else:
                    continue
        self.update()