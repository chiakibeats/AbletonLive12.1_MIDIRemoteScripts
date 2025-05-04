# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\multi_button.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.elements import ButtonElement

class MultiButtonElement(ButtonElement):
    pass

    def __init__(self, *a, **k):
        self._secondary_button = SecondaryButtonElement(self, k.pop('secondary_identifier'), **k)
        super().__init__(*a, is_private=True, **k)

    def send_value(self, value, force=False, channel=None):
        super().send_value(value, force=force, channel=channel)
        self._secondary_button.send_value(value, force=force, channel=channel)

class SecondaryButtonElement(ButtonElement):
    pass

    def __init__(self, parent, *a, **k):
        super().__init__(*a, is_private=True, **k)
        self._parent = parent

    def receive_value(self, value):
        super().receive_value(value)
        self._parent.receive_value(value)

    def script_wants_forwarding(self):
        return True