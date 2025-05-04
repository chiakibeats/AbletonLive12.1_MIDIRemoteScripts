# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchpad_MK2\ControlElementUtils.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ButtonElement import ButtonElement
from _Framework.ComboElement import ComboElement
from _Framework.ComboElement import MultiElement as MultiElementBase
from _Framework.Dependency import depends
from _Framework.InputControlElement import MIDI_NOTE_TYPE
from _Framework.Resource import PrioritizedResource

@depends(skin=None)
def make_button(identifier, channel, name, msg_type=MIDI_NOTE_TYPE, skin=None, is_modifier=False):
    return ButtonElement(True, msg_type, channel, identifier, skin=skin, name=name, resource_type=PrioritizedResource if is_modifier else None)

def with_modifier(modifier, button):
    return ComboElement(button, modifiers=[modifier])

class MultiElement(MultiElementBase):

    def __init__(self, *a, **k):
        super(MultiElement, self).__init__(*a, **k)
        self._is_pressed = False

    def is_pressed(self):
        return self._is_pressed

    def on_nested_control_element_value(self, value, control):
        self._is_pressed = bool(value)
        super(MultiElement, self).on_nested_control_element_value(value, control)

class FilteringMultiElement(MultiElement):

    def __init__(self, controls, feedback_channels=None, **k):
        super(MultiElement, self).__init__(*controls, **k)
        self._feedback_channels = feedback_channels

    def send_value(self, value):
        for control in self.owned_control_elements():
            if control.message_channel() in self._feedback_channels:
                control.send_value(value)
            continue

    def set_light(self, value):
        for control in self.owned_control_elements():
            if control.message_channel() in self._feedback_channels:
                control.set_light(value)
            continue