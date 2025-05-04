# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Oxygen_Pro\session.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.components import SessionComponent as SessionComponentBase
from ableton.v2.control_surface.control import ButtonControl, EncoderControl

class SessionComponent(SessionComponentBase):
    selected_scene_launch_button = ButtonControl()
    scene_encoder = EncoderControl()

    @scene_encoder.value
    def scene_encoder(self, value, _):
        factor = 1 if value < 0 else -1
        new_scene_index = factor + list(self.song.scenes).index(self.song.view.selected_scene)
        if new_scene_index in range(len(self.song.scenes)):
            self.song.view.selected_scene = self.song.scenes[new_scene_index]

    @selected_scene_launch_button.released_immediately
    def selected_scene_launch_button(self, _):
        self.song.view.selected_scene.fire()