# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Arturia\SessionComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.Control import EncoderControl
from _Framework.SessionComponent import SessionComponent as SessionComponentBase

class SessionComponent(SessionComponentBase):
    scene_select_encoder = EncoderControl()
    _session_component_ends_initialisation = False

    def __init__(self, *a, **k):
        super(SessionComponent, self).__init__(*a, **k)
        self.set_offsets(0, 0)
        self.on_selected_scene_changed()
        self.on_selected_track_changed()

    def set_scene_select_control(self, control):
        self.scene_select_encoder.set_control_element(control)

    @scene_select_encoder.value
    def scene_select_encoder(self, value, encoder):
        selected_scene = self.song().view.selected_scene
        all_scenes = self.song().scenes
        current_index = list(all_scenes).index(selected_scene)
        if value > 0 and selected_scene != all_scenes[-1]:
            self.song().view.selected_scene = all_scenes[current_index + 1]
            return
        elif value < 0 and selected_scene != all_scenes[0]:
            self.song().view.selected_scene = all_scenes[current_index - 1]
            return
        else:
            return

    def on_selected_scene_changed(self):
        super(SessionComponent, self).on_selected_scene_changed()
        all_scenes = list(self.song().scenes)
        selected_scene = self.song().view.selected_scene
        new_scene_offset = all_scenes.index(selected_scene)
        self.set_offsets(self.track_offset(), new_scene_offset)

    def on_selected_track_changed(self):
        super(SessionComponent, self).on_selected_track_changed()
        tracks = list(self.song().tracks)
        selected_track = self.song().view.selected_track
        if selected_track in tracks:
            track_index = tracks.index(selected_track)
            new_track_offset = track_index - track_index % self.width()
            self.set_offsets(new_track_offset, self.scene_offset())