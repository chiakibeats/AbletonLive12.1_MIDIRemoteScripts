# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\FireOne\FireOne.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
import MidiRemoteScript
from ableton.v2.base import move_current_song_time
NOTE_OFF_STATUS = 128
NOTE_ON_STATUS = 144
CC_STATUS = 176
NUM_NOTES = 128
NUM_CC_NO = 128
NUM_CHANNELS = 16
JOG_DIAL_CC = 60
RWD_NOTE = 91
FFWD_NOTE = 92
STOP_NOTE = 93
PLAY_NOTE = 94
REC_NOTE = 95
SHIFT_NOTE = 70
FIRE_ONE_TRANSPORT = [RWD_NOTE, FFWD_NOTE, STOP_NOTE, PLAY_NOTE, REC_NOTE]
FIRE_ONE_F_KEYS = list(range(54, 64))
FIRE_ONE_CHANNEL = 0

class FireOne(object):
    pass

    def __init__(self, c_instance):
        self.__c_instance = c_instance
        self.__shift_pressed = False
        self.__rwd_pressed = False
        self.__ffwd_pressed = False
        self.__jog_dial_map_mode = Live.MidiMap.MapMode.absolute
        self.__spooling_counter = 0
        self.song().add_is_playing_listener(self.__playing_status_changed)
        self.song().add_record_mode_listener(self.__recording_status_changed)
        self.song().add_visible_tracks_listener(self.__tracks_changed)
        self.__playing_status_changed()
        self.__recording_status_changed()

    def application(self):
        pass
        return Live.Application.get_application()

    def song(self):
        pass
        return self.__c_instance.song()

    def disconnect(self):
        pass
        self.send_midi((NOTE_OFF_STATUS + FIRE_ONE_CHANNEL, PLAY_NOTE, 0))
        self.send_midi((NOTE_OFF_STATUS + FIRE_ONE_CHANNEL, REC_NOTE, 0))
        self.song().remove_is_playing_listener(self.__playing_status_changed)
        self.song().remove_record_mode_listener(self.__recording_status_changed)
        self.song().remove_visible_tracks_listener(self.__tracks_changed)

    def connect_script_instances(self, instanciated_scripts):
        pass
        return

    def suggest_input_port(self):
        pass
        return str('FireOne Control')

    def suggest_output_port(self):
        pass
        return str('FireOne Control')

    def suggest_map_mode(self, cc_no, channel):
        pass
        suggested_map_mode = Live.MidiMap.MapMode.absolute
        if cc_no == JOG_DIAL_CC:
            suggested_map_mode = self.__jog_dial_map_mode
        return suggested_map_mode

    def can_lock_to_devices(self):
        return False

    def request_rebuild_midi_map(self):
        pass
        self.__c_instance.request_rebuild_midi_map()

    def send_midi(self, midi_event_bytes):
        pass
        self.__c_instance.send_midi(midi_event_bytes)

    def refresh_state(self):
        pass
        return

    def build_midi_map(self, midi_map_handle):
        pass
        script_handle = self.__c_instance.handle()
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, FIRE_ONE_CHANNEL, JOG_DIAL_CC)
        for note in FIRE_ONE_TRANSPORT:
            Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, FIRE_ONE_CHANNEL, note)
        Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, FIRE_ONE_CHANNEL, SHIFT_NOTE)
        for index in range(len(self.song().visible_tracks)):
            if len(FIRE_ONE_F_KEYS) > index:
                Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, FIRE_ONE_CHANNEL, FIRE_ONE_F_KEYS[index])
                continue
            else:
                return

    def update_display(self):
        pass
        if self.__ffwd_pressed:
            self.__spooling_counter += 1
            if self.__spooling_counter % 2 == 0:
                self.song().jump_by(self.song().signature_denominator)
        elif self.__rwd_pressed:
            self.__spooling_counter += 1
            if self.__spooling_counter % 2 == 0:
                self.song().jump_by(-1 * self.song().signature_denominator)
                return

    def receive_midi(self, midi_bytes):
        pass
        cc_or_note = midi_bytes[1]
        if midi_bytes[0] & 240 == CC_STATUS:
            if cc_or_note is JOG_DIAL_CC:
                self.__jog_dial_message(cc_or_note, midi_bytes[2])
        elif midi_bytes[0] & 240 in (NOTE_ON_STATUS, NOTE_OFF_STATUS):
            value = midi_bytes[2]
            if midi_bytes[0] & 240 == NOTE_OFF_STATUS:
                value = 0
            if cc_or_note is SHIFT_NOTE:
                self.__shift_pressed = value != 0
                return
            elif cc_or_note in FIRE_ONE_TRANSPORT:
                self.__transport_message(cc_or_note, value)
                return
            elif cc_or_note in FIRE_ONE_F_KEYS:
                self.__f_key_message(cc_or_note, value)
                return
        else:
            return

    def __playing_status_changed(self):
        pass
        status = NOTE_OFF_STATUS
        note = PLAY_NOTE
        value = 0
        if self.song().is_playing:
            status = NOTE_ON_STATUS
            value = 127
        status += FIRE_ONE_CHANNEL
        self.send_midi((status, note, value))

    def __recording_status_changed(self):
        pass
        status = NOTE_OFF_STATUS
        note = REC_NOTE
        value = 0
        if self.song().record_mode:
            status = NOTE_ON_STATUS
            value = 127
        status += FIRE_ONE_CHANNEL
        self.send_midi((status, note, value))

    def __tracks_changed(self):
        self.request_rebuild_midi_map()

    def __transport_message(self, note, value):
        pass
        if note is PLAY_NOTE and value != 0:
            if self.__shift_pressed:
                self.song().continue_playing()
            else:
                self.song().is_playing = True
                return
        elif note is STOP_NOTE and value != 0:
            self.song().is_playing = False
            return
        elif note is REC_NOTE and value != 0:
            self.song().record_mode = not self.song().record_mode
            return
        elif note is FFWD_NOTE:
            if value != 0 and (not self.__rwd_pressed):
                if self.__shift_pressed:
                    self.song().jump_by(1)
                    return
                else:
                    self.song().jump_by(self.song().signature_denominator)
                    self.__ffwd_pressed = True
                    self.__spooling_counter = 0
                    return
            elif value == 0:
                self.__ffwd_pressed = False
                return
            else:
                return None
        elif note is RWD_NOTE:
            if value != 0 and (not self.__ffwd_pressed):
                if self.__shift_pressed:
                    self.song().jump_by(-1)
                    return
                else:
                    self.song().jump_by(-1 * self.song().signature_denominator)
                    self.__rwd_pressed = True
                    self.__spooling_counter = 0
                    return
            elif value == 0:
                self.__rwd_pressed = False
                return

    def __jog_dial_message(self, cc_no, cc_value):
        pass
        moved_forward = cc_value in range(1, 64)
        if not self.__shift_pressed:
            if self.application().view.is_view_visible('Session'):
                index = list(self.song().scenes).index(self.song().view.selected_scene)
                if moved_forward:
                    if index < len(self.song().scenes) - 1:
                        index = index + 1
                    pass
                elif index > 0:
                    index = index - 1
                self.song().view.selected_scene = self.song().scenes[index]
                return
            else:
                value = cc_value
                if not moved_forward:
                    value -= 64
                    value *= -1
                move_current_song_time(self.song(), value)
                return
        elif self.application().view.is_view_visible('Session'):
            tracks = self.song().visible_tracks
            index = list(tracks).index(self.song().view.selected_track)
            if moved_forward:
                if index < len(tracks) - 1:
                    index = index + 1
                pass
            elif index > 0:
                index = index - 1
            self.song().view.selected_track = tracks[index]
            return
        else:
            value = cc_value
            if not moved_forward:
                value -= 64
                value *= -0.1
            self.song().tempo = self.song().tempo + 0.1 * value
            return

    def __f_key_message(self, f_key, value):
        index = list(FIRE_ONE_F_KEYS).index(f_key)
        tracks = self.song().visible_tracks
        track = tracks[index]
        if value > 0:
            if self.__shift_pressed:
                if track.can_be_armed:
                    track.arm = not track.arm
            else:
                track.mute = not track.mute