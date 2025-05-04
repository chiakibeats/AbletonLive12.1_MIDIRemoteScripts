# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk3\launch_and_stop.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import depends
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.live import liveobj_valid, scene_index

class LaunchAndStopComponent(Component):
    pass
    launch_button = ButtonControl(color=None)
    stop_button = ButtonControl(color=None)

    @depends(target_track=None)
    def __init__(self, target_track=None, *a, **k):
        super().__init__(*a, name='Launch_And_Stop', **k)
        self._target_track = target_track
        self.register_slot(self.application.view, self._update_buttons, 'focused_document_view')
        self._update_buttons()

    @launch_button.pressed
    def launch_button(self, _):
        slot_or_scene = None
        if self._target_track.target_track in self.song.tracks:
            slot_or_scene = self._target_track.target_track.clip_slots[scene_index()]
        elif self.song.view.selected_track == self.song.master_track:
            slot_or_scene = self.song.view.selected_scene
        if liveobj_valid(slot_or_scene):
            slot_or_scene.fire()
            return

    @stop_button.pressed
    def stop_button(self, _):
        if self._target_track.target_track in self.song.tracks:
            self._target_track.target_track.stop_all_clips()
            return
        elif self.song.view.selected_track == self.song.master_track:
            self.song.stop_all_clips()
            return
        else:
            return None

    def _update_buttons(self):
        in_session = self.application.view.focused_document_view == 'Session'
        self.launch_button.enabled = in_session
        self.stop_button.enabled = in_session