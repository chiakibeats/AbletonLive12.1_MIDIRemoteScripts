# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\state.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from dataclasses import dataclass
from pprint import pformat
from typing import Callable, Optional
from weakref import ref
import Live
from ...base import EventObject, listenable_property

@dataclass
class StateFilters:
    pass
    key_filter: Callable = lambda k: not k.startswith('_')
    value_filter: Callable = lambda v: v is not None and v != ''

class State(EventObject):
    pass
    notification_visible = listenable_property.managed(False)
    repr_filters = StateFilters()

    def __init__(self):
        super().__init__()
        self._timers = {}

    def disconnect(self):
        super().disconnect()
        for timer in self._timers:
            timer.stop()
        self._timers = None

    def __repr__(self):
        return pformat(self.get_repr_data(), indent=4)

    def set_delayed(self, attr_name: str, value, delay_time: Optional[float]):
        pass

        def do_setattr(obj, name, value):
            setattr(obj, name, value)
            getattr(obj, '_timers').pop(name, None)
            self.notification_visible = bool(getattr(obj, '_timers'))
        if delay_time is None:
            do_setattr(self, attr_name, value)
            return
        else:
            _self = ref(self)

            def delayed_setattr():
                if _self():
                    do_setattr(_self(), attr_name, value)
            self._timers[attr_name] = Live.Base.Timer(callback=delayed_setattr, interval=int(delay_time * 1000), start=True)
            self.notification_visible = True

    def get_repr_data(self):
        pass
        return State.as_dict(self, self.repr_filters)

    @staticmethod
    def as_dict(instance, state_filters=StateFilters(value_filter=lambda _: True)):
        pass
        if isinstance(instance, dict):
            return instance
        else:
            dct = dict(vars(instance))
            keys_to_remove = set()
            for key, value in dct.items():
                if not state_filters.key_filter(key):
                    keys_to_remove.add(key)
                    continue
                elif isinstance(value, State):
                    dct[key] = State.as_dict(value, state_filters)
                    continue
                else:
                    if not state_filters.value_filter(value):
                        keys_to_remove.add(key)
                    pass
                    continue
            for key in keys_to_remove:
                del dct[key]
            return dct

    def trigger_timers(self, from_test=False):
        for timer in list(self._timers.values()):
            timer.trigger()