# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\session_navigation.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import liveobj_changed
from ableton.v2.control_surface.components import SessionRingTrackPager as SessionRingTrackPagerBase
from novation.session_navigation import SessionNavigationComponent as SessionNavigationComponentBase

class SessionRingTrackPager(SessionRingTrackPagerBase):
    pass

    def __init__(self, song=None, *a, **k):
        super().__init__(*a, **k)
        self.song = song

    def do_scroll_up(self):
        super().do_scroll_up()
        self._do_select_track()

    def do_scroll_down(self):
        super().do_scroll_down()
        self._do_select_track()

    def _do_select_track(self):
        if self._session_ring.track_offset in range(len(self.song.tracks)):
            track_to_select = self.song.tracks[self._session_ring.track_offset]
            if liveobj_changed(self.song.view.selected_track, track_to_select):
                self.song.view.selected_track = track_to_select
                return
        else:
            return

class SessionNavigationComponent(SessionNavigationComponentBase):
    pass

    def __init__(self, session_ring=None, *a, **k):
        super().__init__(*a, session_ring=session_ring, **k)
        self._horizontal_paginator.scrollable = SessionRingTrackPager(session_ring=session_ring, song=self.song)