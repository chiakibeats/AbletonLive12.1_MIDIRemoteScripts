# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\step_sequence.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import depends, flatten, listens, task
from ableton.v3.control_surface.components import GridResolutionComponent
from ableton.v3.control_surface.components import SequencerClip as SequencerClipBase
from ableton.v3.control_surface.components import StepSequenceComponent as StepSequenceComponentBase
from ableton.v3.control_surface.components.bar_based_sequence import PlayheadComponent
from ableton.v3.live import liveobj_valid
from . import midi
from .loop_selector import LoopSelectorComponent
from .note_editor import NoteEditorComponent
from .note_settings import NoteSettingsComponent

class SequencerClip(SequencerClipBase):
    pass

    @depends(parent_task_group=None)
    def __init__(self, parent_task_group=None, *a, **k):
        super().__init__(*a, **k)
        self.__on_target_track_changed.subject = self._target_track
        self._pending_clip = None
        self._tasks = parent_task_group
        self._set_clip_task = self._tasks.add(task.run(self._do_set_clip))
        self._set_clip_task.kill()

    def set_clip(self, clip):
        pass
        self.clip = None
        self._pending_clip = clip
        self._set_clip_task.restart()

    def _do_set_clip(self):
        clip = self._pending_clip if liveobj_valid(self._pending_clip) else None
        if clip:
            self.clip = clip
        else:
            self.__on_target_clip_changed()
        self.__on_target_clip_changed.subject = None if clip else self._target_track
        self.__on_slot_has_clip_changed.subject = clip.canonical_parent if clip else None
        self._pending_clip = None

    @listens('has_clip')
    def __on_slot_has_clip_changed(self):
        self._set_clip_task.restart()

    @listens('target_track')
    def __on_target_track_changed(self):
        self._set_clip_task.restart()

class StepSequenceComponent(StepSequenceComponentBase):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, grid_resolution=GridResolutionComponent(), note_editor_component_type=NoteEditorComponent, loop_selector_component_type=LoopSelectorComponent, playhead_component_type=PlayheadComponent, playhead_notes=list(flatten(midi.MAIN_PAD_IDS)), **k)
        self._note_settings = NoteSettingsComponent(self._note_editor, parent=self)
        self._playhead.set_note_editor(self._note_editor)

    @property
    def playhead(self):
        pass
        return self._playhead

    def set_encoders(self, encoders):
        pass
        self._note_settings.encoders.set_control_element(encoders)

    def set_double_button(self, button):
        pass
        self._loop_selector.double_button.set_control_element(button)

    def set_quantize_button(self, button):
        pass
        self._loop_selector.quantize_button.set_control_element(button)