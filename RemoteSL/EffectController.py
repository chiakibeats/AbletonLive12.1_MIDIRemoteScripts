# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\RemoteSL\EffectController.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.utils import old_div
import Live
from _Generic.Devices import *
from .consts import *
from .RemoteSLComponent import RemoteSLComponent

class EffectController(RemoteSLComponent):
    pass

    def __init__(self, remote_sl_parent, display_controller):
        RemoteSLComponent.__init__(self, remote_sl_parent)
        self.__display_controller = display_controller
        self.__parent = remote_sl_parent
        self.__last_selected_track = None
        self.__assigned_device_is_locked = False
        self.__assigned_device = None
        self.__change_assigned_device(self.__parent.song().appointed_device)
        self.__bank = 0
        self.__show_bank = False
        self.__strips = [EffectChannelStrip(self) for x in range(NUM_CONTROLS_PER_ROW)]
        self.__reassign_strips()

    def disconnect(self):
        self.__change_assigned_device(None)

    def receive_midi_cc(self, cc_no, cc_value):
        if cc_no in fx_display_button_ccs:
            self.__handle_page_up_down_ccs(cc_no, cc_value)
            return
        else:  # inserted
            if cc_no in fx_select_button_ccs:
                self.__handle_select_button_ccs(cc_no, cc_value)
                return
            else:  # inserted
                if cc_no in fx_upper_button_row_ccs:
                    strip = self.__strips[cc_no - FX_UPPER_BUTTON_ROW_BASE_CC]
                    if cc_value == CC_VAL_BUTTON_PRESSED:
                        strip.on_button_pressed()
                        return
                    else:  # inserted
                        return None
                else:  # inserted
                    if cc_no in fx_encoder_row_ccs:
                        strip = self.__strips[cc_no - FX_ENCODER_ROW_BASE_CC]
                        strip.on_encoder_moved(cc_value)
                        return
                    else:  # inserted
                        if cc_no in fx_lower_button_row_ccs:
                            return
                        else:  # inserted
                            if cc_no in fx_poti_row_ccs:
                                return
                            else:  # inserted
                                return None

    def receive_midi_note(self, note, velocity):
        if note in fx_drum_pad_row_notes:
            return
        else:  # inserted
            return None

    def build_midi_map(self, script_handle, midi_map_handle):
        needs_takeover = True
        for s in self.__strips:
            strip_index = self.__strips.index(s)
            cc_no = fx_encoder_row_ccs[strip_index]
            if s.assigned_parameter():
                map_mode = Live.MidiMap.MapMode.relative_smooth_signed_bit
                parameter = s.assigned_parameter()
                if self.support_mkII():
                    feedback_rule = Live.MidiMap.CCFeedbackRule()
                    feedback_rule.cc_no = fx_encoder_feedback_ccs[strip_index]
                    feedback_rule.channel = SL_MIDI_CHANNEL
                    feedback_rule.delay_in_ms = 0
                    feedback_rule.cc_value_map = tuple([int(1.5 + old_div(float(index), 127.0) * 10.0) for index in range(128)])
                    ring_mode_value = FX_RING_VOL_VALUE
                    if parameter.min == (-1) * parameter.max:
                        ring_mode_value = FX_RING_PAN_VALUE
                    else:  # inserted
                        if parameter.is_quantized:
                            ring_mode_value = FX_RING_SIN_VALUE
                    self.send_midi((self.cc_status_byte(), fx_encoder_led_mode_ccs[strip_index], ring_mode_value))
                    Live.MidiMap.map_midi_cc_with_feedback_map(midi_map_handle, parameter, SL_MIDI_CHANNEL, cc_no, map_mode, feedback_rule, not needs_takeover)
                    Live.MidiMap.send_feedback_for_parameter(midi_map_handle, parameter)
                    continue
                else:  # inserted
                    Live.MidiMap.map_midi_cc(midi_map_handle, parameter, SL_MIDI_CHANNEL, cc_no, map_mode, not needs_takeover)
                    continue
            else:  # inserted
                if self.support_mkII():
                    self.send_midi((self.cc_status_byte(), fx_encoder_led_mode_ccs[strip_index], 0))
                    self.send_midi((self.cc_status_byte(), fx_encoder_feedback_ccs[strip_index], 0))
                Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, SL_MIDI_CHANNEL, cc_no)
                continue
        for cc_no in fx_forwarded_ccs:
            Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, SL_MIDI_CHANNEL, cc_no)
        for note in fx_forwarded_notes:
            Live.MidiMap.forward_midi_note(script_handle, midi_map_handle, SL_MIDI_CHANNEL, note)

    def refresh_state(self):
        self.__update_select_row_leds()
        self.__reassign_strips()

    def __reassign_strips(self):
        page_up_value = CC_VAL_BUTTON_RELEASED
        page_down_value = CC_VAL_BUTTON_RELEASED
        if not self.__assigned_device == None:
            param_index = 0
            param_banks = 0
            chosen_bank = 0
            param_names = []
            parameters = []
            if list(DEVICE_DICT.keys()).count(self.__assigned_device.class_name) > 0:
                param_banks = DEVICE_DICT[self.__assigned_device.class_name]
                chosen_bank = param_banks[self.__bank]
            for s in self.__strips:
                param = None
                name = ''
                if chosen_bank:
                    param = get_parameter_by_name(self.__assigned_device, chosen_bank[param_index])
                else:  # inserted
                    new_index = param_index + 8 * self.__bank
                    device_parameters = self.__assigned_device.parameters[1:]
                    device_parameters = self.__assigned_device.parameters[1:]
                    if new_index < len(device_parameters):
                        param = device_parameters[new_index]
                if param:
                    name = param.name
                s.set_assigned_parameter(param)
                parameters.append(param)
                param_names.append(name)
                param_index += 1
                continue
            if self.__bank > 0:
                page_down_value = CC_VAL_BUTTON_PRESSED
            if self.__bank + 1 < number_of_parameter_banks(self.__assigned_device):
                page_up_value = CC_VAL_BUTTON_PRESSED
            self.__report_bank()
        else:  # inserted
            for s in self.__strips:
                s.set_assigned_parameter(None)
            param_names = ['Please select a Device in Live to edit it...']
            parameters = [None for x in range(NUM_CONTROLS_PER_ROW)]
        self.__display_controller.setup_left_display(param_names, parameters)
        self.request_rebuild_midi_map()
        if self.support_mkII():
            self.send_midi((self.cc_status_byte(), FX_DISPLAY_PAGE_DOWN, page_down_value))
            self.send_midi((self.cc_status_byte(), FX_DISPLAY_PAGE_UP, page_up_value))
            for cc_no in fx_upper_button_row_ccs:
                self.send_midi((self.cc_status_byte(), cc_no, CC_VAL_BUTTON_RELEASED))

    def __handle_page_up_down_ccs(self, cc_no, cc_value):
        if self.__assigned_device!= None:
            new_bank = self.__bank
            if cc_value == CC_VAL_BUTTON_PRESSED:
                if cc_no == FX_DISPLAY_PAGE_UP:
                    new_bank = min(self.__bank + 1, number_of_parameter_banks(self.__assigned_device) - 1)
                else:  # inserted
                    if cc_no == FX_DISPLAY_PAGE_DOWN:
                        new_bank = max(self.__bank - 1, 0)
            if not self.__bank == new_bank:
                self.__show_bank = True
                if not self.__assigned_device_is_locked:
                    self.__bank = new_bank
                    self.__reassign_strips()
                    return
                else:  # inserted
                    self.__assigned_device.store_chosen_bank(self.__parent.instance_identifier(), new_bank)
                    return

    def __handle_select_button_ccs(self, cc_no, cc_value):
        if cc_no == FX_SELECT_FIRST_BUTTON_ROW:
            if cc_value == CC_VAL_BUTTON_PRESSED:
                self.__parent.toggle_lock()
            else:  # inserted
                return None
        else:  # inserted
            if cc_no == FX_SELECT_ENCODER_ROW:
                if cc_value == CC_VAL_BUTTON_PRESSED:
                    new_index = min(len(self.song().scenes) - 1, max(0, list(self.song().scenes).index(self.song().view.selected_scene) - 1))
                    self.song().view.selected_scene = self.song().scenes[new_index]
            else:  # inserted
                if cc_no == FX_SELECT_SECOND_BUTTON_ROW:
                    if cc_value == CC_VAL_BUTTON_PRESSED:
                        new_index = min(len(self.song().scenes) - 1, max(0, list(self.song().scenes).index(self.song().view.selected_scene) + 1))
                        self.song().view.selected_scene = self.song().scenes[new_index]
                    else:  # inserted
                        return None
                else:  # inserted
                    if cc_no == FX_SELECT_POTIE_ROW:
                        if cc_value == CC_VAL_BUTTON_PRESSED:
                            self.song().view.selected_scene.fire_as_selected()
                    else:  # inserted
                        if cc_no == FX_SELECT_DRUM_PAD_ROW:
                            if cc_value == CC_VAL_BUTTON_PRESSED:
                                self.song().stop_all_clips()

    def __update_select_row_leds(self):
        if self.__assigned_device_is_locked:
            self.send_midi((self.cc_status_byte(), FX_SELECT_FIRST_BUTTON_ROW, CC_VAL_BUTTON_PRESSED))
            return
        else:  # inserted
            self.send_midi((self.cc_status_byte(), FX_SELECT_FIRST_BUTTON_ROW, CC_VAL_BUTTON_RELEASED))

    def lock_to_device(self, device):
        if device:
            self.__assigned_device_is_locked = True
            self.__change_assigned_device(device)
            self.__update_select_row_leds()
            self.__reassign_strips()

    def unlock_from_device(self, device):
        if not device or device == self.__assigned_device:
                self.__assigned_device_is_locked = False
                self.__update_select_row_leds()
                if not self.__parent.song().appointed_device == self.__assigned_device:
                    self.__reassign_strips()
                    return

    def set_appointed_device(self, device):
        if not self.__assigned_device_is_locked:
            self.__change_assigned_device(device)
            self.__update_select_row_leds()
            self.__reassign_strips()

    def __report_bank(self):
        if self.__show_bank:
            self.__show_bank = False
            if self.__assigned_device.class_name in list(DEVICE_DICT.keys()) and self.__assigned_device.class_name in list(BANK_NAME_DICT.keys()):
                    bank_names = BANK_NAME_DICT[self.__assigned_device.class_name]
                    if not bank_names or len(bank_names) > self.__bank:
                            bank_name = bank_names[self.__bank]
                            self.__show_bank_select(bank_name)
                else:  # inserted
                    self.__show_bank_select('Best of Parameters')
                    return
            else:  # inserted
                self.__show_bank_select('Bank' + str(self.__bank + 1))
                return

    def __show_bank_select(self, bank_name):
        if self.__assigned_device:
            self.__parent.show_message(str(self.__assigned_device.name + ' Bank: ' + bank_name))

    def restore_bank(self, bank):
        if self.__assigned_device_is_locked:
            self.__bank = bank
            self.__reassign_strips()

    def __change_assigned_device(self, device):
        if not device == self.__assigned_device:
            self.__bank = 0
            if not self.__assigned_device == None:
                self.__assigned_device.remove_parameters_listener(self.__parameter_list_of_device_changed)
            self.__show_bank = False
            self.__assigned_device = device
            if not self.__assigned_device == None:
                self.__assigned_device.add_parameters_listener(self.__parameter_list_of_device_changed)
                return

    def __parameter_list_of_device_changed(self):
        self.__reassign_strips()

class EffectChannelStrip(object):
    pass

    def __init__(self, mixer_controller_parent):
        self.__mixer_controller = mixer_controller_parent
        self.__assigned_parameter = None

    def assigned_parameter(self):
        return self.__assigned_parameter

    def set_assigned_parameter(self, parameter):
        self.__assigned_parameter = parameter

    def on_button_pressed(self):
        if self.__assigned_parameter and self.__assigned_parameter.is_enabled:
                if self.__assigned_parameter.is_quantized:
                    if self.__assigned_parameter.value + 1 > self.__assigned_parameter.max:
                        self.__assigned_parameter.value = self.__assigned_parameter.min
                    else:  # inserted
                        self.__assigned_parameter.value = self.__assigned_parameter.value + 1
                else:  # inserted
                    self.__assigned_parameter.value = self.__assigned_parameter.default_value

    def on_encoder_moved(self, cc_value):
        return