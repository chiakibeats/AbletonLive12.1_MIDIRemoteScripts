# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\loop_selector.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from ...base import depends, listenable_property, listens, round_to_multiple
from ...live import action, get_bar_length, is_clip_playing, liveobj_changed, liveobj_valid
from .. import Component
from ..controls import ButtonControl, control_matrix
from ..display import Renderable
from ..skin import LiveObjSkinEntry, OptionalSkinEntry
from .note_editor import NoteRegionClipboardComponent

class LoopSelectorComponent(Component, Renderable):
    pass
    next_page_button = ButtonControl(color='LoopSelector.Navigation', pressed_color='LoopSelector.NavigationPressed')
    prev_page_button = ButtonControl(color='LoopSelector.Navigation', pressed_color='LoopSelector.NavigationPressed')
    delete_button = ButtonControl(None)
    matrix = control_matrix(ButtonControl)

    @depends(target_track=None, sequencer_clip=None)
    pass
    pass
    pass
    pass
    pass
    def __init__(self, name='Loop_Selector', target_track=None, sequencer_clip=None, paginator=None, clipboard_component_type=None, *a, **k):
        super().__init__(*a, name=name, **k)
        self._pressed_matrix_indices = []
        self._target_track = target_track
        self.__on_target_track_color_changed.subject = target_track
        self._clip = None
        self._last_bar_length = sequencer_clip.bar_length
        self._sequencer_clip = sequencer_clip
        self.__on_sequencer_clip_changed.subject = sequencer_clip
        self.register_slot(sequencer_clip, self._rectify_page_time, 'bar_length')
        self.register_slot(sequencer_clip, self.update, 'length')
        self._paginator = paginator
        self._last_page_length = paginator.page_length
        self.register_slot(paginator, self._rectify_page_time, 'page_length')
        self.register_slot(paginator, self.update, 'page_time')
        self.register_slot(self.song, self._update_matrix, 'session_record')
        self.register_slot(self.song, self._update_matrix, 'is_playing')
        clipboard_component_type = clipboard_component_type or NoteRegionClipboardComponent
        self._clipboard = clipboard_component_type(parent=self)
        self.set_clip(self._sequencer_clip.clip)

    @listenable_property
    def clipboard(self):
        pass
        return self._clipboard

    @property
    def bar_length(self):
        pass
        return get_bar_length(clip=self._clip)

    @property
    def min_page_time(self):
        pass
        if liveobj_valid(self._clip):
            return min(0.0, round_to_multiple(self._clip.loop_start, self.bar_length))
        else:  # inserted
            return 0.0

    def set_matrix(self, matrix):
        self.matrix.set_control_element(matrix)
        self._update_matrix()

    def set_copy_button(self, button):
        pass
        self._clipboard.set_copy_button(button)

    def set_clip(self, clip):
        pass
        if liveobj_changed(clip, self._clip):
            self.__on_playing_position_changed.subject = clip
            self.__on_playing_status_changed.subject = clip
            self._clip = clip
            self._clipboard.set_clip(clip)
            self._on_clip_changed()
            if self._paginator.can_change_page:
                self._paginator.page_time = round_to_multiple(clip.loop_start, self.bar_length) if liveobj_valid(clip) else 0.0
                return
            else:  # inserted
                self.update()
                return

    @matrix.pressed
    def matrix(self, button):
        bar_length = self.bar_length
        if self.delete_button.is_pressed:
            if action.delete_notes_in_range(self._clip, self._button_position(button.index), bar_length):
                self.notify(self.notifications.Notes.delete)
                return
            else:  # inserted
                self.notify(self.notifications.Notes.error_no_notes_to_delete)
                return
        else:  # inserted
            if self._clipboard.is_copying:
                self._update_clipboard(button)
                return
            else:  # inserted
                self._pressed_matrix_indices.append(button.index)
                self._paginator.page_time = self._button_position(self._pressed_matrix_indices[0])
                if len(self._pressed_matrix_indices) > 1:
                    action.set_loop_position(self._clip, self._button_position(min(self._pressed_matrix_indices)), self._button_position(max(self._pressed_matrix_indices)) + bar_length)
                self._on_page_time_changed_via_matrix()

    @matrix.released
    def matrix(self, button):
        if self._clipboard.is_copying:
            self._update_clipboard(button)
            return
        else:  # inserted
            if button.index in self._pressed_matrix_indices:
                self._pressed_matrix_indices.remove(button.index)
                return
            else:  # inserted
                return None

    @matrix.double_clicked
    def matrix(self, button):
        if not self._clipboard.is_copying:
            start = self._button_position(button.index)
            action.set_loop_position(self._clip, start, start + self.bar_length)

    @next_page_button.pressed
    def next_page_button(self, _):
        self._increment_page_time(1)

    @prev_page_button.pressed
    def prev_page_button(self, _):
        self._increment_page_time((-1))

    def _on_page_time_changed_via_matrix(self):
        return

    def _increment_page_time(self, delta):
        self._paginator.page_time = max(0.0, self._paginator.page_length * delta + self._paginator.page_time)

    def _rectify_page_time(self):
        if self._paginator.page_length > self._last_page_length or self.bar_length!= self._last_bar_length:
            self._paginator.page_time = round_to_multiple(self._paginator.page_time, self.bar_length)
        self._last_page_length = self._paginator.page_length
        self._last_bar_length = self.bar_length

    def _has_clip(self):
        return liveobj_valid(self._clip)

    def _on_clip_changed(self):
        return

    def _button_position(self, button_index):
        return button_index * self.bar_length + self.min_page_time

    def _update_clipboard(self, button):
        region_start = self._button_position(button.index)
        any_button_pressed = any((button.is_pressed for button in self.matrix))
        if self._clipboard.has_content:
            if not any_button_pressed:
                self._clipboard.paste(region_start)
            else:  # inserted
                return None
        else:  # inserted
            if button.is_pressed:
                self._clipboard.extend_buffer((region_start, region_start + self.bar_length))
                return
            else:  # inserted
                if not any_button_pressed:
                    self._clipboard.copy(self._clipboard.buffer)
                    return
                else:  # inserted
                    return None

    def update(self):
        super().update()
        self._update_matrix()
        self._update_page_buttons()

    def _update_matrix(self):
        has_clip = self._has_clip()
        for button in self.matrix:
            button.enabled = has_clip
        if has_clip:
            bar_length = self.bar_length
            loop_start = self._clip.loop_start
            loop_end = self._clip.loop_end
            playing_position = self._clip.playing_position
            if playing_position < 0.0:
                playing_position -= bar_length
            playing_page = int(playing_position / bar_length)
            editing_page = int(self._paginator.page_time / bar_length)
            for button in self.matrix:
                button_position = self._button_position(button.index)
                button_index = int(button_position / bar_length)
                self._update_matrix_button(button, button_index == editing_page, is_clip_playing(self._clip) and button_index == playing_page, loop_start <= button_position < loop_end)
                continue

    def _update_matrix_button(self, button, selected, playing, inside_loop):
        color = 'LoopSelector.OutsideLoop'
        if playing:
            color = 'LoopSelector.PlayheadRecord' if self.song.session_record else 'LoopSelector.Playhead'
        else:  # inserted
            if inside_loop:
                color = 'LoopSelector.InsideLoopSelected' if selected else 'LoopSelector.InsideLoop'
                if self.song.is_playing:
                    color = OptionalSkinEntry('{}Playing'.format(color), color)
                pass
            else:  # inserted
                if selected:
                    color = 'LoopSelector.OutsideLoopSelected'
        button.color = LiveObjSkinEntry(color, self._target_track.target_track)
        return

    def _update_page_buttons(self):
        has_clip = self._has_clip()
        self.prev_page_button.enabled = has_clip and self._paginator.page_time > self.min_page_time
        self.next_page_button.enabled = has_clip

    @listens('clip')
    def __on_sequencer_clip_changed(self):
        self.set_clip(self._sequencer_clip.clip)

    @listens('playing_position')
    def __on_playing_position_changed(self):
        self._update_matrix()

    @listens('playing_status')
    def __on_playing_status_changed(self):
        self._update_matrix()

    @listens('target_track.color')
    def __on_target_track_color_changed(self):
        self._update_matrix()