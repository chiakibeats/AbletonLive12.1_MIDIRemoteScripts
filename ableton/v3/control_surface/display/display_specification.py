# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\display\display_specification.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import sys
from contextlib import contextmanager
from io import StringIO
from typing import Callable, Optional, Type
from ...base import Disconnectable, const, depends, inject
from .notifications import DefaultNotifications, Notifications
from .renderable import Renderable
from .state import State
from .type_decl import DISCONNECT_EVENT, INIT_EVENT
from .util import updating_display
from .view import View

class DisplaySpecification:
    pass
    pass
    pass
    pass
    def __init__(self, create_root_view: Optional[Callable[[], View]]=None, protocol=None, notifications: Optional[Type[Notifications]]=None):
        self.create_root_view = create_root_view
        self.protocol = protocol
        self.notifications = notifications or DefaultNotifications

class Display(Disconnectable):
    pass

    @depends(display_state=const(None))
    pass
    def __init__(self, specification: DisplaySpecification, renderable_components, elements, display_state=None):
        pass  # cflow: irreducible

    @property
    def state(self):
        pass
        return self._state

    def react(self, event):
        pass
        if self._initialized:
            for fn in self._react_fns:
                fn(self._state, event)
            self._suppress_stdout_from_render = False
            self.render_and_update_display()

    def render(self):
        pass
        return self._root_view(self._state)

    def display(self, content):
        pass  # cflow: irreducible

    def render_and_update_display(self):
        pass  # cflow: irreducible

    @contextmanager
    def deferring_render_and_update_display(self):
        if False: yield  # inserted
        pass  # cflow: irreducible

    @property
    def rendered_content(self):
        pass
        return self._last_displayed_content

    def disconnect(self):
        self.react(DISCONNECT_EVENT)

    def clear_content_cache(self):
        pass
        self._last_displayed_content = None

@contextmanager
def capturing_stdout(temp_output_stream):
    if False: yield  # inserted
    pass  # cflow: irreducible