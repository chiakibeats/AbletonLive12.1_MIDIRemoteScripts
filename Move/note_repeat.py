# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\note_repeat.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from Live.Song import RecordingQuantization
from ableton.v3.base import EventObject, clamp, depends, listenable_property, listens, task
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl, StepEncoderControl
from ableton.v3.control_surface.display import Renderable
REPEAT_RATE_MAP = {1.0 / rate * 4.0: name for rate, name in zip((4, 6, 8, 12, 16, 24, 32, 48), ('1/4', '1/4t', '1/8', '1/8t', '1/16', '1/16t', '1/32', '1/32t'))}
REPEAT_RATE_VALUES = list(REPEAT_RATE_MAP.keys())
DEFAULT_REPEAT_RATE = REPEAT_RATE_VALUES[2]

class NoteRepeatModel(EventObject, Renderable):
    pass

    @depends(song=None, note_repeat=None)
    def __init__(self, song=None, note_repeat=None, *a, **k):
        super().__init__(*a, **k)
        self.song = song
        self._last_record_quantization = None
        self._note_repeat = note_repeat
        self._note_repeat.enabled = False
        self._note_repeat.repeat_rate = DEFAULT_REPEAT_RATE
        self.__on_record_quantization_changed.subject = song
        self.__on_record_quantization_changed()

    @property
    def index(self):
        return REPEAT_RATE_VALUES.index(self._note_repeat.repeat_rate)

    @index.setter
    def index(self, index):
        self.rate = REPEAT_RATE_VALUES[index]

    @listenable_property
    def rate(self):
        return self._note_repeat.repeat_rate

    @rate.setter
    def rate(self, rate):
        if self._note_repeat.repeat_rate != rate:
            self._note_repeat.repeat_rate = rate
            self.notify_rate()
            return

    @listenable_property
    def enabled(self):
        return self._note_repeat.enabled

    @enabled.setter
    def enabled(self, state):
        if self._note_repeat.enabled != state:
            self._note_repeat.enabled = state
            self._update_recording_quantization()
            self.notify_enabled()
        if state:
            self._note_repeat.aftertouch_ramp_start = 300
            self._note_repeat.aftertouch_ramp_length = 250
            return
        else:
            return None

    def toggle_enabled(self):
        pass
        self.enabled = not self._note_repeat.enabled

    def _update_recording_quantization(self):
        if self._note_repeat.enabled:
            self.song.midi_recording_quantization = False
            return
        elif self.song.midi_recording_quantization or self._last_record_quantization:
            self.song.midi_recording_quantization = self._last_record_quantization

    @listens('midi_recording_quantization')
    def __on_record_quantization_changed(self):
        quantization_value = self.song.midi_recording_quantization
        if quantization_value != RecordingQuantization.rec_q_no_q:
            self._last_record_quantization = quantization_value

class NoteRepeatComponent(Component, Renderable):
    pass
    repeat_button = ButtonControl(color='NoteRepeat.Off', on_color='NoteRepeat.On')
    rate_encoder = StepEncoderControl(num_steps=64)
    enabled_state_toggled_by_button = listenable_property.managed(False)

    @depends(note_repeat=None, target_track=None)
    def __init__(self, name='Note_Repeat', note_repeat=None, target_track=None, *a, **k):
        super().__init__(*a, name=name, **k)
        self._note_repeat_model = note_repeat
        self.register_slot(self._note_repeat_model, self._update_repeat_button, 'enabled')
        self.register_slot(self._note_repeat_model, self._store_note_repeat_state, 'rate')
        self._target_track = target_track
        self.__on_target_track_changed.subject = target_track
        self.rate_encoder.connect_property(self._note_repeat_model, 'index', lambda x: clamp(self._note_repeat_model.index + x, 0, len(REPEAT_RATE_VALUES) - 1))

    @listenable_property
    def model(self):
        pass
        return self._note_repeat_model

    @repeat_button.pressed
    def repeat_button(self, _):
        self._note_repeat_model.toggle_enabled()
        self._store_note_repeat_state()
        self.enabled_state_toggled_by_button = self._note_repeat_model.enabled
        if not self._note_repeat_model.enabled:
            self.notify(self.notifications.note_repeat, False)

    def update(self):
        super().update()
        if self.is_enabled():
            self._restore_note_repeat_state()
        else:
            self._note_repeat_model.enabled = False

    def _store_note_repeat_state(self):
        self._target_track.target_track.set_data('move-note-repeat-enabled', self._note_repeat_model.enabled)
        self._target_track.target_track.set_data('move-note-repeat-rate', self._note_repeat_model.rate)

    def _restore_note_repeat_state(self):
        self._note_repeat_model.enabled = self._target_track.target_track.get_data('move-note-repeat-enabled', False)
        self._note_repeat_model.rate = self._target_track.target_track.get_data('move-note-repeat-rate', DEFAULT_REPEAT_RATE)

    def _update_repeat_button(self):
        self.repeat_button.is_on = self._note_repeat_model.enabled

    @listens('target_track')
    def __on_target_track_changed(self):
        self._tasks.add(task.run(self._restore_note_repeat_state))
        self.repeat_button.enabled = not self._target_track.target_track.has_audio_input