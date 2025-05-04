# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MaxForLive\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.capabilities import GENERIC_SCRIPT_KEY
from .MaxForLive import MaxForLive

def get_capabilities():
    return {GENERIC_SCRIPT_KEY: True}

def create_instance(c_instance):
    return MaxForLive(c_instance=c_instance)