# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\session.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import find_if
from ableton.v2.control_surface.components import SessionComponent as SessionComponentBase

class SessionComponent(SessionComponentBase):

    def _update_stop_clips_led(self, index):
        super()._update_stop_clips_led(index)
        self._update_stop_all_clips_button()

    def _update_stop_all_clips_button(self):
        button = self._stop_all_button
        if button:
            value_to_send = self._stop_clip_disabled_value
            tracks = self.song.tracks
            if find_if(lambda x: x.playing_slot_index >= 0 and x.fired_slot_index != -2, tracks):
                value_to_send = self._stop_clip_value
            elif find_if(lambda x: x.fired_slot_index == -2, tracks):
                value_to_send = self._stop_clip_triggered_value
            button.set_light(value_to_send)
            return