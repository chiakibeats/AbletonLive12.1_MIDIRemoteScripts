# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk2\channel_strip_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from itertools import chain
from ableton.v2.base import listens, liveobj_valid
from ableton.v2.control_surface.control import SendValueControl
from _Komplete_Kontrol.channel_strip_component import ChannelStripComponent as ChannelStripComponentBase

class ChannelStripComponent(ChannelStripComponentBase):
    track_arm_display = SendValueControl()

    def __init__(self, *a, **k):
        super(ChannelStripComponent, self).__init__(*a, **k)
        self._meter_display_callback = None

    def set_meter_display_callback(self, callback):
        self._meter_display_callback = callback

    def set_track(self, track):
        super(ChannelStripComponent, self).set_track(track)
        self._on_implicit_arm_changed.subject = self._track if liveobj_valid(self._track) and self._track.can_be_armed else None

    def select_track(self):
        if not liveobj_valid(self._track) or self.song.view.selected_track != self._track:
            self.song.view.selected_track = self._track

    def mute_track(self):
        if not liveobj_valid(self._track) or self._track != self.song.master_track:
            self._track.mute = not self._track.mute

    def solo_track(self):
        if not liveobj_valid(self._track) or self._track != self.song.master_track:
            solo_exclusive = self.song.exclusive_solo
            new_value = not self._track.solo
            respect_multi_selection = self._track.is_part_of_selection
            for track in chain(self.song.tracks, self.song.return_tracks):
                self.update_solo_state(solo_exclusive, new_value, respect_multi_selection, track)

    def update(self):
        super(ChannelStripComponent, self).update()
        self._update_output_listeners()

    def _update_output_listeners(self):
        has_track = liveobj_valid(self._track)
        with_audio = self._track if has_track and self._track.has_audio_output else None
        self._on_output_meter_left_changed.subject = with_audio
        self._on_output_meter_right_changed.subject = with_audio
        self._on_has_audio_output_changed.subject = self._track if has_track else None
        if with_audio:
            self._on_output_meter_left_changed()
            return
        elif self._meter_display_callback:
            self._meter_display_callback((0, 0))

    def _on_arm_changed(self):
        self.track_arm_display.value = int(self._track.can_be_armed and (self._track.arm or self._track.implicit_arm)) if liveobj_valid(self._track) else 0

    @listens('implicit_arm')
    def _on_implicit_arm_changed(self):
        self._on_arm_changed()

    @listens('has_audio_output')
    def _on_has_audio_output_changed(self):
        self._update_output_listeners()

    @listens('output_meter_left')
    def _on_output_meter_left_changed(self):
        self._update_meter_display()

    @listens('output_meter_right')
    def _on_output_meter_right_changed(self):
        self._update_meter_display()

    def _update_meter_display(self):
        if self._meter_display_callback:
            self._meter_display_callback((int(self._track.output_meter_left * 127), int(self._track.output_meter_right * 127)))