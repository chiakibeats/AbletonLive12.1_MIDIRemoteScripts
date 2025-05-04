# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\transport.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from math import isclose
from ableton.v3.base import clamp, listenable_property
from ableton.v3.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v3.control_surface.controls import ButtonControl, StepEncoderControl
GROOVE_AMOUNT_MAX = 1.3125
GROOVE_AMOUNT_STEP_SIZE = GROOVE_AMOUNT_MAX / 131
GROOVE_POOL_EMPTY = "Live's Groove\nPool is empty"

class TransportComponent(TransportComponentBase):
    pass
    tempo_encoder = StepEncoderControl(num_steps=64)
    groove_encoder = StepEncoderControl(num_steps=64)
    shift_button = ButtonControl(color=None)

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._shift_can_fine_tune = False
        self.register_slot(self.song, self.notify_tempo_string, 'tempo')
        self.register_slot(self.song, self.notify_groove_string, 'groove_amount')
        self.register_slot(self.song.groove_pool, self.notify_groove_string, 'grooves')

    @listenable_property
    def tempo_string(self):
        tempo = self.song.tempo
        if self.can_fine_tune() or not isclose(tempo, int(tempo), abs_tol=0.01):
            return '{:.1f} BPM'.format(tempo)
        else:
            return '{} BPM'.format(int(tempo))

    @listenable_property
    def groove_string(self):
        if self.song.groove_pool.grooves:
            return 'Groove\n{}%'.format(round(min(self.song.groove_amount, 1.3) * 100))
        else:
            return GROOVE_POOL_EMPTY

    def set_shift_button(self, button):
        self.shift_button.set_control_element(button)
        self._shift_can_fine_tune = False
        self.notify_tempo_string()

    def increment_tempo(self, delta):
        return clamp(self.song.tempo + delta, 20, 999)

    def increment_groove(self, delta):
        if self.song.groove_pool.grooves:
            self.song.groove_amount = clamp(self.song.groove_amount + GROOVE_AMOUNT_STEP_SIZE * delta, 0, GROOVE_AMOUNT_MAX)

    def can_fine_tune(self):
        if self.shift_button.control_element:
            return self.shift_button.control_element.is_locked or (self.shift_button.is_pressed and self._shift_can_fine_tune)
        else:
            return False

    @tempo_encoder.value
    def tempo_encoder(self, value, _):
        if self.can_fine_tune():
            self.song.tempo = self.increment_tempo(value / 10)
        else:
            self.song.tempo = int(self.increment_tempo(value))

    @groove_encoder.value
    def groove_encoder(self, value, _):
        if self.can_fine_tune():
            self.increment_groove(value)
            return
        else:
            self.increment_groove(value * 5)

    @shift_button.value
    def shift_button(self, *_):
        self._shift_can_fine_tune = True
        self.notify_tempo_string()