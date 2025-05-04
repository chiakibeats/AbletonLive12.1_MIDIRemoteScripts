# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\notifications\meta.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from __future__ import annotations
from inspect import getmro
from typing import Callable
from .type_decl import Notification, _DefaultText, _TransformDefaultText

def transform_notification(default: Notification, transform_fn: Callable[[str], str]):
    if not callable(default):
        return transform_fn(default)
    else:

        def notification_fn(*a, **k) -> str:
            return transform_fn(default(*a, **k))
        return notification_fn

def update_special_attributes(cls, exclude_by_default=True):
    base_class = getmro(cls)[-2]
    for name, value in vars(base_class).items():
        subclass_value = vars(cls).get(name, None)
        if subclass_value is None and isinstance(value, type):
            subclass_value = type(name, (value,), {})
            setattr(cls, name, subclass_value)
        if isinstance(subclass_value, type):
            include_all = getattr(subclass_value, 'INCLUDE_ALL', False)
            update_special_attributes(subclass_value, False if include_all else exclude_by_default)
            continue
        else:
            if not name.startswith('__'):
                if exclude_by_default and subclass_value is None:
                    setattr(cls, name, None)
                    continue
                else:
                    if subclass_value is not None:
                        pass
                    if isinstance(subclass_value, _DefaultText):
                        setattr(cls, name, getattr(base_class, name))
                        continue
                    elif isinstance(subclass_value, _TransformDefaultText):
                        setattr(cls, name, transform_notification(getattr(base_class, name), subclass_value.transform_fn))
            continue

class DefaultNotificationsMeta(type):
    pass

    def __new__(cls, name, bases, dct):
        new_cls = super().__new__(cls, name, bases, dct)
        update_special_attributes(new_cls)
        return new_cls