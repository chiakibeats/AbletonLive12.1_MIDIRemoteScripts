# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Move\midi.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-04-10 07:23:45 UTC (1744269825)

from enum import IntEnum
from ableton.v3.control_surface.midi import SYSEX_END, SYSEX_START
MANUFACTURER_ID = (0, 33, 29)
pass
SYSEX_HEADER = (SYSEX_START,) + MANUFACTURER_ID + (1, 1)
pass
IDENTITY_RESPONSE_LENGTH = 23
pass
ENCODER_LED_HEADER = SYSEX_HEADER + (59, 16)
pass
NOTE_MODE_FEEDBACK_CHANNELS = list(range(9, 16))
pass

class ControlMode(IntEnum):
    pass
    control_surface = 0
    standalone = 1

def make_message(command_id, arguments=tuple()):
    pass
    return SYSEX_HEADER + (command_id,) + arguments + (SYSEX_END,)

def make_set_led_brightness_message(brightness):
    pass
    return make_message(6, (brightness,))

def make_get_led_brightness_message():
    pass
    return make_message(7)

def make_wake_up_display_message():
    pass
    return make_message(8, (127, 127))

def make_set_poly_aftertouch_mode():
    pass
    return make_message(30, (1,))

def make_shut_down_message():
    pass
    return make_message(57, (6,))

def make_clear_power_button_event_message():
    pass
    return make_message(57, (2,))

def make_power_state_message():
    pass
    return make_message(58)

def make_shut_down_image_message():
    pass
    return make_message(65, (1, 0))

def make_set_control_mode_message(mode_id=ControlMode.standalone):
    pass
    return make_message(70, (mode_id,))

def make_get_control_mode_message():
    pass
    return make_message(71)

def bit_is_set(byte, bit_mask):
    pass
    return byte & bit_mask != 0

def from_7L7M(lsb, msb):
    pass
    return lsb + (msb << 7)

def from_7L7777M(data):
    pass
    return data[0] + (data[1] << 7) + (data[2] << 14) + (data[3] << 21) + (data[4] << 28)

def extract_identity_response_info(data):
    pass
    if len(data) != IDENTITY_RESPONSE_LENGTH:
        return ('Identification Error {}'.format(data),)
    else:
        return ('Identified', 'XMOS {}.{} Build {}'.format(data[10], data[11], from_7L7M(data[12], data[13])), 'Serial Number {}'.format(from_7L7777M(data[14:19])), 'Board Revision {}'.format(data[19]), 'PMC {}.{}'.format(data[20], data[21]), 'PMC Bootloader {}'.format(data[22]))