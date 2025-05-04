# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\track_recording.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ableton.v2.base import const, depends, listens
from ableton.v2.control_surface.components import SessionRecordingComponent as SessionRecordingComponentBase
from ableton.v2.control_surface.components import track_is_recording, track_playing_slot

class TrackRecordingComponent(SessionRecordingComponentBase):

    def __init__(self, target_track_component, *a, **k):
        super(TrackRecordingComponent, self).__init__(*a, **k)
        self._target_track_component = target_track_component

    def _trigger_recording(self):
        self.__on_fired_slot_index_changed.subject = None
        track = self._target_track_component.target_track
        if self._track_can_record(track):
            self._record_to_track(track)
            return
        else:
            super(TrackRecordingComponent, self)._trigger_recording()

    def _record_to_track(self, track):
        playing_slot = track_playing_slot(track)
        if not track_is_recording(track) and playing_slot is not None:
            self.song.overdub = not self.song.overdub
            if not self.song.is_playing:
                self.song.is_playing = True
                return
            else:
                return None
        elif not self._stop_recording():
            self._prepare_new_slot(track)
            self._start_recording()
            return
        else:
            self.__on_fired_slot_index_changed.subject = track

    def _prepare_new_slot(self, track):
        try:
            slot_index = list(self.song.scenes).index(self.song.view.selected_scene)
            track.stop_all_clips(False)
            self._jump_to_next_slot(track, slot_index)
        except Live.Base.LimitationError:
            self._handle_limitation_error_on_scene_creation()

    def _track_can_record(self, track):
        return track in self.song.tracks and track.can_be_armed

    @listens('fired_slot_index')
    def __on_fired_slot_index_changed(self):
        if self._target_track_component.target_track.fired_slot_index >= 0:
            self.record_button.color = 'Recording.Transition'

class FixedLengthTrackRecordingComponent(TrackRecordingComponent):
    pass

    @depends(fixed_length_recording=const(None))
    def __init__(self, target_track_component, fixed_length_recording, *a, **k):
        self._fixed_length_recording = fixed_length_recording
        super(FixedLengthTrackRecordingComponent, self).__init__(target_track_component, *a, **k)

    def _start_recording(self):
        track = self._target_track_component.target_track
        song = self.song
        slot_index = list(song.scenes).index(song.view.selected_scene)
        slot = track.clip_slots[slot_index]
        if self._fixed_length_recording.should_start_recording_in_slot(slot):
            self._fixed_length_recording.start_recording_in_slot(slot)
        else:
            super(FixedLengthTrackRecordingComponent, self)._start_recording()