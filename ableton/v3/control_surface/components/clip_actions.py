# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\clip_actions.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from Live.Song import RecordingQuantization
from ...base import depends, listens
from ...live import action, display_name, liveobj_valid
from .. import Component
from ..controls import ButtonControl
from ..display import Renderable
QUANTIZATION_OPTION_NAMES = {RecordingQuantization.rec_q_no_q: 'None', RecordingQuantization.rec_q_quarter: '1/4', RecordingQuantization.rec_q_eight: '1/8', RecordingQuantization.rec_q_eight_triplet: '1/8T', RecordingQuantization.rec_q_eight_eight_triplet: '1/8+T', RecordingQuantization.rec_q_sixtenth: '1/16', RecordingQuantization.rec_q_sixtenth_triplet: '1/16T', RecordingQuantization.rec_q_sixtenth_sixtenth_triplet: '1/16+T', RecordingQuantization.rec_q_thirtysecond: '1/32'}

class ClipActionsComponent(Component, Renderable):
    pass
    delete_button = ButtonControl(color='ClipActions.Delete', pressed_color='ClipActions.DeletePressed')
    double_button = ButtonControl(color='ClipActions.Double', pressed_color='ClipActions.DoublePressed')
    duplicate_button = ButtonControl(color='ClipActions.Duplicate', pressed_color='ClipActions.DuplicatePressed')
    quantize_button = ButtonControl(color='ClipActions.Quantize', pressed_color='ClipActions.QuantizePressed')

    @depends(target_track=None)
    def __init__(self, target_track=None, *a, **k):
        super().__init__(*a, name='Clip_Actions', **k)
        self._target_track = target_track
        self.__on_target_clip_recording_changed.subject = target_track
        self.__on_target_clip_playing_status_changed.subject = target_track
        self._update_action_buttons()
        self._quantization_value = RecordingQuantization.rec_q_sixtenth
        self.__on_record_quantization_changed.subject = self.song
        self.__on_record_quantization_changed()

    @delete_button.pressed
    def delete_button(self, _):
        self.notify(self.notifications.Clip.delete, display_name(self._target_track.target_clip))
        action.delete(self._target_track.target_clip)

    @double_button.pressed
    def double_button(self, _):
        action.duplicate_loop(self._target_track.target_clip)
        self.notify(self.notifications.Clip.double_loop)

    @duplicate_button.pressed
    def duplicate_button(self, _):
        if action.duplicate_clip_special(self._target_track.target_clip):
            self.notify(self.notifications.Clip.duplicate, display_name(self._target_track.target_clip))

    @quantize_button.pressed
    def quantize_button(self, _):
        self._quantize_clip(self._target_track.target_clip)

    def _quantize_clip(self, clip):
        clip.quantize(self._quantization_value, 1.0)
        self.notify(self.notifications.Clip.quantize, display_name(clip), QUANTIZATION_OPTION_NAMES[self._quantization_value])

    def _update_action_buttons(self):
        self._update_delete_button()
        self._update_double_button()
        self._update_duplicate_button()
        self._update_quantize_button()

    def _update_delete_button(self):
        self.delete_button.enabled = self._get_target_clip() is not None

    def _update_double_button(self):
        clip = self._get_target_clip()
        self.double_button.enabled = clip is not None and clip.is_midi_clip

    def _update_duplicate_button(self):
        self.duplicate_button.enabled = self._get_target_clip() is not None

    def _update_quantize_button(self):
        self.quantize_button.enabled = self._get_target_clip() is not None

    def _get_target_clip(self):
        clip = self._target_track.target_clip
        return clip if not liveobj_valid(clip) or clip.is_recording or (not clip.will_record_on_start) else None
        else:  # inserted
            return None

    @listens('target_clip.is_recording')
    def __on_target_clip_recording_changed(self):
        self._update_action_buttons()

    @listens('target_clip.playing_status')
    def __on_target_clip_playing_status_changed(self):
        self._update_action_buttons()

    @listens('midi_recording_quantization')
    def __on_record_quantization_changed(self):
        quantization_value = self.song.midi_recording_quantization
        if quantization_value!= RecordingQuantization.rec_q_no_q:
            self._quantization_value = quantization_value