# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\ChannelStripComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
import Live
from .ControlSurfaceComponent import ControlSurfaceComponent
from .DisplayDataSource import DisplayDataSource
from .Util import nop

def release_control(control):
    if control!= None:
        control.release_parameter()

def reset_button(button):
    if button!= None:
        button.reset()

class ChannelStripComponent(ControlSurfaceComponent):
    pass
    _active_instances = []

    def number_of_arms_pressed():
        result = 0
        for strip in ChannelStripComponent._active_instances:
            if strip.arm_button_pressed():
                result += 1
            pass
            continue
        return result
    number_of_arms_pressed = staticmethod(number_of_arms_pressed)

    def number_of_solos_pressed():
        result = 0
        for strip in ChannelStripComponent._active_instances:
            if strip.solo_button_pressed():
                result += 1
            pass
            continue
        return result
    number_of_solos_pressed = staticmethod(number_of_solos_pressed)
    empty_color = None

    def __init__(self):
        ControlSurfaceComponent.__init__(self)
        ChannelStripComponent._active_instances.append(self)
        self._track = None
        self._send_controls = []
        self._pan_control = None
        self._volume_control = None
        self._select_button = None
        self._mute_button = None
        self._solo_button = None
        self._arm_button = None
        self._shift_button = None
        self._crossfade_toggle = None
        self._shift_pressed = False
        self._solo_pressed = False
        self._arm_pressed = False
        self._invert_mute_feedback = False
        self._track_name_data_source = DisplayDataSource()
        self._update_track_name_data_source()
        self._empty_control_slots = self.register_slot_manager()

        def make_property_slot(name, alias=None):
            alias = alias or name
            return self.register_slot(None, getattr(self, '_on_%s_changed' % alias), name)
        self._track_property_slots = [make_property_slot('mute'), make_property_slot('solo'), make_property_slot('arm'), make_property_slot('input_routing_type', 'input_routing'), make_property_slot('name', 'track_name')]
        self._mixer_device_property_slots = [make_property_slot('crossfade_assign', 'cf_assign'), make_property_slot('sends')]

        def make_button_slot(name):
            return self.register_slot(None, getattr(self, '_%s_value' % name), 'value')
        self._select_button_slot = make_button_slot('select')
        self._mute_button_slot = make_button_slot('mute')
        self._solo_button_slot = make_button_slot('solo')
        self._arm_button_slot = make_button_slot('arm')
        self._shift_button_slot = make_button_slot('shift')
        self._crossfade_toggle_slot = make_button_slot('crossfade_toggle')

    def disconnect(self):
        pass
        ChannelStripComponent._active_instances.remove(self)
        for button in [self._select_button, self._mute_button, self._solo_button, self._arm_button, self._shift_button, self._crossfade_toggle]:
            reset_button(button)
        for control in self._all_controls():
            release_control(control)
        self._track_name_data_source.set_display_string('')
        self._select_button = None
        self._mute_button = None
        self._solo_button = None
        self._arm_button = None
        self._shift_button = None
        self._crossfade_toggle = None
        self._track_name_data_source = None
        self._pan_control = None
        self._volume_control = None
        self._send_controls = None
        self._track = None
        super(ChannelStripComponent, self).disconnect()

    def set_track(self, track):
        for control in self._all_controls():
            release_control(control)
        self._track = track
        for slot in self._track_property_slots:
            slot.subject = track
        for slot in self._mixer_device_property_slots:
            slot.subject = track.mixer_device if track!= None else None
            continue
        if self._track!= None:
            for button in [self._select_button, self._mute_button, self._solo_button, self._arm_button, self._crossfade_toggle]:
                if button!= None:
                    button.turn_off()
                continue
        self._update_track_name_data_source()
        self.update()

    def reset_button_on_exchange(self, button):
        reset_button(button)

    def _update_track_name_data_source(self):
        self._track_name_data_source.set_display_string(self._track.name if self._track!= None else ' - ')

    def set_send_controls(self, controls):
        for control in list(self._send_controls or []):
            release_control(control)
        self._send_controls = controls
        self.update()

    def set_pan_control(self, control):
        if control!= self._pan_control:
            release_control(self._pan_control)
            self._pan_control = control
            self.update()

    def set_volume_control(self, control):
        if control!= self._volume_control:
            release_control(self._volume_control)
            self._volume_control = control
            self.update()

    def set_select_button(self, button):
        if button!= self._select_button:
            self.reset_button_on_exchange(self._select_button)
            self._select_button = button
            self._select_button_slot.subject = button
            self.update()

    def set_mute_button(self, button):
        if button!= self._mute_button:
            self.reset_button_on_exchange(self._mute_button)
            self._mute_button = button
            self._mute_button_slot.subject = button
            self.update()

    def set_solo_button(self, button):
        if button!= self._solo_button:
            self.reset_button_on_exchange(self._solo_button)
            self._solo_pressed = False
            self._solo_button = button
            self._solo_button_slot.subject = button
            self.update()

    def set_arm_button(self, button):
        if button!= self._arm_button:
            self.reset_button_on_exchange(self._arm_button)
            self._arm_pressed = False
            self._arm_button = button
            self._arm_button_slot.subject = button
            self.update()

    def set_shift_button(self, button):
        if button!= self._shift_button:
            self.reset_button_on_exchange(self._shift_button)
            self._shift_button = button
            self._shift_button_slot.subject = button
            self.update()

    def set_crossfade_toggle(self, button):
        if button!= self._crossfade_toggle:
            self.reset_button_on_exchange(self._crossfade_toggle)
            self._crossfade_toggle = button
            self._crossfade_toggle_slot.subject = button
            self.update()

    def set_invert_mute_feedback(self, invert_feedback):
        if invert_feedback!= self._invert_mute_feedback:
            self._invert_mute_feedback = invert_feedback
            self.update()

    def on_enabled_changed(self):
        self.update()

    def on_selected_track_changed(self):
        if not self.is_enabled() or self._select_button!= None:
                if self._track!= None or self.empty_color == None:
                    if self.song().view.selected_track == self._track:
                        self._select_button.turn_on()
                        return
                    else:  # inserted
                        self._select_button.turn_off()
                        return
                else:  # inserted
                    self._select_button.set_light(self.empty_color)
                    return

    def solo_button_pressed(self):
        return self._solo_pressed

    def arm_button_pressed(self):
        return self._arm_pressed

    def track_name_data_source(self):
        return self._track_name_data_source

    @property
    def track(self):
        return self._track

    def _connect_parameters(self):
        if self._pan_control!= None:
            self._pan_control.connect_to(self._track.mixer_device.panning)
        if self._volume_control!= None:
            self._volume_control.connect_to(self._track.mixer_device.volume)
        if self._send_controls!= None:
            index = 0
            for send_control in self._send_controls:
                if send_control!= None:
                    if index < len(self._track.mixer_device.sends):
                        send_control.connect_to(self._track.mixer_device.sends[index])
                    else:  # inserted
                        send_control.release_parameter()
                        self._empty_control_slots.register_slot(send_control, nop, 'value')
                index += 1
                continue
        else:  # inserted
            return

    def _all_controls(self):
        return [self._pan_control, self._volume_control] + list(self._send_controls or [])

    def _disconnect_parameters(self):
        for control in self._all_controls():
            release_control(control)
            self._empty_control_slots.register_slot(control, nop, 'value')

    def update(self):
        super(ChannelStripComponent, self).update()
        if not self._allow_updates or self.is_enabled():
                self._empty_control_slots.disconnect()
                if self._track!= None:
                    self._connect_parameters()
                else:  # inserted
                    self._disconnect_parameters()
                self.on_selected_track_changed()
                self._on_mute_changed()
                self._on_solo_changed()
                self._on_arm_changed()
                self._on_cf_assign_changed()
                return
            else:  # inserted
                self._disconnect_parameters()
                return
        else:  # inserted
            self._update_requests += 1

    def _select_value(self, value):
        if self.is_enabled() and self._track!= None and (value!= 0 or not self._select_button.is_momentary()):
                    if self.song().view.selected_track!= self._track:
                        self.song().view.selected_track = self._track
                        return
        else:  # inserted
            return

    def _mute_value(self, value):
        if self.is_enabled() and self._track!= None and (self._track!= self.song().master_track) and self._mute_button.is_momentary() and (value!= 0):
                        self._track.mute = not self._track.mute
                        return
            else:  # inserted
                return
        else:  # inserted
            return None

    def update_solo_state(self, solo_exclusive, new_value, respect_multi_selection, track):
        if track == self._track or (respect_multi_selection and track.is_part_of_selection):
            track.solo = new_value
            return
        else:  # inserted
            if solo_exclusive and track.solo:
                    track.solo = False
                    return
            else:  # inserted
                return

    def _solo_value(self, value):
        if self.is_enabled() and self._track!= None and (self._track!= self.song().master_track):
                    self._solo_pressed = value!= 0 and self._solo_button.is_momentary()
                    if value!= 0 or not self._solo_button.is_momentary():
                        expected_solos_pressed = 1 if self._solo_pressed else 0
                        solo_exclusive = self.song().exclusive_solo!= self._shift_pressed and (not self._solo_button.is_momentary() or ChannelStripComponent.number_of_solos_pressed() == expected_solos_pressed)
                        new_value = not self._track.solo
                        respect_multi_selection = self._track.is_part_of_selection
                        for track in chain(self.song().tracks, self.song().return_tracks):
                            self.update_solo_state(solo_exclusive, new_value, respect_multi_selection, track)

    def _arm_value(self, value):
        if self.is_enabled() and self._track!= None and self._track.can_be_armed:
                    self._arm_pressed = value!= 0 and self._arm_button.is_momentary()
                    if not self._arm_button.is_momentary() or value!= 0:
                        expected_arms_pressed = 1 if self._arm_pressed else 0
                        arm_exclusive = self.song().exclusive_arm!= self._shift_pressed and (not self._arm_button.is_momentary() or ChannelStripComponent.number_of_arms_pressed() == expected_arms_pressed)
                        new_value = not self._track.arm
                        respect_multi_selection = self._track.is_part_of_selection
                        for track in self.song().tracks:
                            if track.can_be_armed:
                                if track == self._track or (respect_multi_selection and track.is_part_of_selection):
                                    track.arm = new_value
                                    continue
                                else:  # inserted
                                    if arm_exclusive and track.arm:
                                        track.arm = False
                            continue

    def _shift_value(self, value):
        self._shift_pressed = value!= 0

    def _crossfade_toggle_value(self, value):
        if self.is_enabled() and self._track!= None and (value!= 0 or not self._crossfade_toggle.is_momentary()):
                    self._track.mixer_device.crossfade_assign = (self._track.mixer_device.crossfade_assign - 1) % len(self._track.mixer_device.crossfade_assignments.values)
                    return

    def _on_sends_changed(self):
        if self.is_enabled():
            self.update()
            return

    def _on_mute_changed(self):
        if not self.is_enabled() or self._mute_button!= None:
                if self._track!= None or self.empty_color == None:
                    if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.mute!= self._invert_mute_feedback:
                        self._mute_button.turn_on()
                        return
                    else:  # inserted
                        self._mute_button.turn_off()
                        return
                else:  # inserted
                    self._mute_button.set_light(self.empty_color)
                    return

    def _on_solo_changed(self):
        if not self.is_enabled() or self._solo_button!= None:
                if self._track!= None or self.empty_color == None:
                    if self._track in chain(self.song().tracks, self.song().return_tracks) and self._track.solo:
                        self._solo_button.turn_on()
                        return
                    else:  # inserted
                        self._solo_button.turn_off()
                        return
                else:  # inserted
                    self._solo_button.set_light(self.empty_color)
                    return
        else:  # inserted
            return

    def _on_arm_changed(self):
        if not self.is_enabled() or self._arm_button!= None:
                if self._track!= None or self.empty_color == None:
                    if self._track in self.song().tracks and self._track.can_be_armed and self._track.arm:
                        self._arm_button.turn_on()
                        return
                    else:  # inserted
                        self._arm_button.turn_off()
                        return
                else:  # inserted
                    self._arm_button.set_light(self.empty_color)
                    return

    def _on_track_name_changed(self):
        if self._track!= None:
            self._update_track_name_data_source()
            return
        else:  # inserted
            return None

    def _on_cf_assign_changed(self):
        if not self.is_enabled() or self._crossfade_toggle!= None:
                if self._track!= None and self._track in chain(self.song().tracks, self.song().return_tracks) and (self._track.mixer_device.crossfade_assign!= 1):
                    self._crossfade_toggle.turn_on()
                    return
                else:  # inserted
                    self._crossfade_toggle.turn_off()
                    return

    def _on_input_routing_changed(self):
        if self.is_enabled():
            self._on_arm_changed()