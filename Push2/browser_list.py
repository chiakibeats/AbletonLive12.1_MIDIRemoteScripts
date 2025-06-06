# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\browser_list.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import islice
import Live
from ableton.v2.base import EventObject, clamp, listenable_property, nop
from .model.uniqueid import UniqueIdMixin

class BrowserList(EventObject, UniqueIdMixin):
    LAZY_ACCESS_COUNT = 1000
    LAZY_ACCESS_THRESHOLD = LAZY_ACCESS_COUNT - 100

    def __init__(self, item_iterator=None, item_wrapper=nop, limit=-1, *a, **k):
        super(BrowserList, self).__init__(*a, **k)
        self._selected_index = -1
        self._item_iterator = item_iterator
        self._item_wrapper = item_wrapper
        self._limit = limit
        self._access_all = False
        self._items = []
        self._update_items()

    def _get_limit(self):
        return self._limit

    def _set_limit(self, value):
        if value != self._limit:
            self._limit = value
            self._access_all = False
            self._update_items()
            self.notify_items()
            if value != -1:
                self.selected_index = -1
                return
            else:
                return None
        else:
            return None
    limit = property(_get_limit, _set_limit)

    def _get_access_all(self):
        return self._access_all

    def _set_access_all(self, access_all):
        if self._access_all != access_all:
            self._access_all = access_all
            self._limit = -1
            self._update_items()
            self.notify_items()
    access_all = property(_get_access_all, _set_access_all)

    @listenable_property
    def items(self):
        if self.limit > 0:
            return self._items[:self.limit]
        elif not self._access_all:
            return self._items[:self.LAZY_ACCESS_COUNT]
        else:
            return self._items

    def _update_items(self):
        if isinstance(self._item_iterator, Live.Browser.BrowserItemIterator):
            if self.limit > 0 and len(self._items) < self.limit:
                next_slice = islice(self._item_iterator, self.limit)
            elif not self._access_all and len(self._items) < self.LAZY_ACCESS_COUNT:
                next_slice = islice(self._item_iterator, self.LAZY_ACCESS_COUNT - len(self._items))
            else:
                next_slice = self._item_iterator
            self._items.extend(list(map(self._item_wrapper, next_slice)))
            return
        elif len(self._items) < len(self._item_iterator):
            self._items = list(map(self._item_wrapper, self._item_iterator))
            return
        else:
            return None

    @property
    def selected_item(self):
        return None if self.selected_index == -1 else self.items[self.selected_index]

    @listenable_property
    def selected_index(self):
        return self._selected_index

    @selected_index.setter
    def selected_index(self, value):
        if value != self._selected_index:
            num_children = len(self._items)
            if value < -1 or value >= num_children:
                raise IndexError('Index %i must be in [-1..%i]' % (value, num_children - 1))
            else:
                self._selected_index = value
                self.notify_selected_index()
                if self._selected_index >= self.LAZY_ACCESS_THRESHOLD and (not self._access_all):
                    self.access_all = True
                    return

    def select_index_with_offset(self, offset):
        self.selected_index = clamp(self._selected_index + offset, 0, len(self._items) - 1)