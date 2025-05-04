# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk3\session_navigation.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import listens
from ableton.v3.control_surface.components import SessionNavigationComponent as SessionNavigationComponentBase
from .view_control import add_scroll_encoder, update_scroll_encoder

class SessionNavigationComponent(SessionNavigationComponentBase):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, snap_track_offset=True, **k)
        add_scroll_encoder(self._page_horizontal)
        self._session_ring = self.__on_offset_changed.subject
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()

    def set_track_bank_encoder(self, encoder):
        self._page_horizontal.encoder.set_control_element(encoder)
        self._update_horizontal()

    def _update_horizontal(self):
        super()._update_horizontal()
        update_scroll_encoder(self._page_horizontal)

    @listens('selected_track')
    def __on_selected_track_changed(self):
        selected_track = self.song.view.selected_track
        if selected_track not in self._session_ring.tracks:
            all_tracks = list(self._session_ring.tracks_to_use())
            self._session_ring.track_offset = all_tracks.index(selected_track)