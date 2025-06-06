# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Launchkey_MK3\midi.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from novation import sysex
MODEL_ID_BYTE_SUFFIX = (1, 0, 0)
LK_MK3_25_ID_BYTE = 52
LK_MK3_37_ID_BYTE = 53
LK_MK3_49_ID_BYTE = 54
LK_MK3_61_ID_BYTE = 55
LK_MK3_88_ID_BYTE = 64
MODEL_ID_BYTES = (LK_MK3_25_ID_BYTE, LK_MK3_37_ID_BYTE, LK_MK3_49_ID_BYTE, LK_MK3_61_ID_BYTE, LK_MK3_88_ID_BYTE)
SMALL_MODEL_ID_BYTES = MODEL_ID_BYTES[:2]
INCONTROL_ONLINE_VALUE = 127
PAD_DRUM_LAYOUT = 1
PAD_SESSION_LAYOUT = 2
VOLUME_LAYOUT = 1
PAN_LAYOUT = 3
DISPLAY_HEADER = sysex.STD_MSG_HEADER + (15,)
DISPLAY_HEADER_88_KEY = sysex.STD_MSG_HEADER + (18,)
NOTIFICATION_DISPLAY_COMMAND_BYTES = ((4, 0), (4, 1))
PARAMETER_NAME_DISPLAY_COMMAND_BYTE = 7
PARAMETER_VALUE_DISPLAY_COMMAND_BYTE = 8
POT_PARAMETER_DISPLAY_START_INDEX = 56
FADER_PARAMETER_DISPLAY_START_INDEX = 80
MASTER_PARAMETER_DISPLAY_INDEX = FADER_PARAMETER_DISPLAY_START_INDEX + 8