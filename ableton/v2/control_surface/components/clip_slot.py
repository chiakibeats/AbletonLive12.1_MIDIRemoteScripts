# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\components\clip_slot.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ...base import listens, liveobj_valid
from ..component import Component
from ..control import ButtonControl

def find_nearest_color(rgb_table, src_hex_color):

    def hex_to_channels(color_in_hex):
        return ((color_in_hex & 16711680) >> 16, (color_in_hex & 65280) >> 8, color_in_hex & 255)

    def squared_distance(color):
        return sum([(a - b) ** 2 for a, b in zip(hex_to_channels(src_hex_color), hex_to_channels(color[1]))])
    return min(rgb_table, key=squared_distance)[0]

def is_button_pressed(button):
    return button.is_pressed() if button else False

class ClipSlotComponent(Component):
    pass
    launch_button = ButtonControl()

    def __init__(self, *a, **k):
        super(ClipSlotComponent, self).__init__(*a, **k)
        self._clip_slot = None
        self._triggered_to_play_color = 'Session.ClipTriggeredPlay'
        self._triggered_to_record_color = 'Session.ClipTriggeredRecord'
        self._started_value = 'Session.ClipStarted'
        self._recording_color = 'Session.ClipRecording'
        self._stopped_value = 'Session.ClipStopped'
        self._clip_palette = []
        self._clip_rgb_table = None
        self._record_button_color = 'Session.RecordButton'
        self._empty_slot_color = 'Session.ClipEmpty'
        self._delete_button = None
        self._select_button = None
        self._duplicate_button = None

    def set_clip_slot(self, clip_slot):
        self._clip_slot = clip_slot
        self._update_clip_property_slots()
        self.__on_slot_triggered_changed.subject = clip_slot
        self.__on_slot_playing_state_changed.subject = clip_slot
        self.__on_clip_state_changed.subject = clip_slot
        self.__on_controls_other_clips_changed.subject = clip_slot
        self.__on_has_stop_button_changed.subject = clip_slot
        self.__on_clip_slot_color_changed.subject = clip_slot
        track = clip_slot.canonical_parent if clip_slot else None
        if track and track in self.song.tracks:
            self.__on_arm_value_changed.subject = track
            self.__on_implicit_arm_value_changed.subject = track
            self.__on_input_routing_type_changed.subject = track
        self.update()

    def set_launch_button(self, button):
        self.launch_button.set_control_element(button)
        self.update()

    def set_delete_button(self, button):
        self._delete_button = button

    def set_select_button(self, button):
        self._select_button = button

    def set_duplicate_button(self, button):
        self._duplicate_button = button

    def set_clip_palette(self, palette):
        self._clip_palette = palette

    def set_clip_rgb_table(self, rgb_table):
        pass
        self._clip_rgb_table = rgb_table

    def has_clip(self):
        return self._clip_slot.has_clip

    def update(self):
        super(ClipSlotComponent, self).update()
        self._update_launch_button_color()

    def _update_launch_button_color(self):
        if self.is_enabled():
            value_to_send = self._empty_slot_color
            if liveobj_valid(self._clip_slot):
                track = self._clip_slot.canonical_parent
                slot_or_clip = self._clip_slot.clip if self.has_clip() else self._clip_slot
                value_to_send = self._feedback_value(track, slot_or_clip)
            self.launch_button.color = value_to_send

    def _color_value(self, slot_or_clip):
        color = slot_or_clip.color
        try:
            return self._clip_palette[color]
        except (KeyError, IndexError):
            if self._clip_rgb_table is not None:
                return find_nearest_color(self._clip_rgb_table, color)
            else:
                return self._stopped_value

    def _track_is_armed(self, track):
        return liveobj_valid(track) and track.can_be_armed and any([track.arm, track.implicit_arm])

    def _feedback_value(self, track, slot_or_clip):
        if slot_or_clip.is_triggered:
            return self._triggered_to_record_color if slot_or_clip.will_record_on_start else self._triggered_to_play_color
        elif slot_or_clip.is_playing:
            return self._recording_color if slot_or_clip.is_recording else self._started_value
        elif slot_or_clip.color is not None:
            return self._color_value(slot_or_clip)
        elif getattr(slot_or_clip, 'controls_other_clips', True):
            return self._stopped_value
        elif self._track_is_armed(track) and self._clip_slot.has_stop_button and (self._record_button_color is not None):
            return self._record_button_color
        else:
            return self._empty_slot_color

    def _update_clip_property_slots(self):
        clip = self._clip_slot.clip if self._clip_slot else None
        self.__on_clip_playing_state_changed.subject = clip
        self.__on_recording_state_changed.subject = clip
        self.__on_clip_color_changed.subject = clip

    @listens('has_clip')
    def __on_clip_state_changed(self):
        self._update_clip_property_slots()
        self._update_launch_button_color()

    @listens('controls_other_clips')
    def __on_controls_other_clips_changed(self):
        self._update_clip_property_slots()
        self._update_launch_button_color()

    @listens('color')
    def __on_clip_color_changed(self):
        self._update_launch_button_color()

    @listens('color')
    def __on_clip_slot_color_changed(self):
        self._update_launch_button_color()

    @listens('playing_status')
    def __on_slot_playing_state_changed(self):
        self._update_launch_button_color()

    @listens('playing_status')
    def __on_clip_playing_state_changed(self):
        self._update_launch_button_color()

    @listens('is_recording')
    def __on_recording_state_changed(self):
        self._update_launch_button_color()

    @listens('arm')
    def __on_arm_value_changed(self):
        self._update_launch_button_color()

    @listens('implicit_arm')
    def __on_implicit_arm_value_changed(self):
        self._update_launch_button_color()

    @listens('input_routing_type')
    def __on_input_routing_type_changed(self):
        self._update_launch_button_color()

    @listens('has_stop_button')
    def __on_has_stop_button_changed(self):
        self._update_launch_button_color()

    @listens('is_triggered')
    def __on_slot_triggered_changed(self):
        if not self.has_clip():
            self._update_launch_button_color()
            return

    @launch_button.pressed
    def launch_button(self, button):
        self._on_launch_button_pressed()

    def _on_launch_button_pressed(self):
        if is_button_pressed(self._select_button):
            self._do_select_clip(self._clip_slot)
        elif liveobj_valid(self._clip_slot):
            if is_button_pressed(self._duplicate_button):
                self._do_duplicate_clip()
                return
            elif is_button_pressed(self._delete_button):
                self._do_delete_clip()
                return
            else:
                self._do_launch_clip(True)
                self._show_launched_clip_as_highlighted_clip()
                return

    @launch_button.released
    def launch_button(self, button):
        self._on_launch_button_released()

    def _on_launch_button_released(self):
        if self.launch_button.is_momentary and (not is_button_pressed(self._select_button)) and liveobj_valid(self._clip_slot) and (not is_button_pressed(self._duplicate_button)) and (not is_button_pressed(self._delete_button)):
            self._do_launch_clip(False)

    def _do_delete_clip(self):
        if self._clip_slot and self._clip_slot.has_clip:
            self._clip_slot.delete_clip()
            self._on_clip_deleted()
            return

    def _on_clip_deleted(self):
        return

    def _do_select_clip(self, clip_slot):
        if not liveobj_valid(self._clip_slot) or self.song.view.highlighted_clip_slot != self._clip_slot:
            self.song.view.highlighted_clip_slot = self._clip_slot
            self._on_slot_selected()

    def _on_slot_selected(self):
        return

    def _do_duplicate_clip(self):
        if self._clip_slot and self._clip_slot.has_clip:
            try:
                track = self._clip_slot.canonical_parent
                track.duplicate_clip_slot(list(track.clip_slots).index(self._clip_slot))
                self._on_clip_duplicated()
            except Live.Base.LimitationError:
                return
            except RuntimeError:
                return None

    def _on_clip_duplicated(self):
        return

    def _do_launch_clip(self, fire_state):
        object_to_launch = self._clip_slot
        if self.has_clip():
            object_to_launch = self._clip_slot.clip
        object_to_launch.set_fire_button_state(fire_state)

    def _show_launched_clip_as_highlighted_clip(self):
        song = self.song
        if song.select_on_launch and self._clip_slot != song.view.highlighted_clip_slot:
            self.song.view.highlighted_clip_slot = self._clip_slot