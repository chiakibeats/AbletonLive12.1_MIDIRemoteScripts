# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\ClipActionsComponent.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from _Framework.Control import ButtonControl
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SubjectSlot import Subject, subject_slot
from .consts import ACTION_BUTTON_COLORS
_Q = Live.Song.Quantization

def duplicate_clip(song, slot, should_launch=False):
    pass

def double_clip(clip):
    try:
        clip.duplicate_loop()
    except (AttributeError, TypeError):
        return
    except RuntimeError:
        return None

class ClipActionsComponent(ControlSurfaceComponent, Subject):
    pass
    delete_button = ButtonControl(**ACTION_BUTTON_COLORS)
    duplicate_button = ButtonControl(**ACTION_BUTTON_COLORS)
    double_button = ButtonControl(**ACTION_BUTTON_COLORS)
    quantize_button = ButtonControl(**ACTION_BUTTON_COLORS)
    __subject_events__ = ('selected_clip',)

    def __init__(self, target_track_component, quantization_component, *a, **k):
        super(ClipActionsComponent, self).__init__(*a, **k)
        self._target_track_component = target_track_component
        self._on_track_changed.subject = self._target_track_component
        self._quantization_component = quantization_component
        self._use_selected_track = False
        self._selected_clip = None
        self._track = self.song().view.selected_track
        self._on_selection_changed()

    def use_selected_track(self, use_selected_track):
        self._use_selected_track = use_selected_track
        if use_selected_track:
            self._track = self.song().view.selected_track
        else:
            self._track = self._target_track_component.target_track
        self._on_selection_changed()

    @delete_button.pressed
    def delete_button(self, button):
        if self.can_perform_clip_action():
            self._selected_clip.canonical_parent.delete_clip()

    @duplicate_button.pressed
    def duplicate_button(self, button):
        if self.can_perform_clip_action():
            duplicate_clip(self.song(), self._selected_clip.canonical_parent, should_launch=True)

    @double_button.pressed
    def double_button(self, button):
        if self.can_perform_midi_clip_action():
            double_clip(self._selected_clip)
            return
        else:
            return None

    @quantize_button.pressed
    def quantize_button(self, button):
        if self.can_perform_clip_action() and self._quantization_component:
            self._quantization_component.quantize_clip(self._selected_clip)
            return
        else:
            return

    def delete_pitch(self, pitch):
        if self.can_perform_midi_clip_action():
            clip = self._selected_clip
            loop_length = clip.loop_end - clip.loop_start
            clip.remove_notes_extended(from_time=clip.loop_start, from_pitch=pitch, time_span=loop_length, pitch_span=1)
        else:
            return None

    def on_selected_track_changed(self):
        if self._use_selected_track:
            self._track = self.song().view.selected_track
            self._on_selection_changed()
            return
        else:
            return None

    @subject_slot('target_track')
    def _on_track_changed(self):
        if not self._use_selected_track:
            self._track = self._target_track_component.target_track
            self._on_selection_changed()
            return

    @subject_slot('playing_slot_index')
    def _on_selection_changed(self):
        self._selected_clip = None
        if self._track in self.song().tracks:
            slot_index = self._track.playing_slot_index
            if slot_index >= 0 and self._track.clip_slots[slot_index].has_clip:
                self._selected_clip = self._track.clip_slots[slot_index].clip
            self._on_selection_changed.subject = self._track
        else:
            self._on_selection_changed.subject = None
        self._update_control_states()

    def _update_control_states(self):
        can_perform_clip_action = self.can_perform_clip_action()
        self.delete_button.enabled = can_perform_clip_action
        self.duplicate_button.enabled = can_perform_clip_action
        self.quantize_button.enabled = can_perform_clip_action
        self.double_button.enabled = self.can_perform_midi_clip_action()
        self.notify_selected_clip()

    def can_perform_clip_action(self):
        return self._selected_clip is not None

    def can_perform_midi_clip_action(self):
        return self._selected_clip is not None and self._selected_clip.is_midi_clip