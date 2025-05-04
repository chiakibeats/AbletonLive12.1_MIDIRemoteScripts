# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\RemoteSL_Classic\MixerController.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from .consts import *
from .RemoteSLComponent import RemoteSLComponent
SLIDER_MODE_VOLUME = 0
SLIDER_MODE_PAN = 1
SLIDER_MODE_SEND = 2
FORW_REW_JUMP_BY_AMOUNT = 1

class MixerController(RemoteSLComponent):
    pass

    def __init__(self, remote_sl_parent, display_controller):
        RemoteSLComponent.__init__(self, remote_sl_parent)
        self.__display_controller = display_controller
        self.__parent = remote_sl_parent
        self.__forward_button_down = False
        self.__rewind_button_down = False
        self.__strip_offset = 0
        self.__slider_mode = SLIDER_MODE_VOLUME
        self.__strips = [MixerChannelStrip(self, i) for i in range(NUM_CONTROLS_PER_ROW)]
        self.__assigned_tracks = []
        self.__transport_locked = False
        self.__lock_enquiry_delay = 0
        self.song().add_visible_tracks_listener(self.__on_tracks_added_or_deleted)
        self.song().add_record_mode_listener(self.__on_record_mode_changed)
        self.song().add_is_playing_listener(self.__on_is_playing_changed)
        self.song().add_loop_listener(self.__on_loop_changed)
        self.__reassign_strips()

    def disconnect(self):
        self.song().remove_visible_tracks_listener(self.__on_tracks_added_or_deleted)
        self.song().remove_record_mode_listener(self.__on_record_mode_changed)
        self.song().remove_is_playing_listener(self.__on_is_playing_changed)
        self.song().remove_loop_listener(self.__on_loop_changed)
        for strip in self.__strips:
            strip.set_assigned_track(None)
        for track in self.__assigned_tracks:
            if track and track.name_has_listener(self.__on_track_name_changed):
                track.remove_name_listener(self.__on_track_name_changed)
            continue

    def remote_sl_parent(self):
        return self.__parent

    def slider_mode(self):
        return self.__slider_mode

    def receive_midi_cc(self, cc_no, cc_value):
        if cc_no in mx_display_button_ccs:
            self.__handle_page_up_down_ccs(cc_no, cc_value)
        elif cc_no in mx_select_button_ccs:
            self.__handle_select_button_ccs(cc_no, cc_value)
        elif cc_no in mx_first_button_row_ccs:
            channel_strip = self.__strips[cc_no - MX_FIRST_BUTTON_ROW_BASE_CC]
            if cc_value == CC_VAL_BUTTON_PRESSED:
                channel_strip.first_button_pressed()
            else:
                return None
        elif cc_no in mx_second_button_row_ccs:
            channel_strip = self.__strips[cc_no - MX_SECOND_BUTTON_ROW_BASE_CC]
            if cc_value == CC_VAL_BUTTON_PRESSED:
                channel_strip.second_button_pressed()
            else:
                return None
        elif cc_no in mx_slider_row_ccs:
            channel_strip = self.__strips[cc_no - MX_SLIDER_ROW_BASE_CC]
            channel_strip.slider_moved(cc_value)
        elif cc_no in ts_ccs:
            self.__handle_transport_ccs(cc_no, cc_value)
        else:
            return None

    def build_midi_map(self, script_handle, midi_map_handle):
        needs_takeover = True
        for s in self.__strips:
            cc_no = MX_SLIDER_ROW_BASE_CC + self.__strips.index(s)
            if s.assigned_track() and s.slider_parameter():
                map_mode = Live.MidiMap.MapMode.absolute
                parameter = s.slider_parameter()
                Live.MidiMap.map_midi_cc(midi_map_handle, parameter, SL_MIDI_CHANNEL, cc_no, map_mode, not needs_takeover)
                continue
            else:
                Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, SL_MIDI_CHANNEL, cc_no)
                continue
        for cc_no in mx_forwarded_ccs + ts_ccs:
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, SL_MIDI_CHANNEL, cc_no)
        for note in mx_forwarded_notes + ts_notes:
            Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, SL_MIDI_CHANNEL, note)

    def refresh_state(self):
        self.__update_selected_row_leds()
        self.__reassign_strips()
        self.__lock_enquiry_delay = 3

    def update_display(self):
        if self.__lock_enquiry_delay > 0:
            self.__lock_enquiry_delay -= 1
            if self.__lock_enquiry_delay == 0:
                self.send_midi((176, 103, 1))
        if self.__rewind_button_down:
            self.song().jump_by(-FORW_REW_JUMP_BY_AMOUNT)
        if self.__forward_button_down:
            self.song().jump_by(FORW_REW_JUMP_BY_AMOUNT)
            return
        else:
            return None

    def __reassign_strips(self):
        track_index = self.__strip_offset
        track_names = []
        parameters = []
        for track in self.__assigned_tracks:
            if track and track.name_has_listener(self.__on_track_name_changed):
                track.remove_name_listener(self.__on_track_name_changed)
            continue
        self.__assigned_tracks = []
        all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)
        for s in self.__strips:
            if track_index < len(all_tracks):
                track = all_tracks[track_index]
                s.set_assigned_track(track)
                track_names.append(track.name)
                parameters.append(s.slider_parameter())
                track.add_name_listener(self.__on_track_name_changed)
                self.__assigned_tracks.append(track)
            else:
                s.set_assigned_track(None)
                track_names.append('')
                parameters.append(None)
            track_index += 1
            continue
        self.__display_controller.setup_right_display(track_names, parameters)
        self.request_rebuild_midi_map()
        if self.support_mkII():
            page_up_value = CC_VAL_BUTTON_RELEASED
            page_down_value = CC_VAL_BUTTON_RELEASED
            if len(all_tracks) > NUM_CONTROLS_PER_ROW and self.__strip_offset < len(all_tracks) - NUM_CONTROLS_PER_ROW:
                page_up_value = CC_VAL_BUTTON_PRESSED
            if self.__strip_offset > 0:
                page_down_value = CC_VAL_BUTTON_PRESSED
            self.send_midi((self.cc_status_byte(), MX_DISPLAY_PAGE_UP, page_up_value))
            self.send_midi((self.cc_status_byte(), MX_DISPLAY_PAGE_DOWN, page_down_value))
            return
        else:
            return None

    def __handle_page_up_down_ccs(self, cc_no, cc_value):
        all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)
        if cc_no == MX_DISPLAY_PAGE_UP and cc_value == CC_VAL_BUTTON_PRESSED and (len(all_tracks) > NUM_CONTROLS_PER_ROW) and (self.__strip_offset < len(all_tracks) - NUM_CONTROLS_PER_ROW):
            self.__strip_offset += NUM_CONTROLS_PER_ROW
            self.__validate_strip_offset()
            self.__reassign_strips()
        elif cc_no == MX_DISPLAY_PAGE_DOWN and cc_value == CC_VAL_BUTTON_PRESSED and (len(all_tracks) > NUM_CONTROLS_PER_ROW) and (self.__strip_offset > 0):
            self.__strip_offset -= NUM_CONTROLS_PER_ROW
            self.__validate_strip_offset()
            self.__reassign_strips()
            return

    def __handle_select_button_ccs(self, cc_no, cc_value):
        if cc_no == MX_SELECT_SLIDER_ROW:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self.__set_slider_mode(SLIDER_MODE_VOLUME)
                return
            else:
                return None
        elif cc_no == MX_SELECT_FIRST_BUTTON_ROW:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self.__set_slider_mode(SLIDER_MODE_PAN)
                return
            else:
                return None
        elif cc_no == MX_SELECT_SECOND_BUTTON_ROW:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self.__set_slider_mode(SLIDER_MODE_SEND)
                return
            else:
                return None
        else:
            return None

    def __handle_transport_ccs(self, cc_no, cc_value):
        if cc_no == TS_REWIND_CC:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self.__rewind_button_down = True
                self.song().jump_by(-FORW_REW_JUMP_BY_AMOUNT)
            else:
                self.__rewind_button_down = False
        elif cc_no == TS_FORWARD_CC:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self.__forward_button_down = True
                self.song().jump_by(FORW_REW_JUMP_BY_AMOUNT)
            else:
                self.__forward_button_down = False
        elif cc_no == TS_STOP_CC:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self.song().stop_playing()
        elif cc_no == TS_PLAY_CC:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self.song().start_playing()
        elif cc_no == TS_LOOP_CC:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self.song().loop = not self.song().loop
        elif cc_no == TS_RECORD_CC:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self.song().record_mode = not self.song().record_mode
            else:
                return None
        elif cc_no == TS_LOCK:
            self.__transport_locked = cc_value != CC_VAL_BUTTON_RELEASED
            self.__on_transport_lock_changed()

    def __on_transport_lock_changed(self):
        for strip in self.__strips:
            strip.take_control_of_second_button(not self.__transport_locked)
        if self.__transport_locked:
            self.__on_is_playing_changed()
            self.__on_loop_changed()
            self.__on_record_mode_changed()
            return

    def __on_tracks_added_or_deleted(self):
        self.__validate_strip_offset()
        self.__validate_slider_mode()
        self.__reassign_strips()

    def __on_track_name_changed(self):
        self.__reassign_strips()

    def __validate_strip_offset(self):
        all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks) + (self.song().master_track,)
        self.__strip_offset = min(self.__strip_offset, len(all_tracks) - 1)
        self.__strip_offset = max(0, self.__strip_offset)

    def __validate_slider_mode(self):
        if self.__slider_mode - SLIDER_MODE_SEND >= len(self.song().return_tracks):
            self.__slider_mode = SLIDER_MODE_VOLUME

    def __set_slider_mode(self, new_mode):
        if self.__slider_mode >= SLIDER_MODE_SEND and new_mode >= SLIDER_MODE_SEND:
            if self.__slider_mode - SLIDER_MODE_SEND + 1 < len(self.song().return_tracks):
                self.__slider_mode += 1
            else:
                self.__slider_mode = SLIDER_MODE_SEND
            self.__update_selected_row_leds()
            self.__reassign_strips()
            return
        elif self.__slider_mode != new_mode:
            self.__slider_mode = new_mode
            self.__update_selected_row_leds()
            self.__reassign_strips()
            return
        else:
            return None

    def __update_selected_row_leds(self):
        if self.__slider_mode == SLIDER_MODE_VOLUME:
            self.send_midi((self.cc_status_byte(), MX_SELECT_SLIDER_ROW, CC_VAL_BUTTON_PRESSED))
            self.send_midi((self.cc_status_byte(), MX_SELECT_FIRST_BUTTON_ROW, CC_VAL_BUTTON_RELEASED))
            self.send_midi((self.cc_status_byte(), MX_SELECT_SECOND_BUTTON_ROW, CC_VAL_BUTTON_RELEASED))
            return
        elif self.__slider_mode == SLIDER_MODE_PAN:
            self.send_midi((self.cc_status_byte(), MX_SELECT_SLIDER_ROW, CC_VAL_BUTTON_RELEASED))
            self.send_midi((self.cc_status_byte(), MX_SELECT_FIRST_BUTTON_ROW, CC_VAL_BUTTON_PRESSED))
            self.send_midi((self.cc_status_byte(), MX_SELECT_SECOND_BUTTON_ROW, CC_VAL_BUTTON_RELEASED))
            return
        elif self.__slider_mode >= SLIDER_MODE_SEND:
            self.send_midi((self.cc_status_byte(), MX_SELECT_SLIDER_ROW, CC_VAL_BUTTON_RELEASED))
            self.send_midi((self.cc_status_byte(), MX_SELECT_FIRST_BUTTON_ROW, CC_VAL_BUTTON_RELEASED))
            self.send_midi((self.cc_status_byte(), MX_SELECT_SECOND_BUTTON_ROW, CC_VAL_BUTTON_PRESSED))
            return
        else:
            return None

    def __on_record_mode_changed(self):
        if self.__transport_locked or not self.support_mkII():
            record_cc = TS_RECORD_CC
            if self.support_mkII():
                record_cc = 53
            record_value = CC_VAL_BUTTON_PRESSED
            if not self.song().record_mode:
                record_value = CC_VAL_BUTTON_RELEASED
            self.send_midi((self.cc_status_byte(), record_cc, record_value))
            return

    def __on_is_playing_changed(self):
        if self.__transport_locked and self.support_mkII():
            if self.song().is_playing:
                self.send_midi((self.cc_status_byte(), 51, CC_VAL_BUTTON_PRESSED))
                self.send_midi((self.cc_status_byte(), 50, CC_VAL_BUTTON_RELEASED))
            else:
                self.send_midi((self.cc_status_byte(), 51, CC_VAL_BUTTON_RELEASED))
                self.send_midi((self.cc_status_byte(), 50, CC_VAL_BUTTON_PRESSED))

    def __on_loop_changed(self):
        if self.__transport_locked and self.support_mkII():
            if self.song().loop:
                self.send_midi((self.cc_status_byte(), 52, CC_VAL_BUTTON_PRESSED))
            else:
                self.send_midi((self.cc_status_byte(), 52, CC_VAL_BUTTON_RELEASED))

    def is_arm_exclusive(self):
        return self.__parent.song().exclusive_arm

    def set_selected_track(self, track):
        if track:
            self.__parent.song().view.selected_track = track

    def track_about_to_arm(self, track):
        if track:
            if self.__parent.song().exclusive_arm:
                for t in self.__parent.song().tracks:
                    if t.can_be_armed and t.arm and (not t == track):
                        t.arm = False
                    continue
                return None
            else:
                return None
        else:
            return None

class MixerChannelStrip(object):
    pass

    def __init__(self, mixer_controller_parent, index):
        self.__mixer_controller = mixer_controller_parent
        self.__index = index
        self.__assigned_track = None
        self.__control_second_button = True

    def song(self):
        return self.__mixer_controller.song()

    def assigned_track(self):
        return self.__assigned_track

    def set_assigned_track(self, track):
        if self.__assigned_track != None:
            if self.__assigned_track != self.song().master_track:
                self.__assigned_track.remove_mute_listener(self._on_mute_changed)
            if self.__assigned_track.can_be_armed:
                self.__assigned_track.remove_arm_listener(self._on_arm_changed)
        self.__assigned_track = track
        if self.__assigned_track != None:
            if self.__assigned_track != self.song().master_track:
                self.__assigned_track.add_mute_listener(self._on_mute_changed)
            if self.__assigned_track.can_be_armed:
                self.__assigned_track.add_arm_listener(self._on_arm_changed)
        self._on_mute_changed()
        self._on_arm_changed()

    def slider_parameter(self):
        slider_mode = self.__mixer_controller.slider_mode()
        if self.__assigned_track:
            if slider_mode == SLIDER_MODE_VOLUME:
                return self.__assigned_track.mixer_device.volume
            elif slider_mode == SLIDER_MODE_PAN:
                return self.__assigned_track.mixer_device.panning
            elif slider_mode >= SLIDER_MODE_SEND:
                send_index = slider_mode - SLIDER_MODE_SEND
                if send_index < len(self.__assigned_track.mixer_device.sends):
                    return self.__assigned_track.mixer_device.sends[send_index]
                else:
                    return

    def slider_moved(self, cc_value):
        return

    def take_control_of_second_button(self, take_control):
        if self.__mixer_controller.support_mkII():
            self.__mixer_controller.remote_sl_parent().send_midi((self.__mixer_controller.cc_status_byte(), self.__index + MX_SECOND_BUTTON_ROW_BASE_CC, 0))
        self.__control_second_button = take_control
        self._on_mute_changed()
        self._on_arm_changed()

    def first_button_pressed(self):
        if not self.__assigned_track or self.__assigned_track in tuple(self.song().visible_tracks) + tuple(self.song().return_tracks):
            self.__assigned_track.mute = not self.__assigned_track.mute

    def second_button_pressed(self):
        if self.__assigned_track in self.song().visible_tracks and self.__assigned_track.can_be_armed:
            self.__mixer_controller.track_about_to_arm(self.__assigned_track)
            self.__assigned_track.arm = not self.__assigned_track.arm
            if not self.__assigned_track.arm or self.__assigned_track.view.select_instrument():
                self.__mixer_controller.set_selected_track(self.__assigned_track)

    def _on_mute_changed(self):
        if self.__mixer_controller.support_mkII():
            value = 0
            if self.__assigned_track in tuple(self.song().tracks) + tuple(self.song().return_tracks) and (not self.__assigned_track.mute):
                value = 1
            self.__mixer_controller.remote_sl_parent().send_midi((self.__mixer_controller.cc_status_byte(), self.__index + MX_FIRST_BUTTON_ROW_BASE_CC, value))
            return

    def _on_arm_changed(self):
        if self.__control_second_button and self.__mixer_controller.support_mkII():
            value = 0
            if self.__assigned_track and self.__assigned_track in self.song().tracks and self.__assigned_track.can_be_armed and self.__assigned_track.arm:
                value = 1
            self.__mixer_controller.remote_sl_parent().send_midi((self.__mixer_controller.cc_status_byte(), self.__index + MX_SECOND_BUTTON_ROW_BASE_CC, value))