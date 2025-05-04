# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\encoder.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.base import clamp, listens, nop
from ableton.v3.control_surface.elements import EncoderElement as EncoderElementBase
from ableton.v3.control_surface.midi import SYSEX_END
from ableton.v3.live import find_parent_track, liveobj_valid, normalized_parameter_value
from .colors import COLOR_INDEX_TO_MOVE_INDEX, COLOR_TABLE, adjust_hsv_brightness, hex_to_hsv, rgb_to_move
from .midi import ENCODER_LED_HEADER
DEFAULT_LED_COLOR = hex_to_hsv(16777215)
pass
AUTOMATED_LED_COLOR = hex_to_hsv(16711680)
pass
DRY_WET_PARAMETER_NAMES = ('Dry/Wet', 'Dry Wet')
pass
MIN_PARAMETER_VALUE = 0.1
pass

class MoveEncoderElement(EncoderElementBase):
    pass

    def _set_sensitivity(self, use_fine_grain):
        super()._set_sensitivity(use_fine_grain or self._sensitivity_modifier.is_locked)

class ColoredEncoderElement(MoveEncoderElement):
    pass

    def __init__(self, identifier, *a, **k):
        super().__init__(identifier, *a, **k)
        self._base_led_color = DEFAULT_LED_COLOR
        self._track = None
        self._send_message_generator = lambda *values: ENCODER_LED_HEADER + (identifier,) + tuple(values) + (SYSEX_END,)
        self._do_send_value = nop
        self._has_soft_connection = True

    def reset(self):
        self._parameter_value_changed()

    def script_wants_forwarding(self):
        return super().script_wants_forwarding() or self._has_soft_connection

    def connect_to(self, parameter):
        self._has_soft_connection = False
        super().connect_to(parameter)

    def soft_connect_to(self, parameter):
        pass
        self._has_soft_connection = True
        self.mapped_object = parameter
        self._update_listeners_task.restart()

    def install_connections(self, *a, **k):
        pass
        if self._has_soft_connection:
            super().install_connections(nop, nop, a[-1])
            return
        else:
            super().install_connections(*a, **k)

    def is_mapped_manually(self):
        return False

    def _parameter_value_changed(self):
        r, g, b = (0, 0, 0)
        parameter = self.mapped_object
        if liveobj_valid(parameter):
            parameter_value = clamp(normalized_parameter_value(parameter), MIN_PARAMETER_VALUE, 1.0)
            r, g, b = adjust_hsv_brightness(*self._base_led_color, parameter_value)
        message = self._send_message_generator(*rgb_to_move(r, g, b))
        if message != self._last_sent_message:
            self.send_midi(message)
            self._last_sent_message = message
            return

    def _update_parameter_listeners(self):
        parameter = self.mapped_object
        self._track = None
        if liveobj_valid(parameter) and parameter.name in DRY_WET_PARAMETER_NAMES:
            self._track = find_parent_track(parameter)
        self.__on_track_color_index_changed.subject = self._track
        self.__on_automation_state_changed.subject = parameter
        self._update_base_led_color()
        super()._update_parameter_listeners()

    def _update_base_led_color(self):
        parameter = self.mapped_object
        self._base_led_color = DEFAULT_LED_COLOR
        if liveobj_valid(parameter):
            if parameter.automation_state == 1:
                self._base_led_color = AUTOMATED_LED_COLOR
            elif liveobj_valid(self._track) and parameter.name in DRY_WET_PARAMETER_NAMES:
                move_index = COLOR_INDEX_TO_MOVE_INDEX[self._track.color_index or 0]
                self._base_led_color = hex_to_hsv(COLOR_TABLE[move_index][1])
        self._parameter_value_changed()

    @listens('automation_state')
    def __on_automation_state_changed(self):
        self._update_base_led_color()

    @listens('color_index')
    def __on_track_color_index_changed(self):
        self._update_base_led_color()