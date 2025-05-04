# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\firmware.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from enum import IntEnum
from ableton.v3.base import depends, listenable_property
from ableton.v3.control_surface import Component
from ableton.v3.control_surface.controls import ButtonControl, InputControl
from ableton.v3.control_surface.display import Renderable
from . import midi
CHARGING_STATE_MAP = {1: 'Charging', 2: 'Charged', 4: 'Unable to charge', 6: 'Low USB power'}
pass
DEFAULT_CHARGING_STATE = 'Battery'
pass
UNNOTEWORTHY_CHARGING_STATES = ('Charging', 'Charged')
pass

class PowerStatusBitMasks(IntEnum):
    pass
    charging_state = 7
    short_press_event = 8
    battery_low_alarm = 64

class ShutDownState(IntEnum):
    pass
    none = 0
    requested = 1
    in_progress = 2

class LedBrightness(IntEnum):
    pass
    low = 25
    mid = 55
    high = 126
    max = 127

class FirmwareComponent(Component, Renderable):
    pass
    confirm_shut_down_button = ButtonControl(color=None)
    cancel_shut_down_button = ButtonControl(color='DefaultButton.Back')
    power_state_control = InputControl()
    control_mode_control = InputControl()
    led_brightness_control = InputControl()
    battery_level = listenable_property.managed(0)
    charging_state = listenable_property.managed(None)
    shut_down_state = listenable_property.managed(ShutDownState.none)
    in_control_surface_mode = listenable_property.managed(False)
    led_brightness = listenable_property.managed(LedBrightness.mid)

    @depends(send_midi=None)
    def __init__(self, send_midi=None, *a, **k):
        super().__init__(*a, name='Firmware', **k)
        self._send_midi = send_midi
        self._has_shown_low_power_notification = False
        self.reset()

    def reset(self):
        pass
        self._cancel_shut_down()
        self.charging_state = None

    def initialize(self):
        pass
        self.reset()
        self._send_midi(midi.make_wake_up_display_message())
        self._send_midi(midi.make_set_poly_aftertouch_mode())
        self._send_midi(midi.make_power_state_message())
        self._send_midi(midi.make_get_led_brightness_message())

    def switch_to_standalone(self):
        pass
        self._send_midi(midi.make_set_control_mode_message())

    def set_led_brightness_index(self, index):
        pass
        self.led_brightness = list(LedBrightness)[index]
        self._send_midi(midi.make_set_led_brightness_message(self.led_brightness.value))

    @control_mode_control.value
    def control_mode_control(self, value, _):
        self.in_control_surface_mode = value[0] == midi.ControlMode.control_surface

    @power_state_control.value
    def power_state_value(self, value, _):
        self.battery_level = value[1]
        self._update_shut_down_state(value[0])
        self._update_charging_state(value[0])

    @led_brightness_control.value
    def led_brightness_control(self, value, _):
        if value[0] in iter(LedBrightness):
            self.led_brightness = LedBrightness(value[0])
            return
        else:
            self._round_up_to_nearest_led_brightness(value[0])

    def _round_up_to_nearest_led_brightness(self, received_value):
        for index, value in enumerate(LedBrightness):
            if received_value < value:
                self.set_led_brightness_index(index)
            else:
                continue

    @confirm_shut_down_button.pressed
    def confirm_shut_down_button(self, _):
        self.shut_down_state = ShutDownState.in_progress
        self._do_shut_down()

    @cancel_shut_down_button.pressed
    def cancel_shut_down_button(self, _):
        self._cancel_shut_down()

    def _update_shut_down_state(self, state):
        if self.shut_down_state != ShutDownState.in_progress:
            self.shut_down_state = ShutDownState.requested if midi.bit_is_set(state, PowerStatusBitMasks.short_press_event) else ShutDownState.none

    def _update_charging_state(self, state):

        def show_notification(header):
            self.notify(self.notifications.generic, '{}\n{}%'.format(header, self.battery_level))
        current_charging_state = CHARGING_STATE_MAP.get(state & PowerStatusBitMasks.charging_state, DEFAULT_CHARGING_STATE)
        if self._should_show_low_power_notification(state):
            show_notification('Low Battery')
        elif self._should_show_charging_state_notification(current_charging_state):
            show_notification(current_charging_state)
        self.charging_state = current_charging_state

    def _should_show_low_power_notification(self, state):
        has_low_power = midi.bit_is_set(state, PowerStatusBitMasks.battery_low_alarm)
        if has_low_power and (not self._has_shown_low_power_notification):
            self._has_shown_low_power_notification = has_low_power
            return True
        else:
            return False

    def _should_show_charging_state_notification(self, current_charging_state):
        if self.charging_state is None:
            return False
        elif self.charging_state in UNNOTEWORTHY_CHARGING_STATES or current_charging_state in UNNOTEWORTHY_CHARGING_STATES:
            return False
        else:
            return self.charging_state != current_charging_state

    def _do_shut_down(self):
        self._send_midi(midi.make_shut_down_message())

    def _cancel_shut_down(self):
        self.shut_down_state = ShutDownState.none
        self._send_midi(midi.make_clear_power_button_event_message())