# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\step_sequence.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from ableton.v3.control_surface.components import GRID_RESOLUTIONS as RESOLUTIONS_BASE
from ableton.v3.control_surface.components import StepSequenceComponent as StepSequenceComponentBase
from ableton.v3.control_surface.components.bar_based_sequence import PlayheadComponent
from .loop_selector import LoopSelectorComponent
from .note_editor import NoteEditorComponent
from .note_settings import NoteSettingsComponent
GRID_RESOLUTIONS = tuple(reversed(RESOLUTIONS_BASE[:-3]))
DEFAULT_GRID_RESOLUTION_INDEX = 1

class StepSequenceComponent(StepSequenceComponentBase):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, note_editor_component_type=NoteEditorComponent, loop_selector_component_type=LoopSelectorComponent, playhead_component_type=PlayheadComponent, playhead_notes=list(range(16, 32)), playhead_triplet_notes=[16, 17, 18, 20, 21, 22, 24, 25, 26, 28, 29, 30], **k)
        self._note_settings = NoteSettingsComponent(self._note_editor, parent=self)
        self._playhead.set_note_editor(self._note_editor)

    @property
    def note_settings(self):
        pass
        return self._note_settings

    def set_duration_encoder(self, encoder):
        pass
        self._note_settings.set_duration_encoder(encoder)

    def set_duration_encoder_touch(self, button):
        pass
        self._note_settings.duration_encoder_touch.set_control_element(button)

    def set_transpose_up_button(self, button):
        pass
        self._note_settings.transpose_up_button.set_control_element(button)

    def set_transpose_down_button(self, button):
        pass
        self._note_settings.transpose_down_button.set_control_element(button)

    def set_nudge_left_button(self, button):
        pass
        self._note_settings.nudge_left_button.set_control_element(button)

    def set_nudge_right_button(self, button):
        pass
        self._note_settings.nudge_right_button.set_control_element(button)

    def set_prev_bank_button(self, button):
        pass
        self._loop_selector.prev_bank_button.set_control_element(button)

    def set_next_bank_button(self, button):
        pass
        self._loop_selector.next_bank_button.set_control_element(button)