# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk3\display.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from dataclasses import dataclass
from itertools import zip_longest
from typing import List, Optional
from ableton.v3.base import as_ascii, flatten
from ableton.v3.control_surface.display import DisplaySpecification, view
from ableton.v3.control_surface.elements import adjust_string
from ableton.v3.live import is_track_armed, liveobj_valid, song
from . import midi

@dataclass
class TrackDetail:
    track_type: int = 0
    selected: int = 0
    muted: int = 0
    soloed: int = 0
    muted_via_solo: int = 0
    armed: int = 0
    left_meter: int = 0
    right_meter: int = 0
    name: str = ''
    volume: str = ''
    pan: str = ''

    def set_track(self, track, is_selected, is_master):
        self.track_type = midi.MASTER_TRACK_TYPE if is_master else midi.DEFAULT_TRACK_TYPE
        self.name = track.name
        self.selected = int(is_selected)
        self.volume = str(track.mixer_device.volume)
        self.pan = str(track.mixer_device.panning)
        if track.has_audio_output:
            self.left_meter = int(track.output_meter_left * 127)
            self.right_meter = int(track.output_meter_right * 127)
        if not is_master:
            self.muted = int(track.mute)
            self.soloed = int(track.solo)
            self.muted_via_solo = int(track.muted_via_solo)
            self.armed = int(is_track_armed(track))

@dataclass
class Content:
    track_details: List[TrackDetail]

def create_root_view() -> view.View[Optional[Content]]:

    @view.View
    def main_view(state) -> Optional[Content]:
        track_details = [TrackDetail() for _ in range(8)]
        tracks = state.session_ring.tracks
        live_set = song()
        for detail, track in zip_longest(track_details, tracks):
            if liveobj_valid(track):
                detail.set_track(track, track == live_set.view.selected_track, track == live_set.master_track)
            continue
        return Content(track_details=track_details)
    return main_view

def protocol(elements):

    def default_text_format(text):
        return tuple(as_ascii(text))

    def volume_format(text):
        if 'dB' in text:
            text = '{} dB'.format(round(float(text.replace(' dB', '')), 1))
        return default_text_format(text)

    def name_format(text):
        return default_text_format(adjust_string(text, length=30).strip())

    def display(content: Content):
        if content:
            for i, detail in enumerate(content.track_details):
                elements.track_type_displays[i].send_value(detail.track_type)
                elements.track_select_displays[i].send_value(detail.selected)
                elements.track_mute_displays[i].send_value(detail.muted)
                elements.track_solo_displays[i].send_value(detail.soloed)
                elements.track_mute_via_solo_displays[i].send_value(detail.muted_via_solo)
                elements.track_arm_displays[i].send_value(detail.armed)
                elements.track_name_displays[i].send_value(name_format(detail.name))
                elements.track_volume_displays[i].send_value(volume_format(detail.volume))
                elements.track_pan_displays[i].send_value(default_text_format(detail.pan))
            elements.track_meter_display.send_value(flatten([[d.left_meter, d.right_meter] for d in content.track_details]))
    return display
display_specification = DisplaySpecification(create_root_view=create_root_view, protocol=protocol)