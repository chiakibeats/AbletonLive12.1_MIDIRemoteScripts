# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\event_signal\core.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from typing import Any
from ..notifications.type_decl import NOTIFICATION_EVENT_ID
from ..state import State
from ..type_decl import Event
from .type_decl import EventSignalFn

def on_notification() -> EventSignalFn[Any]:

    def signal_fn(_: State, event: Event):
        if event.name == NOTIFICATION_EVENT_ID:
            return event.value
        else:
            return None
    return signal_fn