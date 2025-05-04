# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Alesis_VI\Alesis_VI.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from _Framework.ButtonElement import ButtonElement
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.Layer import Layer
from _Framework.MidiMap import MidiMap as MidiMapBase
from _Framework.MidiMap import make_encoder
from _Framework.MixerComponent import MixerComponent
from _Framework.TransportComponent import TransportComponent

class MidiMap(MidiMapBase):

    def __init__(self, *a, **k):
        super(MidiMap, self).__init__(*a, **k)
        self.add_momentary_button('Stop', 0, 118, MIDI_CC_TYPE)
        self.add_momentary_button('Play', 0, 119, MIDI_CC_TYPE)
        self.add_momentary_button('Loop', 0, 115, MIDI_CC_TYPE)
        self.add_momentary_button('Record', 0, 114, MIDI_CC_TYPE)
        self.add_momentary_button('Forward', 0, 117, MIDI_CC_TYPE)
        self.add_momentary_button('Backward', 0, 116, MIDI_CC_TYPE)
        self.add_matrix('Volume_Encoders', make_encoder, 0, [list(range(20, 32)) + [35, 41, 46, 47]], MIDI_CC_TYPE)

    def add_momentary_button(self, name, channel, number, midi_message_type):
        self[name] = ButtonElement(True, midi_message_type, channel, number, name=name)

class Alesis_VI(ControlSurface):

    def __init__(self, *a, **k):
        pass