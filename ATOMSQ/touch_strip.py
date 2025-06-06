# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ATOMSQ\touch_strip.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

import math
from functools import partial
from itertools import chain, repeat
from ableton.v3.base import listens
from ableton.v3.control_surface.elements import EncoderElement

class TouchStripElement(EncoderElement):

    def __init__(self, leds=None, *a, **k):
        self.map_value_to_led_states = partial(map_value_to_led_states, 127, 0, len(leds))
        super().__init__(0, *a, **k)
        self._leds = leds

    def connect_to(self, parameter):
        super().connect_to(parameter)
        self._update_feedback_leds(force=True)
        self.__on_parameter_value.subject = self.mapped_parameter()

    def release_parameter(self):
        super().release_parameter()
        self.__on_parameter_value.subject = None

    @listens('value')
    def __on_parameter_value(self):
        self._update_feedback_leds()

    def _update_feedback_leds(self, force=False):
        for led, state in zip(self._leds, self.map_value_to_led_states(self._parameter_to_map_to.value)):
            led.send_value(state, force)

def map_value_to_led_states(on, off, num_leds, value):
    pass
    mid_index = int(math.floor(num_leds / 2))
    active_length = mid_index + 1
    active_led_states = list(map(lambda i: on if i / active_length <= abs(value) else off, map(float, range(active_length))))
    inactive_led_states = repeat(0, num_leds - active_length)
    return chain(reversed(active_led_states), inactive_led_states) if value < 0 else chain(inactive_led_states, active_led_states)