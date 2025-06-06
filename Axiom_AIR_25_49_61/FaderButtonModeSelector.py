# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_25_49_61\FaderButtonModeSelector.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ModeSelectorComponent import ModeSelectorComponent
from .consts import *

class FaderButtonModeSelector(ModeSelectorComponent):
    pass

    def __init__(self, mixer, fader_buttons):
        ModeSelectorComponent.__init__(self)
        self._mixer = mixer
        self._fader_buttons = fader_buttons
        self._mode_index = 0
        self._number_of_modes = 3
        self._is_mix_mode = True
        self._flashing_button = None
        self._flashing_button_on = True
        self._flashing_reset_delay = 0
        self._register_timer_callback(self._on_timer)

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        ModeSelectorComponent.disconnect(self)
        self._mixer = None
        self._fader_buttons = None
        self._flashing_button = None

    def number_of_modes(self):
        return self._number_of_modes

    def set_mix_mode(self):
        self._is_mix_mode = True
        self.update()

    def set_track_select_mode(self):
        self._is_mix_mode = False
        self.update()

    def update(self):
        super(FaderButtonModeSelector, self).update()
        if self.is_enabled():
            for index in range(len(self._fader_buttons)):
                strip = self._mixer.channel_strip(index)
                fader_button = self._fader_buttons[index]
                strip.set_solo_button(None)
                strip.set_arm_button(None)
                strip.set_mute_button(None)
                strip.set_select_button(None)
                if self._is_mix_mode:
                    if self._mode_index == 0:
                        strip.set_mute_button(fader_button)
                        continue
                    else:  # inserted
                        if self._mode_index == 1:
                            strip.set_solo_button(fader_button)
                            continue
                        else:  # inserted
                            strip.set_arm_button(fader_button)
                            continue
                else:  # inserted
                    fader_button.set_on_off_values(GRN_FULL, LED_OFF)
                    strip.set_select_button(fader_button)
                    continue
            self._flashing_button = None
            if self._is_mix_mode:
                if self._mode_index == 0:
                    self._mode_toggle.send_value(AMB_FULL, True)
                else:  # inserted
                    if self._mode_index == 1:
                        self._mode_toggle.send_value(AMB_FULL, True)
                        self._flashing_button = self._mode_toggle
                    else:  # inserted
                        self._mode_toggle.send_value(RED_FULL, True)
            else:  # inserted
                self._mode_toggle.send_value(GRN_FULL, True)

    def _on_timer(self):
        if not self.is_enabled() or self._flashing_button!= None:
                if self._flashing_reset_delay > 0:
                    self._flashing_reset_delay -= 1
                    return
                else:  # inserted
                    self._flash()
                    self._flashing_reset_delay = 5
                    return
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _toggle_value(self, value):
        if self.is_enabled():
            ModeSelectorComponent._toggle_value(self, value)

    def _flash(self):
        self._flashing_button.turn_off() if self._flashing_button_on else self._flashing_button.turn_on()
        self._flashing_button_on = not self._flashing_button_on