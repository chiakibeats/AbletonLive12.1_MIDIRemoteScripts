# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\chain_selection_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import count
from ableton.v2.base import listens, listens_group, liveobj_valid
from ableton.v2.control_surface.components import ItemProvider
from .colors import DISPLAY_BUTTON_SHADE_LEVEL, IndexedColor
from .item_lister import ItemListerComponent

class ChainProvider(ItemProvider):

    def __init__(self, *a, **k):
        super(ChainProvider, self).__init__(*a, **k)
        self._rack = None

    def set_rack(self, rack):
        if rack != self._rack:
            rack_view = rack.view if rack else None
            self._rack = rack
            self.__on_chains_changed.subject = rack
            self.__on_selected_chain_changed.subject = rack_view
            self.notify_items()
            self.notify_selected_item()

    @property
    def items(self):
        chains = self._rack.chains if liveobj_valid(self._rack) else []
        return [(chain, 0) for chain in chains]

    @property
    def chains(self):
        return self._rack.chains if liveobj_valid(self._rack) else []

    @property
    def selected_item(self):
        return self._rack.view.selected_chain if liveobj_valid(self._rack) else None

    def select_chain(self, chain):
        self._rack.view.selected_chain = chain

    @listens('chains')
    def __on_chains_changed(self):
        self.notify_items()

    @listens('selected_chain')
    def __on_selected_chain_changed(self):
        self.notify_selected_item()

class ChainSelectionComponent(ItemListerComponent):

    def __init__(self, *a, **k):
        self._chain_parent = ChainProvider()
        super(ChainSelectionComponent, self).__init__(*a, item_provider=self._chain_parent, **k)
        self.register_disconnectable(self._chain_parent)
        self.__on_items_changed.subject = self
        self.__on_items_changed()

    def _on_select_button_pressed(self, button):
        self._chain_parent.select_chain(self.items[button.index].item)

    def _color_for_button(self, button_index, is_selected):
        if is_selected:
            return self.color_class_name + '.ItemSelected'
        else:
            chain_color = self._chain_parent.chains[button_index].color_index
            return IndexedColor.from_live_index(chain_color, DISPLAY_BUTTON_SHADE_LEVEL)

    def set_parent(self, parent):
        self._chain_parent.set_rack(parent)

    @listens('items')
    def __on_items_changed(self):
        self.__on_chain_color_index_changed.replace_subjects(self._chain_parent.chains, identifiers=count())

    @listens_group('color_index')
    def __on_chain_color_index_changed(self, chain_index):
        self.select_buttons[chain_index].color = self._color_for_button(chain_index, self._items_equal(self.items[chain_index], self._item_provider.selected_item))