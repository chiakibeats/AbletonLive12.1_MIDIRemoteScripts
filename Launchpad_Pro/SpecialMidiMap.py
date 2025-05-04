# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_Pro\SpecialMidiMap.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.Dependency import depends
from _Framework.MidiMap import MidiMap
from _Framework.Resource import PrioritizedResource
from .ConfigurableButtonElement import ConfigurableButtonElement
from .consts import USER_MODE_CHANNELS
from .MultiButtonElement import MultiButtonElement
from .SliderElement import SliderElement
USER_LAYOUT_START_CHANNEL = 5
NUM_USER_LAYOUT_CHANNELS = 3

@depends(skin=None)
pass
def make_button(name, channel, number, midi_message_type, skin=None, default_states=None, **k):
    return ConfigurableButtonElement(True, midi_message_type, channel, number, name=name, skin=skin, default_states=default_states, **k)

@depends(skin=None)
pass
def make_multi_button(name, channel, number, midi_message_type, skin=None, default_states=None, **k):
    pass
    is_momentary = True
    return MultiButtonElement(USER_MODE_CHANNELS, is_momentary, midi_message_type, channel, number, name=name, skin=skin, default_states=default_states, **k)

@depends(skin=None)
def make_slider(name, channel, number, midi_message_type, skin=None):
    slider = SliderElement(midi_message_type, channel, number, name=name, skin=skin)
    return slider

class SpecialMidiMap(MidiMap):
    def add_button(self, name, channel, number, midi_message_type, default_states=None, element_factory=make_button, **k):
        self[name] = element_factory(name, channel, number, midi_message_type, default_states=default_states, **k)

    def add_matrix(self, name, element_factory, channel, numbers, midi_message_type):
        def one_dimensional_name(base_name, x, _y):
            return '%s_%d' % (base_name, x)

        def two_dimensional_name(base_name, x, y):
            return '%s_%d_%d' % (base_name, x, y)
        name_factory = two_dimensional_name if len(numbers) > 1 else one_dimensional_name
        elements = []
        id_dict = {}
        for row, identifiers in enumerate(numbers):
            element_row = []
            for column, identifier in enumerate(identifiers):
                element_row.append(element_factory(name_factory(name, column, row), channel, identifier, midi_message_type))
                id_dict[identifier] = (column, row)
            elements.append(element_row)
            continue
        self['%s_Raw' % name] = elements
        self['%s_Ids' % name] = id_dict
        self[name] = ButtonMatrixElement(rows=elements, name=name)

    def add_modifier_button(self, name, channel, number, midi_message_type, default_states=None, element_factory=make_button):
        self.add_button(name, channel, number, midi_message_type, default_states=default_states, element_factory=element_factory, resource_type=PrioritizedResource)