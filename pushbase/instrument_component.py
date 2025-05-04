# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\pushbase\instrument_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.utils import old_div
from contextlib import contextmanager
from ableton.v2.base import EventObject, find_if, index_if, listenable_property, listens, liveobj_valid, task
from ableton.v2.control_surface import defaults
from ableton.v2.control_surface.components import PlayableComponent, Slideable, SlideComponent
from ableton.v2.control_surface.control import ButtonControl, PlayableControl, control_matrix
from . import consts
from .melodic_pattern import SCALES, MelodicPattern, TuningSystemPattern, pitch_index_to_string
from .message_box_component import Messenger
from .note_editor_component import DEFAULT_START_NOTE
from .pad_control import PadControl
from .slideable_touch_strip_component import SlideableTouchStripComponent
DEFAULT_SCALE = SCALES[0]

class NoteLayout(EventObject):
    def __init__(self, song=None, preferences=dict(), *a, **k):
        super(NoteLayout, self).__init__(*a, **k)
        self._song = song
        self._scale = self._get_scale_from_name(self._song.scale_name)
        self._preferences = preferences
        self._is_in_key = self._preferences.setdefault('is_in_key', True)
        self._is_fixed = self._preferences.setdefault('is_fixed', False)
        self._interval = self._song.get_data('push-note-layout-interval', 3)
        self._is_horizontal = self._song.get_data('push-note-layout-horizontal', True)
        self._tuning_system_interval = self._song.get_data('push-note-layout-tuning-system-interval', 5)
        self.__on_root_note_changed.subject = self._song
        self.__on_scale_name_changed.subject = self._song

    @property
    def notes(self):
        return self.scale.to_root_note(self.root_note).notes

    @listenable_property
    def root_note(self):
        return self._song.root_note

    @root_note.setter
    def root_note(self, root_note):
        self._song.root_note = root_note

    @listenable_property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale
        self._song.scale_name = scale.name
        self.notify_scale(self._scale)

    @listenable_property
    def is_in_key(self):
        return self._is_in_key

    @is_in_key.setter
    def is_in_key(self, is_in_key):
        self._is_in_key = is_in_key
        self._preferences['is_in_key'] = self._is_in_key
        self.notify_is_in_key(self._is_in_key)

    @listenable_property
    def is_fixed(self):
        return self._is_fixed

    @is_fixed.setter
    def is_fixed(self, is_fixed):
        self._is_fixed = is_fixed
        self._preferences['is_fixed'] = self._is_fixed
        self.notify_is_fixed(self._is_fixed)

    @listenable_property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, interval):
        if interval!= self._interval:
            self._interval = interval
            self._song.set_data('push-note-layout-interval', interval)
            self.notify_interval(interval)

    @listenable_property
    def tuning_system_interval(self):
        return self._tuning_system_interval

    @tuning_system_interval.setter
    def tuning_system_interval(self, interval):
        if interval!= self._tuning_system_interval:
            self._tuning_system_interval = interval
            self._song.set_data('push-note-layout-tuning-system-interval', interval)
            self.notify_tuning_system_interval(interval)

    @listenable_property
    def is_horizontal(self):
        return self._is_horizontal

    @is_horizontal.setter
    def is_horizontal(self, is_horizontal):
        if is_horizontal!= self._is_horizontal:
            self._is_horizontal = is_horizontal
            self._song.set_data('push-note-layout-horizontal', is_horizontal)
            self.notify_is_horizontal(is_horizontal)

    def _get_scale_from_name(self, name):
        return find_if(lambda scale: scale.name == name, SCALES) or DEFAULT_SCALE

    @listens('root_note')
    def __on_root_note_changed(self):
        self.notify_root_note(self._song.root_note)

    @listens('scale_name')
    def __on_scale_name_changed(self):
        self._scale = self._get_scale_from_name(self._song.scale_name)
        self.notify_scale(self._scale)

def get_tuning_system_lowest_octave(tuning_system):
    pass
    number_of_notes = tuning_system.number_of_notes_in_pseudo_octave
    offset = tuning_system.lowest_note.index_in_octave % number_of_notes
    if offset > 0:
        return number_of_notes - offset
    else:  # inserted
        return 0

class InstrumentComponent(PlayableComponent, Slideable, Messenger):
    pass
    __events__ = ('pattern',)
    matrix = control_matrix(PadControl)
    delete_button = ButtonControl()

    def __init__(self, note_layout=None, *a, **k):
        super(InstrumentComponent, self).__init__(*a, **k)
        self._note_layout = note_layout
        self._first_note = self.page_length * 3 + self.page_offset
        self._last_page_length = self.page_length
        self._last_page_offset = self.page_offset
        self.__on_tuning_system_changed.subject = self.song
        self._detail_clip = None
        self._has_notes = [False] * 128
        self._has_notes_pattern = self._get_pattern(0)
        self._aftertouch_control = None
        self._aftertouch_mode = 'mono'
        self._show_notifications = True
        self.__on_detail_clip_changed.subject = self.song.view
        self.__on_detail_clip_changed()
        self._slider = SlideComponent(slideable=self, parent=self)
        self._touch_slider = SlideableTouchStripComponent(touch_slideable=self, parent=self)
        for event in ['scale', 'root_note', 'is_in_key', 'is_fixed', 'is_horizontal', 'interval', 'tuning_system_interval']:
            self.register_slot(self._note_layout, self._on_note_layout_changed, event)
        self._update_scale()
        self._update_pattern()

    @listens('detail_clip')
    def __on_detail_clip_changed(self):
        clip = self.song.view.detail_clip
        self.set_detail_clip(clip if liveobj_valid(clip) and clip.is_midi_clip else None)

    def set_detail_clip(self, clip):
        if clip!= self._detail_clip:
            self._detail_clip = clip
            self._on_clip_notes_changed.subject = clip
            self._on_loop_start_changed.subject = clip
            self._on_loop_end_changed.subject = clip
            self._on_clip_notes_changed()

    @listens('tuning_system')
    def __on_tuning_system_changed(self):
        self._update_scale()

    @listens('notes')
    def _on_clip_notes_changed(self):
        if self._detail_clip:
            self._has_notes = [False] * 128
            loop_start = self._detail_clip.loop_start
            loop_length = self._detail_clip.loop_end - loop_start
            notes = self._detail_clip.get_notes_extended(from_time=loop_start, from_pitch=0, time_span=loop_length, pitch_span=128)
            for note in notes:
                self._has_notes[note.pitch] = True
        self.notify_contents()

    @listens('loop_start')
    def _on_loop_start_changed(self):
        self._on_loop_selection_changed()

    @listens('loop_end')
    def _on_loop_end_changed(self):
        self._on_loop_selection_changed()

    def _on_loop_selection_changed(self):
        self._on_clip_notes_changed()

    def contents(self, index):
        if self._detail_clip:
            note = self._has_notes_pattern[index].index
            return self._has_notes[note] if note is not None else False
        else:  # inserted
            return False

    @property
    def show_notifications(self):
        return self._show_notifications

    @show_notifications.setter
    def show_notifications(self, value):
        self._show_notifications = value

    @property
    def page_length(self):
        if self.song.tuning_system:
            return self.song.tuning_system.number_of_notes_in_pseudo_octave
        else:  # inserted
            return len(self._note_layout.notes) if self._note_layout.is_in_key else 12

    @property
    def position_count(self):
        if self.song.tuning_system:
            return 128
        else:  # inserted
            if not self._note_layout.is_in_key:
                return 139
            else:  # inserted
                offset = self.page_offset
                octaves = 11 if self._note_layout.notes[0] < 8 else 10
                return offset + len(self._note_layout.notes) * octaves

    def _first_scale_note_offset(self):
        if not self._note_layout.is_in_key:
            return self._note_layout.notes[0]
        else:  # inserted
            if self._note_layout.notes[0] == 0:
                return 0
            else:  # inserted
                return len(self._note_layout.notes) - index_if(lambda n: n >= 12, self._note_layout.notes)

    @property
    def page_offset(self):
        if self.song.tuning_system:
            return get_tuning_system_lowest_octave(self.song.tuning_system)
        else:  # inserted
            return 0 if self._note_layout.is_fixed else self._first_scale_note_offset()

    def _get_position(self):
        return self._first_note

    def _set_position(self, note):
        self._first_note = note
        self._update_pattern()
        self._update_matrix()
        self.notify_position()
    position = property(_get_position, _set_position)

    @property
    def min_pitch(self):
        return self.pattern[0].index

    @property
    def max_pitch(self):
        identifiers = [control.identifier for control in self.matrix]
        return max(identifiers) if len(identifiers) > 0 else 127

    @property
    def pattern(self):
        return self._pattern

    @matrix.pressed
    def matrix(self, button):
        self._on_matrix_pressed(button)

    def _on_matrix_pressed(self, button):
        if self.delete_button.is_pressed:
            pitch = self._get_note_info_for_coordinate(button.coordinate).index
            if pitch and self._detail_clip:
                    self._do_delete_pitch(pitch)
                    return
                else:  # inserted
                    return None
            else:  # inserted
                return None
        else:  # inserted
            return None

    @matrix.released
    def matrix(self, button):
        self._on_matrix_released(button)

    def _on_matrix_released(self, button):
        return

    def _do_delete_pitch(self, pitch):
        clip = self._detail_clip
        if clip:
            note_name = clip.note_number_to_name(pitch)
            loop_length = clip.loop_end - clip.loop_start
            clip.remove_notes_extended(from_time=clip.loop_start, from_pitch=pitch, time_span=loop_length, pitch_span=1)
            self.show_notification(consts.MessageBoxText.DELETE_NOTES % note_name)

    @delete_button.pressed
    def delete_button(self, value):
        self._set_control_pads_from_script(True)

    @delete_button.released
    def delete_button(self, value):
        self._set_control_pads_from_script(False)

    def set_note_strip(self, strip):
        self._touch_slider.set_scroll_strip(strip)

    def set_octave_strip(self, strip):
        self._touch_slider.set_page_strip(strip)

    def set_octave_up_button(self, button):
        self._slider.set_scroll_page_up_button(button)

    def set_octave_down_button(self, button):
        self._slider.set_scroll_page_down_button(button)

    def set_scale_up_button(self, button):
        self._slider.set_scroll_up_button(button)

    def set_scale_down_button(self, button):
        self._slider.set_scroll_down_button(button)

    def set_aftertouch_control(self, control):
        self._aftertouch_control = control
        self._update_aftertouch()

    def set_aftertouch_mode(self, mode):
        if self._aftertouch_mode!= mode:
            self._aftertouch_mode = mode
            self._update_aftertouch()

    def _align_first_note(self):
        self._first_note = self.page_offset + (self._first_note - self._last_page_offset) * old_div(float(self.page_length), float(self._last_page_length))
        if self._first_note >= self.position_count:
            self._first_note -= self.page_length
        self._last_page_length = self.page_length
        self._last_page_offset = self.page_offset

    def _on_note_layout_changed(self, _):
        self._update_scale()

    def show_pitch_range_notification(self):
        if self.is_enabled() and self.show_notifications:
                start_note = self.pattern.note(0, 0).index
                end_note = self.pattern.note(self.width - 1, self.height - 1).index
                if liveobj_valid(self._detail_clip):
                    index_to_name_func = self._detail_clip.note_number_to_name
                else:  # inserted
                    index_to_name_func = pitch_index_to_string
                self.show_notification('Play {start_note} to {end_note}'.format(start_note=index_to_name_func(start_note), end_note=index_to_name_func(end_note)))
                return
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _update_scale(self):
        self._align_first_note()
        self._update_pattern()
        self._update_matrix()
        self.notify_position_count()
        self.notify_position()
        self.notify_contents()

    def update(self):
        super(InstrumentComponent, self).update()
        if self.is_enabled():
            self._update_matrix()
            self._update_aftertouch()

    def _update_pattern(self):
        self._pattern = self._get_pattern()
        self._has_notes_pattern = self._get_pattern(0)
        self.notify_pattern()

    def _invert_and_swap_coordinates(self, coordinates):
        return (coordinates[1], self.height - 1 - coordinates[0])

    def _get_note_info_for_coordinate(self, coordinate):
        x, y = self._invert_and_swap_coordinates(coordinate)
        return self.pattern.note(x, y)

    def _update_button_color(self, button):
        note_info = self._get_note_info_for_coordinate(button.coordinate)
        button.color = 'Instrument.' + note_info.color

    def _button_should_be_enabled(self, button):
        return self._get_note_info_for_coordinate(button.coordinate).index!= None

    def _note_translation_for_button(self, button):
        note_info = self._get_note_info_for_coordinate(button.coordinate)
        return (note_info.index, note_info.channel)

    def _set_button_control_properties(self, button):
        super(InstrumentComponent, self)._set_button_control_properties(button)
        button.sensitivity_profile = 'default' if self._takeover_pads else 'instrument'

    def _update_matrix(self):
        self._update_control_from_script()
        self._update_note_translations()
        self._update_led_feedback()

    def _get_pattern(self, first_note=None):
        if first_note is None:
            first_note = int(round(self._first_note))
        interval = self._note_layout.interval
        notes = self._note_layout.notes
        width = None
        height = None
        octave = old_div(first_note, self.page_length)
        offset = first_note % self.page_length - self._first_scale_note_offset()
        if interval == None:
            if self._note_layout.is_in_key:
                interval = len(self._note_layout.notes)
                if self._note_layout.is_horizontal:
                    width = interval + 1
                else:  # inserted
                    height = interval + 1
            else:  # inserted
                interval = 8
        else:  # inserted
            if not self._note_layout.is_in_key:
                interval = [0, 2, 4, 5, 7, 9, 10, 11][interval]
        if self._note_layout.is_horizontal:
            steps = [1, interval]
            origin = [offset, 0]
        else:  # inserted
            steps = [interval, 1]
            origin = [0, offset]
        if self.song.tuning_system:
            return TuningSystemPattern(first_note, self.song.tuning_system, [1, self._note_layout.tuning_system_interval])
        else:  # inserted
            return MelodicPattern(steps=steps, scale=notes, origin=origin, root_note=octave * 12, chromatic_mode=not self._note_layout.is_in_key, width=width, height=height)

    def _update_aftertouch(self):
        if not self.is_enabled() or self._aftertouch_control!= None:
                self._aftertouch_control.send_value(self._aftertouch_mode)

class SelectedNotesProvider(EventObject):
    _selected_notes = tuple([DEFAULT_START_NOTE])

    @listenable_property
    def selected_notes(self):
        return self._selected_notes

    @selected_notes.setter
    def selected_notes(self, notes):
        self._selected_notes = tuple(sorted(set(notes)))
        self.notify_selected_notes(self._selected_notes)

    def add_note(self, note):
        self.selected_notes += (note,)

    def remove_note(self, note):
        if len(self._selected_notes) > 1 and note in self._selected_notes:
                note_list = list(self._selected_notes)
                note_list.remove(note)
                self.selected_notes = note_list

    def toggle_note(self, note):
        if note in self.selected_notes:
            self.remove_note(note)
            return
        else:  # inserted
            self.add_note(note)

class SelectedNotesInstrumentComponent(InstrumentComponent):
    def __init__(self, note_editor_component=None, *a, **k):
        pass  # cflow: irreducible

    def set_matrix(self, matrix):
        super(SelectedNotesInstrumentComponent, self).set_matrix(matrix)
        self._set_matrix_listenable_and_playable()
        if self.is_enabled():
            self.notify_position()

    def _commit_pressed_notes(self):
        pass  # cflow: irreducible

    def _add_pitch(self, pitch):
        if self._chord_task.is_killed:
            self._chord_task.restart()
        self._pitches.append(pitch)

    def _toggle_pitch_in_note_editor(self, pitch):
        self._note_editor_component.toggle_pitch_for_all_modified_steps(pitch)
        self._tasks.add(task.sequence(task.delay(1), task.run(self._show_notes_in_selected_step)))

    def _set_matrix_listenable_and_playable(self):
        for button in self.matrix:
            button.set_mode(PlayableControl.Mode.playable_and_listenable)

    def _set_matrix_unplayable(self):
        for button in self.matrix:
            button.set_mode(PlayableControl.Mode.listenable)

    def _set_control_pads_from_script(self, is_unplayable):
        if is_unplayable:
            self._set_matrix_unplayable()
            return
        else:  # inserted
            self._set_matrix_listenable_and_playable()

    def _get_color_for_button_in_selected_step(self, button):
        return 'Instrument.SelectedNote' if button.identifier in self._note_editor_component.notes_in_selected_step else 'Instrument.' + self._get_note_info_for_coordinate(button.coordinate).color

    def _show_notes_in_selected_step(self):
        for button in self.matrix:
            button.color = self._get_color_for_button_in_selected_step(button)

    def _on_matrix_pressed(self, button):
        pass  # cflow: irreducible

    def _on_matrix_released(self, button):
        if not self.delete_button.is_pressed and (not self.select_button.is_pressed) and (not self._is_note_editor_step_active()) and self._chord_task.is_killed:
                        self._chord_task.restart()

    def _is_note_editor_step_active(self):
        return len(list(self._note_editor_component.active_steps)) > 0

    @listens('active_steps')
    def __on_pressed_step_changed(self):
        if self._is_note_editor_step_active():
            if self._show_notes_in_selected_step_task.is_killed:
                self._show_notes_in_selected_step_task.restart()
                return
            else:  # inserted
                return None
        else:  # inserted
            self._show_notes_in_selected_step_task.kill()
            self._update_led_feedback()

    def _update_button_color(self, button):
        if self._is_note_editor_step_active():
            button.color = self._get_color_for_button_in_selected_step(button)
            return
        else:  # inserted
            note_info = self._get_note_info_for_coordinate(button.coordinate)
            button.color = 'Instrument.SelectedNote' if note_info.index in self.selected_notes_provider.selected_notes else 'Instrument.' + note_info.color

    def _set_button_control_properties(self, button):
        super(SelectedNotesInstrumentComponent, self)._set_button_control_properties(button)
        button.set_mode(PlayableControl.Mode.listenable if self.select_button.is_pressed else PlayableControl.Mode.playable_and_listenable)

    @listens('position')
    def __on_position_changed(self):
        self.show_pitch_range_notification()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        pass  # cflow: irreducible

    @contextmanager
    def _updating_selected_notes_model(self):
        yield
        self.song.view.selected_track.set_data('push-instrument-selected-notes', self.selected_notes_provider.selected_notes)
        self._update_led_feedback()