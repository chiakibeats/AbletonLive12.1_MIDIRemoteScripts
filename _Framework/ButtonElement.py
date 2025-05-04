# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_Framework\ButtonElement.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from .InputControlElement import MIDI_CC_TYPE, InputControlElement
from .Skin import Skin, SkinColorMissingError
from .Util import nop

class ButtonValue(object):
    pass
    midi_value = 0

    def __init__(self, midi_value=None, *a, **k):
        super(ButtonValue, self).__init__(*a, **k)
        if midi_value is not None:
            self.midi_value = midi_value

    def __int__(self):
        return self.midi_value

    def __eq__(self, other):
        try:
            return id(self) == id(other) or self.midi_value == other
        except NotImplementedError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __bool__(self):
        return self != OFF_VALUE
ON_VALUE = ButtonValue(127)
OFF_VALUE = ButtonValue(0)

class Color(ButtonValue):
    pass

    def draw(self, interface):
        pass
        interface.send_value(self.midi_value)

class DummyUndoStepHandler(object):

    def begin_undo_step(self):
        return

    def end_undo_step(self):
        return

class ButtonElementMixin(object):
    pass

    def set_light(self, is_turned_on):
        if is_turned_on:
            self.turn_on()
        else:
            self.turn_off()

    def turn_on(self):
        self.send_value(ON_VALUE)

    def turn_off(self):
        self.send_value(OFF_VALUE)

class ButtonElement(InputControlElement, ButtonElementMixin):
    pass

    class ProxiedInterface(InputControlElement.ProxiedInterface, ButtonElementMixin):
        is_momentary = nop
        is_pressed = nop

    def __init__(self, is_momentary, msg_type, channel, identifier, skin=Skin(), undo_step_handler=DummyUndoStepHandler(), *a, **k):
        super(ButtonElement, self).__init__(msg_type, channel, identifier, *a, **k)
        self.__is_momentary = bool(is_momentary)
        self._last_received_value = -1
        self._undo_step_handler = undo_step_handler
        self._skin = skin

    def is_momentary(self):
        pass
        return self.__is_momentary

    def message_map_mode(self):
        return Live.MidiMap.MapMode.absolute

    def is_pressed(self):
        return self.__is_momentary and int(self._last_received_value) > 0

    def set_light(self, value):
        self._set_skin_light(value)

    def _set_skin_light(self, value):
        try:
            color = self._skin[value]
            color.draw(self)
        except SkinColorMissingError:
            super(ButtonElement, self).set_light(value)

    def receive_value(self, value):
        pressed_before = self.is_pressed()
        self._last_received_value = value
        if not pressed_before and self.is_pressed():
            self._undo_step_handler.begin_undo_step()
        super(ButtonElement, self).receive_value(value)
        if not pressed_before or not self.is_pressed():
            self._undo_step_handler.end_undo_step()
            return

    def disconnect(self):
        super(ButtonElement, self).disconnect()
        self._undo_step_handler = None