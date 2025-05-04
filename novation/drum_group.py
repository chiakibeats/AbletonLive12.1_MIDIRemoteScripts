# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\novation\drum_group.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.components import DrumGroupComponent as DrumGroupComponentBase
from .util import skin_scroll_buttons

class DrumGroupComponent(DrumGroupComponentBase):

    def __init__(self, *a, **k):
        super(DrumGroupComponent, self).__init__(*a, **k)
        skin_scroll_buttons(self._position_scroll, 'DrumGroup.Navigation', 'DrumGroup.NavigationPressed')
        skin_scroll_buttons(self._page_scroll, 'DrumGroup.Navigation', 'DrumGroup.NavigationPressed')

    def set_parent_track(self, track):
        return