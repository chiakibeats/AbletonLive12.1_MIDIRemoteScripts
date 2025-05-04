# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\notifications\type_decl.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Optional, TypeVar, Union
if TYPE_CHECKING:
    from typing_extensions import ParamSpec, TypeVarTuple
    NotificationParams = TypeVarTuple('NotificationParams')
    NotificationParamSpec = ParamSpec('NotificationParamSpec')
else:
    NotificationParams = TypeVar('NotificationParams')
    NotificationParamSpec = ...

@dataclass
class _TransformDefaultText:
    transform_fn: Callable[[str], str] = lambda s: s

class _DefaultText:
    pass
NotificationFnType = TypeVar('NotificationFnType', bound=Callable)
Notification = Optional[Union[str, _DefaultText, _TransformDefaultText, NotificationFnType]]
pass
Fn = Callable[NotificationParamSpec, Any]
pass
NOTIFICATION_EVENT_ID = 'notification'