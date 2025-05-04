# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MiniLab_3\transport.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ableton.v3.base import sign
from ableton.v3.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v3.control_surface.controls import ButtonControl, EncoderControl, ToggleButtonControl
from ableton.v3.live import move_current_song_time

class TransportComponent(TransportComponentBase):
    pass
    __events__ = ('transport_event',)
    arrangement_position_encoder = EncoderControl()
    tap_tempo_button = ButtonControl(color='Transport.TapTempo', pressed_color='Transport.TapTempoPressed')
    loop_button = ToggleButtonControl(color='Transport.LoopOff', on_color='Transport.LoopOn')

    @arrangement_position_encoder.value
    def arrangement_position_encoder(self, value, _):
        move_current_song_time(self.song, sign(value))
        self.notify_transport_event('', str(self.song.get_current_smpte_song_time(Live.Song.TimeFormat.smpte_25)))

    @tap_tempo_button.pressed
    def tap_tempo_button(self, _):
        self._trigger_tap_tempo()

    @tap_tempo_button.released
    def tap_tempo_button(self, _):
        self.notify_transport_event('Tap Tempo', '{} BPM'.format(int(self.song.tempo)))

    @loop_button.released
    def loop_button(self, *_):
        self.notify_transport_event('Loop Mode', 'ON' if self.song.loop else 'OFF')