# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\note_editor.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import listens
from ableton.v3.control_surface import LiveObjSkinEntry
from ableton.v3.control_surface.components.bar_based_sequence import NoteEditorComponent as NoteEditorComponentBase

class NoteEditorComponent(NoteEditorComponentBase):
    pass

    def set_clip(self, clip):
        super().set_clip(clip)
        self.__on_clip_color_changed.subject = clip

    def get_duration_fine_range_string(self):
        result = self._get_property_range_string('duration', lambda value_range: (v / self.step_length for v in value_range), str_fmt='{:.1f}'.format)
        return '{}{}'.format(result, ' steps' if result != 'No Notes' else '')

    def _update_editor_matrix(self):
        if self.is_enabled():
            visible_steps = self._visible_steps()
            for index, button in enumerate(self.matrix):
                button.color = LiveObjSkinEntry(self._get_color_for_step(index, visible_steps), self._clip)
        else:
            return

    @listens('color')
    def __on_clip_color_changed(self):
        self._update_editor_matrix()