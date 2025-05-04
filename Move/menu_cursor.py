# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\menu_cursor.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from ableton.v3.base import EventObject, clamp
from .menu import MenuItem

class MenuCursor(EventObject):
    pass
    __events__ = ('content',)

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._menu = None
        self._current_item = None

    @property
    def menu(self):
        pass
        return self._menu

    @menu.setter
    def menu(self, menu):
        self._menu = menu
        self._current_item = menu
        if menu:
            menu.index = 0
        self.notify_content()

    @property
    def position(self):
        pass
        num_items = len(self._current_item.items)
        if self._current_item.index == 0:
            return 0
        elif num_items > 2 and self._current_item.index == num_items - 1:
            return 2
        else:
            return 1

    @position.setter
    def position(self, delta):
        if self._current_item.items:
            new_index = clamp(self._current_item.index + delta, 0, len(self._current_item.items) - 1)
            if self._current_item.index != new_index:
                self._current_item.index = new_index
                if isinstance(self._current_item, MenuItem):
                    self._current_item.property_setter(new_index)
                self.notify_content()
                return

    def can_go_back(self):
        pass
        return self._current_item and isinstance(self._current_item, MenuItem)

    def go_back(self, to_top=False):
        pass
        if to_top:
            self._menu.index = 0
        self._current_item = self._menu
        self.notify_content()

    def click(self):
        pass
        item = self._current_item.items[self._current_item.index]
        if item.click_action:
            item.click_action()
        elif item.items:
            self._current_item = item
        else:
            self.go_back()
        self.notify_content()

    def get_content(self):
        pass
        return self._current_item.content_fn(self._current_item, self.position)