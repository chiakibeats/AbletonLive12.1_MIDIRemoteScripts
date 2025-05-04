# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Code_Series\element_utils.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from ableton.v2.base import depends
from ableton.v2.control_surface import MIDI_CC_TYPE, MIDI_NOTE_TYPE, MIDI_PB_TYPE
from ableton.v2.control_surface.elements import ButtonElement, EncoderElement, SliderElement
IS_MOMENTARY = True
CHANNEL = 0

@depends(skin=None)
def make_button(identifier, name, **k):
    return ButtonElement(IS_MOMENTARY, MIDI_NOTE_TYPE, CHANNEL, identifier, name=name, **k)

def make_slider(channel, name):
    return SliderElement(MIDI_PB_TYPE, channel, 0, name=name)

def make_encoder(identifier, name):
    return EncoderElement(MIDI_CC_TYPE, 0, identifier, Live.MidiMap.MapMode.relative_smooth_signed_bit, name=name)