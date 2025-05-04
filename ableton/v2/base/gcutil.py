# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\base\gcutil.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import gc
from collections import defaultdict
from .util import old_hasattr

def typename(obj):
    pass
    if old_hasattr(obj, '__class__'):
        return obj.__class__.__name__
    elif old_hasattr(obj, '__name__'):
        return obj.__name__
    else:
        return '<unknown>'

def histogram(name_filter=None, objs=None):
    pass
    all_ = gc.get_objects() if objs is None else objs

    def _name_filter(name):
        return name_filter is None or name_filter in name
    hist = defaultdict(lambda: 0)
    for o in all_:
        n = typename(o)
        if _name_filter(n):
            hist[n] += 1
        continue
    return hist

def instances_by_name(name_filter):
    pass
    return [o for o in gc.get_objects() if name_filter == typename(o)]

def refget(objs, level=1):
    pass
    for _ in range(level):
        refs = gc.get_referrers(*objs)
        try:
            refs.remove(objs)
        except ValueError:
            pass
        objs = refs
        continue
    return refs