# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\scene_list.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from itertools import zip_longest
from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from .scene import MPCSceneComponent

class SceneListComponent(Component):

    def __init__(self, session_ring=None, num_scenes=0, *a, **k):
        super(SceneListComponent, self).__init__(*a, **k)
        self._session_ring = session_ring
        self.__on_offsets_changed.subject = session_ring
        self._scenes = [MPCSceneComponent(parent=self, session_ring=session_ring) for _ in range(num_scenes)]
        self.__on_scene_list_changed.subject = self.song
        self._reassign_scenes()

    def set_scene_launch_buttons(self, buttons):
        for scene, button in zip_longest(self._scenes, buttons or []):
            scene.set_launch_button(button)

    def set_scene_color_controls(self, controls):
        for scene, control in zip_longest(self._scenes, controls or []):
            scene.scene_color_control.set_control_element(control)

    @listens('offset')
    def __on_offsets_changed(self, *a):
        if self.is_enabled():
            self._reassign_scenes()

    @listens('scenes')
    def __on_scene_list_changed(self):
        self._reassign_scenes()

    def _reassign_scenes(self):
        scenes = self.song.scenes
        for index, scene in enumerate(self._scenes):
            scene_index = self._session_ring.scene_offset + index
            scene.set_scene(scenes[scene_index] if len(scenes) > scene_index else None)
            continue