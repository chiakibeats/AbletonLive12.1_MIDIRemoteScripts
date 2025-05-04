# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\Komplete_Kontrol_S_Mk2\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

from ableton.v2.control_surface.capabilities import SUGGESTED_PORT_NAMES_KEY
from .komplete_kontrol_s_mk2 import Komplete_Kontrol_S_Mk2

def get_capabilities():
    return {SUGGESTED_PORT_NAMES_KEY: ['Komplete Kontrol DAW - 1']}

def create_instance(c_instance):
    return Komplete_Kontrol_S_Mk2(c_instance=c_instance)