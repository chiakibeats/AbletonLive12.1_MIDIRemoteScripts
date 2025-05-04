# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\button_matrix.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import slicer, to_slice
from ableton.v2.control_surface.elements import ButtonMatrixElement as ButtonMatrixElementBase
from ...base import lazy_attribute, recursive_map
from ..display import Renderable

class ButtonMatrixElement(ButtonMatrixElementBase, Renderable):
    pass

    @property
    @slicer(2)
    def submatrix(self, col_slice, row_slice):
        col_slice = to_slice(col_slice)
        row_slice = to_slice(row_slice)
        rows = [row[col_slice] for row in self._orig_buttons[row_slice]]
        return ButtonMatrixElement(rows=rows)

    @lazy_attribute
    def renderable_state(self):
        if not any((isinstance(button, Renderable) for row in self._orig_buttons for button in row)):
            return
        else:
            matrix = recursive_map(lambda button: button.renderable_state if isinstance(button, Renderable) else None, self._orig_buttons)
            return matrix[0] if len(matrix) == 1 else matrix