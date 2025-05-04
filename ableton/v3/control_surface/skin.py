# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
from typing import Any, NamedTuple, Optional
from . import BasicColors
ON_SUFFIXES = ('enabled', 'on', 'pressed', 'selected')

class OptionalSkinEntry(NamedTuple):
    pass
    name: str
    fallback_name: Optional[str] = None

class LiveObjSkinEntry(NamedTuple):
    pass
    name: str
    liveobj: Any

class Skin:
    pass

    def __init__(self, colors=None, *a, **k):
        super().__init__(*a, **k)
        self.colors = {}
        if colors is not None:
            self._fill_colors(colors)

    def _fill_colors(self, colors, pathname=''):
        if getattr(colors, '__bases__', None):
            for base in colors.__bases__:
                self._fill_colors(base, pathname=pathname)
        for k, v in vars(colors).items():
            if k[:1] != '_':
                if callable(v):
                    self._fill_colors(v, '{}{}.'.format(pathname, k))
                self.colors['{}{}'.format(pathname, k)] = v
            continue

    def __getitem__(self, key):
        key = self._from_wrapper(key)
        if key is None:
            return
        else:
            if isinstance(key, LiveObjSkinEntry):
                key_name = self._from_wrapper(key.name)
                color = self.colors[key_name]
                if callable(color):
                    return color(key.liveobj)
                else:
                    key = key_name
            if key not in self.colors:
                if key.lower().endswith(ON_SUFFIXES):
                    return BasicColors.ON
                else:
                    return BasicColors.OFF
            else:
                return self.colors[key]

    def _from_wrapper(self, key):
        if isinstance(key, OptionalSkinEntry):
            return key.name if key.name in self.colors else key.fallback_name
        else:
            return key

def merge_skins(*skins):
    pass
    skin = Skin()
    skin.colors = dict(chain(*map(lambda s: s.colors.items(), skins)))
    return skin