# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\components\undo_redo.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .. import Component
from ..control import ButtonControl

class UndoRedoComponent(Component):
    undo_button = ButtonControl()
    redo_button = ButtonControl()

    @undo_button.pressed
    def undo_button(self, button):
        self._undo()

    @redo_button.pressed
    def redo_button(self, button):
        self._redo()

    def _redo(self):
        if self.song.can_redo:
            self.song.redo()
            return
        else:
            return None

    def _undo(self):
        if self.song.can_undo:
            self.song.undo()
            return
        else:
            return None