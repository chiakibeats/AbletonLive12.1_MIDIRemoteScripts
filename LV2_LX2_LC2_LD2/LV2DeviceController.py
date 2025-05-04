# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\LV2_LX2_LC2_LD2\LV2DeviceController.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import Live
from .FaderfoxDeviceController import FaderfoxDeviceController

class LV2DeviceController(FaderfoxDeviceController):
    __module__ = __name__

    def __init__(self, parent):
        LV2DeviceController.realinit(self, parent)

    def realinit(self, parent):
        FaderfoxDeviceController.realinit(self, parent)