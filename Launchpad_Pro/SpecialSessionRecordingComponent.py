# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\SpecialSessionRecordingComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Framework.ClipCreator import ClipCreator
from _Framework.SessionRecordingComponent import SessionRecordingComponent, subject_slot, track_is_recording, track_playing_slot

class SpecialSessionRecordingComponent(SessionRecordingComponent):
    pass

    def __init__(self, target_track_component, *a, **k):
        self._target_track_component = target_track_component
        self._modes_component = None
        self._note_mode_name = None
        super(SpecialSessionRecordingComponent, self).__init__(ClipCreator(), True, *a, **k)

    def set_modes_component(self, modes_component):
        self._modes_component = modes_component

    def set_note_mode_name(self, name):
        self._note_mode_name = name

    @subject_slot('value')
    def _on_record_button_value(self, value):
        if not self.is_enabled() or value:
            if self._modes_component.selected_mode == self._note_mode_name:
                self._handle_note_mode_record_behavior()
            elif not self._stop_recording():
                self._start_recording()
                return
        else:
            return

    def _handle_note_mode_record_behavior(self):
        track = self._target_track_component.target_track
        if self._track_can_record(track):
            playing_slot = track_playing_slot(track)
            should_overdub = not track_is_recording(track) and playing_slot != None
            if should_overdub:
                self.song().overdub = not self.song().overdub
                if not self.song().is_playing:
                    self.song().is_playing = True
                    return
                else:
                    return None
            elif not self._stop_recording():
                self._prepare_new_slot(track)
                self._start_recording()
                return
            else:
                return None
        elif not self._stop_recording():
            self._start_recording()
            return
        else:
            return None

    def _prepare_new_slot(self, track):
        song = self.song()
        song.overdub = False
        view = song.view
        try:
            slot_index = list(song.scenes).index(view.selected_scene)
            track.stop_all_clips(False)
            self._jump_to_next_slot(track, slot_index)
        except Live.Base.LimitationError:
            self._handle_limitation_error_on_scene_creation()

    def _track_can_record(self, track):
        return track in self.song().tracks and track.can_be_armed