# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AxiomPro\DisplayingMixerComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ButtonElement import ButtonElement
from _Framework.MixerComponent import MixerComponent
from _Framework.PhysicalDisplayElement import PhysicalDisplayElement

class DisplayingMixerComponent(MixerComponent):
    pass

    def __init__(self, num_tracks):
        MixerComponent.__init__(self, num_tracks)
        self._selected_tracks = []
        self._display = None
        self._mute_button = None
        self._solo_button = None
        self._register_timer_callback(self._on_timer)

    def disconnect(self):
        self._unregister_timer_callback(self._on_timer)
        self._selected_tracks = None
        MixerComponent.disconnect(self)
        self._display = None

    def set_display(self, display):
        self._display = display

    def set_solo_button(self, button):
        self.selected_strip().set_solo_button(button)
        if self._solo_button!= button:
            if self._solo_button!= None:
                self._solo_button.remove_value_listener(self._solo_value)
            self._solo_button = button
            if self._solo_button!= None:
                self._solo_button.add_value_listener(self._solo_value)
            self.update()
            return

    def set_mute_button(self, button):
        self.selected_strip().set_mute_button(button)
        if self._mute_button!= button:
            if self._mute_button!= None:
                self._mute_button.remove_value_listener(self._mute_value)
            self._mute_button = button
            if self._mute_button!= None:
                self._mute_button.add_value_listener(self._mute_value)
            self.update()
            return

    def _on_timer(self):
        sel_track = None
        while len(self._selected_tracks) > 0:
            while True:  # inserted
                track = self._selected_tracks[(-1)]
                if track!= None and track.has_midi_input:
                    if track.can_be_armed and (not track.arm):
                        sel_track = track
                        break
                del self._selected_tracks[(-1)]
                    break
                else:  # inserted
                    continue
        if sel_track!= None:
            found_recording_clip = False
            song = self.song()
            tracks = song.tracks
            check_arrangement = song.is_playing and song.record_mode
            for track in tracks:
                if track.can_be_armed and track.arm:
                    if check_arrangement:
                        found_recording_clip = True
                        break
                    else:  # inserted
                        playing_slot_index = track.playing_slot_index
                        if playing_slot_index in range(len(track.clip_slots)):
                            slot = track.clip_slots[playing_slot_index]
                            if slot.has_clip and slot.clip.is_recording:
                                found_recording_clip = True
                                break
                continue
            if not found_recording_clip:
                if song.exclusive_arm:
                    for track in tracks:
                        if track.can_be_armed and track.arm and (track!= sel_track):
                            track.arm = False
                        continue
                sel_track.arm = True
                sel_track.view.select_instrument()
        self._selected_tracks = []

    def _solo_value(self, value):
        if self._display!= None and self.song().view.selected_track not in (self.song().master_track, None):
                if value!= 0:
                    track = self.song().view.selected_track
                    display_string = str(track.name) + ': Solo '
                    if track.solo:
                        display_string += 'On'
                    else:  # inserted
                        display_string += 'Off'
                    self._display.display_message(display_string)
                    return
                else:  # inserted
                    self._display.update()
                    return
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _mute_value(self, value):
        if self._display!= None and self.song().view.selected_track not in (self.song().master_track, None):
                if value!= 0:
                    track = self.song().view.selected_track
                    display_string = str(track.name) + ': Mute '
                    if track.mute:
                        display_string += 'On'
                    else:  # inserted
                        display_string += 'Off'
                    self._display.display_message(display_string)
                    return
                else:  # inserted
                    self._display.update()
                    return
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _next_track_value(self, value):
        MixerComponent._next_track_value(self, value)
        self._selected_tracks.append(self.song().view.selected_track)

    def _prev_track_value(self, value):
        MixerComponent._prev_track_value(self, value)
        self._selected_tracks.append(self.song().view.selected_track)