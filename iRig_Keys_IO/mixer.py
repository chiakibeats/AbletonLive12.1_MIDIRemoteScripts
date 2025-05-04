# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\iRig_Keys_IO\mixer.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import forward_property, liveobj_valid
from ableton.v2.control_surface.components import MixerComponent as MixerComponentBase
from ableton.v2.control_surface.control import ButtonControl
from .scroll import ScrollComponent

class MixerComponent(MixerComponentBase):
    track_scroll_encoder = forward_property('_track_scrolling')('scroll_encoder')
    selected_track_arm_button = ButtonControl()

    def __init__(self, *a, **k):
        super(MixerComponent, self).__init__(*a, **k)
        self._track_scrolling = ScrollComponent(parent=self)
        self._track_scrolling.can_scroll_up = self._can_select_prev_track
        self._track_scrolling.can_scroll_down = self._can_select_next_track
        self._track_scrolling.scroll_up = self._select_prev_track
        self._track_scrolling.scroll_down = self._select_next_track

    @selected_track_arm_button.pressed
    def selected_track_arm_button(self, _):
        selected_track = self.song.view.selected_track
        if not liveobj_valid(selected_track) or selected_track.can_be_armed:
                new_value = not selected_track.arm
                for track in self.song.tracks:
                    if track.can_be_armed and (track == selected_track or (track.is_part_of_selection and selected_track.is_part_of_selection)):
                            track.arm = new_value
                            continue
                        else:  # inserted
                            if self.song.exclusive_arm and track.arm:
                                track.arm = False
                    continue
                return None
            else:  # inserted
                return None
        else:  # inserted
            return None

    def _can_select_prev_track(self):
        return self.song.view.selected_track!= self._provider.tracks_to_use()[0]

    def _can_select_next_track(self):
        return self.song.view.selected_track!= self._provider.tracks_to_use()[(-1)]

    def _select_prev_track(self):
        selected_track = self.song.view.selected_track
        tracks = self._provider.tracks_to_use()
        index = list(tracks).index(selected_track)
        self.song.view.selected_track = tracks[index - 1]

    def _select_next_track(self):
        selected_track = self.song.view.selected_track
        tracks = self._provider.tracks_to_use()
        index = list(tracks).index(selected_track)
        self.song.view.selected_track = tracks[index + 1]