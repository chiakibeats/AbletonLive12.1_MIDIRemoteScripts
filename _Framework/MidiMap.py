# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\MidiMap.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from .ButtonElement import ButtonElement
from .ButtonMatrixElement import ButtonMatrixElement
from .EncoderElement import EncoderElement
from .SliderElement import SliderElement

def make_button(name, channel, number, midi_message_type):
    is_momentary = True
    return ButtonElement(not is_momentary, midi_message_type, channel, number, name=name)

def make_slider(name, channel, number, midi_message_type):
    return SliderElement(midi_message_type, channel, number, name=name)

def make_encoder(name, channel, number, midi_message_type):
    return EncoderElement(midi_message_type, channel, number, Live.MidiMap.MapMode.absolute, name=name)

class MidiMap(dict):

    def add_button(self, name, channel, number, midi_message_type):
        self[name] = make_button(name, channel, number, midi_message_type)

    def add_matrix(self, name, element_factory, channel, numbers, midi_message_type):

        def one_dimensional_name(base_name, x, _y):
            return '%s[%d]' % (base_name, x)

        def two_dimensional_name(base_name, x, y):
            return '%s[%d,%d]' % (base_name, x, y)
        name_factory = two_dimensional_name if len(numbers) > 1 else one_dimensional_name
        elements = [element_factory(name_factory(name, column, row), channel, identifier, midi_message_type) for row, identifiers in enumerate(identifiers)]
        self[name] = ButtonMatrixElement(rows=elements)