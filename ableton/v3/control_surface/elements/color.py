# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v3\control_surface\elements\color.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from abc import ABC, abstractmethod
from typing import NamedTuple, Optional
from ...base import memoize, old_hasattr

@memoize
def create_rgb_color(values):
    pass
    return RgbColor(*values) if values is not None else None

class Color(ABC):
    pass

    @abstractmethod
    def draw(self, interface):
        return

    @property
    def midi_value(self):
        pass
        raise NotImplementedError

class SimpleColor(Color):
    pass

    def __init__(self, value, channel=None, *a, **k):
        super().__init__(*a, **k)
        self._value = value
        self._channel = channel

    @property
    def midi_value(self):
        return self._value

    def draw(self, interface):
        interface.send_value(self._value, channel=self._channel)

class RgbColor(Color):
    pass

    def __init__(self, *values, **k):
        super().__init__(**k)
        self._values = values

    @property
    def midi_value(self):
        raise AssertionError("RgbColor doesn't support a midi_value.")

    def draw(self, interface):
        interface.send_value(*self._values)

class ColorPart(NamedTuple):
    pass
    value: int
    channel: Optional[int] = None

class ComplexColor(Color):
    pass

    def __init__(self, color_parts, *a, **k):
        super().__init__(*a, **k)
        self._color_parts = color_parts

    @property
    def midi_value(self):
        raise AssertionError("ComplexColor doesn't support a midi_value.")

    def draw(self, interface):
        for part in self._color_parts:
            interface.send_value(part.value, channel=part.channel)

class FallbackColor(Color):
    pass

    def __init__(self, rgb_color, fallback_color, *a, **k):
        super().__init__(*a, **k)
        self._rgb_color = rgb_color
        self._fallback_color = fallback_color

    @property
    def midi_value(self):
        pass
        return self._rgb_color.midi_value

    def draw(self, interface):
        if old_hasattr(interface, 'is_rgb') and interface.is_rgb:
            self._rgb_color.draw(interface)
            return
        else:
            self._fallback_color.draw(interface)