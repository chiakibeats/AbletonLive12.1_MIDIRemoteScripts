# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Akai_Force_MPC\session_navigation.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v2.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase

class SessionNavigationComponent(SessionNavigationComponentBase):

    def __init__(self, *a, **k):
        super(SessionNavigationComponent, self).__init__(*a, **k)
        for scroll_component in [self._vertical_banking, self._horizontal_banking, self._vertical_paginator, self._horizontal_paginator]:
            for button in [scroll_component.scroll_up_button, scroll_component.scroll_down_button]:
                button.color = 'Navigation.Enabled'
            continue