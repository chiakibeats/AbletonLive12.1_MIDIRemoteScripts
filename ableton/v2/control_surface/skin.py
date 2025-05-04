# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
from ableton.v2.base import EventObject, const, depends, liveobj_valid
from ableton.v2.control_surface.elements.color import is_dynamic_color_factory

class SkinColorMissingError(Exception):
    pass

class DynamicColorNotAvailableError(Exception):
    msg = 'In order to use dynamic colors, you need to inject the song while creating         the skin'

class Skin(EventObject):

    @depends(song=const(None))
    def __init__(self, colors=None, song=None, *a, **k):
        super(Skin, self).__init__(*a, **k)
        self._colors = {}
        self._factory_to_instance_map = {}
        if colors is not None:
            self._fill_colors(colors, song=song)

    def _fill_colors(self, colors, pathname='', song=None):
        if getattr(colors, '__bases__', None):
            for base in colors.__bases__:
                self._fill_colors(base, song=song, pathname=pathname)
        for k, v in colors.__dict__.items():
            if k[:1] != '_':
                if callable(v):
                    self._fill_colors(v, pathname + k + '.', song=song)
                    continue
                else:
                    if is_dynamic_color_factory(v):
                        v = self._get_dynamic_color(v, song)
                    self._colors[pathname + k] = v
            continue

    def __getitem__(self, key):
        try:
            return self._colors[key]
        except KeyError:
            raise SkinColorMissingError('Skin color missing: %s' % str(key))

    def items(self):
        return self._colors.items()

    def _get_dynamic_color(self, color_factory, song):
        if not liveobj_valid(song):
            raise DynamicColorNotAvailableError
        else:
            if color_factory not in self._factory_to_instance_map:
                self._factory_to_instance_map[color_factory] = self._create_dynamic_color(color_factory, song)
            return self._factory_to_instance_map[color_factory]

    def _create_dynamic_color(self, color_factory, song):
        return self.register_disconnectable(color_factory.instantiate(song))

def merge_skins(*skins):
    skin = Skin()
    skin._colors = dict(chain(*map(lambda s: s._colors.items(), skins)))
    return skin