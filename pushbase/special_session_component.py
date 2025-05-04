# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\special_session_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ableton.v2.base import const, depends, forward_property, inject, listens, liveobj_valid
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import ClipSlotComponent, SceneComponent, SessionComponent
from ableton.v2.control_surface.control import ButtonControl
from ableton.v2.control_surface.mode import EnablingModesComponent
from pushbase.touch_strip_element import TouchStripModes, TouchStripStates
from .actions import clip_name_from_clip_slot, scene_description
from .consts import MessageBoxText
from .message_box_component import Messenger

class ClipSlotCopyHandler(Messenger):

    def __init__(self, *a, **k):
        super(ClipSlotCopyHandler, self).__init__(*a, **k)
        self._is_copying = False
        self._source_clip_slot = None
        self._last_shown_notification_ref = const(None)

    @property
    def is_copying(self):
        return self._is_copying

    def duplicate(self, clip_slot):
        if self._is_copying:
            self._finish_copying(clip_slot)
            return
        else:
            self._start_copying(clip_slot)

    def stop_copying(self):
        self._reset_copying_state()
        notification_ref = self._last_shown_notification_ref()
        if notification_ref is not None:
            notification_ref.hide()
            return
        else:
            return None

    def _show_notification(self, notification):
        self._last_shown_notification_ref = self.show_notification(notification)

    def _start_copying(self, source_clip_slot):
        if not source_clip_slot.is_group_slot:
            if liveobj_valid(source_clip_slot.clip):
                if not source_clip_slot.clip.is_recording:
                    self._is_copying = True
                    self._source_clip_slot = source_clip_slot
                    clip_name = clip_name_from_clip_slot(source_clip_slot)
                    self._show_notification((MessageBoxText.COPIED_CLIP, clip_name))
                else:
                    self._show_notification(MessageBoxText.CANNOT_COPY_RECORDING_CLIP)
            else:
                self._show_notification(MessageBoxText.CANNOT_COPY_EMPTY_CLIP)
                return
        else:
            self._show_notification(MessageBoxText.CANNOT_COPY_GROUP_SLOT)

    def _finish_copying(self, target_clip_slot):
        if not target_clip_slot.is_group_slot:
            source_is_audio = self._source_clip_slot.clip.is_audio_clip
            target_track = target_clip_slot.canonical_parent
            if source_is_audio:
                if target_track.has_audio_input:
                    self._perform_copy(target_clip_slot)
                    return
                else:
                    self._show_notification(MessageBoxText.CANNOT_COPY_AUDIO_CLIP_TO_MIDI_TRACK)
                    return
            elif not target_track.has_audio_input:
                self._perform_copy(target_clip_slot)
                return
            else:
                self._show_notification(MessageBoxText.CANNOT_COPY_MIDI_CLIP_TO_AUDIO_TRACK)
                return
        else:
            self._show_notification(MessageBoxText.CANNOT_PASTE_INTO_GROUP_SLOT)
            return

    def _perform_copy(self, target_clip_slot):
        self._source_clip_slot.duplicate_clip_to(target_clip_slot)
        self._on_duplicated(self._source_clip_slot, target_clip_slot)
        self._reset_copying_state()

    def _reset_copying_state(self):
        self._source_clip_slot = None
        self._is_copying = False

    def _on_duplicated(self, source_clip_slot, target_clip_slot):
        clip_name = clip_name_from_clip_slot(source_clip_slot)
        track_name = target_clip_slot.canonical_parent.name
        self._show_notification((MessageBoxText.PASTED_CLIP, clip_name, track_name))

class DuplicateSceneComponent(Component, Messenger):

    def __init__(self, session_ring=None, *a, **k):
        super(DuplicateSceneComponent, self).__init__(*a, **k)
        self._session_ring = session_ring
        self._scene_buttons = None

    def set_scene_buttons(self, buttons):
        self._scene_buttons = buttons
        self._on_scene_value.subject = buttons

    @listens('value')
    def _on_scene_value(self, value, index, _, is_momentary):
        if self.is_enabled() and (value or not is_momentary):
            try:
                self.song.duplicate_scene(self._session_ring.scene_offset + index)
                self.show_notification(MessageBoxText.DUPLICATE_SCENE % scene_description(self.song.view.selected_scene, self.song))
            except Live.Base.LimitationError:
                self.expect_dialog(MessageBoxText.SCENE_LIMIT_REACHED)
                return
            except RuntimeError:
                self.expect_dialog(MessageBoxText.SCENE_DUPLICATION_FAILED)
                return
            except IndexError:
                return None
            else:
                return
        else:
            return

class SpecialClipSlotComponent(ClipSlotComponent, Messenger):

    @depends(copy_handler=const(None), fixed_length_recording=const(None))
    def __init__(self, copy_handler=None, fixed_length_recording=None, *a, **k):
        super(SpecialClipSlotComponent, self).__init__(*a, **k)
        self._copy_handler = copy_handler
        self._fixed_length_recording = fixed_length_recording

    def _do_delete_clip(self):
        if self._clip_slot and self._clip_slot.has_clip:
            clip_name = self._clip_slot.clip.name
            self._clip_slot.delete_clip()
            self.show_notification(MessageBoxText.DELETE_CLIP % clip_name)

    def _do_select_clip(self, clip_slot):
        if not liveobj_valid(self._clip_slot) or self.song.view.highlighted_clip_slot != self._clip_slot:
            self.song.view.highlighted_clip_slot = self._clip_slot

    def _do_duplicate_clip(self):
        self._copy_handler.duplicate(self._clip_slot)

    def _on_clip_duplicated(self, source_clip, destination_clip):
        slot_name = source_clip.name
        self.show_notification(MessageBoxText.DUPLICATE_CLIP % slot_name)

    def _clip_is_recording(self):
        return self.has_clip() and self._clip_slot.clip.is_recording

    def _do_launch_clip(self, fire_state):
        should_start_fixed_length_recording = self._fixed_length_recording.should_start_fixed_length_recording(self._clip_slot)
        clip_is_recording = self._clip_is_recording()
        if not fire_state or should_start_fixed_length_recording or clip_is_recording:
            pass
        if not fire_state:
            super(SpecialClipSlotComponent, self)._do_launch_clip(fire_state)
            return
        elif should_start_fixed_length_recording:
            track = self._clip_slot.canonical_parent
            self._fixed_length_recording.start_recording_in_slot(track, list(track.clip_slots).index(self._clip_slot))
            return
        elif clip_is_recording:
            self._fixed_length_recording.stop_recording(self._clip_slot.clip)
            return
        else:
            return None

class SpecialSceneComponent(SceneComponent, Messenger):
    clip_slot_component_type = SpecialClipSlotComponent

    def _do_delete_scene(self, scene):
        try:
            if self._scene:
                song = self.song
                description = scene_description(self._scene, song, False)
                song.delete_scene(list(song.scenes).index(self._scene))
                self.show_notification(MessageBoxText.DELETE_SCENE % description)
        except RuntimeError:
            return None

class SpecialSessionComponent(SessionComponent):
    pass
    _session_component_ends_initialisation = False
    scene_component_type = SpecialSceneComponent
    duplicate_button = ButtonControl()

    def __init__(self, clip_slot_copy_handler=None, fixed_length_recording=None, *a, **k):
        pass
    duplicate_layer = forward_property('_duplicate')('layer')

    @duplicate_button.pressed
    def duplicate_button(self, button):
        self._duplicate_enabler.selected_mode = 'enabled'

    @duplicate_button.released
    def duplicate_button(self, button):
        self._duplicate_enabler.selected_mode = 'disabled'
        self._clip_copy_handler.stop_copying()

    def set_slot_launch_button(self, button):
        self._slot_launch_button = button
        self._on_slot_launch_value.subject = button

    def set_clip_launch_buttons(self, buttons):
        if buttons:
            buttons.reset()
        super(SpecialSessionComponent, self).set_clip_launch_buttons(buttons)

    def set_touch_strip(self, touch_strip):
        if touch_strip:
            touch_strip.set_mode(TouchStripModes.CUSTOM_FREE)
            touch_strip.send_state([TouchStripStates.STATE_OFF for _ in range(touch_strip.state_count)])
        self._on_touch_strip_value.subject = touch_strip

    @listens('value')
    def _on_touch_strip_value(self, value):
        return

    @listens('value')
    def _on_slot_launch_value(self, value):
        if self.is_enabled():
            if value != 0 or not self._slot_launch_button.is_momentary():
                if liveobj_valid(self.song.view.highlighted_clip_slot):
                    self.song.view.highlighted_clip_slot.fire()
                self._slot_launch_button.turn_on()
                return
            else:
                self._slot_launch_button.turn_off()
                return