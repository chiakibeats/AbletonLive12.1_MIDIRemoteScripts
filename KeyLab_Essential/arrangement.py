# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential\arrangement.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import move_current_song_time
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl, EncoderControl

class ArrangementComponent(Component):
    set_or_delete_cue_button = ButtonControl()
    jump_encoder = EncoderControl()

    @set_or_delete_cue_button.pressed
    def set_or_delete_cue_button(self, _):
        if self.application.view.focused_document_view == 'Arranger':
            self.song.set_or_delete_cue()

    @jump_encoder.value
    def jump_encoder(self, value, _):
        step = -1.0 if value < 0 else 1.0
        if self.song.is_playing:
            step *= 4.0
        move_current_song_time(self.song, step)