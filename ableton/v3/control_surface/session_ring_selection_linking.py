# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\session_ring_selection_linking.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ..base import EventObject, depends, index_if, listens
from ..live import scene_index

class SessionRingSelectionLinking(EventObject):
    pass

    @depends(song=None, session_ring=None)
    pass
    pass
    pass
    pass
    pass
    def __init__(self, song=None, session_ring=None, selection_changed_notifier=None, link_to_track_selection=True, link_to_scene_selection=False, *a, **k):
        super().__init__(*a, **k)
        self.song = song
        self._session_ring = session_ring
        if link_to_track_selection:
            self.__on_track_selection_scrolled.subject = selection_changed_notifier
        if link_to_scene_selection:
            self.__on_scene_selection_scrolled.subject = selection_changed_notifier
            return

    @listens('track_selection_scrolled')
    def __on_track_selection_scrolled(self):
        if self.song.view.selected_track not in self._session_ring.tracks_to_use():
            return
        else:  # inserted
            track_index = index_if(lambda t: t == self.song.view.selected_track, self._session_ring.tracks_to_use())
            self._link_session_ring_with_minimal_travel('track', track_index)

    @listens('scene_selection_scrolled')
    def __on_scene_selection_scrolled(self):
        self._link_session_ring_with_minimal_travel('scene', scene_index())

    def _link_session_ring_with_minimal_travel(self, axis_name, current_index):
        ring_axis_offset = getattr(self._session_ring, '{}_offset'.format(axis_name))
        ring_axis_size = getattr(self._session_ring, 'num_{}s'.format(axis_name))
        ending_ring_index = ring_axis_offset + ring_axis_size - 1
        offset_start = current_index - ring_axis_offset
        offset_end = current_index - ending_ring_index
        adjustment = min(0, offset_start) + max(0, offset_end)
        new_offset = ring_axis_offset + adjustment
        if new_offset!= ring_axis_offset:
            track_offset = new_offset
            scene_offset = self._session_ring.scene_offset
            if axis_name == 'scene':
                track_offset = self._session_ring.track_offset
                scene_offset = new_offset
            self._session_ring.set_offsets(track_offset, scene_offset)
            return