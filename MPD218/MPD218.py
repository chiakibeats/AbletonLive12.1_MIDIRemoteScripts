# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MPD218\MPD218.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from _MPDMkIIBase.MPDMkIIBase import MPDMkIIBase
PAD_CHANNEL = 9
PAD_IDS = [[48, 49, 50, 51], [44, 45, 46, 47], [40, 41, 42, 43], [36, 37, 38, 39]]

class MPD218(MPDMkIIBase):

    def __init__(self, *a, **k):
        super(MPD218, self).__init__(PAD_IDS, PAD_CHANNEL, *a, **k)