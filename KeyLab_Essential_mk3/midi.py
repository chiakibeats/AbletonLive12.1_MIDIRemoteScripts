# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\KeyLab_Essential_mk3\midi.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.midi import SYSEX_END, SYSEX_START
SYSEX_HEADER = (SYSEX_START, 0, 32, 107, 127, 66)
DISPLAY_HEADER = SYSEX_HEADER + (4, 1, 96)
LED_HEADER = SYSEX_HEADER + (4, 1, 22)
ENCODER_VALUE_HEADER = SYSEX_HEADER + (2, 15, 64)
DAW_PROGRAM_BYTE = 1
PROGRAM_HEADER = SYSEX_HEADER + (33, 17, 64, 2, 0)
REQUEST_PROGRAM_MESSAGE = SYSEX_HEADER + (1, 17, 64, 2, SYSEX_END)
make_connection_message = lambda parameter_byte: SYSEX_HEADER + (2, 15, 64, 90, parameter_byte, SYSEX_END)
CONNECTION_MESSAGE = make_connection_message(1)
DISCONNECTION_MESSAGE = make_connection_message(0)
BUTTON_ID_TO_SYSEX_ID = {20: 20, 21: 21, 22: 22, 23: 23, 24: 16, 25: 17, 26: 18, 27: 19, 40: 12, 41: 13, 42: 14, 43: 15, 44: 24, 45: 25, 46: 26, 47: 27, 119: 7}
PAD_ID_TO_SYSEX_ID = {36: 32, 37: 33, 38: 34, 39: 35, 40: 28, 41: 29, 42: 30, 43: 31, 44: 40, 45: 41, 46: 42, 47: 43, 48: 36, 49: 37, 50: 38, 51: 39}

def make_full_screen_message(screen_id, line1=None, line2=None, line3=None):
    pass
    line1_bytes = (1,) + line1 + (0,) if line1 is not None else tuple()
    line2_bytes = (2,) + line2 + (0,) if line2 is not None else tuple()
    line3_bytes = (3, line3, 0) if line3 else tuple()
    return DISPLAY_HEADER + (screen_id,) + line1_bytes + line2_bytes + line3_bytes + (SYSEX_END,)