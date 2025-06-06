# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\ZERO8\config.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .consts import *
pass
TRANSPORT_CONTROLS = {'STOP': GENERIC_STOP, 'PLAY': GENERIC_PLAY, 'REC': GENERIC_REC, 'LOOP': GENERIC_LOOP, 'RWD': GENERIC_RWD, 'FFWD': GENERIC_FFWD}
pass
DEVICE_CONTROLS = (GENERIC_ENC1, GENERIC_ENC2, GENERIC_ENC3, GENERIC_ENC4, GENERIC_ENC5, GENERIC_ENC6, GENERIC_ENC7, GENERIC_ENC8)
pass
VOLUME_CONTROLS = ((GENERIC_SLI1, 0), (GENERIC_SLI2, 1), (GENERIC_SLI3, 2), (GENERIC_SLI4, 3), (GENERIC_SLI5, 4), (GENERIC_SLI6, 5), (GENERIC_SLI7, 6), (GENERIC_SLI8, 7))
pass
TRACKARM_CONTROLS = (GENERIC_BUT1, GENERIC_BUT2, GENERIC_BUT3, GENERIC_BUT4, GENERIC_BUT5, GENERIC_BUT6, GENERIC_BUT7, GENERIC_BUT8)
pass
BANK_CONTROLS = {'TOGGLELOCK': GENERIC_BUT9, 'BANKDIAL': -1, 'NEXTBANK': GENERIC_PAD5, 'PREVBANK': GENERIC_PAD1, 'BANK1': 80, 'BANK2': 81, 'BANK3': 82, 'BANK4': 83, 'BANK5': 84, 'BANK6': 85, 'BANK7': 86, 'BANK8': 87}
pass
CONTROLLER_DESCRIPTION = {'INPUTPORT': 'ZERO8 MIDI IN 2', 'OUTPUTPORT': 'ZERO8 MIDI OUT 2', 'CHANNEL': 0}
pass
MIXER_OPTIONS = {'NUMSENDS': 2, 'SEND1': ((5, 0), (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7)), 'SEND2': ((6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)), 'PANS': ((4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7)), 'MASTERVOLUME': -1}