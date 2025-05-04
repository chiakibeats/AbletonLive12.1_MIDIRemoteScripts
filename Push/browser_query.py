# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\browser_query.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from functools import partial
import Live
from ableton.v2.base import const, find_if, first
from .browser_model import VirtualBrowserItem

class BrowserQuery(object):
    pass

    def __init__(self, subfolder=None, *a, **k):
        self.subfolder = subfolder

    def __call__(self, browser):
        if self.subfolder:
            return [VirtualBrowserItem(name=self.subfolder, children_query=partial(self.query, browser), is_folder=True)]
        else:
            return self.query(browser)

    def query(self, browser):
        raise NotImplementedError

class PathBrowserQuery(BrowserQuery):
    pass

    def __init__(self, path=tuple(), root_name=None, *a, **k):
        super(PathBrowserQuery, self).__init__(*a, **k)
        self.path = path
        self.root_name = root_name

    def query(self, browser):
        return self._find_item(self.path, [getattr(browser, self.root_name)], browser) or []

    def _find_item(self, path, items=None, browser=None):
        name = path[0]
        elem = find_if(lambda x: x.name == name, items)
        if elem:
            return [elem] if len(path) == 1 else self._find_item(path[1:], elem.children)

class TagBrowserQuery(BrowserQuery):
    pass

    def __init__(self, include=tuple(), exclude=tuple(), root_name=None, *a, **k):
        super(TagBrowserQuery, self).__init__(*a, **k)
        self.include = include
        self.exclude = exclude
        self.root_name = root_name

    def query(self, browser):
        return list(filter(lambda item: item.name not in self.exclude, sum(list(map(partial(self._extract_path, browser=browser), self.include)), tuple())))

    def _extract_path(self, path, items=None, browser=None):
        if isinstance(path, str):
            path = [path]
        if items is None:
            items = [getattr(browser, self.root_name)]
        if path:
            name = path[0]
            elem = find_if(lambda x: x.name == name, items)
            if elem:
                items = self._extract_path(path[1:], elem.children)
        return tuple(items)

class SourceBrowserQuery(TagBrowserQuery):
    pass

    def __init__(self, *a, **k):
        super(SourceBrowserQuery, self).__init__(*a, **k)

    def query(self, browser):
        root = super(SourceBrowserQuery, self).query(browser)
        groups = dict()
        for item in root:
            groups.setdefault(item.source, []).append(item)
        return list(map(lambda k_g: VirtualBrowserItem(name=k_g[0] if k_g[0] is not None else '', children_query=const(k_g[1])), sorted(list(groups.items()), key=first)))

class PlacesBrowserQuery(BrowserQuery):
    pass

    def __init__(self, *a, **k):
        super(PlacesBrowserQuery, self).__init__(*a, **k)

    def query(self, browser):
        return [browser.packs, browser.user_library] + [browser.current_project] + list(browser.user_folders)

class ColorTagsBrowserQuery(BrowserQuery):
    pass

    def __init__(self, *a, **k):
        super(ColorTagsBrowserQuery, self).__init__(*a, **k)

    def query(self, browser):
        return list(browser.colors)