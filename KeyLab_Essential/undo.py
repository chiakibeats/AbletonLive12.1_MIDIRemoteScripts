# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential\undo.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
from ableton.v2.base import task
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.control import ButtonControl

class UndoComponent(Component):
    undo_button = ButtonControl(color='DefaultButton.Off')

    def __init__(self, *a, **k):
        super(UndoComponent, self).__init__(*a, **k)
        self._light_undo_button_task = self._tasks.add(task.sequence(task.run(partial(self._set_undo_button_light, 'DefaultButton.On')), task.wait(1.0), task.run(partial(self._set_undo_button_light, 'DefaultButton.Off'))))
        self._light_undo_button_task.kill()

    @undo_button.pressed
    def undo_button(self, _):
        if self.song.can_undo:
            self.song.undo()
            if not self._light_undo_button_task.is_running:
                self._light_undo_button_task.restart()
                return

    def _set_undo_button_light(self, value):
        self.undo_button.color = value