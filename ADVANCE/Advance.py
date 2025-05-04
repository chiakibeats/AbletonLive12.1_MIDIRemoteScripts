# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ADVANCE\Advance.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ControlSurface import ControlSurface
from _Framework.DeviceComponent import DeviceComponent
from _Framework.DrumRackComponent import DrumRackComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.Layer import Layer
from _Framework.TransportComponent import TransportComponent
PAD_CHANNEL = 1
PAD_IDS = ((81, 83, 84, 86), (74, 76, 77, 79), (67, 69, 71, 72), (60, 62, 64, 65))

def make_encoder(identifier, name):
    return EncoderElement(MIDI_CC_TYPE, 0, identifier, Live.MidiMap.MapMode.absolute, name=name)

def make_button(identifier, name, msg_type=MIDI_NOTE_TYPE, channel=PAD_CHANNEL):
    return ButtonElement(True, msg_type, channel, identifier, name=name)

class Advance(ControlSurface):

    def __init__(self, *a, **k):
        pass