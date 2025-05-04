# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AxiomPro\SelectButtonModeSelector.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ButtonElement import ButtonElement
from _Framework.MixerComponent import MixerComponent
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

class SelectButtonModeSelector(ModeSelectorComponent):
    pass

    def __init__(self, mixer, buttons):
        ModeSelectorComponent.__init__(self)
        self._mixer = mixer
        self._buttons = buttons
        self._mode_display = None
        self._mode_index = 0
        self.update()

    def disconnect(self):
        self._mixer = None
        self._buttons = None
        self._mode_display = None

    def set_mode_display(self, display):
        self._mode_display = display

    def number_of_modes(self):
        return 4

    def update(self):
        super(SelectButtonModeSelector, self).update()
        if self.is_enabled():
            for index in range(len(self._buttons)):
                if self._mode_index == 0:
                    self._mixer.channel_strip(index).set_select_button(self._buttons[index])
                    self._mixer.channel_strip(index).set_arm_button(None)
                    self._mixer.channel_strip(index).set_mute_button(None)
                    self._mixer.channel_strip(index).set_solo_button(None)
                    continue
                elif self._mode_index == 1:
                    self._mixer.channel_strip(index).set_select_button(None)
                    self._mixer.channel_strip(index).set_arm_button(self._buttons[index])
                    self._mixer.channel_strip(index).set_mute_button(None)
                    self._mixer.channel_strip(index).set_solo_button(None)
                    continue
                elif self._mode_index == 2:
                    self._mixer.channel_strip(index).set_select_button(None)
                    self._mixer.channel_strip(index).set_arm_button(None)
                    self._mixer.channel_strip(index).set_mute_button(self._buttons[index])
                    self._mixer.channel_strip(index).set_solo_button(None)
                    continue
                elif self._mode_index == 3:
                    self._mixer.channel_strip(index).set_select_button(None)
                    self._mixer.channel_strip(index).set_arm_button(None)
                    self._mixer.channel_strip(index).set_mute_button(None)
                    self._mixer.channel_strip(index).set_solo_button(self._buttons[index])
                    continue
                else:
                    print('Invalid mode index')
                    continue
            return None
        else:
            return None

    def _toggle_value(self, value):
        ModeSelectorComponent._toggle_value(self, value)
        if value != 0 and self._mode_display is not None:
            mode_name = ''
            if self._mode_index == 0:
                mode_name = 'Select'
            elif self._mode_index == 1:
                mode_name = 'Arm'
            elif self._mode_index == 2:
                mode_name = 'Mute'
            elif self._mode_index == 3:
                mode_name = 'Solo'
            self._mode_display.display_message(mode_name)
            return
        else:
            self._mode_display.update()