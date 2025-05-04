# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK4\midi.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v3.control_surface.midi import SYSEX_END, SYSEX_START
MAIN_PAD_IDS = [range(96, 104), range(112, 120)]
SMALL_MODEL_ID_BYTES = (67, 68)
SET_RELATIVE_ENCODER_MODE = (182, 69, 127)
LAUNCHKEY_COMMON_SYSEX_HEADER = (SYSEX_START, 0, 32, 41)
MK4_SYSEX_HEADER = LAUNCHKEY_COMMON_SYSEX_HEADER + (2, 20)
MINI_MK4_SYSEX_HEADER = LAUNCHKEY_COMMON_SYSEX_HEADER + (2, 19)

def make_connection_message(sysex_header, connect=True):
    pass
    return sysex_header + (2, 127 if connect else 0, SYSEX_END)

def make_disable_daw_label_popup(sysex_header):
    pass
    return sysex_header + (4, 34, 1, SYSEX_END)

def make_enable_touch_output_message():
    pass
    return (182, 71, 127)

def make_enable_keyboard_message(enable=True):
    pass
    return (182, 76, 127 if enable else 0)

def make_enable_drum_pads_message(enable=True):
    pass
    return (182, 84, 127 if enable else 0)