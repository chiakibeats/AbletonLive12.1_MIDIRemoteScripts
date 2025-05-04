# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\note_settings.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from ableton.v3.base import listenable_property
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl, StepEncoderControl
from ableton.v3.control_surface.display import Renderable

class NoteSettingsComponent(Component, Renderable):
    pass
    duration_range_string = listenable_property.managed('-')
    can_display_duration = listenable_property.managed(False)
    duration_encoder = StepEncoderControl(num_steps=64)
    duration_encoder_touch = ButtonControl(color=None)
    cursor_skin = {'color': 'NoteSettings.CursorButton', 'pressed_color': 'NoteSettings.CursorButtonPressed'}
    transpose_up_button = ButtonControl(**cursor_skin)
    transpose_down_button = ButtonControl(**cursor_skin)
    nudge_left_button = ButtonControl(**cursor_skin)
    nudge_right_button = ButtonControl(**cursor_skin)

    def __init__(self, note_editor, *a, **k):
        super().__init__(*a, name='Note_Settings', **k)
        self._note_editor = note_editor
        self.register_slot(self._note_editor, self._update_from_property_ranges, 'pitch_provider')
        self.register_slot(self._note_editor, self._update_from_property_ranges, 'active_steps')
        self.register_slot(self._note_editor, self._update_from_property_ranges, 'clip_notes')
        self._update_from_property_ranges()

    def set_duration_encoder(self, encoder):
        pass
        self.can_display_duration = False
        self.duration_encoder.set_control_element(encoder)

    @duration_encoder.value
    def duration_encoder(self, value, _):
        self._note_editor.set_duration_offset(self._note_editor.step_length * 0.1 * value)

    @duration_encoder_touch.pressed
    def duration_encoder_touch(self, _):
        self._show_tied_steps()
        self.can_display_duration = True

    @duration_encoder_touch.released
    def duration_encoder_touch(self, _):
        self._note_editor.step_color_manager.revert_colors()

    def _show_tied_steps(self):
        colors = {}
        step_length = self._note_editor.step_length
        for step in self._note_editor.active_steps:
            durations = self._note_editor.get_durations_from_step(step)
            if not durations:
                continue
            else:
                num_steps = max(durations) / step_length
                step_index = int(step[0] // step_length)
                colors[step_index] = 'NoteEditor.StepTied' if num_steps > 1 else 'NoteEditor.StepPartiallyTied'
                for i in range(int(num_steps - 1)):
                    colors[step_index + 1 + i] = 'NoteEditor.StepTied'
                if num_steps > 1 and num_steps % 1.0:
                    colors[step_index + int(num_steps)] = 'NoteEditor.StepPartiallyTied'
                pass
                continue
        self._note_editor.step_color_manager.show_colors(colors)

    @transpose_up_button.released_immediately
    def transpose_up_button(self, _):
        self._transpose_notes(1)

    @transpose_up_button.pressed_delayed
    def transpose_up_button(self, _):
        self._transpose_notes(12)

    @transpose_down_button.released_immediately
    def transpose_down_button(self, _):
        self._transpose_notes(-1)

    @transpose_down_button.pressed_delayed
    def transpose_down_button(self, _):
        self._transpose_notes(-12)

    @nudge_left_button.pressed
    def nudge_left_button(self, _):
        self._nudge_notes(-1)

    @nudge_right_button.pressed
    def nudge_right_button(self, _):
        self._nudge_notes(1)

    def _nudge_notes(self, delta):
        self._note_editor.set_nudge_offset(self._note_editor.step_length * 0.1 * delta)
        self.notify(self.notifications.Notes.nudge, self._note_editor.get_nudge_offset_range_string())

    def _transpose_notes(self, amount):
        self._note_editor.set_pitch_offset(amount)
        self.notify(self.notifications.Notes.transpose)

    def _update_from_property_ranges(self):
        values = self._note_editor.get_note_property_ranges()
        can_enable = self._note_editor.pitch_provider is not None and values is not None
        is_polyphonic = can_enable and self._note_editor.pitch_provider.is_polyphonic
        pitch_min, pitch_max = values.get('pitch', (0, 0))
        self.transpose_up_button.enabled = is_polyphonic and (pitch_min != pitch_max or pitch_max != 127)
        self.transpose_down_button.enabled = is_polyphonic and (pitch_min != pitch_max or pitch_max != 0)
        nudge_offset = self._note_editor.step_length * 0.1
        self.nudge_left_button.enabled = can_enable and self._note_editor.can_nudge_by_offset(-nudge_offset)
        self.nudge_right_button.enabled = can_enable and self._note_editor.can_nudge_by_offset(nudge_offset)
        self.duration_range_string = self._note_editor.get_duration_range_string()
        if self.duration_encoder_touch.is_pressed:
            self._show_tied_steps()