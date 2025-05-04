# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\components\target_track.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import listens, listens_group, liveobj_valid
from ableton.v2.control_surface import Component

class TargetTrackComponent(Component):
    pass
    __events__ = ('target_track',)

    def __init__(self, *a, **k):
        super(TargetTrackComponent, self).__init__(*a, **k)
        self._target_track = None
        self._armed_track_list = []
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()

    @property
    def target_track(self):
        return self._target_track

    @listens('selected_track')
    def __on_selected_track_changed(self):
        if not self._armed_track_list:
            self._set_target_track()
            return

    def _set_target_track(self):
        new_target = self._target_track
        if self._armed_track_list:
            new_target = self._armed_track_list[-1]
        else:
            new_target = self.song.view.selected_track
        if self._target_track != new_target:
            self._target_track = new_target
            self.notify_target_track()

class ArmedTargetTrackComponent(TargetTrackComponent):
    pass

    def __init__(self, *a, **k):
        super(ArmedTargetTrackComponent, self).__init__(*a, **k)
        self.__on_tracks_changed.subject = self.song
        self.__on_tracks_changed()

    @property
    def tracks(self):
        return list(filter(lambda t: liveobj_valid(t) and t.can_be_armed and (t.has_midi_input or False), self.song.tracks))

    @listens('visible_tracks')
    def __on_tracks_changed(self):
        tracks = self.tracks
        self.__on_arm_changed.replace_subjects(tracks)
        self.__on_frozen_state_changed.replace_subjects(tracks)
        self._refresh_armed_track_list()

    @listens_group('arm')
    def __on_arm_changed(self, _):
        self._refresh_armed_track_list()

    @listens_group('is_frozen')
    def __on_frozen_state_changed(self, _):
        self._refresh_armed_track_list()

    def _refresh_armed_track_list(self):
        tracks = self.tracks
        for track in self._armed_track_list:
            if not liveobj_valid(track) or not track.arm or track.is_frozen or (track not in tracks):
                self._armed_track_list.remove(track)
            pass
            continue
        for track in tracks:
            if track.arm and (not track.is_frozen) and (track not in self._armed_track_list):
                self._armed_track_list.append(track)
            continue
        self._set_target_track()