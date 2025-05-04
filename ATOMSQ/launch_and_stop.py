# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\launch_and_stop.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v3.base import depends, listens
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.components import ClipSlotComponent
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.live import liveobj_valid

class LaunchAndStopComponent(Component):
    scene_launch_button = ButtonControl(color='DefaultButton.Off', pressed_color='DefaultButton.On')
    track_stop_button = ButtonControl()

    @depends(target_track=None)
    def __init__(self, target_track=None, *a, **k):
        super().__init__(*a, **k)
        self._target_track = target_track
        self._clip_slot = ClipSlotComponent()
        self.register_slot(self._target_track, self.__on_track_or_scene_changed, 'target_track')
        self.register_slot(self.song.view, self.__on_track_or_scene_changed, 'selected_scene')
        self.__on_playing_status_changed.subject = self._target_track
        self.__on_track_or_scene_changed()
        self.__on_playing_status_changed()

    def set_clip_launch_button(self, button):
        self._clip_slot.set_launch_button(button)

    @scene_launch_button.pressed
    def scene_launch_button(self, _):
        self.song.view.selected_scene.fire()

    @track_stop_button.pressed
    def track_stop_button(self, _):
        self.song.view.selected_track.stop_all_clips()

    def __on_track_or_scene_changed(self):
        slot = self.song.view.highlighted_clip_slot
        self._clip_slot.set_clip_slot(slot if liveobj_valid(slot) else None)

    @listens('target_track.playing_slot_index')
    def __on_playing_status_changed(self):
        track = self._target_track.target_track
        self.track_stop_button.enabled = track in self.song.tracks and track.playing_slot_index >= 0