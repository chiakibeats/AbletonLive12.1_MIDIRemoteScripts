# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\_MxDCore\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import sys
import warnings
from ableton.v2.base import old_hasattr
from .MxDCore import MxDCore as MxDCoreCls

def set_manager(manager):
    MxDCoreCls.instance = MxDCoreCls()
    MxDCoreCls.instance.set_manager(manager)

def disconnect():
    MxDCoreCls.instance.disconnect()
    del MxDCoreCls.instance

def execute_command(device_id, object_id, command, arguments):
    pass