# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push2\sliced_simpler.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from pushbase.colors import Pulse
from pushbase.sliced_simpler_component import SlicedSimplerComponent
from .colors import IndexedColor
NEXT_SLICE_PULSE_SPEED = 48

def next_slice_color(track_color_index):
    return Pulse(color1=IndexedColor.from_live_index(track_color_index, shade_level=2), color2=IndexedColor.from_live_index(track_color_index, shade_level=1), speed=NEXT_SLICE_PULSE_SPEED)

class Push2SlicedSimplerComponent(SlicedSimplerComponent):

    def _next_slice_color(self):
        return next_slice_color(self.song.view.selected_track.color_index)