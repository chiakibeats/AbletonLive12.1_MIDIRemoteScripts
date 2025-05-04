# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\loop_selector.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from Live.Song import RecordingQuantization
from ableton.v3.base import listens
from ableton.v3.control_surface.components.bar_based_sequence import LoopSelectorComponent as LoopSelectorComponentBase
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.live import action, liveobj_name, liveobj_valid

class LoopSelectorComponent(LoopSelectorComponentBase):
    pass
    double_button = ButtonControl(color='LoopSelector.Double', pressed_color='LoopSelector.DoublePressed')
    quantize_button = ButtonControl(color='LoopSelector.Quantize', pressed_color='LoopSelector.QuantizePressed')
    page_dict = {'color': 'LoopSelector.Navigation', 'pressed_color': 'LoopSelector.NavigationPressed', 'repeat': True}
    next_page_button = ButtonControl(**page_dict)
    prev_page_button = ButtonControl(**page_dict)

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._update_action_buttons()
        self._quantization_value = RecordingQuantization.rec_q_sixtenth
        self.__on_record_quantization_changed.subject = self.song
        self.__on_record_quantization_changed()

    @next_page_button.pressed
    def next_page_button(self, _):
        self._increment_page_time(1)

    @prev_page_button.pressed
    def prev_page_button(self, _):
        self._increment_page_time(-1)

    @quantize_button.pressed
    def quantize_button(self, _):
        self._sequencer_clip.clip.quantize(self._quantization_value, 1.0)

    @double_button.pressed
    def double_button(self, _):
        action.duplicate_loop(self._sequencer_clip.clip)
        self._notify_page_time()

    def notify(self, notification, *a):
        num_bars = '{} Bars'.format(self._sequencer_clip.num_bars)
        if self.double_button.is_pressed:
            if len(a) == 2:
                super().notify(self.notifications.generic, 'Loop doubled\nBar {} Page {}\n{}'.format(*a, num_bars))
            else:
                super().notify(self.notifications.generic, 'Loop doubled\nBar {}\n{}'.format(*a, num_bars))
        else:
            super().notify('{}\n{}\n{}'.format(liveobj_name(self._target_track.target_track), notification(*a), num_bars))

    def _on_clip_changed(self):
        self._update_action_buttons()

    def _update_action_buttons(self):
        self.double_button.enabled = liveobj_valid(self._sequencer_clip.clip)
        self.quantize_button.enabled = liveobj_valid(self._sequencer_clip.clip)

    @listens('midi_recording_quantization')
    def __on_record_quantization_changed(self):
        quantization_value = self.song.midi_recording_quantization
        if quantization_value != RecordingQuantization.rec_q_no_q:
            self._quantization_value = quantization_value