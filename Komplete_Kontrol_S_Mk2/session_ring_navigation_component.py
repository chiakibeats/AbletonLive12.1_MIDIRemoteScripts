# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk2\session_ring_navigation_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import listens
from ableton.v2.control_surface import Component
from ableton.v2.control_surface.components import SessionRingTrackPager
from ableton.v2.control_surface.control import SendValueEncoderControl

class SessionRingNavigationComponent(Component):
    navigation_encoder = SendValueEncoderControl()

    def __init__(self, session_ring, *a, **k):
        super(SessionRingNavigationComponent, self).__init__(*a, **k)
        self._track_pager = SessionRingTrackPager(session_ring)
        self.__on_offset_changed.subject = session_ring
        self.__on_tracks_changed.subject = session_ring
        self._update_navigation_encoder()

    @navigation_encoder.value
    def navigation_encoder(self, value, _):
        if value < 0:
            self._track_pager.scroll_up()
            return
        else:
            self._track_pager.scroll_down()

    @listens('offset')
    def __on_offset_changed(self, *_):
        self._update_navigation_encoder()

    @listens('tracks')
    def __on_tracks_changed(self):
        self._update_navigation_encoder()

    def _update_navigation_encoder(self):
        self.navigation_encoder.value = int(self._track_pager.can_scroll_up()) | int(self._track_pager.can_scroll_down() << 1)