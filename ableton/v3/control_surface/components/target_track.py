# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\target_track.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from typing import cast
from ...base import MultiSlot, listenable_property, listens, listens_group
from ...live import liveobj_changed, liveobj_valid, playing_clip_slot, scene_index
from .. import Component
from ..controls import ToggleButtonControl
from ..display import Renderable

class TargetTrackComponent(Component, Renderable):
    pass
    lock_button = ToggleButtonControl(color='TargetTrack.LockOff', on_color='TargetTrack.LockOn')

    def __init__(self, name='Target_Track', is_private=False, *a, **k):
        super().__init__(*a, name=name, is_private=is_private, **k)
        self._target_track = None
        self._target_clip = None
        self._locked_to_track = False
        self.lock_button.connect_property(self, 'is_locked_to_track')
        self.register_slot(self.song.view, self._selected_track_changed, 'selected_track')
        for event_name in ['arrangement_clips', 'playing_slot_index']:
            self.register_slot(MultiSlot(subject=self, listener=self._update_target_clip, event_name_list=('target_track', event_name)))
        self.register_slot(self.application.view, self._update_target_clip, 'focused_document_view')
        self.register_slot(self.song.view, self._update_target_clip, 'detail_clip')
        self.register_slot(self.song.view, self._update_target_clip, 'selected_scene')
        self._selected_track_changed()

    def disconnect(self):
        self._target_track = None
        self._target_clip = None
        super().disconnect()

    @listenable_property
    def target_track(self):
        pass
        return self._target_track

    @listenable_property
    def target_clip(self):
        pass
        return self._target_clip

    @listenable_property
    def is_locked_to_track(self):
        pass
        return self._locked_to_track

    @is_locked_to_track.setter
    def is_locked_to_track(self, is_locked):
        if is_locked != self._locked_to_track:
            self._locked_to_track = is_locked
            current_track = self._target_track
            self._set_target_track()
            self.notify_is_locked_to_track()
            self.notify(self.notifications.Track.lock, cast(str, self._target_track.name if self._locked_to_track else current_track.name), self._locked_to_track)

    def _selected_track_changed(self):
        self._set_target_track()

    def _set_target_track(self):
        if not self._locked_to_track or not liveobj_valid(self._target_track):
            new_target = self._get_new_target_track()
            if liveobj_changed(self._target_track, new_target):
                self._target_track = new_target
                self._update_target_clip()
                self.notify_target_track()
            self.is_locked_to_track = False
            return

    def _get_new_target_track(self):
        return self.song.view.selected_track

    def _update_target_clip(self):
        self.__on_target_clip_slot_has_clip_changed.subject = None
        clip = None
        if self._target_track in self.song.tracks:
            if self.application.view.focused_document_view == 'Session':
                clip = self._target_clip_from_session()
            else:
                clip = self._target_clip_from_arrangement()
        if liveobj_changed(self._target_clip, clip):
            self._target_clip = clip
            self.notify_target_clip()
            return

    def _target_clip_from_arrangement(self):
        clip = self.song.view.detail_clip
        if liveobj_valid(clip) and clip in self._target_track.arrangement_clips:
            return clip
        else:
            return None

    def _target_clip_from_session(self):
        clip_slot = playing_clip_slot(self._target_track)
        if not liveobj_valid(clip_slot):
            slot_index = scene_index()
            if slot_index < len(self._target_track.clip_slots):
                clip_slot = self._target_track.clip_slots[slot_index]
        self.__on_target_clip_slot_has_clip_changed.subject = clip_slot
        return clip_slot.clip if clip_slot and clip_slot.has_clip else None

    @listens('has_clip')
    def __on_target_clip_slot_has_clip_changed(self):
        self._update_target_clip()

class ArmedTargetTrackComponent(TargetTrackComponent):
    pass

    def __init__(self, *a, **k):
        self._armed_track_list = []
        super().__init__(*a, **k)
        self.__on_tracks_changed.subject = self.song
        self.__on_tracks_changed()

    def disconnect(self):
        self._armed_track_list = None
        super().disconnect()

    def _selected_track_changed(self):
        if not self._armed_track_list:
            self._set_target_track()
            return

    def _get_new_target_track(self):
        if self._armed_track_list:
            return self._armed_track_list[-1]
        else:
            return super()._get_new_target_track()

    @listens('visible_tracks')
    def __on_tracks_changed(self):
        tracks = self._tracks()
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
        tracks = self._tracks()
        for track in self._armed_track_list:
            if liveobj_valid(track) and track.arm and (not track.is_frozen):
                pass
            if track not in tracks:
                self._armed_track_list.remove(track)
            pass
            continue
        for track in tracks:
            if track.arm and (not track.is_frozen) and (track not in self._armed_track_list):
                self._armed_track_list.append(track)
            continue
        self._set_target_track()

    def _tracks(self):
        return [t for t in self.song.tracks if liveobj_valid(t) and t.can_be_armed]