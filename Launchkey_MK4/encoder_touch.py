# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\encoder_touch.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from functools import partial
from ableton.v3.base import listenable_property, task
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl, control_matrix
from ableton.v3.control_surface.display import Renderable

class EncoderTouchComponent(Component, Renderable):
    pass
    touch_controls = control_matrix(ButtonControl)
    last_released_index = listenable_property.managed(None)

    def __init__(self, *a, **k):
        super().__init__(*a, name='Encoder_Touch', **k)
        self._release_tasks = [self._tasks.add(task.sequence(task.wait(0.1), task.run(partial(self._set_released, i)), task.run(partial(self._set_released, None)))) for i in range(8)]
        for release_task in self._release_tasks:
            release_task.kill()

    @touch_controls.pressed
    def touch_controls(self, control):
        self._release_tasks[control.index].kill()

    @touch_controls.released
    def touch_controls(self, control):
        self._release_tasks[control.index].restart()

    def _set_released(self, index):
        self.last_released_index = index