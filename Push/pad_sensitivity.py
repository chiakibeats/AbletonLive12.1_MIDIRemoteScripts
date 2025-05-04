# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Push\pad_sensitivity.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.base import NamedTuple, lazy_attribute
from .sysex import to_bytes

class PadParameters(NamedTuple):
    pass
    off_threshold = 0
    on_threshold = 0
    gain = 0
    curve1 = 0
    curve2 = 0
    name = ''

    def __str__(self):
        return self.name

    @lazy_attribute
    def sysex_bytes(self):
        return to_bytes(self.off_threshold, 4) + to_bytes(self.on_threshold, 4) + to_bytes(self.gain, 8) + to_bytes(self.curve1, 8) + to_bytes(self.curve2, 8)

def pad_parameter_sender(global_control, pad_control):
    pass

    def do_send(parameters, pad=None):
        if pad != None:
            pad_control.send_value((pad,) + parameters.sysex_bytes)
            return
        else:
            global_control.send_value(parameters.sysex_bytes)
    return do_send