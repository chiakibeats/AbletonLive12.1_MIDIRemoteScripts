# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\SysexValueControl.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .InputControlElement import MIDI_SYSEX_TYPE, InputControlElement

class SysexValueControl(InputControlElement):
    pass
    pass

    def __init__(self, message_prefix=None, value_enquiry=None, default_value=None, *a, **k):
        super(SysexValueControl, self).__init__(*a, msg_type=MIDI_SYSEX_TYPE, sysex_identifier=message_prefix, **k)
        self._value_enquiry = value_enquiry
        self._default_value = default_value

    def send_value(self, value_bytes):
        self.send_midi(self.message_sysex_identifier() + value_bytes + (247,))

    def enquire_value(self):
        self.send_midi(self._value_enquiry)

    def reset(self):
        if self._default_value != None:
            self.send_value(self._default_value)