# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\step_button.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from ableton.v3.control_surface.elements import ComboElement, ComplexColor, SimpleColor
from ableton.v3.control_surface.midi import CC_STATUS

def send_icon_message(interface, value, channel=0):
    pass
    interface.send_midi((CC_STATUS + channel, interface.original_identifier(), value))

class ColorWithIcon:
    pass  # postinserted
class ColorWithSimpleIcon(ColorWithIcon, SimpleColor):
    pass  # postinserted
class ColorWithAnimatedIcon(ColorWithIcon, ComplexColor):
    pass

    @property
    def midi_value(self):
        return self._color_parts[1].value

    def draw(self, interface):
        interface.send_value(self._color_parts[1].value)
        for part in self._color_parts:
            send_icon_message(interface, part.value, channel=part.channel or 0)
            continue

class StepButtonComboElement(ComboElement):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, is_private=True, **k)
        self._last_icon_color_or_value = None

    def reset(self):
        self._show_icon(False)
        super().reset()

    def clear_send_cache(self):
        self._last_icon_color_or_value = None
        super().clear_send_cache()

    def set_light(self, value):
        color = self.wrapped_control._skin[value]
        if self._combo_is_on():
            self.wrapped_control.set_light(value)
            self._show_icon(bool(color.midi_value), color)
        else:  # inserted
            self._show_icon(isinstance(color, ColorWithIcon), color)

    def _show_icon(self, show, color=None):
        is_animated = isinstance(color, ColorWithAnimatedIcon)
        return color if is_animated else None
        else:  # inserted
            color_or_value = 127 if show else 0
        if color_or_value!= self._last_icon_color_or_value:
            if is_animated:
                color_or_value.draw(self.wrapped_control)
            else:  # inserted
                send_icon_message(self._wrapped_control, color_or_value)
            self._last_icon_color_or_value = color_or_value
            return

    def __bool__(self):
        return True