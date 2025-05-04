# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\FANTOM\mixer.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import listens_group
from ableton.v3.control_surface.components import MixerComponent as MixerComponentBase
from ableton.v3.control_surface.controls import InputControl
from ableton.v3.live import liveobj_valid
from .control import DisplayControl

class MixerComponent(MixerComponentBase):
    track_select_control = InputControl()
    track_info_display = DisplayControl()

    def set_track_select_control(self, control):
        self.track_select_control.set_control_element(control)

    def set_track_info_display(self, control):
        self.track_info_display.set_control_element(control)

    @track_select_control.value
    def track_select_control(self, value, _):
        if value <= len(self._channel_strips):
            strip = self._master_strip
            if value:
                strip = self._channel_strips[value - 1]
            track = strip.track
            if not liveobj_valid(track) or self.song.view.selected_track != track:
                self.song.view.selected_track = track
                return

    def _reassign_tracks(self):
        super()._reassign_tracks()
        tracks = self._provider.tracks
        self.__on_track_name_changed.replace_subjects(tracks)
        self.__on_track_color_index_changed.replace_subjects(tracks)
        self.__on_track_output_options_changed.replace_subjects(tracks)
        self.__on_track_panning_mode_changed.replace_subjects([t.mixer_device for t in tracks if liveobj_valid(t)])
        self._update_track_info_display()

    def _update_track_info_display(self):
        tracks = self._provider.tracks
        self.track_info_display.data = [t for t in tracks if liveobj_valid(t)]

    @listens_group('name')
    def __on_track_name_changed(self, _):
        self._update_track_info_display()

    @listens_group('color_index')
    def __on_track_color_index_changed(self, _):
        self._update_track_info_display()

    @listens_group('available_output_routing_types')
    def __on_track_output_options_changed(self, _):
        self._update_track_info_display()

    @listens_group('panning_mode')
    def __on_track_panning_mode_changed(self, _):
        self._update_track_info_display()