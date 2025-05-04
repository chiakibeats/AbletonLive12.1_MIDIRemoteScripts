# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: ..\..\..\output\Live\win_64_static\Release\python-bundle\MIDI Remote Scripts\MIDI_Mix\__init__.py
# Bytecode version: 3.11a7e (3495)
# Source timestamp: 2025-03-17 14:05:58 UTC (1742220358)

import _Framework.Capabilities as caps
from .MIDI_Mix import MIDI_Mix

def get_capabilities():
    return {caps.CONTROLLER_ID_KEY: caps.controller_id(vendor_id=2536, product_ids=[49], model_name='MIDI Mix'), caps.PORTS_KEY: [caps.inport(props=[caps.NOTES_CC, caps.SCRIPT]), caps.outport(props=[caps.NOTES_CC, caps.SCRIPT])]}

def create_instance(c_instance):
    return MIDI_Mix(c_instance)