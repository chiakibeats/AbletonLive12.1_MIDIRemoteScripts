# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\padKONTROL\config.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from .consts import *
pass
TRANSPORT_CONTROLS = {'STOP': GENERIC_STOP, 'PLAY': GENERIC_PLAY, 'REC': GENERIC_REC, 'LOOP': GENERIC_LOOP, 'RWD': GENERIC_RWD, 'FFWD': GENERIC_FFWD}
pass
DEVICE_CONTROLS = (GENERIC_ENC1, GENERIC_ENC2, GENERIC_ENC3, GENERIC_ENC4, GENERIC_ENC5, GENERIC_ENC6, GENERIC_ENC7, GENERIC_ENC8)
pass
VOLUME_CONTROLS = GENERIC_SLIDERS
pass
TRACKARM_CONTROLS = (GENERIC_BUT1, GENERIC_BUT2, GENERIC_BUT3, GENERIC_BUT4, GENERIC_BUT5, GENERIC_BUT6, GENERIC_BUT7, GENERIC_BUT8)
pass
BANK_CONTROLS = {'TOGGLELOCK': GENERIC_BUT9, 'BANKDIAL': -1, 'NEXTBANK': -1, 'PREVBANK': -1, 'BANK1': -1, 'BANK2': -1, 'BANK3': -1, 'BANK4': -1, 'BANK5': -1, 'BANK6': -1, 'BANK7': -1, 'BANK8': -1}
pass
PAD_TRANSLATION = ((0, 0, 61, 9), (1, 0, 69, 9), (2, 0, 65, 9), (3, 0, 63, 9), (0, 1, 60, 9), (1, 1, 59, 9), (2, 1, 57, 9), (3, 1, 55, 9), (0, 2, 49, 9), (1, 2, 51, 9), (2, 2, 68, 9), (3, 2, 56, 9), (0, 3, 48, 9), (1, 3, 52, 9), (2, 3, 54, 9), (3, 3, 58, 9))
pass
CONTROLLER_DESCRIPTIONS = {'INPUTPORT': 'padKONTROL (Port 2)', 'OUTPUTPORT': 'padKONTROL (Port 2)', 'CHANNEL': 9, 'PAD_TRANSLATION': PAD_TRANSLATION}
pass
MIXER_OPTIONS = {'NUMSENDS': 2, 'SEND1': (-1, -1, -1, -1, -1, -1, -1, -1), 'SEND2': (-1, -1, -1, -1, -1, -1, -1, -1), 'MASTERVOLUME': 21}