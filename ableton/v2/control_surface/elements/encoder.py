# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ableton\v2\control_surface\elements\encoder.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from past.utils import old_div
import Live
from ...base import Event, clamp, const, in_range, listens, nop
from .. import midi
from ..compound_element import CompoundElement
from ..input_control_element import MIDI_CC_TYPE, InputControlElement, InputSignal
from .combo import WrapperElement
_map_modes = map_modes = Live.MidiMap.MapMode
ABSOLUTE_MAP_MODES = (_map_modes.absolute, _map_modes.absolute_14_bit)

def _not_implemented(value):
    raise NotImplementedError

def signed_bit_delta(value):
    delta = SIGNED_BIT_DEFAULT_DELTA
    is_increment = value <= 64
    index = value - 1 if is_increment else value - 64
    if in_range(index, 0, len(SIGNED_BIT_VALUE_MAP)):
        delta = SIGNED_BIT_VALUE_MAP[index]
    return delta if is_increment else -delta
SIGNED_BIT_DEFAULT_DELTA = 20.0
SIGNED_BIT_VALUE_MAP = (1, 2, 3, 4, 5, 8, 10, 20, 50)

def normalize_two_compliment(value):
    return value if value <= 64 else value - 128
ENCODER_VALUE_NORMALIZER = {_map_modes.relative_two_compliment: normalize_two_compliment, _map_modes.relative_smooth_two_compliment: normalize_two_compliment, _map_modes.relative_smooth_signed_bit: lambda v: v if v <= 64 else 64 - v, _map_modes.relative_smooth_binary_offset: lambda v: v - 64, _map_modes.relative_signed_bit: signed_bit_delta}
MAX_14_BIT_CC = 95

def accumulate_relative_two_compliment_chunk(chunk):
    right = 0
    left = 0
    for value in chunk:
        if value <= 64:
            right += value
            continue
        else:
            left += 128 - value
            continue
    result = clamp(right - left, -63, 64)
    return result if result >= 0 else 128 + result
ENCODER_VALUE_ACCUMULATOR = {_map_modes.relative_smooth_two_compliment: accumulate_relative_two_compliment_chunk}

class EncoderElement(InputControlElement):
    pass

    class ProxiedInterface(InputControlElement.ProxiedInterface):
        normalize_value = nop
    __events__ = (Event(name='normalized_value', signal=InputSignal),)
    encoder_sensitivity = 1.0
    allow_receiving_chunks = True
    pass

    def __init__(self, msg_type, channel, identifier, map_mode, encoder_sensitivity=None, *a, **k):
        super(EncoderElement, self).__init__(msg_type, channel, identifier, *a, **k)
        if encoder_sensitivity is not None:
            self.encoder_sensitivity = encoder_sensitivity
        if map_mode is _map_modes.absolute_14_bit and identifier > MAX_14_BIT_CC:
            self._map_mode = _map_modes.absolute
        else:
            self._map_mode = map_mode
        self._last_received_value = None
        self._value_normalizer = ENCODER_VALUE_NORMALIZER.get(map_mode, _not_implemented)
        self._value_accumulator = ENCODER_VALUE_ACCUMULATOR.get(map_mode, None)
        self._half_value_range = self._max_value / 2

    def message_map_mode(self):
        return self._map_mode

    def receive_value(self, value):
        super().receive_value(value)
        self._last_received_value = value

    def relative_value_to_delta(self, value):
        if self._map_mode in ABSOLUTE_MAP_MODES:
            if self._last_received_value is not None:
                return value - self._last_received_value
            else:
                return 0
        else:
            return self._value_normalizer(value)

    def normalize_value(self, value):
        return old_div(self.relative_value_to_delta(value), self._half_value_range) * self.encoder_sensitivity

    def notify_value(self, value):
        super(EncoderElement, self).notify_value(value)
        if self.normalized_value_listener_count():
            self.notify_normalized_value(self.normalize_value(value))

    def receive_chunk(self, chunk):
        if self._value_accumulator is not None:
            value = self._value_accumulator(chunk)
            if value != 0:
                self.receive_value(value)
            else:
                return None
        else:
            super(EncoderElement, self).receive_chunk(chunk)

class TouchEncoderElementBase(EncoderElement):
    pass

    class ProxiedInterface(EncoderElement.ProxiedInterface):
        is_pressed = const(False)
        touch_element = const(None)
    __events__ = ('touch_value',)

    @property
    def touch_element(self):
        raise NotImplementedError

    def is_pressed(self):
        raise NotImplementedError

class TouchEncoderElement(CompoundElement, TouchEncoderElementBase):
    pass

    def __init__(self, msg_type=MIDI_CC_TYPE, channel=0, identifier=0, map_mode=_map_modes.absolute, touch_element=None, *a, **k):
        super(TouchEncoderElement, self).__init__(*a, msg_type=msg_type, channel=channel, identifier=identifier, map_mode=map_mode, control_elements=None, **k)
        self._touch_element = self.register_control_element(touch_element)
        self.request_listen_nested_control_elements()

    def on_nested_control_element_value(self, value, control):
        self.notify_touch_value(value)

    @property
    def touch_element(self):
        return self._touch_element if self.owns_control_element(self._touch_element) else None

    def is_pressed(self):
        return self.owns_control_element(self._touch_element) and self._touch_element.is_pressed()

    def on_nested_control_element_received(self, control):
        return

    def on_nested_control_element_lost(self, control):
        return

class FineGrainWithModifierEncoderElement(WrapperElement):
    pass
    pass
    pass
    pass

    def __init__(self, encoder=None, modifier=None, modified_sensitivity=0.1, default_sensitivity=None, *a, **k):
        super(FineGrainWithModifierEncoderElement, self).__init__(*a, wrapped_control=encoder, **k)
        self._normalized_value_listeners = []
        self._modified_sensitivity = modified_sensitivity
        self._default_sensitivity = default_sensitivity or self.wrapped_control.mapping_sensitivity
        self._modifier = modifier
        self.register_control_elements(modifier, encoder)
        self.__on_modifier_value.subject = self._modifier

    def add_normalized_value_listener(self, listener):
        self._normalized_value_listeners.append(listener)
        if len(self._normalized_value_listeners) == 1:
            self._enforce_control_invariant()

    def remove_normalized_value_listener(self, listener):
        self._normalized_value_listeners.remove(listener)
        if len(self._normalized_value_listeners) == 0:
            self._enforce_control_invariant()

    def normalized_value_has_listener(self, listener):
        return listener in self._normalized_value_listeners

    @listens('normalized_value')
    def __on_normalized_value(self, value):
        for listener in self._normalized_value_listeners:
            listener(value)

    @listens('value')
    def __on_modifier_value(self, value):
        if self.owns_control_element(self._modifier):
            self.on_nested_control_element_value(value, self._modifier)

    def on_nested_control_element_received(self, control):
        super(FineGrainWithModifierEncoderElement, self).on_nested_control_element_received(control)
        self._enforce_control_invariant()

    def on_nested_control_element_lost(self, control):
        super(FineGrainWithModifierEncoderElement, self).on_nested_control_element_lost(control)
        self._enforce_control_invariant()

    def on_nested_control_element_value(self, value, control):
        if control == self._modifier:
            self._enforce_control_invariant()
            return
        else:
            super(FineGrainWithModifierEncoderElement, self).on_nested_control_element_value(value, control)

    def _enforce_control_invariant(self):
        if self.owns_control_element(self._wrapped_control):
            if self._modifier.is_pressed():
                self.wrapped_control.mapping_sensitivity = self._modified_sensitivity
            else:
                self.wrapped_control.mapping_sensitivity = self._default_sensitivity
        should_listen = self.owns_control_element(self._wrapped_control) and len(self._normalized_value_listeners) > 0
        self.__on_normalized_value.subject = self._wrapped_control if should_listen else None

    def set_sensitivities(self, default, modified):
        self._default_sensitivity = default
        self._modified_sensitivity = modified
        self._enforce_control_invariant()