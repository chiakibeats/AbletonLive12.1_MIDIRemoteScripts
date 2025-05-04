# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\TargetTrackComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import Subject, subject_slot, subject_slot_group

class TargetTrackComponent(ControlSurfaceComponent, Subject):
    pass
    __subject_events__ = ('target_track',)

    def __init__(self, *a, **k):
        super(TargetTrackComponent, self).__init__(*a, **k)
        self._target_track = None
        self._armed_track_stack = []
        self._on_tracks_changed.subject = self.song()
        self._on_tracks_changed()

    @property
    def target_track(self):
        return self._target_track

    def on_selected_track_changed(self):
        if not self._armed_track_stack:
            self._set_target_track()
            return

    @subject_slot('tracks')
    def _on_tracks_changed(self):
        tracks = [t for t in self.song().tracks if t.can_be_armed and t.has_midi_input]
        self._on_arm_changed.replace_subjects(tracks)
        self._on_frozen_state_changed.replace_subjects(tracks)
        self._refresh_armed_track_stack(tracks)

    @subject_slot_group('arm')
    def _on_arm_changed(self, track):
        if track in self._armed_track_stack:
            self._armed_track_stack.remove(track)
        if track.arm:
            self._armed_track_stack.append(track)
            self._set_target_track(track)
            return
        else:
            self._set_target_track()

    @subject_slot_group('is_frozen')
    def _on_frozen_state_changed(self, track):
        if track in self._armed_track_stack:
            self._armed_track_stack.remove(track)
        if track == self._target_track:
            self._set_target_track()
            return

    def _set_target_track(self, target=None):
        new_target = self._target_track
        if target is None:
            if self._armed_track_stack:
                new_target = self._armed_track_stack[-1]
            else:
                new_target = self.song().view.selected_track
        else:
            new_target = target
        if self._target_track != new_target:
            self._target_track = new_target
        self.notify_target_track()

    def _refresh_armed_track_stack(self, all_tracks):
        for track in self._armed_track_stack:
            if track not in all_tracks:
                self._armed_track_stack.remove(track)
            pass
            continue
        for track in all_tracks:
            if track.arm and track not in self._armed_track_stack:
                self._armed_track_stack.append(track)
            pass
            continue
        self._set_target_track()