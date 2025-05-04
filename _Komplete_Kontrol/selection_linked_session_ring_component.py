# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\selection_linked_session_ring_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import listens
from ableton.v2.control_surface.components import SessionRingComponent

class SelectionLinkedSessionRingComponent(SessionRingComponent):

    def __init__(self, *a, **k):
        super(SelectionLinkedSessionRingComponent, self).__init__(*a, **k)
        self.__on_selected_track_changed.subject = self.song.view
        self.__on_selected_track_changed()

    @listens('selected_track')
    def __on_selected_track_changed(self):
        selected_track = self.song.view.selected_track
        if selected_track not in self.controlled_tracks():
            all_tracks = list(self.tracks_to_use())
            self.track_offset = all_tracks.index(selected_track)