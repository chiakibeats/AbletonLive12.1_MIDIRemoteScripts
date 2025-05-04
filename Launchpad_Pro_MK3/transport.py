# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro_MK3\transport.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from novation.blinking_button import BlinkingButtonControl
from novation.transport import TransportComponent as TransportComponentBase

class TransportComponent(TransportComponentBase):
    capture_midi_button = BlinkingButtonControl(color='Transport.CaptureOff', blink_on_color='Transport.CaptureOn', blink_off_color='Transport.CaptureOff')

    @capture_midi_button.pressed
    def capture_midi_button(self, _):
        try:
            if self.song.can_capture_midi:
                self.song.capture_midi()
                self.capture_midi_button.start_blinking()
        except RuntimeError:
            return None