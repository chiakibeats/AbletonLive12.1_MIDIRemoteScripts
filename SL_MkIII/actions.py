# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\actions.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from contextlib import contextmanager
from Live.Song import RecordingQuantization
from ableton.v2.base import listens
from ableton.v2.control_surface.components import ClipActionsComponent
from ableton.v2.control_surface.control import ButtonControl, ColorSysexControl, ToggleButtonControl, control_list
from ableton.v3.live import action
from .control import BinaryControl, TextDisplayControl
ACTION_NAMES = ('Undo', 'Redo', 'Click', '', '', '', '', '')
UNDO_DISPLAY_INDEX = 0
REDO_DISPLAY_INDEX = 1
METRONOME_DISPLAY_INDEX = 2
QUANTIZE_DISPLAY_INDEX = 5
CAPTURE_DISPLAY_INDEX = 7

class ActionsComponent(ClipActionsComponent):
    actions_display = TextDisplayControl(segments=ACTION_NAMES)
    actions_color_fields = control_list(ColorSysexControl, len(ACTION_NAMES))
    actions_selection_fields = control_list(BinaryControl, len(ACTION_NAMES))
    undo_button = ButtonControl(color='Action.Available')
    redo_button = ButtonControl(color='Action.Available')
    delete_button = ButtonControl(color='Action.Available')
    duplicate_button = ButtonControl(color='Action.Available')
    double_loop_button = ButtonControl(color='Action.Available')
    capture_midi_button = ButtonControl()
    quantize_button = ButtonControl()
    metronome_button = ToggleButtonControl(toggled_color='Transport.MetronomeOn', untoggled_color='Transport.MetronomeOff')

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.__on_can_capture_midi_changed.subject = self.song
        self.__on_can_capture_midi_changed()
        self.actions_color_fields[METRONOME_DISPLAY_INDEX].color = 'Transport.MetronomeOn'
        self.actions_color_fields[UNDO_DISPLAY_INDEX].color = 'Action.Available'
        self.actions_color_fields[REDO_DISPLAY_INDEX].color = 'Action.Available'
        self.__on_metronome_changed.subject = self.song
        self.__on_metronome_changed()
        self._quantization_value = RecordingQuantization.rec_q_sixtenth
        self.__on_record_quantization_changed.subject = self.song
        self.__on_record_quantization_changed()

    @property
    def capture_midi_display(self):
        return self.actions_display[CAPTURE_DISPLAY_INDEX]

    @capture_midi_display.setter
    def capture_midi_display(self, string):
        self.actions_display[CAPTURE_DISPLAY_INDEX] = string

    @property
    def capture_midi_color_field(self):
        return self.actions_color_fields[CAPTURE_DISPLAY_INDEX]

    @property
    def capture_midi_selection_field(self):
        return self.actions_selection_fields[CAPTURE_DISPLAY_INDEX]

    @property
    def quantize_display(self):
        return self.actions_display[QUANTIZE_DISPLAY_INDEX]

    @quantize_display.setter
    def quantize_display(self, string):
        self.actions_display[QUANTIZE_DISPLAY_INDEX] = string

    @property
    def quantize_color_field(self):
        return self.actions_color_fields[QUANTIZE_DISPLAY_INDEX]

    @property
    def quantize_selection_field(self):
        return self.actions_selection_fields[QUANTIZE_DISPLAY_INDEX]

    @undo_button.pressed
    def undo_button(self, _):
        if self.song.can_undo:
            self.song.undo()
            return
        else:
            return None

    @redo_button.pressed
    def redo_button(self, _):
        if self.song.can_redo:
            self.song.redo()
            return
        else:
            return None

    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        try:
            self.song.capture_midi()
        except RuntimeError:
            return None

    @quantize_button.pressed
    def quantize_button(self, _):
        pass

    @delete_button.released
    def delete_button(self, _):
        pass

    @duplicate_button.pressed
    def duplicate_button(self, _):
        pass

    @double_loop_button.pressed
    def double_loop_button(self, _):
        pass

    @metronome_button.toggled
    def metronome_button(self, toggled, _):
        self.song.metronome = toggled

    @contextmanager
    def _handling_undo_step(self):
        self.song.begin_undo_step()
        yield
        self.song.end_undo_step()

    @listens('can_capture_midi')
    def __on_can_capture_midi_changed(self):
        self._update_conditional_controls('capture_midi', 'capture', self._song.can_capture_midi)

    @listens('metronome')
    def __on_metronome_changed(self):
        self._update_metronome_controls()

    @listens('midi_recording_quantization')
    def __on_record_quantization_changed(self):
        quantization_value = self.song.midi_recording_quantization
        if quantization_value != RecordingQuantization.rec_q_no_q:
            self._quantization_value = quantization_value

    def _update_metronome_controls(self):
        metronome = self.song.metronome
        self.metronome_button.is_toggled = metronome
        self.actions_selection_fields[METRONOME_DISPLAY_INDEX].is_on = metronome

    def _update_action_buttons(self):
        super()._update_action_buttons()
        self._update_conditional_controls('quantize', 'quantise', self._can_perform_clip_action())

    def _update_conditional_controls(self, name, display_name, condition_met):
        setattr(self, '{}_display'.format(name), display_name if condition_met else '')
        getattr(self, '{}_color_field'.format(name)).color = 'DefaultButton.On' if condition_met else 'DefaultButton.Disabled'
        getattr(self, '{}_selection_field'.format(name)).is_on = condition_met
        getattr(self, '{}_button'.format(name)).enabled = condition_met