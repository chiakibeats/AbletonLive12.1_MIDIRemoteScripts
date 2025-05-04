# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\step_sequence.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from Live.Song import Quantization
from ...base import EventObject, depends, listenable_property, listens
from ...live import get_bar_length, liveobj_changed, liveobj_valid, prepare_new_clip_slot, song
from .. import Component
from . import LoopSelectorComponent, NoteEditorComponent, NoteEditorPaginator, PlayheadComponent

def create_sequencer_clip(track, slot=None, length=None):
    pass
    length = length or get_bar_length()
    slot = slot or prepare_new_clip_slot(track)
    slot.create_clip(length)
    slot.fire(force_legato=True, launch_quantization=Quantization.q_no_q)
    song().view.detail_clip = slot.clip
    return slot.clip

class SequencerClip(EventObject):
    pass

    @depends(target_track=None)
    def __init__(self, target_track=None, *a, **k):
        super().__init__(*a, **k)
        self._clip = None
        self._target_track = target_track
        self.__on_target_clip_changed.subject = target_track
        self.__on_target_clip_changed()

    @listenable_property
    def clip(self):
        pass
        return self._clip

    @clip.setter
    def clip(self, clip):
        clip = clip if liveobj_valid(clip) and clip.is_midi_clip else None
        if liveobj_changed(clip, self._clip):
            self._clip = clip
            self.__on_looping_changed.subject = self._clip
            self.__on_loop_start_changed.subject = self._clip
            self.__on_loop_end_changed.subject = self._clip
            self.__on_signature_numerator_changed.subject = self._clip
            self.__on_signature_denominator_changed.subject = self._clip
            self.notify_clip()
            self.notify_length()
            self.notify_bar_length()

    @listenable_property
    def length(self):
        pass
        if liveobj_valid(self._clip):
            return self._clip.loop_end - self._clip.loop_start
        else:  # inserted
            return 0

    @listenable_property
    def bar_length(self):
        pass
        return get_bar_length(clip=self._clip)

    @property
    def num_bars(self):
        pass
        return self.length / self.bar_length

    def create_clip(self, length=None):
        pass
        if self._target_track.target_track.has_midi_input:
            self.clip = create_sequencer_clip(self._target_track.target_track, length=length)
            return self.clip
        else:  # inserted
            return None

    @listens('target_clip')
    def __on_target_clip_changed(self):
        clip = self._target_track.target_clip
        clip = clip if liveobj_valid(clip) and clip.is_midi_clip else clip
        else:  # inserted
            self.clip = None

    @listens('looping')
    def __on_looping_changed(self):
        self.notify_length()

    @listens('loop_start')
    def __on_loop_start_changed(self):
        self.notify_length()

    @listens('loop_end')
    def __on_loop_end_changed(self):
        self.notify_length()

    @listens('signature_numerator')
    def __on_signature_numerator_changed(self):
        self.notify_length()
        self.notify_bar_length()

    @listens('signature_denominator')
    def __on_signature_denominator_changed(self):
        self.notify_length()
        self.notify_bar_length()

class StepSequenceComponent(Component):
    pass

    @depends(grid_resolution=None)
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    pass
    def __init__(self, name='Step_Sequence', grid_resolution=None, note_editor_component_type=None, note_editor_paginator_type=None, loop_selector_component_type=None, playhead_component_type=None, playhead_notes=None, playhead_triplet_notes=None, playhead_channels=None, *a, **k):
        super().__init__(*a, name=name, **k)
        self._grid_resolution = self.add_children(grid_resolution)
        note_editor_component_type = note_editor_component_type or NoteEditorComponent
        self._note_editor = note_editor_component_type(grid_resolution=self._grid_resolution, parent=self)
        note_editor_paginator_type = note_editor_paginator_type or NoteEditorPaginator
        paginator = note_editor_paginator_type(note_editor=self._note_editor, parent=self)
        loop_selector_component_type = loop_selector_component_type or LoopSelectorComponent
        self._loop_selector = loop_selector_component_type(paginator=paginator, parent=self)
        playhead_component_type = playhead_component_type or PlayheadComponent
        self._playhead = playhead_component_type(notes=playhead_notes, triplet_notes=playhead_triplet_notes, channels=playhead_channels, grid_resolution=self._grid_resolution, paginator=paginator, parent=self)

    @property
    def note_editor(self):
        pass
        return self._note_editor

    def set_pitch_provider(self, provider):
        pass
        self._note_editor.pitch_provider = provider

    def set_step_buttons(self, buttons):
        pass
        self._note_editor.set_matrix(buttons)

    def set_note_copy_button(self, button):
        pass
        self._note_editor.set_copy_button(button)

    def set_resolution_buttons(self, buttons):
        pass
        self._grid_resolution.resolution_buttons.set_control_element(buttons)

    def set_loop_buttons(self, matrix):
        pass
        self._loop_selector.set_matrix(matrix)

    def set_loop_delete_button(self, button):
        pass
        self._loop_selector.delete_button.set_control_element(button)

    def set_loop_copy_button(self, button):
        pass
        self._loop_selector.set_copy_button(button)

    def set_prev_page_button(self, button):
        pass
        self._loop_selector.prev_page_button.set_control_element(button)

    def set_next_page_button(self, button):
        pass
        self._loop_selector.next_page_button.set_control_element(button)