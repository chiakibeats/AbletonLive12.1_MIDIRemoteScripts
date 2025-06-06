# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\LPD8\config.py
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
PAD_TRANSLATION = ((0, 2, 40, 0), (1, 2, 41, 0), (2, 2, 42, 0), (3, 2, 43, 0), (0, 3, 36, 0), (1, 3, 37, 0), (2, 3, 38, 0), (3, 3, 39, 0))
pass
CONTROLLER_DESCRIPTION = {'INPUTPORT': 'LPD8', 'OUTPUTPORT': 'LPD8', 'CHANNEL': 0, 'PAD_TRANSLATION': PAD_TRANSLATION}
pass
MIXER_OPTIONS = {'NUMSENDS': 2, 'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1), 'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1), 'MASTERVOLUME': -1}