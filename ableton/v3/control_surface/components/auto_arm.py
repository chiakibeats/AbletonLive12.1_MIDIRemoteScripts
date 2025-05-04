# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\auto_arm.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import depends, listens, listens_group, task
from ...live import liveobj_changed, liveobj_valid
from .. import Component

def track_can_be_auto_armed(track):
    pass
    return liveobj_valid(track) and track.can_be_armed and (track.has_midi_input or False)

class AutoArmComponent(Component):
    pass

    @depends(target_track=None)
    def __init__(self, name='Auto_Arm', target_track=None, *a, **k):
        super().__init__(*a, name=name, **k)
        self._target_track = target_track
        self._auto_arm_target = None
        self._update_auto_arm_task = self._tasks.add(task.run(self._update_auto_arm))
        self.register_slot(self.application, self.update, 'control_surfaces')
        self.register_slot(self.song, self.update, 'exclusive_arm')
        self.register_slot(self._target_track, self.update, 'target_track')
        self.__on_tracks_changed.subject = self.song
        self.__on_tracks_changed()

    def disconnect(self):
        self._setup_new_auto_arm_target(None)
        super().disconnect()

    def update(self):
        super().update()
        self._update_auto_arm()

    @property
    def needs_restore_auto_arm(self):
        pass
        song = self.song
        exclusive_arm = song.exclusive_arm
        target_track = self._target_track.target_track
        return self.is_enabled() and track_can_be_auto_armed(target_track) and (not target_track.arm) and any(filter(lambda track: (track_can_be_auto_armed(track) and track.can_be_armed) and track.arm or (track_can_be_auto_armed(track) and track.arm or (track_can_be_auto_armed(track) and track.can_be_armed)), song.tracks))

    def _can_auto_arm(self):
        return self.is_enabled() and self.application.number_of_push_apps_running == 0 and (not self.needs_restore_auto_arm)

    def _auto_arm_target_changed(self, target_track):
        return liveobj_changed(target_track, self._auto_arm_target) or not track_can_be_auto_armed(self._auto_arm_target)

    def _set_auto_arm_state(self, state):
        if not liveobj_valid(self._auto_arm_target) or self._auto_arm_target.implicit_arm != state:
            self._auto_arm_target.implicit_arm = state

    def _setup_new_auto_arm_target(self, target_track):
        new_target = target_track if track_can_be_auto_armed(target_track) else None
        self.__on_implicit_arm_changed.subject = new_target
        self._set_auto_arm_state(False)
        self._auto_arm_target = new_target

    def _update_auto_arm(self):
        self._update_auto_arm_task.kill()
        if self._can_auto_arm():
            target_track = self._target_track.target_track
            if self._auto_arm_target_changed(target_track):
                self._setup_new_auto_arm_target(target_track)
            self._set_auto_arm_state(True)
            return
        else:
            self._setup_new_auto_arm_target(None)

    @listens('implicit_arm')
    def __on_implicit_arm_changed(self):
        self._update_auto_arm()

    @listens_group('arm')
    def __on_arm_changed(self, _):
        self._update_auto_arm_task.restart()

    @listens_group('input_routing_type')
    def __on_input_routing_type_changed(self, _):
        self._update_auto_arm_task.restart()

    @listens_group('is_frozen')
    def __on_frozen_state_changed(self, _):
        self._update_auto_arm_task.restart()

    @listens('tracks')
    def __on_tracks_changed(self):
        tracks = list(filter(lambda t: t.can_be_armed, self.song.tracks))
        self.__on_arm_changed.replace_subjects(tracks)
        self.__on_input_routing_type_changed.replace_subjects(tracks)
        self.__on_frozen_state_changed.replace_subjects(tracks)