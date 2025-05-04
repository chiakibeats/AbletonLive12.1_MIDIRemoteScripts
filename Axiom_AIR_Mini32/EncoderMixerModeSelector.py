# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Axiom_AIR_Mini32\EncoderMixerModeSelector.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ModeSelectorComponent import ModeSelectorComponent

class EncoderMixerModeSelector(ModeSelectorComponent):
    pass

    def __init__(self, mixer):
        ModeSelectorComponent.__init__(self)
        self._mixer = mixer
        self._controls = None

    def disconnect(self):
        self._mixer = None
        self._controls = None
        ModeSelectorComponent.disconnect(self)

    def set_mode_toggle(self, button):
        ModeSelectorComponent.set_mode_toggle(self, button)
        self.set_mode(0)

    def set_controls(self, controls):
        self._controls = controls
        self.update()

    def number_of_modes(self):
        return 2

    def update(self):
        super(EncoderMixerModeSelector, self).update()
        if not self.is_enabled() or self._controls!= None:
                mode = self._mode_index
                for index in range(len(self._controls)):
                    strip = self._mixer.channel_strip(index)
                    if mode == 0:
                        strip.set_pan_control(None)
                        strip.set_volume_control(self._controls[index])
                        continue
                    else:  # inserted
                        if mode == 1:
                            strip.set_volume_control(None)
                            strip.set_pan_control(self._controls[index])
                        continue
            else:  # inserted
                return
        else:  # inserted
            return None