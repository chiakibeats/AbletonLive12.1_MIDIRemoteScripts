# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPK_mini_mkI\config.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .consts import *
pass
TRANSPORT_CONTROLS = {'STOP': -1, 'PLAY': -1, 'REC': -1, 'LOOP': -1, 'RWD': -1, 'FFWD': -1}
pass
DEVICE_CONTROLS = (GENERIC_ENC1, GENERIC_ENC2, GENERIC_ENC3, GENERIC_ENC4, GENERIC_ENC5, GENERIC_ENC6, GENERIC_ENC7, GENERIC_ENC8)
pass
VOLUME_CONTROLS = ((-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1), (-1, -1))
pass
TRACKARM_CONTROLS = (-1, -1, -1, -1, -1, -1, -1, -1)
pass
BANK_CONTROLS = {'TOGGLELOCK': -1, 'BANKDIAL': -1, 'NEXTBANK': -1, 'PREVBANK': -1, 'BANK1': -1, 'BANK2': -1, 'BANK3': -1, 'BANK4': -1, 'BANK5': -1, 'BANK6': -1, 'BANK7': -1, 'BANK8': -1}
pass
PAD_TRANSLATION = ((0, 0, 48, 9), (1, 0, 49, 9), (2, 0, 50, 9), (3, 0, 51, 9), (0, 1, 44, 9), (1, 1, 45, 9), (2, 1, 46, 9), (3, 1, 47, 9), (0, 2, 40, 9), (1, 2, 41, 9), (2, 2, 42, 9), (3, 2, 43, 9), (0, 3, 36, 9), (1, 3, 37, 9), (2, 3, 38, 9), (3, 3, 39, 9))
pass
CONTROLLER_DESCRIPTION = {'INPUTPORT': 'MPK mini', 'OUTPUTPORT': 'MPK mini', 'CHANNEL': -1, 'PAD_TRANSLATION': PAD_TRANSLATION}
pass
MIXER_OPTIONS = {'NUMSENDS': 2, 'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1), 'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1), 'MASTERVOLUME': -1}