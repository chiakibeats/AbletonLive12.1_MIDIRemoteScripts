# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Tranzport\consts.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

NOTE_OFF_STATUS = 128
NOTE_ON_STATUS = 144
CC_STATUS = 176
NUM_NOTES = 127
NUM_CC_NO = 127
NUM_CHANNELS = 15
NUM_PAGES = 4
PAGES_NAMES = (('P', 'o', 's', 'i', 't', 'i', 'o', 'n', ' ', '&', ' ', 'T', 'e', 'm', 'p', 'o'), ('C', 'l', 'i', 'p', ' ', '&', ' ', 'T', 'e', 'm', 'p', 'o'), ('V', 'o', 'l', 'u', 'm', 'e', ' ', '&', ' ', 'P', 'a', 'n', 'n', 'i', 'n', 'g'), ('L', 'o', 'o', 'p', ' ', 'S
TRANZ_NATIVE_MODE = (240, 0, 1, 64, 16, 1, 0, 247)
TRANZ_TRANS_SECTION = list(range(91, 96))
TRANZ_RWD = 91
TRANZ_FFWD = 92
TRANZ_STOP = 93
TRANZ_PLAY = 94
TRANZ_REC = 95
TRANZ_PREV_TRACK = 48
TRANZ_NEXT_TRACK = 49
TRANZ_ARM_TRACK = 0
TRANZ_MUTE_TRACK = 16
TRANZ_SOLO_TRACK = 8
TRANZ_ANY_SOLO = 115
TRANZ_TRACK_SECTION = (TRANZ_PREV_TRACK, TRANZ_NEXT_TRACK, TRANZ_ARM_TRACK, TRANZ_MUTE_TRACK, TRANZ_SOLO_TRACK, TRANZ_ANY_SOLO)
TRANZ_LOOP = 86
TRANZ_PUNCH_IN = 87
TRANZ_PUNCH_OUT = 88
TRANZ_PUNCH = 120
TRANZ_LOOP_SECTION = (TRANZ_LOOP, TRANZ_PUNCH_IN, TRANZ_PUNCH_OUT, TRANZ_PUNCH)
TRANZ_PREV_CUE = 84
TRANZ_ADD_CUE = 82
TRANZ_NEXT_CUE = 85
TRANZ_CUE_SECTION = (TRANZ_PREV_CUE, TRANZ_ADD_CUE, TRANZ_NEXT_CUE)
TRANZ_UNDO = 76
TRANZ_SHIFT = 121
M = {'0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, 'D': 77, 'N': 78, '78': O, '79': 79, 'P': 78, '80': O, 'Q': O, '81': O, 'R': O, '82': O, 'S': O, '83': O, 'T': O, '84': O, 'U': O, '85': O, 'V': O, '86': O, 'W': O, '87': O, 'X': O, '88': O, 'Y'
SYSEX_START = (240, 0, 1, 64, 16, 0)
SYSEX_END = (247,)
CLEAR_LINE = (32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32)
LED_ON = 127
LED_OFF = 0