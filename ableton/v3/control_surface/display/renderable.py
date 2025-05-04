# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\renderable.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from __future__ import annotations
import inspect
from typing import TYPE_CHECKING, Callable, Optional, Type
from ...base import CompoundDisconnectable, EventObject, EventObjectMeta, const, depends, lazy_attribute, nop
from .notifications import Notifications
from .notifications.type_decl import NOTIFICATION_EVENT_ID, Notification, NotificationParams
from .state import State
from .type_decl import Event
if TYPE_CHECKING:
    from typing_extensions import Unpack

def collect_properties(cls):
    pass
    return (name for cls in inspect.getmro(cls) for name, _ in EventObjectMeta.collect_listenable_properties(cls.__dict__))

class Renderable(CompoundDisconnectable):
    pass
    control_base_type = type(object)
    include_in_top_level_state = True

    @depends(react=const(None), notifications=const(None), suppress_notifications=const(None))
    pass
    pass
    pass
    def __init__(self, react=None, notifications: Optional[Type[Notifications]]=None, suppress_notifications: Optional[Callable]=None, *a, **k):
        super().__init__(*a, **k)
        self._react = react or nop
        self._suppress_notifications = suppress_notifications or nop
        self.notifications = notifications if notifications is not None else Notifications

    @lazy_attribute
    def renderable_state(self):
        renderable_state = State()
        self._init_state_from_listenable_properties(renderable_state)
        self._init_state_from_controls(renderable_state)
        return renderable_state

    def notify(self, notification: Notification[Callable[[Unpack[NotificationParams]], Optional[str]]], *a: Unpack[NotificationParams]):
        pass
        data = notification(*a) if notification is None or (callable(notification) else notification)
            if data is not None:
                self.dispatch_event(NOTIFICATION_EVENT_ID, data)

    def suppress_notifications(self):
        pass
        self._suppress_notifications()

    def _init_state_from_listenable_properties(self, renderable_state):
        pass
        if isinstance(self, EventObject):
            for property_name in collect_properties(self.__class__):
                setattr(renderable_state, property_name, getattr(self, property_name))
                self.register_slot(self, self._create_event_handler(property_name), property_name)

    def _init_state_from_controls(self, renderable_state):
        pass
        if hasattr(self, '_control_states'):
            for cls in reversed(inspect.getmro(self.__class__)):
                for name, value in vars(cls).items():
                    if isinstance(value, self.control_base_type):
                        control_state = getattr(value, '_get_state')(self)
                        if isinstance(control_state, Renderable):
                            setattr(renderable_state, name, control_state.renderable_state)
                    continue
                continue
        else:  # inserted
            return

    def dispatch_event(self, name: str, value):
        self._react(Event(name=name, origin=self, value=value))

    def _create_event_handler(self, property_name):
        def on_event(*_):
            property_value = getattr(self, property_name)
            setattr(self.renderable_state, property_name, property_value.renderable_state if isinstance(property_value, Renderable) else property_value)
            self._react(Event(name=property_name, origin=self, value=property_value))
        return on_event