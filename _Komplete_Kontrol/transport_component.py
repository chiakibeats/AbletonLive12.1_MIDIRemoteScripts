# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Komplete_Kontrol\transport_component.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.utils import old_div
from ableton.v2.base import listens, move_current_song_time
from ableton.v2.control_surface.components import ToggleComponent
from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase
from ableton.v2.control_surface.control import ButtonControl, EncoderControl

class TransportComponent(TransportComponentBase):
    play_button = ButtonControl(color='Transport.PlayOff')
    jump_encoder = EncoderControl()
    loop_start_encoder = EncoderControl()

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self.__on_signature_numerator_changed.subject = self.song
        self.__on_signature_denominator_changed.subject = self.song
        self._session_record_toggle = ToggleComponent('session_record', self.song, parent=self)
        self._calculate_distance_to_move()

    def set_play_button(self, button):
        self.play_button.set_control_element(button)

    def set_session_record_button(self, button):
        self._session_record_toggle.set_toggle_button(button)

    @play_button.pressed
    def play_button(self, _):
        self.song.start_playing()

    @jump_encoder.value
    def jump_encoder(self, value, _):
        move_current_song_time(self.song, value * self._distance_to_move)

    @loop_start_encoder.value
    def loop_start_encoder(self, value, _):
        self.song.loop_start = max(0.0, self.song.loop_start + value * self._distance_to_move)

    @listens('signature_numerator')
    def __on_signature_numerator_changed(self):
        self._calculate_distance_to_move()

    @listens('signature_denominator')
    def __on_signature_denominator_changed(self):
        self._calculate_distance_to_move()

    def _calculate_distance_to_move(self):
        self._distance_to_move = old_div(4.0, self.song.signature_denominator) * self.song.signature_numerator * 64

    def _update_button_states(self):
        super(TransportComponent, self)._update_button_states()
        self.play_button.color = 'Transport.PlayOn' if self.song.is_playing else 'Transport.PlayOff'

    def _update_stop_button_color(self):
        self.stop_button.color = 'Transport.PlayOff' if self.song.is_playing else 'Transport.PlayOn'