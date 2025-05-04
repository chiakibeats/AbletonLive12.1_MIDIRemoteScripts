# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\APC64\midi.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:57 UTC (1742220357)

from ableton.v3.control_surface.midi import SYSEX_END, SYSEX_START
HALF_BRIGHTNESS_LED_CHANNEL = 0
FULL_BRIGHTNESS_LED_CHANNEL = 6
PULSE_LED_CHANNEL = 10
BLINK_LED_CHANNEL = 14
SYSEX_HEADER = (SYSEX_START, 71, 0, 83)
DISPLAY_MESSAGE_ID = 16
SET_DISPLAY_OWNER_ID = 28
MODE_MESSAGE_ID = 25
TRACK_TYPE_MESSAGE_ID = 27
RTC_START_MESSAGE_ID = 32
RTC_DATA_MESSAGE_ID = 33
RTC_END_MESSAGE_ID = 34

def make_message(message_id, *payload):
    pass
    msg_size = len(payload)
    return SYSEX_HEADER + (message_id,) + (msg_size >> 7 & 127, msg_size & 127) + payload + (SYSEX_END,)