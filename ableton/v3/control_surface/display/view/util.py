# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\view\util.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from typing import List, Optional
from ..state import State

def suppress_notifications(state: State, exclude: Optional[List[str]]=None):
    pass
    if exclude is None:
        exclude = []
    for notification in getattr(state, '_notifications', set()) - set(exclude):
        state.set_delayed(notification, None, None)