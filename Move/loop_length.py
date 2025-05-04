# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\loop_length.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import depends, listenable_property
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl, StepEncoderControl
from ableton.v3.control_surface.display import Renderable
from ableton.v3.live import action, get_bar_length, is_clip_new_recording
from .display_util import ELLIPSIS_CHAR
FINE_TUNE_FACTOR = 0.25

class LoopLengthComponent(Component, Renderable):
    pass
    length_encoder = StepEncoderControl(num_steps=64)
    shift_button = ButtonControl(color=None)

    @depends(sequencer_clip=None)
    def __init__(self, sequencer_clip=None, *a, **k):
        super().__init__(*a, name='Loop_Length', **k)
        self._sequencer_clip = sequencer_clip
        self.register_slot(sequencer_clip, self.update, 'clip')
        self.register_slot(sequencer_clip, self.update, 'length')

    @listenable_property
    def length_string(self):
        num_bars = self._sequencer_clip.num_bars
        if num_bars:
            if is_clip_new_recording(self._sequencer_clip.clip):
                return ELLIPSIS_CHAR
            else:
                complete_bars = int(num_bars)
                remainder = self._sequencer_clip.length - complete_bars * get_bar_length(clip=self._sequencer_clip.clip)
                if not self.can_fine_tune():
                    pass
                if remainder:
                    bar_fraction = int(remainder / FINE_TUNE_FACTOR)
                    if complete_bars:
                        return '{} + {}/16'.format(complete_bars, bar_fraction)
                    else:
                        return '{}/16'.format(bar_fraction)
                else:
                    return '1 Bar' if num_bars == 1 else '{} Bars'.format(complete_bars) + ''

    def increment_length(self, delta, fine_tune=False):
        clip = self._sequencer_clip.clip
        bar_length = get_bar_length(clip=clip)
        num_bars = self._sequencer_clip.num_bars
        if num_bars < 1 or (delta < 0 and num_bars == 1):
            fine_tune = True
        step_size = FINE_TUNE_FACTOR if fine_tune else bar_length
        num_steps = int(clip.loop_end / step_size)
        action.set_loop_end(clip, max(step_size, (num_steps + delta) * step_size))

    def can_fine_tune(self):
        if self.shift_button.control_element:
            return self.shift_button.control_element.is_locked or self.shift_button.is_pressed
        else:
            return False

    @length_encoder.value
    def length_encoder(self, value, _):
        self.increment_length(value, fine_tune=self.can_fine_tune())
        self.notify_length_string()

    @shift_button.value
    def shift_button(self, *_):
        self.notify_length_string()

    def update(self):
        super().update()
        self.length_encoder.enabled = self._sequencer_clip.clip is not None
        self.notify_length_string()