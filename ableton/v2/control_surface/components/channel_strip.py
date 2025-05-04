# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\components\channel_strip.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
from ...base import EventObject, listens, liveobj_valid, nop
from ..component import Component
from ..control import ButtonControl
from ..elements import DisplayDataSource

def release_control(control):
    if control is not None:
        control.release_parameter()

def reset_button(button):
    if button is not None:
        button.reset()

class ChannelStripComponent(Component):
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
    select_button = ButtonControl()

    def __init__(self, *a, **k):
        super(ChannelStripComponent, self).__init__(self, *a, **k)
        ChannelStripComponent._active_instances.append(self)
        self._track = None
        self._send_controls = []
        self._pan_control = None
        self._volume_control = None
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
        self._empty_control_slots = self.register_disconnectable(EventObject())
        self.__on_selected_track_changed.subject = self.song.view

        def make_property_slot(name, alias=None):
            alias = alias or name
            return self.register_slot(None, getattr(self, '_on_%s_changed' % alias), name)
        self._track_property_slots = [make_property_slot('mute'), make_property_slot('solo'), make_property_slot('arm'), make_property_slot('input_routing_type', 'input_routing'), make_property_slot('name', 'track_name')]
        self._mixer_device_property_slots = [make_property_slot('crossfade_assign', 'cf_assign'), make_property_slot('sends')]

        def make_button_slot(name):
            return self.register_slot(None, getattr(self, '_%s_value' % name), 'value')
        self._mute_button_slot = make_button_slot('mute')
        self._solo_button_slot = make_button_slot('solo')
        self._arm_button_slot = make_button_slot('arm')
        self._shift_button_slot = make_button_slot('shift')
        self._crossfade_toggle_slot = make_button_slot('crossfade_toggle')

    def disconnect(self):
        pass
        ChannelStripComponent._active_instances.remove(self)
        for button in [self._mute_button, self._solo_button, self._arm_button, self._shift_button, self._crossfade_toggle]:
            reset_button(button)
        for control in self._all_controls():
            release_control(control)
        self._track_name_data_source.set_display_string('')
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
            slot.subject = track.mixer_device if liveobj_valid(track) else None
            continue
        if liveobj_valid(self._track):
            for button in [self._mute_button, self._solo_button, self._arm_button, self._crossfade_toggle]:
                if button is not None:
                    button.set_light(False)
                continue
        self.select_button.enabled = True if self._track else False
        self._update_track_name_data_source()
        self.update()

    def reset_button_on_exchange(self, button):
        reset_button(button)

    def _update_track_name_data_source(self):
        self._track_name_data_source.set_display_string(self._track.name if liveobj_valid(self._track) else ' - ')

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
        self.select_button.set_control_element(button)
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

    @listens('selected_track')
    def __on_selected_track_changed(self):
        self._update_select_button()

    def _update_select_button(self):
        if liveobj_valid(self._track) or self.empty_color is None:
            if self.song.view.selected_track == self._track:
                self.select_button.color = 'DefaultButton.On'
            else:  # inserted
                self.select_button.color = 'DefaultButton.Off'
        else:  # inserted
            self.select_button.color = self.empty_color

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
        if self._pan_control is not None:
            self._pan_control.connect_to(self._track.mixer_device.panning)
        if self._volume_control is not None:
            self._volume_control.connect_to(self._track.mixer_device.volume)
        if self._send_controls is not None:
            index = 0
            for send_control in self._send_controls:
                if send_control is not None:
                    if index < len(self._track.mixer_device.sends):
                        send_control.connect_to(self._track.mixer_device.sends[index])
                    else:  # inserted
                        send_control.release_parameter()
                        self._empty_control_slots.register_slot(send_control, nop, 'value')
                index += 1
                continue
            return None
        else:  # inserted
            return None

    def _all_controls(self):
        return [self._pan_control, self._volume_control] + list(self._send_controls or [])

    def _disconnect_parameters(self):
        for control in self._all_controls():
            release_control(control)
            self._empty_control_slots.register_slot(control, nop, 'value')

    def update(self):
        super(ChannelStripComponent, self).update()
        if self.is_enabled():
            self._empty_control_slots.disconnect()
            if liveobj_valid(self._track):
                self._connect_parameters()
            else:  # inserted
                self._disconnect_parameters()
            self.__on_selected_track_changed()
            self._on_mute_changed()
            self._on_solo_changed()
            self._on_arm_changed()
            self._on_cf_assign_changed()
        else:  # inserted
            self._disconnect_parameters()

    @select_button.pressed
    def select_button(self, button):
        self._on_select_button_pressed(button)

    def _on_select_button_pressed(self, button):
        if not liveobj_valid(self._track) or self.song.view.selected_track!= self._track:
                self.song.view.selected_track = self._track

    @select_button.pressed_delayed
    def select_button(self, button):
        self._on_select_button_pressed_delayed(button)

    def _on_select_button_pressed_delayed(self, button):
        return

    @select_button.released
    def select_button(self, button):
        self._on_select_button_released(button)

    def _on_select_button_released(self, button):
        return

    @select_button.double_clicked
    def select_button(self, button):
        self._on_select_button_double_clicked(button)

    def _on_select_button_double_clicked(self, button):
        return

    def _mute_value(self, value):
        if self.is_enabled() and liveobj_valid(self._track) and (self._track!= self.song.master_track):
                    if not self._mute_button.is_momentary() or value!= 0:
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
                    return None
            else:  # inserted
                return None

    def _solo_value(self, value):
        if self.is_enabled() and liveobj_valid(self._track) and (self._track!= self.song.master_track):
                    self._solo_pressed = value!= 0 and self._solo_button.is_momentary()
                    if value!= 0 or not self._solo_button.is_momentary():
                        expected_solos_pressed = 1 if self._solo_pressed else 0
                        solo_exclusive = self.song.exclusive_solo!= self._shift_pressed and (not self._solo_button.is_momentary() or ChannelStripComponent.number_of_solos_pressed() == expected_solos_pressed)
                        new_value = not self._track.solo
                        respect_multi_selection = self._track.is_part_of_selection
                        for track in chain(self.song.tracks, self.song.return_tracks):
                            self.update_solo_state(solo_exclusive, new_value, respect_multi_selection, track)
                    else:  # inserted
                        return
                else:  # inserted
                    return None

    def _arm_value(self, value):
        if self.is_enabled() and liveobj_valid(self._track) and self._track.can_be_armed:
                    self._arm_pressed = value!= 0 and self._arm_button.is_momentary()
                    if not self._arm_button.is_momentary() or value!= 0:
                        expected_arms_pressed = 1 if self._arm_pressed else 0
                        arm_exclusive = self.song.exclusive_arm!= self._shift_pressed and (not self._arm_button.is_momentary() or ChannelStripComponent.number_of_arms_pressed() == expected_arms_pressed)
                        new_value = not self._track.arm
                        respect_multi_selection = self._track.is_part_of_selection
                        for track in self.song.tracks:
                            if track.can_be_armed:
                                if track == self._track or (respect_multi_selection and track.is_part_of_selection):
                                    track.arm = new_value
                                    continue
                                else:  # inserted
                                    if arm_exclusive and track.arm:
                                        track.arm = False
                            continue
                else:  # inserted
                    return
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _shift_value(self, value):
        self._shift_pressed = value!= 0

    def _crossfade_toggle_value(self, value):
        if self.is_enabled() and liveobj_valid(self._track) and (value!= 0 or not self._crossfade_toggle.is_momentary()):
                    self._track.mixer_device.crossfade_assign = (self._track.mixer_device.crossfade_assign - 1) % len(self._track.mixer_device.crossfade_assignments.values)

    def _on_sends_changed(self):
        if self.is_enabled():
            self.update()
            return

    def _on_mute_changed(self):
        if self.is_enabled():
            if self._mute_button is not None:
                if liveobj_valid(self._track) or self.empty_color is None:
                    if self._track in chain(self.song.tracks, self.song.return_tracks) and self._track.mute!= self._invert_mute_feedback:
                        self._mute_button.set_light('Mixer.MuteOff')
                    else:  # inserted
                        self._mute_button.set_light('Mixer.MuteOn')
                else:  # inserted
                    self._mute_button.set_light(self.empty_color)

    def _on_solo_changed(self):
        if self.is_enabled():
            if self._solo_button is not None:
                if liveobj_valid(self._track) or self.empty_color is None:
                    if self._track in chain(self.song.tracks, self.song.return_tracks) and self._track.solo:
                        self._solo_button.set_light('Mixer.SoloOn')
                        return
                    else:  # inserted
                        self._solo_button.set_light('Mixer.SoloOff')
                else:  # inserted
                    self._solo_button.set_light(self.empty_color)

    def _on_arm_changed(self):
        if self.is_enabled():
            if self._arm_button is not None:
                if liveobj_valid(self._track) or self.empty_color is None:
                    if self._track in self.song.tracks and self._track.can_be_armed and self._track.arm:
                        self._arm_button.set_light('Mixer.ArmOn')
                        return
                    else:  # inserted
                        self._arm_button.set_light('Mixer.ArmOff')
                else:  # inserted
                    self._arm_button.set_light(self.empty_color)

    def _on_track_name_changed(self):
        if liveobj_valid(self._track):
            self._update_track_name_data_source()
            return
        else:  # inserted
            return None

    def _on_cf_assign_changed(self):
        if self.is_enabled():
            if self._crossfade_toggle is not None:
                if liveobj_valid(self._track) and self._track in chain(self.song.tracks, self.song.return_tracks) and (self._track.mixer_device.crossfade_assign!= 1):
                    self._crossfade_toggle.set_light(True)
                else:  # inserted
                    self._crossfade_toggle.set_light(False)

    def _on_input_routing_changed(self):
        if self.is_enabled():
            self._on_arm_changed()
            return