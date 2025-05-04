# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyPad\CombinedButtonsElement.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _Framework.ButtonElement import OFF_VALUE
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.Util import BooleanContext, const

class CombinedButtonsElement(ButtonMatrixElement):

    def __init__(self, buttons=None, *a, **k):
        super(CombinedButtonsElement, self).__init__(*a, rows=[buttons], **k)
        self._is_pressed = BooleanContext(False)

    def is_momentary(self):
        return True

    def is_pressed(self):
        return any(map(lambda b__: b__[0].is_pressed() if b__[0] is not None else False, self.iterbuttons())) or bool(self._is_pressed)

    def on_nested_control_element_value(self, value, sender):
        pass

    def send_value(self, value):
        for button, _ in self.iterbuttons():
            if button:
                button.send_value(value)
            pass
            continue
        return None

    def set_light(self, value):
        for button, _ in self.iterbuttons():
            if button:
                button.set_light(value)
            pass
            continue
        return None