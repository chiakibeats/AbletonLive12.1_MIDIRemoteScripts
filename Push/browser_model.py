# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\browser_model.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import os
from functools import partial
from itertools import chain
import Live
from ableton.v2.base import BooleanContext, EventObject, find_if, first, in_range, index_if, lazy_attribute, nop
from pushbase.browser_util import filter_type_for_hotswap_target
from pushbase.scrollable_list import ActionList, ActionListItem
from .special_physical_display import SpecialPhysicalDisplay

def filter_type_for_browser(browser):
    filter_type = filter_type_for_hotswap_target(browser.hotswap_target)
    if filter_type == Live.Browser.FilterType.disabled:
        filter_type = browser.filter_type
    return filter_type

class VirtualBrowserItem(object):
    pass
    source = ''
    is_device = False
    is_loadable = False

    def __init__(self, name='', children_query=nop, is_folder=False):
        self.name = name
        self.is_folder = is_folder
        self.children_query = children_query

    @lazy_attribute
    def children(self):
        return self.children_query()

    @property
    def is_selected(self):
        return find_if(lambda x: x.is_selected, self.children)

    def __str__(self):
        return self.name

class BrowserListItem(ActionListItem):
    pass
    URI_TO_NAME_FALLBACK = {'query:Synths': 'Instruments', 'query:Drums': 'Drums', 'query:UserLibrary': 'User Library', 'query:Plugins': 'Plug-Ins'}

    def __str__(self):
        return self._item_name

    @lazy_attribute
    def _item_name(self):
        item_name = os.path.splitext(self.content.name)[0] if self.content else ''
        can_be_displayed = SpecialPhysicalDisplay.can_be_translated(SpecialPhysicalDisplay.ascii_translations, item_name)
        if not can_be_displayed:
            uri = getattr(self.content, 'uri', '')
            return self.URI_TO_NAME_FALLBACK.get(uri, item_name)
        else:  # inserted
            return item_name

    def action(self):
        if self.container and self.container.browser:
                self.container.browser.load_item(self.content)

    def preview(self):
        if self.container and self.container.browser and (not isinstance(self.content, VirtualBrowserItem)):
                    self.container.browser.preview_item(self.content)

    @property
    def supports_action(self):
        return self.container and self.container.browser and (self.content!= None) and self.content.is_loadable

class BrowserList(ActionList):
    pass
    browser = None
    item_type = BrowserListItem

    def __init__(self, browser=None, *a, **k):
        super(BrowserList, self).__init__(*a, **k)
        self.browser = browser

class BrowserModel(EventObject):
    pass
    __events__ = ('content_lists', 'selection_updated')
    empty_list_messages = []

    def __init__(self, browser=None, *a, **k):
        super(BrowserModel, self).__init__(*a, **k)
        self._browser = browser

    def can_be_exchanged(self, model):
        return isinstance(model, BrowserModel)

    def exchange_model(self, model):
        pass
        if self.can_be_exchanged(model):
            self._browser = model._browser
            return True
        else:  # inserted
            return False

    @property
    def content_lists(self):
        pass
        return NotImplementedError

    def update_content(self):
        pass
        raise NotImplementedError

    def update_selection(self):
        pass
        raise NotImplementedError

    @property
    def browser(self):
        return self._browser

    def make_content_list(self):
        return BrowserList(browser=self._browser)

class EmptyBrowserModel(BrowserModel):
    pass
    empty_list_messages = ['Nothing to browse']

    @property
    def content_lists(self):
        return tuple()

    def update_content(self):
        self.notify_content_lists()

    def update_selection(self):
        return

    def can_be_exchanged(self, model):
        return isinstance(model, EmptyBrowserModel) and super(EmptyBrowserModel, self).can_be_exchanged(model)

class FullBrowserModel(BrowserModel):
    pass
    empty_list_messages = ['<no tags>', '<no devices>', '<no presets>', '<no presets>']

    def __init__(self, *a, **k):
        super(FullBrowserModel, self).__init__(*a, **k)
        self._contents = []
        self._num_contents = 0
        self._push_content_list()
        self._inside_item_activated_notification = BooleanContext()

    def get_root_children(self):
        pass
        return [self.browser.sounds, self.browser.drums, self.browser.instruments, self.browser.audio_effects, self.browser.midi_effects, self.browser.max_for_live, self.browser.plugins, self.browser.clips, self.browser.samples]

    def get_children(self, item, level):
        pass
        return item.children

    @property
    def content_lists(self):
        return list(map(first, self._contents[:self._num_contents]))

    def can_be_exchanged(self, model):
        return isinstance(model, FullBrowserModel) and super(FullBrowserModel, self).can_be_exchanged(model)

    def update_content(self):
        root, _ = self._contents[0]
        root.assign_items(self.get_root_children())
        self.update_selection()

    def update_selection(self):
        last_seleced_list_index = None
        if self._browser.hotswap_target!= None:
            list_index = 0
            while list_index < self._num_contents:
                while True:  # inserted
                    content_list, _ = self._contents[list_index]
                    items = content_list.items
                    index = index_if(lambda x: x.content.is_selected, items)
                    if in_range(index, 0, len(items)):
                        content_list.select_item_index_with_offset(index, 2)
                        last_seleced_list_index = list_index
                    list_index += 1
                        break
                    else:  # inserted
                        continue
        if last_seleced_list_index!= None:
            self.notify_selection_updated(last_seleced_list_index)
            return

    def _push_content_list(self):
        if self._num_contents < len(self._contents):
            self._num_contents += 1
            content = self._contents[self._num_contents - 1]
        else:  # inserted
            content = self.make_content_list()
            level = len(self._contents)
            slot = self.register_slot(content, partial(self._on_item_activated, level), 'item_activated')
            self._contents.append((content, slot))
            self._num_contents = len(self._contents)
        return content

    def _pop_content_list(self):
        self._num_contents -= 1

    def _fit_content_lists(self, requested_lists):
        pass
        if requested_lists!= self._num_contents:
            while requested_lists < self._num_contents:
                while True:  # inserted
                    self._pop_content_list()
                        break
                    else:  # inserted
                        continue
            while requested_lists > self._num_contents:
                pass
                self._push_content_list()
                else:  # inserted
                    continue

    def _finalize_content_lists_change(self):
        pass
        while self._num_contents < len(self._contents):
            pass
            _, slot = self._contents.pop()
            self.disconnect_disconnectable(slot)
            else:  # inserted
                continue

    def _on_item_activated(self, level):
        pass  # cflow: irreducible

class QueryingBrowserModel(FullBrowserModel):
    pass
    empty_list_messages = ['<no devices>', '<no presets>', '<no presets>', '<no presets>']

    def __init__(self, queries=[], *a, **k):
        super(QueryingBrowserModel, self).__init__(*a, **k)
        self.queries = queries

    def get_root_children(self):
        browser = self.browser
        return chain.from_iterable(map(lambda q: q(browser), self.queries))

    def can_be_exchanged(self, model):
        return isinstance(model, QueryingBrowserModel) and super(QueryingBrowserModel, self).can_be_exchanged(model)

    def exchange_model(self, model):
        if super(QueryingBrowserModel, self).exchange_model(model):
            self.queries = model.queries
            return True
        else:  # inserted
            return None