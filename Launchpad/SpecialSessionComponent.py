# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad\SpecialSessionComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.SessionComponent import SessionComponent

class SpecialSessionComponent(SessionComponent):
    pass

    def _update_stop_clips_led(self, index):
        if self.is_enabled() and self._stop_track_clip_buttons != None and (index < len(self._stop_track_clip_buttons)):
            button = self._stop_track_clip_buttons[index]
            tracks_to_use = self.tracks_to_use()
            track_index = index + self.track_offset()
            if 0 <= track_index < len(tracks_to_use):
                track = tracks_to_use[track_index]
                if track.fired_slot_index == -2:
                    button.send_value(self._stop_clip_triggered_value)
                    return
                elif track.playing_slot_index >= 0:
                    button.send_value(self._stop_clip_value)
                    return
                else:
                    button.turn_off()
                    return
            else:
                button.send_value(4)
                return
        else:
            return