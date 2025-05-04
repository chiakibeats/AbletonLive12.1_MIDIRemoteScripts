# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\Skin.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain

class SkinColorMissingError(Exception):
    pass

class Skin(object):

    def __init__(self, colors=None, *a, **k):
        super(Skin, self).__init__(*a, **k)
        self._colors = {}
        if colors is not None:
            self._fill_colors(colors)

    def _fill_colors(self, colors, pathname=''):
        if getattr(colors, '__bases__', None):
            for base in colors.__bases__:
                self._fill_colors(base)
        for k, v in colors.__dict__.items():
            if k[:1] != '_':
                if callable(v):
                    self._fill_colors(v, pathname + k + '.')
                    continue
                else:
                    self._colors[pathname + k] = v
            continue

    def __getitem__(self, key):
        try:
            return self._colors[key]
        except KeyError:
            raise SkinColorMissingError('Skin color missing: %s' % str(key))

    def items(self):
        return iter(self._colors.items())

def merge_skins(*skins):
    skin = Skin()
    skin._colors = dict(chain(*[list(s._colors.items()) for s in skins]))
    return skin