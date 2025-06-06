# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\AIRA_MX_1\ControlElementUtils.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:24:29 UTC (1744269869)

import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.ComboElement import ComboElement
from _Framework.Dependency import depends
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import MIDI_CC_TYPE, MIDI_NOTE_TYPE
from _Framework.Resource import PrioritizedResource

@depends(skin=None)
def make_button(name, identifier, channel=0, msg_type=MIDI_NOTE_TYPE, is_momentary=True, is_modifier=False, skin=None):
    return ButtonElement(is_momentary, msg_type, channel, identifier, name=name, resource_type=PrioritizedResource if is_modifier else None, skin=skin)

def make_encoder(name, identifier, channel=0):
    return EncoderElement(MIDI_CC_TYPE, channel, identifier, Live.MidiMap.MapMode.absolute, name=name)

def with_modifier(control, modifier):
    return ComboElement(control, modifiers=[modifier], name=control.name + '_With_Modifier')