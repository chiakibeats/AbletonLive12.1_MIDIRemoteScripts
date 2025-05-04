# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\note_settings.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import control_list
from .internal_parameter import InternalParameterControl, register_internal_parameter

class NoteSettingsComponent(Component):
    pass
    encoders = control_list(InternalParameterControl, 8, num_steps=10)

    def __init__(self, note_editor, *a, **k):
        super().__init__(*a, name='Note_Settings', **k)
        self._note_editor = note_editor
        self.encoders[0].parameter = register_internal_parameter(self, 'Velocity', lambda _: self._note_editor.get_velocity_range_string())
        self.encoders[1].parameter = register_internal_parameter(self, 'Length', lambda _: self._note_editor.get_duration_range_string())
        self.encoders[2].parameter = register_internal_parameter(self, 'Fine', lambda _: self._note_editor.get_duration_fine_range_string())
        self.encoders[3].parameter = register_internal_parameter(self, 'Nudge', lambda _: self._note_editor.get_nudge_offset_range_string())
        self.encoders[0].num_steps = 64

    @encoders.value
    def encoders(self, value, encoder):
        index = encoder.index
        if index == 0:
            self._note_editor.set_velocity_offset(value)
        elif index == 1:
            self._note_editor.set_duration_offset(self._note_editor.step_length * value)
            return
        elif index == 2:
            self._note_editor.set_duration_offset(self._note_editor.step_length * 0.1 * value)
            return
        elif index == 3:
            self._note_editor.set_nudge_offset(self._note_editor.step_length * 0.1 * value)
            return
        else:
            return None