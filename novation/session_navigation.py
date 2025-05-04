# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\session_navigation.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase
from .util import skin_scroll_buttons

class SessionNavigationComponent(SessionNavigationComponentBase):

    def __init__(self, *a, **k):
        super(SessionNavigationComponent, self).__init__(*a, **k)
        skin_scroll_buttons(self._vertical_banking, 'Session.Navigation', 'Session.NavigationPressed')
        skin_scroll_buttons(self._horizontal_banking, 'Session.Navigation', 'Session.NavigationPressed')
        skin_scroll_buttons(self._vertical_paginator, 'Session.Navigation', 'Session.NavigationPressed')
        skin_scroll_buttons(self._horizontal_paginator, 'Session.Navigation', 'Session.NavigationPressed')