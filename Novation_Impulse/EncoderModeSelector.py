# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Novation_Impulse\EncoderModeSelector.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Framework.ModeSelectorComponent import ModeSelectorComponent

class EncoderModeSelector(ModeSelectorComponent):
    pass

    def __init__(self, device, mixer, bank_up_button, bank_down_button, encoders):
        ModeSelectorComponent.__init__(self)
        self._mixer = mixer
        self._device = device
        self._bank_up_button = bank_up_button
        self._bank_down_button = bank_down_button
        self._encoders = encoders
        self._device_button = None
        self._mixer_button = None
        self._device_mode = True
        self._mode_index = 0
        self._number_of_modes = 5
        self._bank_down_button.add_value_listener(self._bank_down_value)
        self._bank_up_button.add_value_listener(self._bank_up_value)
        self.update()

    def disconnect(self):
        self._bank_down_button.remove_value_listener(self._bank_down_value)
        self._bank_up_button.remove_value_listener(self._bank_up_value)
        self.set_device_mixer_buttons(None, None)
        ModeSelectorComponent.disconnect(self)
        self._mixer = None
        self._device = None
        self._bank_up_button = None
        self._bank_down_button = None
        self._encoders = None

    def set_device_mixer_buttons(self, device_button, mixer_button):
        if self._device_button!= None:
            self._device_button.remove_value_listener(self._device_value)
            self._mixer_button.remove_value_listener(self._mixer_value)
        self._device_button = device_button
        self._mixer_button = mixer_button
        if self._device_button!= None:
            self._device_button.add_value_listener(self._device_value)
            self._mixer_button.add_value_listener(self._mixer_value)

    def set_provide_volume_mode(self, provide_volume_mode):
        self._number_of_modes = 6 if provide_volume_mode else 5

    def number_of_modes(self):
        return self._number_of_modes

    def update(self):
        super(EncoderModeSelector, self).update()
        if self.is_enabled():
            self._device.set_allow_update(False)
            self._mixer.set_allow_update(False)
            self._device.set_bank_nav_buttons(None, None)
            self._device.set_parameter_controls(())
            for index in range(len(self._encoders)):
                strip = self._mixer.channel_strip(index)
                strip.set_pan_control(None)
                strip.set_send_controls(None)
                if self.number_of_modes() > 5:
                    strip.set_volume_control(None)
                continue
            if self._device_mode:
                self._device.set_bank_nav_buttons(self._bank_down_button, self._bank_up_button)
                self._device.set_parameter_controls(self._encoders)
            else:  # inserted
                for index in range(len(self._encoders)):
                    strip = self._mixer.channel_strip(index)
                    if self._mode_index == 0:
                        strip.set_pan_control(self._encoders[index])
                        continue
                    else:  # inserted
                        if self._mode_index < 5:
                            sends = [None, None, None, None]
                            sends[self._mode_index - 1] = self._encoders[index]
                            strip.set_send_controls(tuple(sends))
                            continue
                        else:  # inserted
                            strip.set_volume_control(self._encoders[index])
                            continue
            self._device.set_allow_update(True)
            self._mixer.set_allow_update(True)

    def _bank_down_value(self, value):
        if self.is_enabled() and (not self._device_mode) and (value > 0 or not self._bank_down_button.is_momentary()):
                    new_mode = max(self._mode_index - 1, 0)
                    self.set_mode(new_mode)
                    return

    def _bank_up_value(self, value):
        if self.is_enabled() and (not self._device_mode) and (value > 0 or not self._bank_up_button.is_momentary()):
                    new_mode = min(self._mode_index + 1, self.number_of_modes() - 1)
                    self.set_mode(new_mode)
                    return
        else:  # inserted
            return

    def _device_value(self, value):
        if self.is_enabled() and (not self._device_mode) and (value > 0 or not self._device_button.is_momentary()):
                    self._device_mode = True
                    self.update()
                    return
            else:  # inserted
                return
        else:  # inserted
            return None

    def _mixer_value(self, value):
        if self.is_enabled() and self._device_mode and (value > 0 or not self._mixer_button.is_momentary()):
                    self._device_mode = False
                    self.update()
                    return
            else:  # inserted
                return
        else:  # inserted
            return None