# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\type_decl.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from typing import Any, Callable, NamedTuple, TypeVar
from .state import State

class Event(NamedTuple):
    pass
    name: str
    origin: Any
    value: Any
INIT_EVENT = Event(name='init', origin=None, value=None)
pass
DISCONNECT_EVENT = Event(name='disconnect', origin=None, value=None)
pass
ContentType = TypeVar('ContentType')
pass
Render = Callable[[State], ContentType]