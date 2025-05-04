# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\components\undo_redo.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from typing import cast
from .. import Component
from ..controls import ButtonControl
from ..display import Renderable

class UndoRedoComponent(Component, Renderable):
    pass
    undo_button = ButtonControl(color='UndoRedo.Undo', pressed_color='UndoRedo.UndoPressed')
    redo_button = ButtonControl(color='UndoRedo.Redo', pressed_color='UndoRedo.RedoPressed')

    def __init__(self, name='Undo_Redo', *a, **k):
        super().__init__(*a, name=name, **k)

    @undo_button.pressed
    def undo_button(self, _):
        if self.song.can_undo:
            self.notify(self.notifications.UndoRedo.undo, cast(str, self.song.undo()))
        else:
            self.notify(self.notifications.UndoRedo.error_undo_no_action)

    @redo_button.pressed
    def redo_button(self, _):
        if self.song.can_redo:
            self.notify(self.notifications.UndoRedo.redo, cast(str, self.song.redo()))
        else:
            self.notify(self.notifications.UndoRedo.error_redo_no_action)