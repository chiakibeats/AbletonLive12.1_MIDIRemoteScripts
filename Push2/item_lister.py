# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\item_lister.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.components import ItemListerComponent as ItemListerComponentBase
from ableton.v2.control_surface.components import ItemSlot, SimpleItemSlot

class IconItemSlot(SimpleItemSlot):

    def __init__(self, icon='', *a, **k):
        super(IconItemSlot, self).__init__(*a, **k)
        self._icon = icon

    @property
    def icon(self):
        return self._icon

class ItemListerComponent(ItemListerComponentBase):

    def _create_slot(self, index, item, nesting_level):
        items = self._item_provider.items[self.item_offset:]
        num_slots = min(self._num_visible_items, len(items))
        slot = None
        if index == 0 and self.can_scroll_left():
            slot = IconItemSlot(icon='page_left.svg')
            slot.is_scrolling_indicator = True
        elif index == num_slots - 1 and self.can_scroll_right():
            slot = IconItemSlot(icon='page_right.svg')
            slot.is_scrolling_indicator = True
        else:
            slot = ItemSlot(item=item, nesting_level=nesting_level)
            slot.is_scrolling_indicator = False
        return slot