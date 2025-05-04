# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\instrument.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from ableton.v3.base import EventObject, MultiSlot, depends, find_if, index_if, listenable_property, listens, task
from ableton.v3.control_surface import LiveObjSkinEntry
from ableton.v3.control_surface.components import Pageable, PageComponent, PitchProvider, PlayableComponent
from ableton.v3.control_surface.controls import ButtonControl
from ableton.v3.control_surface.display import Renderable
from ableton.v3.live import action
from .melodic_pattern import CHROMATIC_MODE_OFFSET, SCALES, MelodicPattern
DEFAULT_SCALE = SCALES[0]

class NoteLayout(EventObject, Renderable):
    pass

    @depends(song=None)
    def __init__(self, song=None, preferences=None, *a, **k):
        super().__init__(*a, **k)
        self._song = song
        self._scale = self._get_scale_from_name(self._song.scale_name)
        self._preferences = preferences if preferences is not None else {}
        self._is_in_key = self._preferences.setdefault('is_in_key', True)
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

    def toggle_is_in_key(self):
        self.is_in_key = not self._is_in_key

    @staticmethod
    def _get_scale_from_name(name):
        return find_if(lambda scale: scale.name == name, SCALES) or DEFAULT_SCALE

    @listens('root_note')
    def __on_root_note_changed(self):
        self.notify_root_note(self._song.root_note)

    @listens('scale_name')
    def __on_scale_name_changed(self):
        self._scale = self._get_scale_from_name(self._song.scale_name)
        self.notify_scale(self._scale)

class InstrumentComponent(PlayableComponent, PageComponent, Pageable, Renderable, PitchProvider):
    pass
    delete_button = ButtonControl(color=None)
    is_polyphonic = True

    @depends(note_layout=None, target_track=None)
    def __init__(self, note_layout=None, target_track=None, *a, **k):
        super().__init__(*a, name='Instrument', scroll_skin_name='Instrument.Scroll', matrix_always_listenable=True, **k)
        self._note_layout = note_layout
        self._target_track = target_track
        self._first_note = self.page_length * 5 + self.page_offset
        self._pattern = self._get_pattern()
        self._note_editor = None
        self.pitches = [self._pattern.note(0, 0).index]
        self._last_page_length = self.page_length
        self._last_page_offset = self.page_offset
        for event in ['scale', 'root_note', 'is_in_key']:
            self.register_slot(self._note_layout, self._on_note_layout_changed, event)
        self.register_slot(MultiSlot(subject=self._target_track, listener=self._update_led_feedback, event_name_list=('target_track', 'color_index')))
        self._chord_detection_task = self._tasks.add(task.wait(0.3))
        self._chord_detection_task.kill()
        self._update_pattern()

    @property
    def note_layout(self):
        pass
        return self._note_layout

    @property
    def page_length(self):
        return len(self._note_layout.notes) if self._note_layout.is_in_key else 12

    @property
    def position_count(self):
        if not self._note_layout.is_in_key:
            return 139
        else:
            offset = self.page_offset
            octaves = 11 if self._note_layout.notes[0] < 8 else 10
            return offset + len(self._note_layout.notes) * octaves

    def _first_scale_note_offset(self):
        if not self._note_layout.is_in_key:
            return self._note_layout.notes[0]
        elif self._note_layout.notes[0] == 0:
            return 0
        else:
            return len(self._note_layout.notes) - index_if(lambda n: n >= 12, self._note_layout.notes)

    @property
    def page_offset(self):
        return self._first_scale_note_offset()

    @property
    def position(self):
        return self._first_note

    @position.setter
    def position(self, note):
        self._first_note = note
        self._update_pattern()
        self._update_matrix()
        self.notify_position()

    @property
    def min_pitch(self):
        return self.pattern[0].index

    @property
    def max_pitch(self):
        identifiers = [control.identifier for control in self.matrix if control.identifier is not None]
        return max(identifiers) if len(identifiers) > 0 else 127

    @property
    def pattern(self):
        return self._pattern

    def set_note_editor(self, note_editor):
        pass
        self._note_editor = note_editor
        self.__on_active_steps_changed.subject = note_editor

    def _on_matrix_pressed(self, button):
        pitch = self._get_note_info_for_coordinate(button.coordinate).index
        if pitch is not None:
            if self.delete_button.is_pressed:
                button.color = 'Instrument.PadAction'
                if action.delete_notes_with_pitch(self._target_track.target_clip, pitch):
                    self.notify(self.notifications.Notes.Pitch.delete, pitch)
                    return
                else:
                    self.notify(self.notifications.Notes.error_no_notes_to_delete)
                    return
            else:
                if self.select_button.is_pressed and pitch not in self.pitches:
                    self.notify(self.notifications.Notes.Pitch.select, pitch)
                if self._note_editor and self._note_editor.active_steps:
                    self._note_editor.toggle_pitch_for_all_active_steps(pitch)
                elif self._chord_detection_task.is_running:
                    self.pitches.append(pitch)
                else:
                    self.pitches = [pitch]
                    self._chord_detection_task.restart()
                self._update_button_color(button)
                return

    @delete_button.value
    def delete_button(self, _, button):
        self._set_control_pads_from_script(button.is_pressed)

    def scroll_page_up(self):
        super().scroll_page_up()
        self.notify(self.notifications.Notes.Octave.up)

    def scroll_page_down(self):
        super().scroll_page_down()
        self.notify(self.notifications.Notes.Octave.down)

    def scroll_up(self):
        super().scroll_up()
        self.notify(self.notifications.Notes.ScaleDegree.up)

    def scroll_down(self):
        super().scroll_down()
        self.notify(self.notifications.Notes.ScaleDegree.down)

    def _align_first_note(self):
        self._first_note = self.page_offset + (self._first_note - self._last_page_offset) * (self.page_length / self._last_page_length)
        if self._first_note >= self.position_count:
            self._first_note -= self.page_length
        self._last_page_length = self.page_length
        self._last_page_offset = self.page_offset

    def _on_note_layout_changed(self, _):
        self._update_scale()

    def _update_scale(self):
        self._align_first_note()
        self._update_pattern()
        self._update_matrix()
        self.notify_position()

    def update(self):
        super().update()
        if self.is_enabled():
            self._update_matrix()
            return

    def _update_pattern(self):
        self._pattern = self._get_pattern()

    def _invert_and_swap_coordinates(self, coordinates):
        return (coordinates[1], self.height - 1 - coordinates[0])

    def _get_note_info_for_coordinate(self, coordinate):
        x, y = self._invert_and_swap_coordinates(coordinate)
        return self.pattern.note(x, y)

    def _update_button_color(self, button):
        note_info = self._get_note_info_for_coordinate(button.coordinate)
        color = LiveObjSkinEntry('Instrument.{}'.format(note_info.color), self._target_track.target_track)
        if self._note_editor:
            if self._note_editor.active_steps:
                if self._note_editor.is_pitch_active(button.identifier):
                    color = 'Instrument.NoteInStep'
                pass
            elif button.identifier in self.pitches:
                color = 'Instrument.NoteSelected'
        button.color = color

    def _button_should_be_enabled(self, button):
        return self._get_note_info_for_coordinate(button.coordinate).index is not None

    def _note_translation_for_button(self, button):
        note_info = self._get_note_info_for_coordinate(button.coordinate)
        return (note_info.index, note_info.channel)

    def _update_matrix(self):
        self._update_control_from_script()
        self._update_note_translations()
        self._update_led_feedback()

    @listens('active_steps')
    def __on_active_steps_changed(self):
        self._update_led_feedback()

    def _get_pattern(self, first_note=None):
        if first_note is None:
            first_note = int(round(self._first_note))
        interval = len(self._note_layout.notes)
        notes = self._note_layout.notes
        width = None
        height = None
        octave = first_note // self.page_length
        offset = first_note % self.page_length - self._first_scale_note_offset()
        if self._note_layout.is_in_key:
            width = interval + 1
        else:
            interval = 5
            offset -= CHROMATIC_MODE_OFFSET
        steps = [1, interval]
        origin = [offset, 0]
        return MelodicPattern(steps=steps, scale=notes, origin=origin, root_note=octave * 12, chromatic_mode=not self._note_layout.is_in_key, width=width, height=height)