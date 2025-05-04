# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\recording.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from abc import ABC, abstractmethod
from Live.Song import Quantization, SessionRecordStatus
from ...base import depends
from ...live import is_track_armed, is_track_recording, liveobj_valid, playing_clip_slot, prepare_new_clip_slot, selected_clip_slot
from .. import Component
from ..controls import ButtonControl, ToggleButtonControl
from ..display import Renderable

class RecordingMethod(ABC):
    pass

    @depends(song=None, target_track=None)
    def __init__(self, song=None, target_track=None, *a, **k):
        super().__init__(*a, **k)
        self.song = song
        self.target_track = target_track

    @abstractmethod
    def trigger_recording(self):
        return

    def start_recording(self, *_):
        pass
        self.song.session_record = True

    def stop_recording(self):
        pass
        status = self.song.session_record_status
        was_recording = status!= SessionRecordStatus.off or self.song.session_record
        if was_recording:
            self.song.session_record = False
        return was_recording

    @staticmethod
    def can_record_into_clip_slot(clip_slot):
        pass
        return liveobj_valid(clip_slot) and is_track_armed(clip_slot.canonical_parent)

class BasicRecordingMethod(RecordingMethod):
    pass

    def trigger_recording(self):
        if not self.stop_recording():
            self.start_recording()
            return

class NextSlotRecordingMethod(RecordingMethod):
    pass

    def trigger_recording(self):
        if not self.stop_recording():
            slot = prepare_new_clip_slot(self.target_track.target_track)
            if self.can_record_into_clip_slot(slot):
                slot.fire()
            else:  # inserted
                self.start_recording()

class NextSlotWithOverdubRecordingMethod(NextSlotRecordingMethod):
    pass

    def trigger_recording(self):
        track = self.target_track.target_track
        playing_slot = playing_clip_slot(track)
        if not is_track_recording(track) and playing_slot is not None:
            self.song.overdub = not self.song.overdub
            if not self.song.is_playing:
                self.song.is_playing = True
                return
            else:  # inserted
                return None
        else:  # inserted
            super().trigger_recording()

class SelectedSlotRecordingMethod(RecordingMethod):
    pass

    def trigger_recording(self):
        if not self.stop_recording():
            self.song.overdub = True
            slot = selected_clip_slot(self.target_track.target_track)
            if self.can_record_into_clip_slot(slot):
                self._record_in_slot(slot)
            if not self.song.is_playing:
                self.song.is_playing = True
                return
        else:  # inserted
            return

    def _record_in_slot(self, slot):
        if not slot.is_playing or not self.song.is_playing:
            if slot.has_clip:
                slot.stop()
                slot.fire(force_legato=True, launch_quantization=Quantization.q_no_q)
                return
            else:  # inserted
                slot.fire()

class RecordingComponent(Component, Renderable):
    pass
    session_record_button = ButtonControl()
    session_overdub_button = ToggleButtonControl(color='Recording.SessionOverdubOff', on_color='Recording.SessionOverdubOn')
    arrangement_record_button = ToggleButtonControl(color='Recording.ArrangementRecordOff', on_color='Recording.ArrangementRecordOn')
    arrangement_overdub_button = ToggleButtonControl(color='Recording.ArrangementOverdubOff', on_color='Recording.ArrangementOverdubOn')
    new_button = ButtonControl(color='Recording.New', pressed_color='Recording.NewPressed')

    @depends(target_track=None)
    pass
    def __init__(self, target_track=None, recording_method_type=None, name='Recording', *a, **k):
        super().__init__(*a, name=name, **k)
        recording_method_type = recording_method_type or BasicRecordingMethod
        self._recording_method = recording_method_type()
        song = self.song
        self.session_overdub_button.connect_property(song, 'overdub')
        self.arrangement_record_button.connect_property(song, 'record_mode')
        self.arrangement_overdub_button.connect_property(song, 'arrangement_overdub')
        self.register_slot(song, self._update_session_record_button, 'session_record_status')
        self.register_slot(song, self._update_session_record_button, 'session_record')
        self._update_session_record_button()
        self._target_track = target_track
        self.register_slot(target_track, self._update_new_button, 'target_clip')
        self._update_new_button()

    @session_record_button.pressed
    def session_record_button(self, _):
        self._recording_method.trigger_recording()

    @new_button.pressed
    def new_button(self, _):
        if prepare_new_clip_slot(self._target_track.target_track, stop=True):
            self.notify(self.notifications.Recording.new)

    def _update_session_record_button(self):
        song = self.song
        status = song.session_record_status
        if status == SessionRecordStatus.transition:
            self.session_record_button.color = 'Recording.SessionRecordTransition'
            return
        else:  # inserted
            if status == SessionRecordStatus.on or song.session_record:
                self.session_record_button.color = 'Recording.SessionRecordOn'
                return
            else:  # inserted
                self.session_record_button.color = 'Recording.SessionRecordOff'

    def _update_new_button(self):
        self.new_button.enabled = liveobj_valid(self._target_track.target_clip)

class ViewBasedRecordingComponent(RecordingComponent):
    pass

    def __init__(self, name='View_Based_Recording', *a, **k):
        super().__init__(*a, name=name, **k)
        self._record_button = None
        self._overdub_button = None
        self.register_slot(self.application.view, self.update, 'focused_document_view')

    def disconnect(self):
        super().disconnect()
        self._record_button = None
        self._overdub_button = None

    def set_record_button(self, button):
        self._record_button = button
        self._update_record_button_assignments()

    def set_overdub_button(self, button):
        self._overdub_button = button
        self._update_overdub_button_assignments()

    def update(self):
        super().update()
        self._update_record_button_assignments()
        self._update_overdub_button_assignments()

    def _update_record_button_assignments(self):
        self.arrangement_record_button.set_control_element(None)
        self.session_record_button.set_control_element(None)
        if self.application.view.focused_document_view == 'Session':
            self.session_record_button.set_control_element(self._record_button)
            return
        else:  # inserted
            self.arrangement_record_button.set_control_element(self._record_button)

    def _update_overdub_button_assignments(self):
        self.arrangement_overdub_button.set_control_element(None)
        self.session_overdub_button.set_control_element(None)
        if self.application.view.focused_document_view == 'Session':
            self.session_overdub_button.set_control_element(self._overdub_button)
            return
        else:  # inserted
            self.arrangement_overdub_button.set_control_element(self._overdub_button)