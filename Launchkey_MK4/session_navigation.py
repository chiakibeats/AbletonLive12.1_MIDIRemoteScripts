# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\session_navigation.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from typing import cast
from ableton.v3.base import depends
from ableton.v3.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase
from ableton.v3.control_surface.display import Renderable
from ableton.v3.live import action

class SessionNavigationComponent(SessionNavigationComponentBase, Renderable):
    pass

    @depends(session_ring=None)
    def __init__(self, session_ring=None, *a, **k):
        super().__init__(*a, session_ring=session_ring, **k)
        self._session_ring = session_ring
        self.register_slot(self._page_horizontal.scrollable, self._on_tracks_scrolled, 'scrolled')

    def _on_tracks_scrolled(self):
        if self._session_ring.track_offset in range(len(self.song.tracks)) and action.select(self.song.tracks[self._session_ring.track_offset]):
            self.notify(self.notifications.Track.select, cast(str, self.song.view.selected_track.name))