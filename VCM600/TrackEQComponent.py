# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\VCM600\TrackEQComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Generic.Devices import get_parameter_by_name
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.EncoderElement import EncoderElement
EQ_DEVICES = {'Eq8': {'Gains': ['%i Gain A' % (index + 1) for index in range(8)]}, 'FilterEQ3': {'Gains': ['GainLo', 'GainMid', 'GainHi'], 'Cuts': ['LowOn', 'MidOn', 'HighOn']}}

class TrackEQComponent(ControlSurfaceComponent):
    pass

    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        self._track = None
        self._device = None
        self._gain_controls = None
        self._cut_buttons = None

    def disconnect(self):
        if self._gain_controls!= None:
            for control in self._gain_controls:
                control.release_parameter()
            self._gain_controls = None
        if self._cut_buttons!= None:
            for button in self._cut_buttons:
                button.remove_value_listener(self._cut_value)
        self._cut_buttons = None
        if self._track!= None:
            self._track.remove_devices_listener(self._on_devices_changed)
            self._track = None
        self._device = None
        if self._device!= None:
            device_dict = EQ_DEVICES[self._device.class_name]
            if 'Cuts' in list(device_dict.keys()):
                cut_names = device_dict['Cuts']
                for cut_name in cut_names:
                    parameter = get_parameter_by_name(self._device, cut_name)
                    if parameter!= None and parameter.value_has_listener(self._on_cut_changed):
                        parameter.remove_value_listener(self._on_cut_changed)
                    continue
                return None
            else:  # inserted
                return None
        else:  # inserted
            return None

    def on_enabled_changed(self):
        self.update()

    def set_track(self, track):
        if self._track!= None:
            self._track.remove_devices_listener(self._on_devices_changed)
            if self._gain_controls!= None and self._device!= None:
                for control in self._gain_controls:
                    control.release_parameter()
        self._track = track
        if self._track!= None:
            self._track.add_devices_listener(self._on_devices_changed)
        self._on_devices_changed()

    def set_cut_buttons(self, buttons):
        if buttons!= self._cut_buttons:
            if self._cut_buttons!= None:
                for button in self._cut_buttons:
                    button.remove_value_listener(self._cut_value)
            self._cut_buttons = buttons
            if self._cut_buttons!= None:
                for button in self._cut_buttons:
                    button.add_value_listener(self._cut_value, identify_sender=True)
            self.update()

    def set_gain_controls(self, controls):
        if self._device!= None and self._gain_controls!= None:
            for control in self._gain_controls:
                control.release_parameter()
        for control in controls:
            pass  # postinserted
        self._gain_controls = controls
        self.update()

    def update(self):
        super(TrackEQComponent, self).update()
        if self.is_enabled() and self._device!= None:
            device_dict = EQ_DEVICES[self._device.class_name]
            if self._gain_controls!= None:
                gain_names = device_dict['Gains']
                for index in range(len(self._gain_controls)):
                    self._gain_controls[index].release_parameter()
                    if len(gain_names) > index:
                        parameter = get_parameter_by_name(self._device, gain_names[index])
                        if parameter!= None:
                            self._gain_controls[index].connect_to(parameter)
                    continue
            if self._cut_buttons!= None:
                if 'Cuts' in list(device_dict.keys()):
                    cut_names = device_dict['Cuts']
                    for index in range(len(self._cut_buttons)):
                        self._cut_buttons[index].turn_off()
                        if len(cut_names) > index:
                            parameter = get_parameter_by_name(self._device, cut_names[index])
                            if parameter!= None:
                                if parameter.value == 0.0:
                                    self._cut_buttons[index].turn_on()
                                if not parameter.value_has_listener(self._on_cut_changed):
                                    parameter.add_value_listener(self._on_cut_changed)
                        pass
                        continue
                    return None
                else:  # inserted
                    return None
            else:  # inserted
                return None
        else:  # inserted
            if self._cut_buttons!= None:
                for button in self._cut_buttons:
                    if button!= None:
                        button.turn_off()
                    continue
            if self._gain_controls!= None:
                for control in self._gain_controls:
                    control.release_parameter()
            else:  # inserted
                return

    def _cut_value(self, value, sender):
        if self.is_enabled() and self._device!= None and sender.is_momentary() and (value!= 0):
                    device_dict = EQ_DEVICES[self._device.class_name]
                    if 'Cuts' in list(device_dict.keys()):
                        cut_names = device_dict['Cuts']
                        index = list(self._cut_buttons).index(sender)
                        if index in range(len(cut_names)):
                            parameter = get_parameter_by_name(self._device, cut_names[index])
                            if parameter!= None and parameter.is_enabled:
                                    parameter.value = float(int(parameter.value + 1) % 2)
                                    return
                                else:  # inserted
                                    return None
                            else:  # inserted
                                return None
                        else:  # inserted
                            return None
                    else:  # inserted
                        return None
                else:  # inserted
                    return None

    def _on_devices_changed(self):
        if self._device!= None:
            device_dict = EQ_DEVICES[self._device.class_name]
            if 'Cuts' in list(device_dict.keys()):
                cut_names = device_dict['Cuts']
                for cut_name in cut_names:
                    parameter = get_parameter_by_name(self._device, cut_name)
                    if parameter!= None and parameter.value_has_listener(self._on_cut_changed):
                        parameter.remove_value_listener(self._on_cut_changed)
                    continue
        self._device = None
        if self._track!= None:
            for index in range(len(self._track.devices)):
                device = self._track.devices[(-1) * (index + 1)]
                if device.class_name in list(EQ_DEVICES.keys()):
                    self._device = device
                    break
                else:  # inserted
                    continue
        self.update()

    def _on_cut_changed(self):
        if not self.is_enabled() or self._cut_buttons!= None:
                cut_names = EQ_DEVICES[self._device.class_name]['Cuts']
                for index in range(len(self._cut_buttons)):
                    self._cut_buttons[index].turn_off()
                    if len(cut_names) > index:
                        parameter = get_parameter_by_name(self._device, cut_names[index])
                        if parameter!= None and parameter.value == 0.0:
                            self._cut_buttons[index].turn_on()
                    pass
                    continue
                return None
            else:  # inserted
                return None
        else:  # inserted
            return None