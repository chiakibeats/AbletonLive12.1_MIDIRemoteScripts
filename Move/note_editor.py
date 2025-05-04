# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\note_editor.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from sys import maxsize
from ableton.v3.base import depends
from ableton.v3.control_surface import RelativeInternalParameter
from ableton.v3.control_surface.components.bar_based_sequence import NoteEditorComponent as NoteEditorComponentBase
from ableton.v3.control_surface.components.note_editor import get_notes
from ableton.v3.live import liveobj_valid
from .step_color_manager import StepColorManager
DEFAULT_STEP_COUNT = 16

class NoteEditorComponent(NoteEditorComponentBase):
    pass

    @depends(volume_parameters=None)
    def __init__(self, volume_parameters=None, *a, **k):
        super().__init__(*a, **k)
        self._step_start_times = []
        self._step_color_manager = self.register_disconnectable(StepColorManager(update_method=self._update_editor_matrix))
        self._step_color_manager.set_clip(self._clip)
        self._volume_parameters = volume_parameters
        self._velocity_offset_parameter = self.register_disconnectable(RelativeInternalParameter(name='Velocity', display_value_conversion=lambda _: self.get_velocity_range_string()))
        self.register_slot(self._velocity_offset_parameter, lambda x: self.set_velocity_offset(x * 50), 'delta')

    @property
    def step_color_manager(self):
        pass
        return self._step_color_manager

    @property
    def step_start_times(self):
        pass
        return self._step_start_times

    def get_durations_from_step(self, step):
        pass
        notes = self._time_step(step[0]).filter_notes(self._clip_notes)
        return [note.duration for note in notes]

    def get_duration_range_string(self):
        pass
        return self._get_property_range_string('duration', lambda value_range: (v / self.step_length for v in value_range), str_fmt='{:.1f}'.format)

    def set_clip(self, clip):
        super().set_clip(clip)
        if hasattr(self, '_step_color_manager'):
            self._step_color_manager.set_clip(self._clip)

    def notify_clip_notes(self):
        if liveobj_valid(self._clip) and self._pitches:
            notes = get_notes(self._clip, self._pitches, 0.0, maxsize, self._pitch_provider.is_polyphonic)
            self._step_start_times = sorted(list({n.start_time for n in notes}))
        super().notify_clip_notes()

    def _on_pad_pressed(self, pad):
        super()._on_pad_pressed(pad)
        self._volume_parameters.add_parameter(pad, self._velocity_offset_parameter)

    def _on_pad_released(self, pad, *a, **k):
        super()._on_pad_released(pad, *a, **k)
        self._volume_parameters.remove_parameter(pad, force=True)

    @staticmethod
    def _modify_duration(time_step, duration_offset, note):
        note.duration = max(time_step.length * 0.1, note.duration + duration_offset)

    def _get_alternate_color_for_step(self, index, visible_steps):
        return self._step_color_manager.get_color_for_step(index, visible_steps)