# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\transport.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import round_to_multiple, sign
from ableton.v3.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v3.live import get_bar_length, move_current_song_time
from .internal_parameter import InternalParameterControl, register_internal_parameter

def format_beat_time(beat_time):
    return '{}.{}.{}'.format(beat_time.bars, beat_time.beats, beat_time.sub_division)

class TransportComponent(TransportComponentBase):
    pass
    tempo_coarse_encoder = InternalParameterControl()
    arrangement_position_encoder = InternalParameterControl()
    loop_start_encoder = InternalParameterControl()
    loop_length_encoder = InternalParameterControl()

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.tempo_coarse_encoder.parameter = register_internal_parameter(self, 'Tempo', lambda _: '{} BPM'.format(int(self.song.tempo)))
        self.arrangement_position_encoder.parameter = register_internal_parameter(self, 'Playback Position', self._position_display_fn)
        self.loop_start_encoder.parameter = register_internal_parameter(self, 'Loop Start', self._loop_start_display_fn)
        self.loop_length_encoder.parameter = register_internal_parameter(self, 'Loop End', self._loop_length_display_fn)
        self.set_position_encoders_use_bar_increments(True)

    @arrangement_position_encoder.value
    def arrangement_position_encoder(self, value, _):
        move_current_song_time(self.song, self._get_quantized_delta(value))

    def _get_quantized_delta(self, value):
        bar_length = get_bar_length()
        if not self.song.is_playing:
            distance_from_bar = round_to_multiple(self.song.current_song_time, bar_length) - self.song.current_song_time
            if distance_from_bar:
                return distance_from_bar if value < 0 else bar_length + distance_from_bar
        return sign(value) * bar_length

    def _position_display_fn(self, _):
        return format_beat_time(self.song.get_current_beats_song_time())

    def _loop_start_display_fn(self, _):
        return format_beat_time(self.song.get_beats_loop_start())

    def _loop_length_display_fn(self, _):
        return format_beat_time(self.song.get_beats_loop_length())