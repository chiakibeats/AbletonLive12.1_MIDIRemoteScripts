# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\SL_MkIII\transport.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.components import TransportComponent as TransportComponentBase

class TransportComponent(TransportComponentBase):

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._loop_toggle.view_transform = lambda v: 'Transport.LoopOn' if v else 'Transport.LoopOff'
        self._record_toggle.view_transform = lambda v: 'Recording.On' if v else 'Recording.Off'

    def set_seek_forward_button(self, ffwd_button):
        super().set_seek_forward_button(ffwd_button)
        self._update_seek_button(self._ffwd_button)

    def set_seek_backward_button(self, rwd_button):
        super().set_seek_backward_button(rwd_button)
        self._update_seek_button(self._rwd_button)

    def _ffwd_value(self, value):
        super()._ffwd_value(value)
        self._update_seek_button(self._ffwd_button)

    def _rwd_value(self, value):
        super()._rwd_value(value)
        self._update_seek_button(self._rwd_button)

    def _update_button_states(self):
        super()._update_button_states()
        self._update_continue_playing_button()

    def _update_continue_playing_button(self):
        self.continue_playing_button.color = 'Transport.PlayOn' if self.song.is_playing else 'Transport.PlayOff'

    def _update_seek_button(self, button):
        if self.is_enabled() and button is not None:
            button.set_light('Transport.SeekOn' if button.is_pressed() else 'Transport.SeekOff')

    def _update_stop_button_color(self):
        self.stop_button.color = 'Transport.StopEnabled' if self.play_button.is_toggled else 'Transport.StopDisabled'