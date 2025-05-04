# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MackieControl\ChannelStrip.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
from ableton.v2.base import liveobj_valid
from .MackieControlComponent import *

class ChannelStrip(MackieControlComponent):
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    def __init__(self, main_script, strip_index):
        MackieControlComponent.__init__(self, main_script)
        self.__channel_strip_controller = None
        self.__is_touched = False
        self.__strip_index = strip_index
        self.__stack_offset = 0
        self.__bank_and_channel_offset = 0
        self.__assigned_track = None
        self.__v_pot_parameter = None
        self.__v_pot_display_mode = VPOT_DISPLAY_SINGLE_DOT
        self.__fader_parameter = None
        self.__meters_enabled = False
        self.__last_meter_value = (-1)
        self.__send_meter_mode()
        self.__within_track_added_or_deleted = False
        self.__within_destroy = False
        self.set_bank_and_channel_offset(offset=0, show_return_tracks=False, within_track_added_or_deleted=False)

    def destroy(self):
        self.__within_destroy = True
        if self.__assigned_track:
            self.__remove_listeners()
        self.__assigned_track = None
        self.send_midi((208, 0 + (self.__strip_index << 4)))
        self.__meters_enabled = False
        self.__send_meter_mode()
        self.refresh_state()
        MackieControlComponent.destroy(self)
        self.__within_destroy = False

    def set_channel_strip_controller(self, channel_strip_controller):
        self.__channel_strip_controller = channel_strip_controller

    def strip_index(self):
        return self.__strip_index

    def assigned_track(self):
        return self.__assigned_track

    def is_touched(self):
        return self.__is_touched

    def set_is_touched(self, touched):
        self.__is_touched = touched

    def stack_offset(self):
        return self.__stack_offset

    def set_stack_offset(self, offset):
        pass
        self.__stack_offset = offset

    def set_bank_and_channel_offset(self, offset, show_return_tracks, within_track_added_or_deleted):
        final_track_index = self.__strip_index + self.__stack_offset + offset
        self.__within_track_added_or_deleted = within_track_added_or_deleted
        if show_return_tracks:
            tracks = self.song().return_tracks
        else:  # inserted
            tracks = self.song().visible_tracks
        if final_track_index < len(tracks):
            new_track = tracks[final_track_index]
        else:  # inserted
            new_track = None
        if new_track!= self.__assigned_track:
            if self.__assigned_track:
                self.__remove_listeners()
            self.__assigned_track = new_track
            if self.__assigned_track:
                self.__add_listeners()
        self.refresh_state()
        self.__within_track_added_or_deleted = False
        return

    def v_pot_parameter(self):
        return self.__v_pot_parameter

    def set_v_pot_parameter(self, parameter, display_mode=VPOT_DISPLAY_SINGLE_DOT):
        self.__v_pot_display_mode = display_mode
        self.__v_pot_parameter = parameter
        if not parameter:
            self.unlight_vpot_leds()

    def fader_parameter(self):
        return self.__fader_parameter

    def set_fader_parameter(self, parameter):
        self.__fader_parameter = parameter
        if not parameter:
            self.reset_fader()
            return
        else:  # inserted
            return None

    def enable_meter_mode(self, Enabled, needs_to_send_meter_mode=True):
        self.__meters_enabled = Enabled
        if needs_to_send_meter_mode or Enabled:
            self.__send_meter_mode()
            return
        else:  # inserted
            return None

    def reset_fader(self):
        self.send_midi((PB_STATUS + self.__strip_index, 0, 0))

    def unlight_vpot_leds(self):
        self.send_midi((CC_STATUS + 0, 48 + self.__strip_index, 32))

    def show_full_enlighted_poti(self):
        self.send_midi((CC_STATUS + 0, 48 + self.__strip_index, VPOT_DISPLAY_WRAP * 16 + 11))

    def handle_channel_strip_switch_ids(self, sw_id, value):
        if sw_id in range(SID_RECORD_ARM_BASE, SID_RECORD_ARM_BASE + NUM_CHANNEL_STRIPS):
            if sw_id - SID_RECORD_ARM_BASE is self.__strip_index:
                if value == BUTTON_PRESSED:
                    if self.song().exclusive_arm:
                        exclusive = not self.control_is_pressed()
                    else:  # inserted
                        exclusive = self.control_is_pressed()
                    self.__toggle_arm_track(exclusive)
        else:  # inserted
            if sw_id in range(SID_SOLO_BASE, SID_SOLO_BASE + NUM_CHANNEL_STRIPS):
                if sw_id - SID_SOLO_BASE is self.__strip_index:
                    if value == BUTTON_PRESSED:
                        if self.song().exclusive_solo:
                            exclusive = not self.control_is_pressed()
                        else:  # inserted
                            exclusive = self.control_is_pressed()
                        self.__toggle_solo_track(exclusive)
            else:  # inserted
                if sw_id in range(SID_MUTE_BASE, SID_MUTE_BASE + NUM_CHANNEL_STRIPS):
                    if sw_id - SID_MUTE_BASE is self.__strip_index and value == BUTTON_PRESSED:
                            self.__toggle_mute_track()
                            return
                        else:  # inserted
                            return None
                else:  # inserted
                    if sw_id in range(SID_SELECT_BASE, SID_SELECT_BASE + NUM_CHANNEL_STRIPS) and sw_id - SID_SELECT_BASE is self.__strip_index and (value == BUTTON_PRESSED):
                                self.__select_track()
                    else:  # inserted
                        if sw_id in range(SID_VPOD_PUSH_BASE, SID_VPOD_PUSH_BASE + NUM_CHANNEL_STRIPS) and sw_id - SID_VPOD_PUSH_BASE is self.__strip_index and (value == BUTTON_PRESSED) and (self.__channel_strip_controller!= None):
                                        self.__channel_strip_controller.handle_pressed_v_pot(self.__strip_index, self.__stack_offset)
                        else:  # inserted
                            if sw_id in fader_touch_switch_ids and sw_id - SID_FADER_TOUCH_SENSE_BASE is self.__strip_index and (value == BUTTON_PRESSED or value == BUTTON_RELEASED):
                                        touched = self.__channel_strip_controller!= None and value == BUTTON_PRESSED
                                            self.set_is_touched(touched)
                                            self.__channel_strip_controller.handle_fader_touch(self.__strip_index, self.__stack_offset, touched)

    def handle_vpot_rotation(self, strip_index, cc_value):
        if strip_index is self.__strip_index and self.__channel_strip_controller!= None:
                self.__channel_strip_controller.handle_vpot_rotation(self.__strip_index, self.__stack_offset, cc_value)

    def refresh_state(self):
        if not self.__within_track_added_or_deleted:
            self.__update_track_is_selected_led()
        self.__update_solo_led()
        self.__update_mute_led()
        self.__update_arm_led()
        if not self.__within_destroy and self.__assigned_track!= None:
            self.__send_meter_mode()
            self.__last_meter_value = (-1)
        if not self.__assigned_track:
            self.reset_fader()
            self.unlight_vpot_leds()
            return
        else:  # inserted
            return None

    def on_update_display_timer(self):
        pass  # cflow: irreducible

    def build_midi_map(self, midi_map_handle):
        needs_takeover = False
        if self.__fader_parameter:
            feeback_rule = Live.MidiMap.PitchBendFeedbackRule()
            feeback_rule.channel = self.__strip_index
            feeback_rule.value_pair_map = tuple()
            feeback_rule.delay_in_ms = 200.0
            Live.MidiMap.map_midi_pitchbend_with_feedback_map(midi_map_handle, self.__fader_parameter, self.__strip_index, feeback_rule, not needs_takeover)
            Live.MidiMap.send_feedback_for_parameter(midi_map_handle, self.__fader_parameter)
        else:  # inserted
            channel = self.__strip_index
            Live.MidiMap.forward_midi_pitchbend(self.script_handle(), midi_map_handle, channel)
        if self.__v_pot_parameter:
            if self.__v_pot_display_mode == VPOT_DISPLAY_SPREAD:
                range_end = 7
            else:  # inserted
                range_end = 12
            feeback_rule = Live.MidiMap.CCFeedbackRule()
            feeback_rule.channel = 0
            feeback_rule.cc_no = 48 + self.__strip_index
            feeback_rule.cc_value_map = tuple([self.__v_pot_display_mode * 16 + x for x in range(1, range_end)])
            feeback_rule.delay_in_ms = (-1.0)
            Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, self.__v_pot_parameter, 0, FID_PANNING_BASE + self.__strip_index, Live.MidiMap.MapMode.relative_signed_bit, feeback_rule, needs_takeover)
            Live.MidiMap.send_feedback_for_parameter(midi_map_handle, self.__v_pot_parameter)
        else:  # inserted
            channel = 0
            cc_no = FID_PANNING_BASE + self.__strip_index
            Live.MidiMap.forward_midi_cc(self.script_handle(), midi_map_handle, channel, cc_no)

    def __assigned_track_index(self):
        index = 0
        for t in chain(self.song().visible_tracks, self.song().return_tracks):
            if t == self.__assigned_track:
                return index
            else:  # inserted
                index += 1
                continue
        if self.__assigned_track:
            pass  # postinserted
        return None

    def __add_listeners(self):
        if self.__assigned_track and self.__assigned_track in self.song().tracks:
            self.__assigned_track.add_input_routing_type_listener(self.__update_arm_led)
            if self.__assigned_track.can_be_armed:
                self.__assigned_track.add_arm_listener(self.__update_arm_led)
        self.__assigned_track.add_mute_listener(self.__update_mute_led)
        self.__assigned_track.add_solo_listener(self.__update_solo_led)
        if not self.song().view.selected_track_has_listener(self.__update_track_is_selected_led):
            self.song().view.add_selected_track_listener(self.__update_track_is_selected_led)

    def __remove_listeners(self):
        if liveobj_valid(self.__assigned_track):
            if self.__assigned_track in self.song().tracks:
                self.__remove_listener(self.__assigned_track, 'input_routing_type', self.__update_arm_led)
                if self.__assigned_track.can_be_armed:
                    self.__remove_listener(self.__assigned_track, 'arm', self.__update_arm_led)
            self.__remove_listener(self.__assigned_track, 'mute', self.__update_mute_led)
            self.__remove_listener(self.__assigned_track, 'solo', self.__update_solo_led)
            self.__remove_listener(self.song().view, 'selected_track', self.__update_track_is_selected_led)
            return

    def __remove_listener(self, object, property, listener):
        if getattr(object, '{}_has_listener'.format(property))(listener):
            getattr(object, 'remove_{}_listener'.format(property))(listener)

    def __send_meter_mode(self):
        on_mode = 1
        off_mode = 0
        if self.__meters_enabled:
            on_mode = on_mode | 2
        if self.__assigned_track:
            mode = on_mode
        else:  # inserted
            mode = off_mode
        if self.main_script().is_extension():
            device_type = SYSEX_DEVICE_TYPE_XT
        else:  # inserted
            device_type = SYSEX_DEVICE_TYPE
        self.send_midi((240, 0, 0, 102, device_type, 32, self.__strip_index, mode, 247))

    def __toggle_arm_track(self, exclusive):
        if self.__assigned_track and self.__assigned_track.can_be_armed:
                self.__assigned_track.arm = not self.__assigned_track.arm
                if exclusive:
                    for t in self.song().tracks:
                        if t!= self.__assigned_track and t.can_be_armed:
                            t.arm = False
                        pass
                        continue
                else:  # inserted
                    return
            else:  # inserted
                return None
        else:  # inserted
            return None

    def __toggle_mute_track(self):
        if self.__assigned_track:
            self.__assigned_track.mute = not self.__assigned_track.mute

    def __toggle_solo_track(self, exclusive):
        if self.__assigned_track:
            self.__assigned_track.solo = not self.__assigned_track.solo
            if exclusive:
                for t in chain(self.song().tracks, self.song().return_tracks):
                    if t!= self.__assigned_track:
                        t.solo = False
                    pass
                    continue
            else:  # inserted
                return
        else:  # inserted
            return None

    def __select_track(self):
        if self.__assigned_track:
            all_tracks = tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)
            if self.song().view.selected_track!= all_tracks[self.__assigned_track_index()]:
                self.song().view.selected_track = all_tracks[self.__assigned_track_index()]
                return
            else:  # inserted
                if self.application().view.is_view_visible('Arranger') and self.__assigned_track:
                        self.__assigned_track.view.is_collapsed = not self.__assigned_track.view.is_collapsed
                        return
                else:  # inserted
                    return
        else:  # inserted
            return None

    def __update_arm_led(self):
        track = self.__assigned_track
        if track and track.can_be_armed and track.arm:
            self.send_midi((NOTE_ON_STATUS, SID_RECORD_ARM_BASE + self.__strip_index, BUTTON_STATE_ON))
            return
        else:  # inserted
            self.send_midi((NOTE_ON_STATUS, SID_RECORD_ARM_BASE + self.__strip_index, BUTTON_STATE_OFF))
            return

    def __update_mute_led(self):
        if self.__assigned_track and self.__assigned_track.mute:
            self.send_midi((NOTE_ON_STATUS, SID_MUTE_BASE + self.__strip_index, BUTTON_STATE_ON))
            return
        else:  # inserted
            self.send_midi((NOTE_ON_STATUS, SID_MUTE_BASE + self.__strip_index, BUTTON_STATE_OFF))
            return

    def __update_solo_led(self):
        if self.__assigned_track and self.__assigned_track.solo:
            self.send_midi((NOTE_ON_STATUS, SID_SOLO_BASE + self.__strip_index, BUTTON_STATE_ON))
            return
        else:  # inserted
            self.send_midi((NOTE_ON_STATUS, SID_SOLO_BASE + self.__strip_index, BUTTON_STATE_OFF))

    def __update_track_is_selected_led(self):
        if self.song().view.selected_track == self.__assigned_track:
            self.send_midi((NOTE_ON_STATUS, SID_SELECT_BASE + self.__strip_index, BUTTON_STATE_ON))
            return
        else:  # inserted
            self.send_midi((NOTE_ON_STATUS, SID_SELECT_BASE + self.__strip_index, BUTTON_STATE_OFF))
            return

class MasterChannelStrip(MackieControlComponent):
    def __init__(self, main_script):
        MackieControlComponent.__init__(self, main_script)
        self.__strip_index = MASTER_CHANNEL_STRIP_INDEX
        self.__assigned_track = self.song().master_track

    def destroy(self):
        self.reset_fader()
        MackieControlComponent.destroy(self)

    def set_channel_strip_controller(self, channel_strip_controller):
        return

    def handle_channel_strip_switch_ids(self, sw_id, value):
        return

    def refresh_state(self):
        return

    def on_update_display_timer(self):
        return

    def enable_meter_mode(self, Enabled):
        return

    def reset_fader(self):
        self.send_midi((PB_STATUS + self.__strip_index, 0, 0))

    def build_midi_map(self, midi_map_handle):
        if self.__assigned_track:
            needs_takeover = False
            volume = self.__assigned_track.mixer_device.volume
            feeback_rule = Live.MidiMap.PitchBendFeedbackRule()
            feeback_rule.channel = self.__strip_index
            feeback_rule.value_pair_map = tuple()
            feeback_rule.delay_in_ms = 200.0
            Live.MidiMap.map_midi_pitchbend_with_feedback_map(midi_map_handle, volume, self.__strip_index, feeback_rule, not needs_takeover)
            Live.MidiMap.send_feedback_for_parameter(midi_map_handle, volume)