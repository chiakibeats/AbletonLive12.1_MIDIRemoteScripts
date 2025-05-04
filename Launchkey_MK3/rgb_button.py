# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\rgb_button.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.elements import ButtonElement

class RgbButtonElement(ButtonElement):
    pass

    def __init__(self, *a, **k):
        self._led_channel = k.pop('led_channel', 0)
        super(RgbButtonElement, self).__init__(*a, **k)

    def _do_send_value(self, value, channel=None):
        super(RgbButtonElement, self)._do_send_value(value, channel=self._led_channel)