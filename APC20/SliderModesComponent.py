# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC20\SliderModesComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from _Framework.ButtonElement import ButtonElement
from _Framework.ModeSelectorComponent import ModeSelectorComponent

class SliderModesComponent(ModeSelectorComponent):
    pass

    def __init__(self, mixer, sliders, *a, **k):
        super(SliderModesComponent, self).__init__(*a, **k)
        self._mixer = mixer
        self._sliders = sliders
        self._mode_index = 0

    def disconnect(self):
        super(SliderModesComponent, self).disconnect()
        self._mixer = None
        self._sliders = None

    def set_mode_buttons(self, buttons):
        for button in self._modes_buttons:
            button.remove_value_listener(self._mode_value)
        self._modes_buttons = []
        if buttons != None:
            for button in buttons:
                identify_sender = True
                button.add_value_listener(self._mode_value, identify_sender)
                self._modes_buttons.append(button)
        self.update()

    def number_of_modes(self):
        return 8

    def update(self):
        super(SliderModesComponent, self).update()
        if self.is_enabled():
            for index in range(len(self._modes_buttons)):
                if index == self._mode_index:
                    self._modes_buttons[index].turn_on()
                    continue
                else:
                    self._modes_buttons[index].turn_off()
                    continue
            for index in range(len(self._sliders)):
                strip = self._mixer.channel_strip(index)
                slider = self._sliders[index]
                slider.use_default_message()
                slider.set_identifier(slider.message_identifier() - self._mode_index)
                strip.set_volume_control(None)
                strip.set_pan_control(None)
                strip.set_send_controls((None, None, None))
                slider.release_parameter()
                if self._mode_index == 0:
                    strip.set_volume_control(slider)
                    continue
                elif self._mode_index == 1:
                    strip.set_pan_control(slider)
                    continue
                else:
                    if self._mode_index < 5:
                        send_controls = [None, None, None]
                        send_controls[self._mode_index - 2] = slider
                        strip.set_send_controls(tuple(send_controls))
                    continue