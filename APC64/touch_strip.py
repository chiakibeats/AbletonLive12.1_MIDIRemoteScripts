# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\touch_strip.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from enum import Enum
from ableton.v3.base import clamp, listens, nop
from ableton.v3.control_surface.elements import EncoderElement, TouchElement
from ableton.v3.control_surface.midi import CC_STATUS
from ableton.v3.live import find_parent_track, is_parameter_bipolar, is_parameter_quantized, liveobj_valid, parameter_value_to_midi_value
from .colors import make_color_for_liveobj
FINE_TUNE_FACTOR = 65536

class TouchStripTouchElement(TouchElement):
    pass

    def receive_value(self, value):
        super().receive_value(value)
        self._encoder.on_touch_strip_touched_or_released(value != 0)

class LedStyle(Enum):
    pass
    off = 0
    default = 1
    bipolar = 3

class TouchStripElement(EncoderElement):
    pass

    def __init__(self, *a, **k):
        super().__init__(*a, feedback_delay=-1, send_should_depend_on_forwarding=False, **k)
        self._track = None
        self._led_style_cc = self.message_channel() + 104
        self._led_color_cc = self.message_channel() + 112
        self._is_touched = False
        self._can_fine_tune_parameter = False

        def patched_request_rebuild(request_fn):

            def inner():
                parameter = self.mapped_object
                self._can_fine_tune_parameter = liveobj_valid(parameter) and (not is_parameter_quantized(parameter, parameter.canonical_parent))
                request_fn()
            return inner
        self._request_rebuild = patched_request_rebuild(self._request_rebuild)

    def reset(self):
        self._send_led_style_value(LedStyle.off.value)

    def script_wants_forwarding(self):
        return super().script_wants_forwarding() or (self._can_fine_tune_parameter and (self._sensitivity_modifier.is_pressed or self._is_touched))

    def install_connections(self, *a, **k):
        pass
        if self._can_fine_tune_parameter and self._sensitivity_modifier.is_pressed:
            super().install_connections(nop, nop, a[-1])
        else:
            super().install_connections(*a, **k)
        self._last_received_value = None

    def on_touch_strip_touched_or_released(self, is_touched):
        self._is_touched = is_touched
        self._last_received_value = None

    def receive_value(self, value):
        parameter = self.mapped_object
        if self._last_received_value is not None and liveobj_valid(parameter):
            diff = value - self._last_received_value
            step_size = (parameter.max - parameter.min) / FINE_TUNE_FACTOR
            parameter.value = clamp(parameter.value + diff * step_size, parameter.min, parameter.max)
        self._last_received_value = value
        self.notify_value(value)

    def _update_parameter_listeners(self):
        self._track = None
        if self.is_mapped_to_parameter():
            self._track = find_parent_track(self.mapped_object)
        self.__on_automation_state_changed.subject = self.mapped_object
        self.__on_track_color_index_changed.subject = self._track
        self.__on_automation_state_changed()
        self.__on_track_color_index_changed()
        super()._update_parameter_listeners()

    def _parameter_value_changed(self):
        self.send_value(parameter_value_to_midi_value(self.mapped_object, max_value=self._max_value))

    def _send_led_style_value(self, style_value):
        self.send_midi((CC_STATUS, self._led_style_cc, style_value))

    def _get_led_style_value(self):
        style_value = LedStyle.off.value
        if self.is_mapped_to_parameter():
            style_value = LedStyle.bipolar.value if is_parameter_bipolar(self.mapped_object) else LedStyle.default.value
            if self.mapped_object.automation_state == 1:
                style_value += 1
        return style_value

    @listens('color_index')
    def __on_track_color_index_changed(self):
        self.send_midi((CC_STATUS, self._led_color_cc, make_color_for_liveobj(self._track).midi_value))

    @listens('automation_state')
    def __on_automation_state_changed(self):
        self._send_led_style_value(self._get_led_style_value())