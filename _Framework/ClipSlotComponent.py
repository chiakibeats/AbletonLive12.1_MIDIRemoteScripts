# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\ClipSlotComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from .ControlSurfaceComponent import ControlSurfaceComponent
from .SubjectSlot import subject_slot
from .Util import in_range

def find_nearest_color(rgb_table, src_hex_color):
    def hex_to_channels(color_in_hex):
        return ((color_in_hex & 16711680) >> 16, (color_in_hex & 65280) >> 8, color_in_hex & 255)

    def squared_distance(color):
        return sum([(a - b) ** 2 for a, b in zip(hex_to_channels(src_hex_color), hex_to_channels(color[1]))])
    return min(rgb_table, key=squared_distance)[0]

class ClipSlotComponent(ControlSurfaceComponent):
    pass

    def __init__(self, *a, **k):
        super(ClipSlotComponent, self).__init__(*a, **k)
        self._clip_slot = None
        self._triggered_to_play_value = 126
        self._triggered_to_record_value = 121
        self._started_value = 127
        self._recording_value = 120
        self._stopped_value = 0
        self._clip_palette = []
        self._clip_rgb_table = None
        self._record_button_value = None
        self._has_fired_slot = False
        self._delete_button = None
        self._select_button = None
        self._duplicate_button = None

    def on_enabled_changed(self):
        self.update()

    def set_clip_slot(self, clip_slot):
        self._clip_slot = clip_slot
        self._update_clip_property_slots()
        self._on_slot_triggered_changed.subject = clip_slot
        self._on_slot_playing_state_changed.subject = clip_slot
        self._on_clip_state_changed.subject = clip_slot
        self._on_controls_other_clips_changed.subject = clip_slot
        self._on_has_stop_button_changed.subject = clip_slot
        self._on_clip_slot_color_changed.subject = clip_slot
        track = clip_slot.canonical_parent if clip_slot else None
        if track and track in self.song().tracks:
            self._on_arm_value_changed.subject = track
            self._on_implicit_arm_value_changed.subject = track
            self._on_input_routing_type_changed.subject = track
        self.update()

    def set_launch_button(self, button):
        self._launch_button_value.subject = button
        self.update()

    def set_delete_button(self, button):
        self._delete_button = button

    def set_select_button(self, button):
        self._select_button = button

    def set_duplicate_button(self, button):
        self._duplicate_button = button

    def set_triggered_to_play_value(self, value):
        self._triggered_to_play_value = value

    def set_triggered_to_record_value(self, value):
        self._triggered_to_record_value = value

    def set_started_value(self, value):
        self._started_value = value

    def set_recording_value(self, value):
        self._recording_value = value

    def set_stopped_value(self, value):
        self._stopped_value = value
        self._clip_palette = []

    def set_record_button_value(self, value):
        self._record_button_value = value

    def set_clip_palette(self, palette):
        self._stopped_value = None
        self._clip_palette = palette

    def set_clip_rgb_table(self, rgb_table):
        pass
        self._clip_rgb_table = rgb_table

    def has_clip(self):
        return self._clip_slot.has_clip

    def update(self):
        super(ClipSlotComponent, self).update()
        self._has_fired_slot = False
        button = self._launch_button_value.subject
        if self._allow_updates and self.is_enabled() and (button!= None):
                    value_to_send = self._feedback_value()
                    if value_to_send in (None, (-1)):
                        button.turn_off()
                        return
                    else:  # inserted
                        if in_range(value_to_send, 0, 128):
                            button.send_value(value_to_send)
                            return
                        else:  # inserted
                            button.set_light(value_to_send)
                            return
                else:  # inserted
                    return None
            else:  # inserted
                return None
        else:  # inserted
            self._update_requests += 1

    def _color_value(self, color):
        try:
            return self._clip_palette[color]
        except (KeyError, IndexError):
            if self._clip_rgb_table!= None:
                return find_nearest_color(self._clip_rgb_table, color)
            else:  # inserted
                return self._stopped_value

    def _track_is_armed(self, track):
        return track!= None and track.can_be_armed and any([track.arm, track.implicit_arm])

    def _feedback_value(self):
        if self._clip_slot!= None:
            track = self._clip_slot.canonical_parent
            slot_or_clip = self._clip_slot.clip if self.has_clip() else self._clip_slot
            if slot_or_clip.is_triggered:
                return self._triggered_to_record_value if slot_or_clip.will_record_on_start else self._triggered_to_play_value
            else:  # inserted
                if slot_or_clip.is_playing:
                    return self._recording_value if slot_or_clip.is_recording else self._started_value
                else:  # inserted
                    if slot_or_clip.color!= None:
                        return self._color_value(slot_or_clip.color)
                    else:  # inserted
                        if getattr(slot_or_clip, 'controls_other_clips', True) and self._stopped_value!= None:
                            return self._stopped_value
                        else:  # inserted
                            if self._track_is_armed(track) and self._clip_slot.has_stop_button and (self._record_button_value!= None):
                                return self._record_button_value
        return None

    def _update_clip_property_slots(self):
        clip = self._clip_slot.clip if self._clip_slot else None
        self._on_clip_playing_state_changed.subject = clip
        self._on_recording_state_changed.subject = clip
        self._on_clip_color_changed.subject = clip

    @subject_slot('has_clip')
    def _on_clip_state_changed(self):
        self._update_clip_property_slots()
        self.update()

    @subject_slot('controls_other_clips')
    def _on_controls_other_clips_changed(self):
        self._update_clip_property_slots()
        self.update()

    @subject_slot('color')
    def _on_clip_color_changed(self):
        self.update()

    @subject_slot('color')
    def _on_clip_slot_color_changed(self):
        self.update()

    @subject_slot('playing_status')
    def _on_slot_playing_state_changed(self):
        self.update()

    @subject_slot('playing_status')
    def _on_clip_playing_state_changed(self):
        self.update()

    @subject_slot('is_recording')
    def _on_recording_state_changed(self):
        self.update()

    @subject_slot('arm')
    def _on_arm_value_changed(self):
        self.update()

    @subject_slot('implicit_arm')
    def _on_implicit_arm_value_changed(self):
        self.update()

    @subject_slot('input_routing_type')
    def _on_input_routing_type_changed(self):
        self.update()

    @subject_slot('has_stop_button')
    def _on_has_stop_button_changed(self):
        self.update()

    @subject_slot('is_triggered')
    def _on_slot_triggered_changed(self):
        if not self.has_clip():
            song = self.song()
            view = song.view
            if song.select_on_launch and self._clip_slot.is_triggered and self._has_fired_slot and self._clip_slot.will_record_on_start and (self._clip_slot!= view.highlighted_clip_slot):
                view.highlighted_clip_slot = self._clip_slot
            self.update()
            return

    @subject_slot('value')
    def _launch_button_value(self, value):
        if self.is_enabled():
            if self._select_button and self._select_button.is_pressed() and value:
                self._do_select_clip(self._clip_slot)
                return
            else:  # inserted
                if self._clip_slot!= None:
                    if self._duplicate_button and self._duplicate_button.is_pressed():
                        if value:
                            self._do_duplicate_clip()
                            return
                        else:  # inserted
                            return None
                    else:  # inserted
                        if self._delete_button and self._delete_button.is_pressed():
                            if value:
                                self._do_delete_clip()
                                return
                            else:  # inserted
                                return None
                        else:  # inserted
                            self._do_launch_clip(value)
                            return
        else:  # inserted
            return

    def _do_delete_clip(self):
        if self._clip_slot and self._clip_slot.has_clip:
                self._clip_slot.delete_clip()
                return

    def _do_select_clip(self, clip_slot):
        if self._clip_slot!= None and self.song().view.highlighted_clip_slot!= self._clip_slot:
                self.song().view.highlighted_clip_slot = self._clip_slot

    def _do_duplicate_clip(self):
        if self._clip_slot and self._clip_slot.has_clip:
                try:
                    track = self._clip_slot.canonical_parent
                    track.duplicate_clip_slot(list(track.clip_slots).index(self._clip_slot))
                except Live.Base.LimitationError:
                    return None
                    return None
        else:  # inserted
            return

    def _do_launch_clip(self, value):
        button = self._launch_button_value.subject
        object_to_launch = self._clip_slot
        launch_pressed = value or not button.is_momentary()
        if self.has_clip():
            object_to_launch = self._clip_slot.clip
        else:  # inserted
            self._has_fired_slot = True
        if button.is_momentary():
            object_to_launch.set_fire_button_state(value!= 0)
        else:  # inserted
            if launch_pressed:
                object_to_launch.fire()
        if launch_pressed and self.has_clip():
                if self.song().select_on_launch:
                    self.song().view.highlighted_clip_slot = self._clip_slot
                    return
            else:  # inserted
                return
        else:  # inserted
            return None