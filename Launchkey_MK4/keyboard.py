# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\keyboard.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import task
from ableton.v3.control_surface.components import PitchProvider, PlayableComponent

class KeyboardComponent(PlayableComponent, PitchProvider):
    pass
    is_polyphonic = True

    def __init__(self, *a, **k):
        super().__init__(*a, matrix_always_listenable=True, **k)
        self._note_editor = None
        self.pitches = [36]
        self._chord_detection_task = self._tasks.add(task.wait(0.3))
        self._chord_detection_task.kill()

    def set_note_editor(self, note_editor):
        pass
        self._note_editor = note_editor

    def _on_matrix_pressed(self, button):
        pitch = button.index
        if self._note_editor and self._note_editor.active_steps:
            self._note_editor.toggle_pitch_for_all_active_steps(pitch)
            return
        elif self._chord_detection_task.is_running:
            self.pitches.append(pitch)
            return
        else:
            self.pitches = [pitch]
            self._chord_detection_task.restart()

    def _update_led_feedback(self):
        return