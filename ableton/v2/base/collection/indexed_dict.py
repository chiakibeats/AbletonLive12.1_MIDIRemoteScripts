# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\collection\indexed_dict.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from collections import OrderedDict

class IndexedDict(OrderedDict):
    pass

    def __init__(self, *args, **kwds):
        self.__keys = []
        super(IndexedDict, self).__init__(*args, **kwds)

    def __setitem__(self, key, value, *args, **kwds):
        super(IndexedDict, self).__setitem__(key, value, *args, **kwds)
        if key not in self.__keys:
            self.__keys.append(key)

    def __delitem__(self, key, *args, **kwds):
        super(IndexedDict, self).__delitem__(key, *args, **kwds)
        self.__keys.remove(key)

    def clear(self):
        super(IndexedDict, self).clear()
        self.__keys = []

    def popitem(self, last=True):
        item = super(IndexedDict, self).popitem(last)
        self.__keys.pop(-1 if last else 0)
        return item

    def keys(self):
        return self.__keys

    def item_by_index(self, ix):
        pass
        key = self.__keys[ix]
        return (key, self[key])

    def key_by_index(self, ix):
        pass
        return self.__keys[ix]

    def value_by_index(self, ix):
        pass
        return self[self.__keys[ix]]

    def index_by_key(self, key):
        pass
        return self.__keys.index(key)