# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\BLOCKS\target_track_provider.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import listens, listens_group
from ableton.v2.control_surface import Component

class TargetTrackProvider(Component):
    __events__ = ('target_track', 'armed_tracks')

    def __init__(self, *a, **k):
        super(TargetTrackProvider, self).__init__(*a, **k)
        self._target_track = None
        self._armed_tracks = []
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_tracks_changed.subject = self.song
        self.__on_tracks_changed()

    @property
    def target_track(self):
        return self._target_track

    @listens('selected_track')
    def __on_selected_track_changed(self):
        if not self._armed_tracks:
            self._update_target_track()

    @listens('tracks')
    def __on_tracks_changed(self):
        tracks = [t for t in self.song.tracks if t.can_be_armed and t.has_midi_input]
        self.__on_arm_changed.replace_subjects(tracks)
        self.__on_frozen_state_changed.replace_subjects(tracks)
        self._update_tracks(tracks)

    @listens_group('arm')
    def __on_arm_changed(self, track):
        if track in self._armed_tracks:
            self._armed_tracks.remove(track)
        if track.arm:
            self._armed_tracks.append(track)
            self._set_target_track(track)
        else:
            self._update_target_track()
        self.notify_armed_tracks()

    @listens_group('is_frozen')
    def __on_frozen_state_changed(self, track):
        if track in self._armed_tracks:
            self._armed_tracks.remove(track)
        self._update_target_track()

    def _update_tracks(self, all_tracks):
        for track in self._armed_tracks:
            if track not in all_tracks:
                self._armed_tracks.remove(track)
            pass
            continue
        for track in all_tracks:
            if track.arm and track not in self._armed_tracks:
                self._armed_tracks.append(track)
            pass
            continue
        self._update_target_track()

    def _update_target_track(self):
        target_track = None
        selected_track = self.song.view.selected_track
        if self._armed_tracks:
            target_track = self._armed_tracks[-1]
        elif not selected_track.is_frozen:
            target_track = selected_track
        self._set_target_track(target_track)

    def _set_target_track(self, track):
        if self._target_track != track:
            self._target_track = track
            self.notify_target_track()