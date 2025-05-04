# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\transport.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.control import ButtonControl
from novation.transport import TransportComponent as TransportComponentBase

class TransportComponent(TransportComponentBase):
    alt_stop_button = ButtonControl()

    @alt_stop_button.pressed
    def alt_stop_button(self, _):
        self.song.is_playing = False

    def _toggle_playback(self, toggle_on):
        self.song.is_playing = toggle_on