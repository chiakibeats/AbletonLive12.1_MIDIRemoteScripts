# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\SliderElement.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from .EncoderElement import EncoderElement
from .InputControlElement import MIDI_NOTE_TYPE

class SliderElement(EncoderElement):
    pass

    def __init__(self, msg_type, channel, identifier, *a, **k):
        super(SliderElement, self).__init__(msg_type, channel, identifier, *a, map_mode=Live.MidiMap.MapMode.absolute, **k)