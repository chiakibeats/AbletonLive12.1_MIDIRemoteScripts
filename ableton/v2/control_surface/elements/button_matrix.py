# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\button_matrix.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ...base import const, in_range, product, slicer, to_slice
from ..compound_element import CompoundElement

class ButtonMatrixElement(CompoundElement):
    pass

    def __init__(self, rows=[], *a, **k):
        super(ButtonMatrixElement, self).__init__(*a, **k)
        self._buttons = []
        self._orig_buttons = []
        self._button_coordinates = {}
        self._max_row_width = 0
        for row in rows:
            self.add_row(row)

    @property
    @slicer(2)
    def submatrix(self, col_slice, row_slice):
        col_slice = to_slice(col_slice)
        row_slice = to_slice(row_slice)
        rows = [row[col_slice] for row in self._orig_buttons[row_slice]]
        return ButtonMatrixElement(rows=rows)

    def add_row(self, buttons):
        self._buttons.append([None] * len(buttons))
        self._orig_buttons.append(buttons)
        for index, button in enumerate(buttons):
            self._button_coordinates[button] = (index, len(self._buttons) - 1)
            self.register_control_element(button)
        if self._max_row_width < len(buttons):
            self._max_row_width = len(buttons)

    def width(self):
        return self._max_row_width

    def height(self):
        return len(self._buttons)

    def send_value(self, column, row, value, force=False):
        if len(self._buttons[row]) > column:
            button = self._buttons[row][column]
            if button:
                button.send_value(value, force=force)

    def set_light(self, column, row, value):
        if len(self._buttons[row]) > column:
            button = self._buttons[row][column]
            if button:
                button.set_light(value)

    def get_button(self, row, column):
        row = int(row)
        if len(self._buttons[row]) > column:
            return self._buttons[row][column]
        else:
            return None

    def set_channel(self, channel):
        for button in self:
            if button:
                button.set_channel(channel)
            pass
            continue
        return None

    def reset(self):
        for button in self:
            if button:
                button.reset()
            continue
        return None

    def __iter__(self):
        for j, i in product(range(self.height()), range(self.width())):
            button = self.get_button(j, i)
            yield button

    def __getitem__(self, index):
        if isinstance(index, slice):
            indices = index.indices(len(self))
            return list(map(self._do_get_item, range(*indices)))
        else:
            if index < 0:
                index += len(self)
            return self._do_get_item(index)

    def _do_get_item(self, index):
        row, col = divmod(index, self.width())
        return self.get_button(row, col)

    def __len__(self):
        return self.width() * self.height()

    def iterbuttons(self):
        for j, i in product(range(self.height()), range(self.width())):
            button = self.get_button(j, i)
            yield (button, (i, j))

    def on_nested_control_element_value(self, value, sender):
        x, y = self._button_coordinates[sender]
        is_momentary = getattr(sender, 'is_momentary', const(None))()
        self.notify_value(value, x, y, is_momentary)

    def on_nested_control_element_received(self, control):
        x, y = self._button_coordinates[control]
        self._buttons[y][x] = control

    def on_nested_control_element_lost(self, control):
        x, y = self._button_coordinates[control]
        self._buttons[y][x] = None